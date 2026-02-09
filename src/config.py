from pydantic_settings import BaseSettings
from dotenv import dotenv_values


config = dotenv_values()


class Settings(BaseSettings):
    LLM_MODEL_NAME: str = config.get("LLM_MODEL_NAME", "gpt-3.5-turbo")
    LLM_API_KEY: str = config.get("LLM_API_KEY", "")
    LLM_BASE_URL: str = config.get("LLM_BASE_URL", "https://api.openai.com/v1")

    class Config:
        env_file = ".env"  # Load environment variables from a .env file