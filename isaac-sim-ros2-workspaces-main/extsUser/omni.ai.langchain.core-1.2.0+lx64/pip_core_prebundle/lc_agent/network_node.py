from .network_modifier import NetworkModifier
from .node_factory import get_node_factory
from .runnable_network import RunnableNetwork
from .runnable_node import RunnableNode


class NetworkNodeModifier(NetworkModifier):
    """
    A class that helps to connect subnetwork to the parent network.
    """

    def on_begin_invoke(self, network: "NetworkNode"):
        """
        Create a default node if the network is empty.
        """
        if not network.nodes:
            default_node = network.default_node
            if default_node:
                with network:
                    node = get_node_factory().create_node(default_node)

    def on_pre_invoke(self, network: "NetworkNode", node: "RunnableNode"):
        """
        Connect the root nodes to the parents of the agent node.
        """
        if not network.get_parents(node):
            network.parents >> node


class NetworkNode(RunnableNode, RunnableNetwork):
    """
    Represents a subnetwork.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_modifier(NetworkNodeModifier())

    def _pre_invoke_network(self):
        """Called before invoking the network."""
        parent_network = RunnableNetwork.get_active_network()
        if parent_network and not self.chat_model_name:
            self.chat_model_name = parent_network.chat_model_name

    def _post_invoke_network(self):
        pass

    async def _ainvoke_chat_model(self, chat_model, chat_model_input, invoke_input, config, **kwargs):
        self._pre_invoke_network()

        result = await RunnableNetwork.ainvoke(self, invoke_input, config, **kwargs)

        self._post_invoke_network()

        return result

    def _invoke_chat_model(self, chat_model, chat_model_input, invoke_input, config, **kwargs):
        self._pre_invoke_network()

        result = RunnableNetwork.invoke(self, invoke_input, config, **kwargs)

        self._post_invoke_network()

        return result

    async def _astream_chat_model(self, chat_model, chat_model_input, invoke_input, config, **kwargs):
        self._pre_invoke_network()

        async for item in RunnableNetwork.astream(self, invoke_input, config, **kwargs):
            yield item

        self._post_invoke_network()
