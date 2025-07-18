from .chat_model_registry import get_chat_model_registry
from .network_modifier import NetworkModifier
from .network_node import NetworkNode
from .node_factory import get_node_factory
from .runnable_network import RunnableNetwork
from .runnable_node import RunnableNode
from .runnable_utils import RunnableHumanNode, RunnableToolNode, RunnableAINode
from .utils.multi_agent_utils import determine_next_action
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.pydantic_v1 import Field
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool
from typing import Any, List, Optional, Type
import time

PRINT_TIME = False


class MultiAgentNetworkNode(NetworkNode):
    """
    A specialized NetworkNode that handles routing between different nodes based on tool calls
    from AI messages. It sets up tools and modifies the network to handle multi-step conversations.
    """

    default_node: str = "RunnableNode"
    route_nodes: List[str] = []
    multishot: bool = True
    function_calling: bool = True
    generate_prompt_per_agent: bool = True

    class RunnableSupervisorNode(RunnableNode):
        subnode: RunnableNode

        def __getattribute__(self, name):
            if name in ["subnode", "json", "dict"] or name.startswith("_") or self.subnode is None:
                return super().__getattribute__(name)
            try:
                # Try to get the attribute from 'subnode' first
                subnode_attr = getattr(super().__getattribute__("subnode"), name)
                return subnode_attr
            except AttributeError:
                # If not found in 'subnode', get it from self (RunnableSupervisorNode)
                return super().__getattribute__(name)

        def __setattr__(self, name, value):
            if name in ["subnode"] or name.startswith("_") or self.subnode is None:
                super().__setattr__(name, value)
            else:
                try:
                    # Try to set the attribute on 'subnode'
                    setattr(self.subnode, name, value)
                except AttributeError:
                    # If the attribute doesn't exist on 'subnode', set it on self
                    super().__setattr__(name, value)

    class RoutingTool(BaseTool):
        """
        A tool that routes the execution to the appropriate node based on tool calls.
        """

        class RoutingToolInput(BaseModel):
            """Input schema for the RoutingTool."""

            pass

        args_schema: Type[BaseModel] = RoutingToolInput

        def _run(self, *args, config: RunnableConfig, **kwargs):
            """
            Executes the tool by creating and connecting the appropriate node in the network.

            Args:
                config (RunnableConfig): The configuration for the runnable, containing metadata.

            Returns:
                RunnableNode: The node representing the tool in the network.
            """
            prompt = kwargs.get("prompt")

            node: RunnableNode = config["metadata"].get("node")
            network: RunnableNetwork = config["metadata"].get("network")
            tool_call_id: str = config["metadata"].get("tool_call_id")

            with network:
                metadata = {"tool_call_id": tool_call_id, "tool_call_name": self.name}
                if isinstance(network, NetworkNode):
                    # Rag metadata should override the tool metadata
                    for metadata_key in ["rag_top_k", "rag_max_tokens"]:
                        metadata_value = network.find_metadata(metadata_key)
                        if metadata_value is not None:
                            metadata[metadata_key] = metadata_value

                # Create a new node for the tool and connect it to the current node
                tool_node = get_node_factory().create_node(self.name, metadata=metadata)
                node >> tool_node  # Connect the current node to the new tool node
                if PRINT_TIME:
                    routing_time = time.time() - network._start_time
                    print(f"Time to first routing: {routing_time:.2f} seconds")
                    print(f"Route to: {self.name}")

                if prompt and isinstance(tool_node, NetworkNode):
                    with tool_node:
                        # Create a human node with the prompt
                        RunnableHumanNode(prompt)

            return tool_node

    class RoutingToolWithArgs(RoutingTool):
        """With prompt"""

        class RoutingToolInput(BaseModel):
            """Input schema for the RoutingTool."""

            prompt: str = Field(description="The question or prompt to ask the function")

        args_schema: Type[BaseModel] = RoutingToolInput

    class ToolModifier(NetworkModifier):
        """
        Modifier to the network that handles tool calls and inserts the appropriate nodes.
        """

        def __init__(self, tools: List[BaseTool]):
            """
            Initializes the ToolModifier with a list of tools.

            Args:
                tools (List[BaseTool]): The list of tools available for routing.
            """
            super().__init__()
            self._tools = tools

        def _find_tool(self, name: str) -> Optional[BaseTool]:
            """
            Finds a tool by name from the list of tools.

            Args:
                name (str): The name of the tool to find.

            Returns:
                Optional[BaseTool]: The tool if found, else None.
            """
            name_lower = name.lower()
            for tool in self._tools:
                if tool.name.lower() == name_lower:
                    return tool
            return None

        async def _create_next_action_node(self, network: "NetworkNode", node=None):
            """
            Creates a next action node based on the classification result.
            """
            classification = await determine_next_action(network, node)
            if not classification:
                return

            with network:
                content = classification.get("content")
                metadata = {"tool_call_name": classification["action"], "tool_call_content": classification["content"]}
                if isinstance(network, NetworkNode):
                    for metadata_key in ["rag_top_k", "rag_max_tokens"]:
                        metadata_value = network.find_metadata(metadata_key)
                        if metadata_value is not None:
                            metadata[metadata_key] = metadata_value

                if classification["action"] == "FINAL":
                    content = content or "Done"
                    if node:
                        node >> RunnableAINode(content, metadata=metadata)
                    else:
                        RunnableAINode(content, metadata=metadata)
                else:
                    created_node = get_node_factory().create_node(classification["action"], metadata=metadata)
                    if node:
                        node >> created_node
                    if content and isinstance(created_node, NetworkNode):
                        with created_node:
                            RunnableHumanNode(content)

        async def on_begin_invoke_async(self, network: "NetworkNode"):
            """
            Create a superviser node if the network is empty.
            """
            if not network.nodes:
                # entry point is here
                if isinstance(network, MultiAgentNetworkNode) and not network.function_calling:
                    await self._create_next_action_node(network)
                else:
                    self._create_supervisor_node(None, network)

        async def on_post_invoke_async(self, network: "RunnableNetwork", node: "RunnableNode"):
            """
            Post-invoke hook that modifies the network based on the outputs of a node.

            Args:
                network (RunnableNetwork): The current network being executed.
                node (RunnableNode): The node that was just invoked.
            """
            if (
                node.invoked
                and isinstance(node.outputs, AIMessage)
                and node.outputs.tool_calls
                and not network.get_children(node)
            ):
                self._process_tool_calls(network, node)
            elif node.invoked and not network.get_children(node) and node.metadata.get("tool_call_id"):
                # This is the node that was created by a tool invocation
                # Handle nodes that need to pass their output directly to the next node
                node.metadata["contribute_to_history"] = False  # Do not include in conversation history
                self._create_invoked_node(node, network, node.metadata["tool_call_id"])
            elif (
                node.invoked
                and isinstance(node, RunnableToolNode)
                and not network.get_children(node)
                and isinstance(network, MultiAgentNetworkNode)
                and network.multishot
            ):
                # Handle multi-step conversations if multishot is enabled
                # Automatically continue the conversation by connecting to the default node
                self._create_supervisor_node(node, network)
            elif (
                isinstance(network, MultiAgentNetworkNode)
                and network.function_calling
                and node.invoked
                and isinstance(node.outputs, HumanMessage)
                and not network.get_children(node)
            ):
                # Default node after a human message
                self._create_supervisor_node(node, network)
            elif (
                isinstance(network, MultiAgentNetworkNode)
                and not network.function_calling
                and node.invoked
                and not network.get_children(node)
                and network.multishot
            ):
                metadata = node.metadata
                tool_call_name = metadata.get("tool_call_name")
                if tool_call_name in network.route_nodes:
                    await self._create_next_action_node(network, node)

        def _process_tool_calls(self, network: "RunnableNetwork", node: "RunnableNode"):
            """
            Process tool calls from an AI message and modify the network accordingly.

            Args:
                network (RunnableNetwork): The current network being executed.
                node (RunnableNode): The node that contains tool calls in its outputs.
            """
            for tool_call in node.outputs.tool_calls:
                selected_tool = self._find_tool(tool_call["name"])
                if not selected_tool:
                    continue

                config = self._prepare_tool_config(network, node, tool_call["id"])
                tool_output = selected_tool.invoke(tool_call["args"], config=config)
                node = self._handle_tool_output(network, node, tool_output, tool_call["id"])

        def _prepare_tool_config(
            self, network: "RunnableNetwork", node: "RunnableNode", tool_call_id: str
        ) -> RunnableConfig:
            """
            Prepare the configuration for tool invocation.

            Args:
                network (RunnableNetwork): The current network being executed.
                node (RunnableNode): The current node in the network.
                tool_call_id (str): The ID of the tool call.

            Returns:
                RunnableConfig: The prepared configuration for tool invocation.
            """
            return RunnableConfig(
                metadata={
                    "node": node,
                    "network": network,
                    "tool_call_id": tool_call_id,
                }
            )

        def _handle_tool_output(
            self, network: "RunnableNetwork", node: "RunnableNode", tool_output: Any, tool_call_id: str
        ) -> "RunnableNode":
            """
            Handle the output of a tool invocation and update the network accordingly.

            Args:
                network (RunnableNetwork): The current network being executed.
                node (RunnableNode): The current node in the network.
                tool_output (Any): The output from the tool invocation.
                tool_call_id (str): The ID of the tool call.

            Returns:
                RunnableNode: The updated current node after handling the tool output.
            """
            if isinstance(tool_output, RunnableNode):
                tool_output.metadata["tool_call_id"] = tool_call_id
                return tool_output
            elif isinstance(tool_output, str):
                tool_node = self._create_invoked_node(node, network, tool_call_id)
                return tool_node
            return node

        def _create_invoked_node(self, parent, network, tool_call_id):
            with network:
                # Create a RunnableToolNode with the content and connect it
                interpreter_error = parent.metadata.get("interpreter_error")
                invoked_node = RunnableToolNode(
                    parent.outputs.content, tool_call_id, status="error" if interpreter_error else "success"
                )
                parent >> invoked_node

                invoked_node.metadata["multi_agent_invoked_node"] = True

            return invoked_node

        def _create_supervisor_node(self, parent, network):
            default_node = network.default_node
            if default_node:
                with RunnableNetwork():
                    # No network is attached
                    default_node = get_node_factory().create_node(default_node)

                supervisor_node = MultiAgentNetworkNode.RunnableSupervisorNode(subnode=default_node)
                if parent:
                    parent >> supervisor_node

                # Just add a metadata to determine it's a supervisor
                supervisor_node.chat_model_name = network._chat_agent_name
                supervisor_node.metadata["multi_agent_supervisor"] = True

    def __init__(self, **kwargs):
        """
        Initializes the MultiAgentNetworkNode with given keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(**kwargs)
        self._chat_agent_name: Optional[str] = None  # Name of the temporary chat agent
        self._tools: List[BaseTool] = []  # List of tools for routing
        self._start_time = time.time()
        self.add_modifier(self.ToolModifier(self._tools), priority=-100)

    def _iter(self, *args, **kwargs):
        """Pydantic serialization method"""
        kwargs["exclude"] = (kwargs.get("exclude", None) or set()) | {
            "_chat_agent_name",
            "_tools",
            "_start_time",
        }

        # Call super
        yield from super()._iter(*args, **kwargs)

    def __setattr__(self, name, value):
        """
        Custom setattr to handle internal attributes starting with '_'.

        Args:
            name (str): Attribute name.
            value (Any): Attribute value.
        """
        if name.startswith("_"):
            object.__setattr__(self, name, value)
        else:
            super().__setattr__(name, value)

    def _pre_invoke_network(self):
        """
        Prepares the network before invocation by setting up tools and models.

        This method is called before the network starts processing messages.
        It sets up the tools and updates the default node to use a temporary chat agent that
        has the tools bound to it.
        """
        if not self.function_calling:
            return super()._pre_invoke_network()

        # Add timing measurement
        self._start_time = time.time()

        node_factory = get_node_factory()
        self._tools.clear()  # Clear any existing tools

        # Initialize tools for each route node specified in route_nodes
        for route in self.route_nodes:
            # Retrieve the node type registered with the node factory
            node_type = node_factory.get_registered_node_type(route)
            if not node_type:
                continue  # Skip if the node type is not registered

            # Extract the description from the node type to use in the tool
            description_field = node_type.__fields__.get("description")
            description = description_field.default if description_field else node_type.__doc__

            # Create a new RoutingTool for this route node
            if self.generate_prompt_per_agent:
                tool = self.RoutingToolWithArgs(name=route, description=description or "")
            else:
                tool = self.RoutingTool(name=route, description=description or "")
            self._tools.append(tool)  # Add the tool to the list of tools

        # Get the base chat model name
        chat_model_name = self._get_chat_model_name(None, None, None)
        # Retrieve the chat model and bind the tools to it
        chat_agent = get_chat_model_registry().get_model(chat_model_name).bind_tools(tools=self._tools)
        # Register a new chat agent with a unique name including route nodes
        self._chat_agent_name = f"{chat_model_name}_tools(" + ", ".join(self.route_nodes) + ")"
        get_chat_model_registry().register(self._chat_agent_name, chat_agent, hidden=True)

        return super()._pre_invoke_network()

    def _post_invoke_network(self):
        """
        Cleans up after network invocation by unregistering temporary nodes and models.

        This method is called after the network has finished processing messages.
        It cleans up the temporary chat agents and nodes that were created during preprocessing.
        """
        result = super()._post_invoke_network()

        self._tools.clear()
        self._chat_agent_name = None

        # Add timing measurement and print
        execution_time = time.time() - self._start_time
        if PRINT_TIME:
            print(f"[Multi Agent Network Node] Network execution time: {execution_time:.2f} seconds")

        return result
