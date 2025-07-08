from lc_agent import RunnableNode

from ..utils.chat_model_utils import sanitize_messages_with_expert_type


class USDCodeNode(RunnableNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _sanitize_messages_for_chat_model(self, messages, chat_model_name, chat_model):
        """Sanitizes messages and adds metafunction expert type for USD operations."""
        messages = super()._sanitize_messages_for_chat_model(messages, chat_model_name, chat_model)
        return sanitize_messages_with_expert_type(messages, "code")
