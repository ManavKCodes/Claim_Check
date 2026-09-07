from functools import lru_cache
import os


class Settings:
    def __init__(self) -> None:
        self.app_name = "ClaimCheck"
        self.app_env = os.getenv("APP_ENV", "development")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./claimcheck.db")
        self.openfoodfacts_base_url = os.getenv(
            "OPENFOODFACTS_BASE_URL", "https://world.openfoodfacts.org"
        )
        self.openfoodfacts_user_agent = os.getenv(
            "OPENFOODFACTS_USER_AGENT", "ClaimCheck/0.1 (configure-contact-before-production)"
        )
        self.openfoodfacts_timeout_seconds = float(os.getenv("OPENFOODFACTS_TIMEOUT_SECONDS", "10"))
        self.allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
        self.max_upload_bytes = int(os.getenv("MAX_UPLOAD_BYTES", "10485760"))
        self.benchmark_path = os.getenv("BENCHMARK_PATH", "data/benchmark/records.json")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
