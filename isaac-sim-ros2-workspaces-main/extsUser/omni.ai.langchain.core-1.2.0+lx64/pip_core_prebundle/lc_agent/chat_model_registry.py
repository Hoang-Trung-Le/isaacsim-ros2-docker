from dataclasses import dataclass
from langchain_core.language_models.chat_models import BaseChatModel
from typing import Callable
from typing import Dict
from typing import Optional


class ChatModelRegistry:
    @dataclass
    class _ChatModelEntry:
        chat_model: BaseChatModel
        tokenizer: Optional[Callable]
        max_tokens: Optional[int]
        hidden: bool

    def __init__(self):
        """
        Instantiate the Registry with empty lists and dictionaries for storing class names,
        Chat Models, and optional Generators.
        """
        self.registered_names = []
        self.chat_models: Dict[str, "_ChatModelEntry"] = {}

    def register(
        self,
        name: str,
        chat_model: BaseChatModel,
        tokenizer: Optional[Callable] = None,
        max_tokens: Optional[int] = None,
        hidden: bool = False,
    ):
        """
        Register a Chat Model and optionally a Generator under the same name.

        Args:
            name (str): Name under which the Chat Model and optional Generator will be registered.
            chat_model: The Chat Model object to store.
            generator: The optional Generator object to store.
        """
        self.registered_names.append(name)
        self.chat_models[name] = self._ChatModelEntry(chat_model, tokenizer, max_tokens, hidden)

    def unregister(self, name: str):
        """
        Unregister a Chat Model and optionally a Generator under a given name.

        Args:
            name (str): Name under which the Chat Model and optional Generator were registered.
        """
        self.registered_names.remove(name)
        self.chat_models.pop(name)

    def get_model(self, name: str) -> Optional[BaseChatModel]:
        """
        Get the Chat Model registered under a given name. If name is not provided,
        it defaults to the first registered name.

        Args:
            name (str): Name under which the Chat Model was registered.
        """
        if not self.chat_models or not self.registered_names:
            return None

        if not name:
            # Default is the first one
            name = self.registered_names[0]  # Default is the first one

        entry = self.chat_models.get(name)
        if entry:
            return entry.chat_model

    def get_tokenizer(self, name: str = None) -> Optional[Callable]:
        """
        Get the tokenizer registered under a given name. If name is not provided,
        it defaults to the first registered name.

        Args:
            name (str): Name under which the tokenizer was registered.

        Returns:
            The tokenizer function or None if not registered.
        """
        if not self.chat_models or not self.registered_names:
            return None

        if not name:
            name = self.registered_names[0]  # Default is the first one

        entry = self.chat_models.get(name)
        if entry:
            return entry.tokenizer

    def get_max_tokens(self, name: str = None) -> Optional[int]:
        """
        Get the max tokens registered under a given name. If name is not provided,
        it defaults to the first registered name.

        Args:
            name (str): Name under which the max tokens was registered.

        Returns:
            The max tokens value or None if not registered.
        """
        if not self.chat_models or not self.registered_names:
            return None

        if not name:
            name = self.registered_names[0]  # Default is the first one

        entry = self.chat_models.get(name)
        if entry:
            return entry.max_tokens

    def get_registered_names(self):
        """
        Get a list of all names under which Chat Models and Generators have been registered.

        Returns:
            List of registered names.
        """
        return [name for name in self.registered_names if not self.chat_models[name].hidden]


REGISTRY = ChatModelRegistry()


def get_chat_model_registry():
    """
    Get the global Chat Model Registry.

    Returns:
        The global Chat Model Registry.
    """
    global REGISTRY
    return REGISTRY
