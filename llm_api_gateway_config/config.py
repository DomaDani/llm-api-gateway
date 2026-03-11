from dotenv import load_dotenv
import os

load_dotenv()

TARGET_URL = os.getenv("TARGET_URL")
TARGET_KEY = os.getenv("TARGET_KEY")

EXPECTED_KEY_LENGTH = 64
FINGERPRINT_LENGTH = 12

QUOTA_STRICTNESS = 0.5

DEFAULT_MAX_COMPLETION_TOKENS = 4096

#####

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "sqlite:///./test.db")