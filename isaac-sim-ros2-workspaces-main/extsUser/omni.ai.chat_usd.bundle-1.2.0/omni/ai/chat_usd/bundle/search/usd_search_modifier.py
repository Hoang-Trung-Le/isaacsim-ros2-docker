import base64
import json
import re
import tempfile

import carb.settings
import requests
from lc_agent import AIMessage, NetworkModifier, RunnableNetwork, RunnableNode

from .usd_search_node import USDSearchNode


def get_api_key():
    import carb.settings

    api_key = None
    settings = carb.settings.get_settings().get("/exts/omni.ai.chat_usd.bundle/nvidia_api_key")
    if settings:
        api_key = settings
    else:
        import os

        api_key = os.environ.get("NVIDIA_API_KEY")

    return api_key


class USDSearchModifier(NetworkModifier):
    """USDSearch API Command:
    @USDSearch(query: str, metadata: bool, limit: int)@

    Description: Searches the USD API with the given query and parameters.
    - query: The search query string
    - metadata: Whether to include metadata in the search results (true/false)
    - limit: The maximum number of results to return

    Example: @USDSearch("big box", false, 10)@"""

    def __init__(self):
        self._settings = carb.settings.get_settings()
        self._service_url = self._settings.get("exts/omni.ai.chat_usd.bundle/usd_search_host_url")
        self._api_key = get_api_key()

    def _process_json_data(self, json_data):
        """Process the JSON data returned by the USD Search API."""
        for item in json_data:
            item["url"] = item["url"].replace(
                "s3://deepsearch-demo-content/", "https://omniverse-content-production.s3.us-west-2.amazonaws.com/"
            )

            if "image" in item:
                # Create a temporary file in the system's temp directory
                with tempfile.NamedTemporaryFile(prefix="temp_", suffix=".png", delete=False) as temp_file:
                    # Decode the base64 image data and write it to the temp file
                    image_data = base64.b64decode(item["image"])
                    temp_file.write(image_data)
                    full_path = temp_file.name

                # Replace the base64 encoded image with the file path
                item["image"] = full_path

                if "bbox_dimension_x" in item:
                    item["bbox_dimension"] = [
                        item["bbox_dimension_x"],
                        item["bbox_dimension_y"],
                        item["bbox_dimension_z"],
                    ]

        clean_json_data = []
        for item in json_data:
            new_item = {}
            # Remove any other keys that we dont care about
            for key in item.keys():
                if key in ["url", "image", "bbox_dimension"]:
                    new_item[key] = item[key]

            clean_json_data.append(new_item)

        return clean_json_data

    def on_post_invoke(self, network: "RunnableNetwork", node: RunnableNode):
        output = node.outputs.content if node.outputs else ""
        matches = re.findall(r'@USDSearch\("(.*?)", (.*?), (\d+)\)@', output)

        search_results = {}
        for query, metadata, limit in matches:
            # Cast to proper Python types
            metadata = metadata.lower() == "true"
            limit = int(limit)

            # Call the actual USD Search API
            api_response = self.usd_search_post(query, metadata, limit)
            search_results[query] = api_response

        if search_results:
            search_results_str = json.dumps(search_results, indent=2) + "\n\n"
            search_result_node = USDSearchNode()
            search_result_node.outputs = AIMessage(search_results_str)
            network.outputs = search_result_node.outputs
            network._event_callback(
                RunnableNetwork.Event.NODE_INVOKED,
                {"node": network, "network": network},
            )
            node >> search_result_node

    def usd_search_post(self, query, return_metadata, limit):
        """Call the USD Search API with the given query and parameters."""
        # fixed parameters
        # USD File only for now
        filter = "usd*"
        # we get the images
        images = True

        url = self._service_url
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self._api_key),
        }

        payload = {
            "description": query,
            "return_metadata": return_metadata,
            "limit": limit,
            "file_extension_include": filter,
            "return_images": images,
            "return_root_prims": False,
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Raise an exception for non-200 status codes

            result = response.json()

            filtered_result = self._process_json_data(result)
            return filtered_result

        except requests.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}
