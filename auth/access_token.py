import os
import json
import time
import requests
from auth.generate_jwt import generate_jwt
from firebase_admin import credentials, initialize_app, db
import firebase_admin

# === Firebase 初始化 ===
FIREBASE_CREDENTIAL_PATH = os.getenv("FIREBASE_CREDENTIAL_PATH")
FIREBASE_DB_URL = os.getenv("FIREBASE_DB_URL")

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIAL_PATH)
    initialize_app(cred, {
        'databaseURL': FIREBASE_DB_URL
    })

# === Firebase 資料位置 ===
TOKEN_REF = db.reference("line_bot/access_token")

# === 本地備份用路徑 ===
CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "cache")
ACCESS_TOKEN_FILE = os.path.join(CACHE_DIR, "access_token.json")
os.makedirs(CACHE_DIR, exist_ok=True)

def load_token():
    # 嘗試從 Firebase 中讀取 access token
    token_data = TOKEN_REF.get()
    if token_data and "expires_at" in token_data:
        if int(time.time()) < token_data["expires_at"]:
            print("使用 Firebase 中的 Access Token")
            return token_data["access_token"]
        else:
            print("⚠️ Firebase 中的 Token 已過期")
    return None

def save_token(token, expires_in, key_id):
    expires_at = int(time.time() + expires_in - 60)
    token_data = {
        "access_token": token,
        "token_type": "Bearer",
        "expires_in": expires_in,
        "key_id": key_id,
        "expires_at": expires_at
    }
    # 同步儲存到 Firebase
    TOKEN_REF.set(token_data)
    # 同步儲存到本地快取檔
    with open(ACCESS_TOKEN_FILE, "w") as f:
        json.dump(token_data, f, indent=2)
    print(f"✅ 新的 Access Token 已儲存至 Firebase 與 {ACCESS_TOKEN_FILE}")

def get_access_token():
    cached_token = load_token()
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
