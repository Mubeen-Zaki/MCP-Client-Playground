from typing import Any
from src.config import Settings
from langchain_openai import ChatOpenAI


settings = Settings()


def get_llm(tools: Any = None) -> ChatOpenAI:
    llm_client = ChatOpenAI(
        model=settings.LLM_MODEL_NAME,
        api_key=settings.LLM_API_KEY,
        base_url=settings.LLM_BASE_URL
    )
    if tools:
        llm_client = llm_client.bind_tools(tools)
    return llm_client

