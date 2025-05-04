import os
import json
import time
import requests
from auth.generate_jwt import generate_jwt

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "cache")
ACCESS_TOKEN_FILE = os.path.join(CACHE_DIR, "access_token.json")

os.makedirs(CACHE_DIR, exist_ok=True)

def load_cached_token():
    if os.path.exists(ACCESS_TOKEN_FILE):
        with open(ACCESS_TOKEN_FILE, "r") as f:
            token_data = json.load(f)
        # 若存在 expires_at 且尚未過期，則回傳 access_token
        if "expires_at" in token_data and int(time.time()) < token_data["expires_at"]:
            return token_data["access_token"]
        else:
            print("⚠️ Token 已過期或缺少 expires_at 欄位")
    return None

def save_token(token, expires_in, key_id):
    expires_at = int(time.time() + expires_in - 60) # 提前 1 分鐘過期保險
    token_data = {
        "access_token": token,
        "token_type": "Bearer",
        "expires_in": expires_in,
        "key_id": key_id,
        "expires_at": expires_at
    }
    with open(ACCESS_TOKEN_FILE, "w") as f:
        json.dump(token_data, f, indent=2)
    print(f"✅ 新的 Access Token 已儲存至 {ACCESS_TOKEN_FILE}")

def get_access_token():
    cached_token = load_cached_token()
    if cached_token:
        print("使用快取 Access Token")
        return cached_token

    print("Access Token 已過期或不存在，重新取得...")
    jwt_token = generate_jwt()

    headers = { "Content-Type": "application/x-www-form-urlencoded" }
    data = {
        "grant_type": "client_credentials",
        "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        "client_assertion": jwt_token
    }

    response = requests.post("https://api.line.me/oauth2/v2.1/token", headers=headers, data=data)
    response.raise_for_status()
    result = response.json()

    save_token(result["access_token"], result["expires_in"], result.get("key_id", ""))
    print("新的 Access Token 已儲存至 access_token.json")
    return result["access_token"]

# if __name__ == "__main__":
#     token = get_access_token()
#     print("Access Token:", token)
