from pathlib import Path
from typing import List, Optional

from lc_agent import MultiAgentNetworkNode, RunnableNode, RunnableSystemAppend
from omni.ai.langchain.agent.usd_code.utils.chat_model_utils import sanitize_messages_with_expert_type

SYSTEM_PATH = Path(__file__).parent.joinpath("systems")


def read_md_file(file_path: str):
    with open(file_path, "r") as file:
        return file.read()


identity = read_md_file(f"{SYSTEM_PATH}/chat_usd_supervisor_identity.md")


class ChatUSDSupervisorNode(RunnableNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inputs.append(RunnableSystemAppend(system_message=identity))

    def _sanitize_messages_for_chat_model(self, messages, chat_model_name, chat_model):
        """Sanitizes messages and adds metafunction expert type for USD operations."""
        messages = super()._sanitize_messages_for_chat_model(messages, chat_model_name, chat_model)
        return sanitize_messages_with_expert_type(messages, "knowledge", rag_max_tokens=0, rag_top_k=0)


class ChatUSDNetworkNode(MultiAgentNetworkNode):
    """
    ChatUSDNetworkNode is a specialized network node designed to handle conversations related to USD (Universal Scene Description).
    It utilizes the ChatUSDNodeModifier to dynamically modify the scene or search for USD assets based on the conversation's context.

    This class is an example of how to implement a multi-agent system where different tasks are handled by specialized agents (nodes)
    based on the user's input.
    """

    default_node: str = "ChatUSDSupervisorNode"
    route_nodes: List[str] = [
        "ChatUSD_USDCodeInteractive",
        "ChatUSD_USDSearch",
        "ChatUSD_SceneInfo",
    ]
    function_calling = False
    generate_prompt_per_agent = True
    multishot = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.metadata["description"] = "Multi-agents to modify the scene and search USD assets."
        self.metadata["examples"] = [
            "Find me a traffic cone",
            "Create a sphere with a red material",
            "Find an orange and import it to the scene",
        ]
