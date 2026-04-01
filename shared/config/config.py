from dotenv import load_dotenv
import os


env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", ".env"))
load_dotenv(dotenv_path=env_path)

# ----- Configuration constants ----

# --- Endpoint configuration ---
# -- .ENV variables --
# These variables should be set in the .env file at project root.

# TARGET_URL is the URL of the target LLM API endpoint that the gateway will forward requests to.
TARGET_URL = os.getenv("TARGET_URL")
# TARGET_KEY is the API key or token used by the gateway to authenticate with the target LLM API.
TARGET_KEY = os.getenv("TARGET_KEY")

# --- Authentication configuration ---
# EXPECTED_KEY_LENGTH is minimum expected length of API keys for basic validation.
EXPECTED_KEY_LENGTH = 64
# FINGERPRINT_LENGTH is the number of characters at the start of the API key used for identification.
FINGERPRINT_LENGTH = 12

# --- Quota and pricing configuration ---
# QUOTA_STRICTNESS is a multiplier applied to the estimated completion tokens when checking quota, to provide a buffer against under/overestimation.
# For example, a value of 0.5 means we will only count 50% of the max_completion_tokens towards the quota check, allowing for some flexibility.
QUOTA_STRICTNESS = 0.5

# DEFAULT_MAX_COMPLETION_TOKENS is the default value for max_completion_tokens if not specified in the request, used for estimating costs and quota.
DEFAULT_MAX_COMPLETION_TOKENS = 4096


# --- Database configuration ---
# -- .ENV variables --
# These variables should be set in the .env file at project root.

# SQLALCHEMY_DATABASE_URL is the database connection URL used by SQLAlchemy to connect to the database for logging usage and managing API keys, projects, etc.
# A database container is included in the docker-compose setup, and the URL should be set accordingly (e.g., "postgresql://user:password@db:5432/mydatabase"). For local testing, a SQLite URL is provided as a default.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")