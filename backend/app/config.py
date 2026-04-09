from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    All application configuration loaded from environment variables.
    Add new env vars here — never call os.getenv() directly in business logic.
    """

    openai_api_key: str
    chroma_db_path: str = "./chroma_db"
    chroma_collection_name: str = "fannie_mae_docs"
    pdf_directory: str = "./data/pdfs"
    embedding_model: str = "text-embedding-3-small"
    chat_model: str = "gpt-4o-mini"
    allowed_origins: str = "http://localhost:3000,http://localhost:4173"
    debug: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @field_validator("allowed_origins")
    @classmethod
    def reject_wildcard_origins(cls, value: str) -> str:
        """Prevents accidentally allowing all origins via CORS wildcard."""
        origins = [origin.strip() for origin in value.split(",")]
        if "*" in origins:
            raise ValueError(
                "Wildcard '*' is not allowed in ALLOWED_ORIGINS. "
                "Specify explicit origins instead."
            )
        return value

    def get_allowed_origins_list(self) -> list[str]:
        """Returns the allowed origins as a list, split from the comma-separated string."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]


# Single shared instance — import this everywhere instead of constructing a new Settings()
settings = Settings()
