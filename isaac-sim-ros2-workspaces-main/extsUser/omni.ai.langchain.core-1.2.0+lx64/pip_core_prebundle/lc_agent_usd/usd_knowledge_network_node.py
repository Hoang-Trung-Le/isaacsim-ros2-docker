from .modifiers.usd_knowledge_rag_modifier import USDKnowledgeRagModifier
from lc_agent import NetworkNode
from lc_agent import get_node_factory

from .nodes.usd_knowledge_node import USDKnowledgeNode
get_node_factory().register(USDKnowledgeNode)


class USDKnowledgeNetworkNode(NetworkNode):
    default_node: str = "USDKnowledgeNode"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_modifier(USDKnowledgeRagModifier())
