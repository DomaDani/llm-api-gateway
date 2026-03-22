from dotenv import load_dotenv
import os


env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", ".env"))
load_dotenv(dotenv_path=env_path)

TARGET_URL = os.getenv("TARGET_URL")
TARGET_KEY = os.getenv("TARGET_KEY")

EXPECTED_KEY_LENGTH = 64
FINGERPRINT_LENGTH = 12

QUOTA_STRICTNESS = 0.5

DEFAULT_MAX_COMPLETION_TOKENS = 4096

#####

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "sqlite:///./test.db")