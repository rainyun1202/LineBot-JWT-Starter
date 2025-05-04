import os
import time
import jwt
from dotenv import load_dotenv

load_dotenv()

def generate_jwt():
    channel_id = os.getenv("LINE_CHANNEL_ID")
    kid = os.getenv("LINE_CHANNEL_KID")
    private_key_path = os.getenv("LINE_PRIVATE_KEY_PATH")

    if not all([channel_id, kid, private_key_path]):
        raise ValueError("環境變數缺失，請確認 .env 設定完整")

    with open(private_key_path, 'r') as f:
        private_key = f.read()
    
    now = int(time.time())
    
    headers = {
        "alg": "RS256",
        "typ": "JWT",
        "kid": kid
    }
    
    payload = {
        "iss": channel_id,
        "sub": channel_id,
        "aud": "https://api.line.me/",
        "exp": now + (60 * 30),
        "token_exp": 60 * 60 * 24 * 30
    }

    return jwt.encode(payload, private_key, algorithm="RS256", headers=headers, json_encoder=None)
