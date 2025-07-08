from .network_modifier import NetworkModifier
from .node_factory import get_node_factory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage


class DefaultModifier(NetworkModifier):
    def on_post_invoke(self, network: "RunnableNetwork", node: "RunnableNode"):
        if (
            node.invoked
            and isinstance(node.outputs, HumanMessage)
            and not network.get_children(node)
        ):
            default_node = network.default_node
            if default_node:
                node >> get_node_factory().create_node(default_node)
