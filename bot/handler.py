from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage, QuickReply, QuickReplyItem, MessageAction,
    FlexMessage
)
from linebot.v3.webhooks import FollowEvent
from auth.access_token import get_access_token
from firebase_admin import db
from datetime import datetime
import json
import os

# === 使用者狀態節點 ===
USERS_REF = db.reference("users")

# === 載入 birthday_flex.json（支援 Render Secret Files） ===
FLEX_JSON_PATH = os.getenv("BIRTHDAY_FLEX_PATH", "bot/flex/birthday_flex.json")
with open(FLEX_JSON_PATH, "r", encoding="utf-8") as f:
    BIRTHDAY_FLEX = json.load(f)

# === 基礎回覆封裝函數 ===
def reply_message(reply_token, messages):
    access_token = get_access_token()
    configuration = Configuration(access_token=access_token)
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=messages
            )
        )

# === 使用者加入時歡迎訊息 ===
def handle_follow(event):
    reply_message(event.reply_token, [
        TextMessage(text="👋 歡迎加入，點選下方『八字命盤』開始輸入生日與性別！")
    ])

# === 回覆生日與性別選擇 Flex 卡片 ===
def ask_birthday_and_gender(reply_token):
    reply_message(reply_token, [FlexMessage(alt_text="請輸入生日與性別", contents=BIRTHDAY_FLEX)])

# === 回覆確認卡片（改為簡單文字訊息版） ===
def confirm_user_input(reply_token, user_data):
    date = user_data.get("birthday_date", "未知")
    time = user_data.get("birthday_time", "未知")
    gender = "男" if user_data.get("gender") == 1 else "女"
    confirm_text = f"✅ 你的輸入如下：\n📅 {date} {time}\n👤 性別：{gender}\n\n請輸入『分析八字』開始分析"
    reply_message(reply_token, [TextMessage(text=confirm_text)])

# === 儲存使用者資料欄位 ===
def save_user_data(user_id, field, value):
    user_ref = USERS_REF.child(user_id)
    user_ref.update({field: value})

# === 讀取使用者完整資料 ===
def get_user_data(user_id):
    return USERS_REF.child(user_id).get() or {}

# === 主處理器：處理文字訊息 ===
def handle_text_message(event):
    user_id = event.source.user_id
    msg = event.message.text.strip()
    reply_token = event.reply_token

    if msg in ["八字命盤", "開始"]:
        save_user_data(user_id, "step", "ask_input")
        return ask_birthday_and_gender(reply_token)

    user_data = get_user_data(user_id)
    step = user_data.get("step")

    # 處理生日與時間輸入（使用者以文字輸入）
    if step == "ask_input" and ("/" in msg or "-" in msg) and (":" in msg):
        try:
            dt = datetime.strptime(msg.replace("-", "/"), "%Y/%m/%d %H:%M")
            save_user_data(user_id, "birthday_date", dt.strftime("%Y/%m/%d"))
            save_user_data(user_id, "birthday_time", dt.strftime("%H:%M"))
            save_user_data(user_id, "step", "ask_gender")
            return reply_message(reply_token, [TextMessage(text="✅ 請繼續選擇性別：男 / 女")])
        except ValueError:
            return reply_message(reply_token, [TextMessage(text="❌ 日期格式錯誤，請輸入 YYYY/MM/DD HH:MM")])

    # 處理性別選擇階段
    if step == "ask_gender" and msg.startswith("性別"):
        gender_str = msg.replace("性別", "").strip()
        gender = 1 if gender_str == "男" else 0
        save_user_data(user_id, "gender", gender)
        save_user_data(user_id, "step", "confirm")
        return confirm_user_input(reply_token, get_user_data(user_id))

    # 使用者確認後分析八字
    if msg.startswith("分析八字"):
        user_data = get_user_data(user_id)
        if all(k in user_data for k in ["birthday_date", "birthday_time", "gender"]):
            from bot.bazi import get_bazi_from_input
            dt_str = f"{user_data['birthday_date']} {user_data['birthday_time']}"
            result = get_bazi_from_input(dt_str, user_data["gender"])
            return reply_message(reply_token, [TextMessage(text=result)])
        else:
            return reply_message(reply_token, [TextMessage(text="⚠️ 請先完成出生日期與性別輸入。")])

    return  # 暫時忽略其他訊息
