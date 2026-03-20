import logging
import os
import warnings

warnings.filterwarnings(
    "ignore",
    message=r".*Core Pydantic V1 functionality isn't compatible with Python 3\.14 or greater.*",
    category=UserWarning,
    module=r"langchain_core\._api\.deprecation",
)

from langchain.chat_models import init_chat_model
from langchain_google_genai import ChatGoogleGenerativeAI


def call_ai(model: str, pattern: str, prompt: str) -> str:
    logging.info("Calling openai API without tools")
    llm = _create_llm(model)
    response = llm.invoke(_create_messages(pattern, prompt))
    logging.info(f"Input tokens: {response.usage_metadata["input_tokens"]}")
    logging.info(f"Output tokens: {response.usage_metadata["output_tokens"]}")
    return response.text

def _create_llm(model: str) -> ChatGoogleGenerativeAI:
    if model.startswith("gemini"):
        return ChatGoogleGenerativeAI(
            model=model,
            temperature=0,
            google_api_key=os.environ.get("GOOGLE_API_KEY"),
        )

    return init_chat_model(model)


def _create_messages(pattern: str, prompt: str):
    return [
        {
            "role": "system",
            "content": pattern,
        },
        {
            "role": "user",
            "content": prompt,
        }
    ]
