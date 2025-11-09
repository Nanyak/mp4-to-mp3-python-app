from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_NAME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: str

    JWT_SECRET_KEY: str = "supersecretkey"  # Default value if not set in the environment
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        # Optional: Specify a .env file path if it's not in the root directory
        env_file = ".env"

# Initialize settings (this will automatically read from environment variables)
settings = Settings()

# You can now access settings, like:
print(settings.POSTGRES_HOST)
print(settings.POSTGRES_NAME)
