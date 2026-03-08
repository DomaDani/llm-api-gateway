from ..utils.hashing import hash_key

fake_db = {
    "API_KEYS": {
        "TTcj1lxYOY9d": {
            "id": 1,
            "fingerprint": "TTcj1lxYOY9d",
            "key_hash": hash_key("TTcj1lxYOY9dB25bVh6IKfOrwW8ERIWHXJKqxYYwxHM-_LHTf3isqFhitJxpVGiZaLf2GVwiKsQZLhnR-xYJ2Q"),
            "is_active": True
        }
    },
    "V_LIMIT_TRACKING": {
        1 : {
            "limit_value": 1000000, #CURRENTLY ONLY TOKENS, LATER REQUEST OR MONEY IS ALSO POSSIBLE
            "spent_value": 0
            # EXPIRATION AND RENEWING NOT MODELED
        }
    }
}

def mock_db_key_check(api_key: str) -> dict:

    api_fingerprint = api_key[:12]

    return fake_db["API_KEYS"][api_fingerprint]

def mock_db_limit_check(key_id: int) -> dict:
    return fake_db["V_LIMIT_TRACKING"][key_id]

def mock_limit_change(key_id: int, changeBy: int):
    fake_db["V_LIMIT_TRACKING"][key_id]["spent_value"] += changeBy