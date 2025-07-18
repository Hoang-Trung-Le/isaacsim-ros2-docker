from ..runnable_utils import RunnableSystemAppend
from ..runnable_node_agent import RunnableNodeAgent
from .usd_atlas_tool import USDAtlasTool
from .codeinterpreter_tool import CodeInterpreterTool
import os


class USDAtlasAgent(RunnableNodeAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Get the current directory
        current_dir = os.path.dirname(os.path.realpath(__file__))

        # Load the system
        with open(
            os.path.join(current_dir, f"{current_dir}/../data/usd_agent_system.md"), "r"
        ) as file:
            system_prompt = file.read()

        self.inputs.append(RunnableSystemAppend(system_message=system_prompt))

        # Create tools
        self.tools = [USDAtlasTool(), CodeInterpreterTool()]
