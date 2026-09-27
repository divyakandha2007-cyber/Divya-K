from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    gemini_api_key: str = ""
    hf_token: str = ""

    gemini_model: str = "gemini-3.8-flash"

    image_model: str = "black-forest-labs/FLUX.1-schnell"
    image_provider: str = "auto"
    image_backend: str = "huggingface"

    num_panels: int = 5

    image_width: int = 768
    image_height: int = 768
    image_steps: int = 4

    app_name: str = "ComicCraft"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()