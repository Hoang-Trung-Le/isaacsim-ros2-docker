from lc_agent_rag_modifiers import SystemRagModifier


class USDKnowledgeRagModifier(SystemRagModifier):
    def __init__(self):
        super().__init__(retriever_name="usd_knowledge_qa")


