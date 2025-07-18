import os

import carb.settings
import omni.ext
from lc_agent import MultiAgentNetworkNode, RunnableToolNode, get_node_factory
from omni.ai.langchain.agent.usd_code import SceneInfoNetworkNode, USDCodeInteractiveNetworkNode
from omni.ai.langchain.agent.usd_code.extension import USDCodeExtension

from .register_chat_model import register_chat_model, unregister_chat_model
from .search.usd_search_network_node import USDSearchNetworkNode
from .search.usd_search_node import USDSearchNode

# from lc_agent_chat_models import register_all, unregister_all

REGISTER_CHAT_USD_SETTING = "/exts/omni.ai.chat_usd.bundle/register_chat_usd_agent"
REGISTER_CHAT_USD_OMNI_UI_SETTING = "/exts/omni.ai.chat_usd.bundle/chat_usd_with_omni_ui"


class ChatUSDBundleExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        register_chat_model()
        # register_all()

        # Register Search Node
        get_node_factory().register(USDSearchNetworkNode, name="USD Search")
        get_node_factory().register(USDSearchNode, hidden=True)

        # Register Search Delegate if we have ChatView
        try:
            from omni.ai.langchain.widget.core import ChatView

            from .search.usd_search_delegate import USDSearchImageDelegate

            ChatView.add_delegate("USDSearchNode", USDSearchImageDelegate())
            ChatView.add_delegate("USDSearchNetworkNode", USDSearchImageDelegate())
        except ImportError:
            # this extension is not available in the current environment
            # print("ChatView not available")
            pass

        enable_code_interpreter = carb.settings.get_settings().get(
            "/exts/omni.ai.langchain.agent.usd_code/enable_code_interpreter"
        )

        enable_interpreter_security = carb.settings.get_settings().get(
            "/exts/omni.ai.langchain.agent.usd_code/enable_interpreter_security"
        )
        if enable_interpreter_security:
            code_interpreter_hide_items = USDCodeExtension.CODE_INTERPRETER_HIDE_ITEMS
        else:
            code_interpreter_hide_items = None

        chat_usd_multishot = carb.settings.get_settings().get("/exts/omni.ai.chat_usd.bundle/chat_usd_multishot")

        chat_usd_developer_mode = carb.settings.get_settings().get(
            "/exts/omni.ai.chat_usd.bundle/chat_usd_developer_mode"
        )
        chat_usd_developer_mode = chat_usd_developer_mode or os.environ.get("USD_AGENT_DEV_MODE")

        need_rags = chat_usd_developer_mode

        # Register Chat USD Network Node only if the setting is on, it is Off by default
        register_chat_usd_agent = carb.settings.get_settings().get(REGISTER_CHAT_USD_SETTING)
        if register_chat_usd_agent:
            from .chat.chat_usd_network_node import ChatUSDNetworkNode, ChatUSDSupervisorNode

            get_node_factory().register(ChatUSDSupervisorNode, hidden=True)
            get_node_factory().register(ChatUSDNetworkNode, name="Chat USD", multishot=chat_usd_multishot)

            if carb.settings.get_settings().get(REGISTER_CHAT_USD_OMNI_UI_SETTING):
                from .chat.chat_usd_network_node import ChatUSDWithOmniUINetworkNode, ChatUSDWithOmniUISupervisorNode

                get_node_factory().register(ChatUSDWithOmniUISupervisorNode, hidden=True)
                get_node_factory().register(
                    ChatUSDWithOmniUINetworkNode, name="Chat USD with omni.ui", multishot=chat_usd_multishot
                )

            # Register Chat USD tools
            get_node_factory().register(
                USDCodeInteractiveNetworkNode,
                name="ChatUSD_USDCodeInteractive",
                scene_info=False,
                enable_code_interpreter=enable_code_interpreter,
                code_interpreter_hide_items=code_interpreter_hide_items,
                enable_code_atlas=need_rags,
                enable_metafunctions=need_rags,
                enable_interpreter_undo_stack=True,
                max_retries=1,
                enable_code_promoting=True,
                hidden=True,
            )

            get_node_factory().register(USDSearchNetworkNode, name="ChatUSD_USDSearch", hidden=True)

            get_node_factory().register(
                SceneInfoNetworkNode,
                name="ChatUSD_SceneInfo",
                enable_interpreter_undo_stack=False,
                max_retries=1,
                enable_rag=need_rags,
                hidden=True,
            )

            # "Chat USD" is a MultiAgentNetworkNode, so we need to register
            # RunnableToolNode and RunnableSupervisorNode for serialization
            get_node_factory().register(RunnableToolNode, hidden=True)
            get_node_factory().register(MultiAgentNetworkNode.RunnableSupervisorNode, hidden=True)

            try:
                from omni.ai.langchain.widget.core import ChatView

                from .chat.chat_usd_network_node_delegate import ChatUSDNetworkNodeDelegate
                from .chat.multi_agent_delegate import SupervisorNodeDelegate, ToolNodeDelegate

                ChatView.add_delegate("ChatUSDNetworkNode", ChatUSDNetworkNodeDelegate())
                ChatView.add_delegate("RunnableSupervisorNode", SupervisorNodeDelegate())
                ChatView.add_delegate("RunnableToolNode", ToolNodeDelegate())

            except ImportError:
                # this extension is not available in the current environment
                pass

    def on_shutdown(self):
        unregister_chat_model()
        # unregister_all()

        get_node_factory().unregister(USDSearchNetworkNode)
        get_node_factory().unregister(USDSearchNode)

        # if the ChatView is available remove the search delegates
        try:
            from omni.ai.langchain.widget.core import ChatView

            ChatView.remove_delegate("USDSearchNode")
            ChatView.remove_delegate("USDSearchNetworkNode")

        except ImportError:
            # this extension is not available in the current environment
            pass

        register_chat_usd_agent = carb.settings.get_settings().get(REGISTER_CHAT_USD_SETTING)
        if register_chat_usd_agent:
            try:
                from .chat.chat_usd_network_node import ChatUSDNetworkNode

                get_node_factory().unregister("Chat USD")
                get_node_factory().unregister("ChatUSD_USDCodeInteractive")
                get_node_factory().unregister("ChatUSD_USDSearch")
                get_node_factory().unregister("ChatUSD_SceneInfo")

                get_node_factory().unregister(RunnableToolNode)
                get_node_factory().unregister(MultiAgentNetworkNode.RunnableSupervisorNode)

            except ImportError:
                # this extension is not available in the current environment
                pass

            # remove the Chat USD Network Node Delegate if it was added
            try:
                from omni.ai.langchain.widget.core import ChatView

                ChatView.remove_delegate("ChatUSDNetworkNode")
                ChatView.remove_delegate("RunnableSupervisorNode")
                ChatView.remove_delegate("RunnableToolNode")
            except Exception as e:  # noqa
                # this extension is not available in the current environment
                pass
