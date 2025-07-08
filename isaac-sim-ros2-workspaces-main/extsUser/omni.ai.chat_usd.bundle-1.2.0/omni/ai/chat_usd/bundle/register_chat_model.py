import os
from pathlib import Path
from typing import Any, List, Optional

import carb.settings
from langchain_core.language_models import LanguageModelInput
from langchain_openai import ChatOpenAI
from lc_agent import get_chat_model_registry

from .chat_models.chat_nvnim import ChatNVNIM
from .tokenizer import Tokenizer


def get_custom_payload_fn(custom_payload):
    """Return a function that adds custom payload to the payload of the model."""

    def payload_fn(payload):
        for key, value in custom_payload.items():
            payload[key] = value
        return payload

    return payload_fn


MODELS = {
    "nvidia/usdcode-llama3-70b-instruct": (
        {
            "model": "nvidia/usdcode-llama3-70b-instruct",
            "temperature": 0.1,
            "max_tokens": 1024,
            "extra_body": {
                # limit rag to 5 entries
                "rag_top_k": 5,
                # limit rag tokens to 2000 token server side
                "rag_max_tokens": 2000,
            },
        },
        6192,  # 8192 - rag_max_tokens,
        False,
        None,
        True,  # Development mode only
    ),
    "nvidia/usdcode-llama3-70b-instruct-interactive": (
        {
            "model": "nvidia/usdcode-llama3-70b-instruct",
            "temperature": 0.1,
            "max_tokens": 1024,
            "extra_body": {
                # No RAGs
                "rag_type": "none",
                "rag_top_k": 0,
                "rag_max_tokens": 0,
            },
        },
        8192,
        True,
        None,
        True,  # Development mode only
    ),
    "nvidia/usdcode-llama-3.1-70b-instruct": (
        {
            "model": "nvidia/usdcode-llama-3.1-70b-instruct",
            "temperature": 0.1,
            "max_tokens": 4 * 1024,
            "top_p": 0.95,
        },
        128 * 1024,
        False,
        "ChatNVNIM",  # Custom Chat Model
        False,
    ),
    "meta/llama-3.1-70b-instruct": (
        {
            "model": "meta/llama-3.1-70b-instruct",
            "temperature": 0.1,
            "max_tokens": 4 * 1024,
            "base_url": "https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions/{func_id}",
        },
        128 * 1024,
        False,
        None,
        True,  # Development mode only
    ),
    "meta/llama-3.1-405b-instruct": (
        {
            "model": "meta/llama-3.1-405b-instruct",
            "temperature": 0.1,
            "max_tokens": 4 * 1024,
        },
        128 * 1024,
        False,
        None,
        True,  # Development mode only
    ),
}

TOKENIZER_PATH = Path(__file__).parent.joinpath("../../../../data/Llama3-70B-tokenizer.model")


