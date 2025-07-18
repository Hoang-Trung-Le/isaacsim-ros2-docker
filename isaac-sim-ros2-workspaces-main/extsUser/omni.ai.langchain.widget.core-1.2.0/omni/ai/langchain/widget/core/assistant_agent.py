from lc_agent import RunnableNode, RunnableSystemAppend

_SYSTEM = """
You are the Omniverse Assistant tool.

You have to assist and guide the writing and debugging code in Python.
"""


class AssistantAgent(RunnableNode):
    """This is an example default agent for the AI widget. It is extends from  RunnableNode."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inputs.append(RunnableSystemAppend(system_message=_SYSTEM))
        self.metadata["description"] = "Generic AI Assistant"
        self.metadata["examples"] = ["Who are you in two words?"]
