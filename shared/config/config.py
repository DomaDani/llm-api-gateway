from dotenv import load_dotenv
import os


env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", ".env"))
load_dotenv(dotenv_path=env_path)

# ----- Configuration -----
# These variables should be set in the .env file at project root.
# See .env.example for reference.

# --- Endpoint configuration ---

TARGET_URL = os.getenv("TARGET_URL")
TARGET_KEY = os.getenv("TARGET_KEY")

PROVIDER_ID = os.getenv("PROVIDER_ID")

# --- Authentication configuration ---

EXPECTED_KEY_LENGTH = int(os.getenv("EXPECTED_KEY_LENGTH", 64))
FINGERPRINT_LENGTH = int(os.getenv("FINGERPRINT_LENGTH", 12))

# --- Quota and pricing configuration ---

QUOTA_STRICTNESS = float(os.getenv("QUOTA_STRICTNESS", 0.5))
DEFAULT_MAX_COMPLETION_TOKENS = int(os.getenv("DEFAULT_MAX_COMPLETION_TOKENS", 4096))
DEFAULT_INPUT_MTOKEN_PRICE = float(os.getenv("DEFAULT_INPUT_MTOKEN_PRICE", 0.2))
DEFAULT_OUTPUT_MTOKEN_PRICE = float(os.getenv("DEFAULT_OUTPUT_MTOKEN_PRICE", 1.1))

# --- Database configuration ---

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")