def register_chat_model(model_names=None, api_key=None):
    chat_usd_developer_mode = carb.settings.get_settings().get("/exts/omni.ai.chat_usd.bundle/chat_usd_developer_mode")
    chat_usd_developer_mode = chat_usd_developer_mode or os.environ.get("USD_AGENT_DEV_MODE")

    # Fallback URL
    base_url = "https://integrate.api.nvidia.com/v1"

    # API Key
    if api_key is None:
        settings = carb.settings.get_settings().get("/exts/omni.ai.chat_usd.bundle/nvidia_api_key")
        if settings:
            api_key = settings
        else:
            # Get from NVIDIA_API_KEY environment variable
            api_key = os.environ.get("NVIDIA_API_KEY")
            if api_key is None:
                carb.log_warn(f"NVIDIA_API_KEY is required for {list(MODELS.keys())[0]} model")

    # Func ID
    func_id = carb.settings.get_settings().get("/exts/omni.ai.chat_usd.bundle/nvidia_func_id")
    if not func_id:
        func_id = os.environ.get("NVIDIA_FUNC_ID")

    model_registry = get_chat_model_registry()

    # Add custom models from settings
    settings = carb.settings.get_settings()
    custom_models = settings.get("/exts/omni.ai.chat_usd.bundle/custom_chat_model")

    if custom_models:
        # Convert string to dict with base_url
        if isinstance(custom_models, str):
            custom_models = {"base_url": custom_models}

        # Convert single dict to list
        if isinstance(custom_models, dict):
            custom_models = [custom_models]

        # Process each custom model
        for idx, model_config in enumerate(custom_models):
            # Extract and set defaults for special fields
            nice_name = model_config.pop("nice_name", None)
            context_window_size = model_config.pop("context_window_size", 128 * 1024)
            hidden = model_config.pop("hidden", False)

            # Generate model name if not provided
            if not nice_name:
                if "model" in model_config:
                    nice_name = model_config["model"]
                else:
                    nice_name = f"Custom Model {idx:02d}" if idx > 0 else "Custom Model"

            # Skip if model_names is specified and this model isn't in it
            if model_names is not None and nice_name not in model_names:
                continue

            # Create model instance
            model_args = model_config.copy()
            if api_key and "api_key" not in model_args:
                model_args["api_key"] = api_key

            if "temperature" not in model_args:
                model_args["temperature"] = 0.1

            if "max_tokens" not in model_args:
                model_args["max_tokens"] = 4096

            if "top_p" not in model_args:
                model_args["top_p"] = 0.95

            # Handle custom URL
            custom_url = model_args.pop("custom_url", None)
            if custom_url:
                model = ChatNVNIM(**model_args)

                # Patching to use exact URL and streaming support
                async def edit_url_and_post_async(
                    *args, original_post=model.async_client._post, url=custom_url, **kwargs
                ):
                    kwargs["options"]["headers"] = {"Accept": "text/event-stream"}
                    args = (url,) + args[1:]
                    return await original_post(*args, **kwargs)

                async def edit_url_and_post(*args, original_post=model.client._post, url=custom_url, **kwargs):
                    kwargs["options"]["headers"] = {"Accept": "text/event-stream"}
                    args = (url,) + args[1:]
                    return await original_post(*args, **kwargs)

                model.async_client._post = edit_url_and_post_async
                model.client._post = edit_url_and_post
            else:
                model = ChatNVNIM(**model_args)

            tokenizer = Tokenizer(model_path=f"{TOKENIZER_PATH}")

            # Register the model
            max_tokens = context_window_size - model_args.get("max_tokens", 1024)
            model_registry.register(
                nice_name,
                model,
                tokenizer,
                max_tokens,
                hidden,
            )

    # Continue with built-in models
    models = MODELS
    for name, config in models.items():
        if model_names is None or name in model_names:
            args, max_tokens, hidden, chat_model_class, devmode_only = config

            hidden = hidden or (not chat_usd_developer_mode and devmode_only)

            args = args.copy()
            custom_url = args.pop("base_url", None)
            custom_func_id = args.pop("func_id", None) or func_id
            if custom_func_id and custom_url and "{func_id}" in custom_url:
                url = custom_url.replace("{func_id}", custom_func_id)
            else:
                url = base_url

            tokenizer = Tokenizer(model_path=f"{TOKENIZER_PATH}")

            if chat_model_class and chat_model_class == "ChatNVNIM":
                model = ChatNVNIM(api_key=api_key, base_url=url, **args)
            else:
                model = ChatOpenAI(api_key=api_key, base_url=url, **args)

            if custom_url:
                # Patching to use exact URL and streaming support
                async def edit_url_and_post(*args, original_post=model.async_client._post, url=url, **kwargs):
                    kwargs["options"]["headers"] = {"Accept": "text/event-stream"}
                    args = (url,) + args[1:]
                    return await original_post(*args, **kwargs)

                model.async_client._post = edit_url_and_post

            model_registry.register(
                name,
                model,
                tokenizer,
                max_tokens - args["max_tokens"],
                hidden,
            )


def unregister_chat_model(model_names=None):
    model_registry = get_chat_model_registry()
    models = MODELS.keys()
    for name in models:
        if model_names is None or name in model_names:
            model_registry.unregister(name)
