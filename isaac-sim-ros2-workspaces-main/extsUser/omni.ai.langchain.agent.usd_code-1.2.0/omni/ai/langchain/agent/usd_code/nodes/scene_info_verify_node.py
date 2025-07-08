from pathlib import Path
from typing import Optional

from lc_agent_usd import USDCodeGenNode

from ..utils.chat_model_utils import sanitize_messages_with_expert_type

SYSTEM_PATH = Path(__file__).parent.joinpath("systems")


def read_md_file(file_path: str):
    with open(file_path, "r") as file:
        return file.read()


system_message = read_md_file(f"{SYSTEM_PATH}/scene_info_verify.md")


class SceneInfoVerifyNode(USDCodeGenNode):
    system_message: Optional[str] = system_message

    def _sanitize_messages_for_chat_model(self, messages, chat_model_name, chat_model):
        """Sanitizes messages and adds metafunction expert type for USD operations."""
        messages = super()._sanitize_messages_for_chat_model(messages, chat_model_name, chat_model)
        return sanitize_messages_with_expert_type(messages, "code", rag_max_tokens=0, rag_top_k=0)
