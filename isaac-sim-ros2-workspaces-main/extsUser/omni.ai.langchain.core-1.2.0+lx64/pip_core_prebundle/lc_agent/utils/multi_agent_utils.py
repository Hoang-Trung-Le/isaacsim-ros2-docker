from ..network_node import NetworkNode
from ..node_factory import get_node_factory
from ..runnable_network import RunnableNetwork
from ..runnable_node import RunnableNode
from ..runnable_utils import RunnableHumanNode
from ..runnable_utils import RunnableSystemAppend
import time

PRINT_TIME = False
MAX_ITERATIONS = 10

ROUTING_SYSTEM_LONG = """
Respond to the human as helpfully and accurately as possible. You have access to the following tools:

{tools}

Respond with ONE LINE in either of these formats:
{tool_names}
- FINAL <answer>
- <tool_name> <short question>

Example responses:
{first_tool} How do I start?
FINAL This solves the problem

Begin! Remember to respond with exactly one line in the allowed format.
"""

ROUTING_SYSTEM_SHORT = """
Respond to the human as helpfully and accurately as possible. You have access to the following tools:

{tools}

Respond with ONLY ONE WORD from these options:
{tool_names}
- FINAL (if you can answer directly)

Example responses:
{first_tool}
FINAL It solves the problem

Begin! Remember to respond with exactly one word from the allowed options.
"""

LONG_FIRST_TOOL_CALL_TEMPLATE = (
    '(Reminder to respond in one line only. Format: "<tool_name> <question>". '
    "The only available options are: {options})"
)

LONG_SUBSEQUENT_TOOL_CALL_TEMPLATE = (
    '(Reminder to respond in one line only. Either "<tool_name> <question>" or "FINAL <answer>". '
    'If there is answer, respond with "FINAL <answer>". '
    'If you see the same question and result repeating, respond with "FINAL Done" to avoid loops.)'
)

SHORT_FIRST_TOOL_CALL_TEMPLATE = (
    "(Reminder to respond in one word only no matter what. The only available options are: {options})"
)

SHORT_SUBSEQUENT_TOOL_CALL_TEMPLATE = (
    '(Reminder to respond in one word only no matter what. If there is answer, respond with "FINAL". '
    'If you see the same question and result repeating, respond with "FINAL" to avoid loops.)'
)


class RunnableRoutingNode(RunnableNode):
    def __init__(self, system_message, **kwargs):
        super().__init__(**kwargs)
        self.inputs.append(RunnableSystemAppend(system_message=system_message))


def get_routing_prompt(network: "MultiAgentNetworkNode", long) -> str:
    node_factory = get_node_factory()
    tools = ""
    tool_names = ""
    first_tool = ""

    # Initialize tools for each route node specified in route_nodes
    for route in network.route_nodes:
        # Retrieve the node type registered with the node factory
        node_type = node_factory.get_registered_node_type(route)
        if not node_type:
            continue  # Skip if the node type is not registered

        # Extract the description from the node type to use in the tool
        description_field = node_type.__fields__.get("description")
        description = description_field.default if description_field else node_type.__doc__

        tools += f"\n{route} - {description or ''}\n"
        if long:
            tool_names += f"- {route} <question>\n"
        else:
            tool_names += f"- {route}\n"

        if not first_tool:
            first_tool = route

    if long:
        prompt = ROUTING_SYSTEM_LONG
    else:
        prompt = ROUTING_SYSTEM_SHORT

    prompt = prompt.replace("{tools}", tools).replace("{tool_names}", tool_names).replace("{first_tool}", first_tool)

    return prompt


async def determine_next_action(network: "MultiAgentNetworkNode", node=None):
    if not node:
        node = network
        while node and not isinstance(node, RunnableHumanNode):
            node = node.parents[0] if node.parents else None

    if not node:
        return False

    long = network.generate_prompt_per_agent

    # Find the human node
    human_node = node
    tools_called = []
    while human_node:
        metadata = human_node.metadata
        tool_call_name = metadata.get("tool_call_name")
        tool_call_content = metadata.get("tool_call_content")
        if tool_call_name:
            tools_called.append(
                {
                    "tool_call_name": tool_call_name,
                    "tool_call_content": tool_call_content,
                    "result": human_node.outputs.content,
                }
            )

        if isinstance(human_node, RunnableHumanNode):
            break

        human_node = human_node.parents[0] if human_node.parents else None

    # Check if we have reached the maximum number of iterations
    if len(tools_called) > MAX_ITERATIONS:
        return False

    question = str(human_node.outputs.content)
    if not question:
        return False

    chat_model_name = network._get_chat_model_name(None, None, None)

    routing_prompt = get_routing_prompt(network, long)

    human_message = ""
    if tools_called:
        human_message += f"Question: {question}\n"
        for tool in reversed(tools_called):
            tool_call_name = tool["tool_call_name"]
            tool_call_content = tool["tool_call_content"]
            tool_call_result = tool["result"]
            human_message += f"\nAction: {tool_call_name}\n"
            if tool_call_content:
                human_message += f"Question: {tool_call_content}\n"
            if tool_call_result:
                human_message += f"Result: {tool_call_result}\n"
        human_message += "\nAction:\n"

    options = ", ".join(network.route_nodes)
    if long:
        if not tools_called:
            # First tool call
            human_message_footer = LONG_FIRST_TOOL_CALL_TEMPLATE
        else:
            human_message_footer = LONG_SUBSEQUENT_TOOL_CALL_TEMPLATE
    else:
        if not tools_called:
            # First tool call
            human_message_footer = SHORT_FIRST_TOOL_CALL_TEMPLATE
        else:
            human_message_footer = SHORT_SUBSEQUENT_TOOL_CALL_TEMPLATE

    human_message_footer = human_message_footer.replace("{options}", options)
    human_message += human_message_footer

    if PRINT_TIME:
        print(f"ToolModifier._get_classification human_message: '{human_message}'")

    start_time = time.time()

    inner_node = node
    if isinstance(node, NetworkNode):
        inner_node = node.get_leaf_node()

    # Classification step.
    default_node = network.default_node
    with RunnableNetwork(chat_model_name=chat_model_name) as tmp_network:
        inner_node >> RunnableHumanNode(human_message=human_message)
        if default_node:
            # Using the default node will let to use the system message from the supervisor node
            get_node_factory().create_node(default_node, inputs=[RunnableSystemAppend(system_message=routing_prompt)])
        else:
            RunnableRoutingNode(routing_prompt)

    result = await tmp_network.ainvoke()
    result = f"{result.content}"

    # Simple parsing
    result = result.strip()
    parts = result.split(maxsplit=1)
    action = parts[0].upper()
    content = parts[1] if len(parts) > 1 else None

    if PRINT_TIME:
        print(f"ToolModifier._get_classification took {time.time() - start_time} seconds. {result}")

    # Handle Final Answer case
    if action == "FINAL":
        return {"action": "FINAL", "content": content}

    # Handle routing case
    for route in network.route_nodes:
        if action == route.upper():
            return {"action": route, "content": content}

    return None
