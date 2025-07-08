from lc_agent import NetworkNode

from .usd_search_modifier import USDSearchModifier


class USDSearchNetworkNode(NetworkNode):
    """
    Use this node to search any asset in Deep Search. It can search, to import call another tool after this one.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Add the USDSearchModifier to the network
        self.add_modifier(USDSearchModifier())

        # Set the default node to USDSearchNode
        self.default_node = "USDSearchNode"

        self.metadata[
            "description"
        ] = """Agent to search and Import Assets.
Connect to the USD Search NIM to find USD assets base on the natural language query.
Drag and drop discovered assets directly into your scene for seamless integration"""

        self.metadata["examples"] = [
            "What can you do?",
            "Find 3 traffic cones and 2 Boxes",
            "I need 3 office chairs",
            "10 warehouse shelves",
        ]
