from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage, QuickReply, QuickReplyItem, MessageAction,
    FlexMessage
)
from linebot.v3.messaging.models import FlexContainer
from linebot.v3.webhooks import PostbackEvent
from auth.access_token import get_access_token
from firebase_admin import db
from datetime import datetime
import json
import os

# === 使用者狀態節點 ===
USERS_REF = db.reference("users")

# === 錯誤最大次數 ===
MAX_ERRORS = 3

# === 載入 birthday_flex.json（支援 Render Secret Files） ===
FLEX_JSON_PATH = os.getenv("BIRTHDAY_FLEX_PATH")
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

# === 回覆生日與性別選擇 Flex 卡片 ===
def ask_birthday_and_gender(reply_token):
    container = FlexContainer.from_dict(BIRTHDAY_FLEX)
    reply_message(reply_token, [
        FlexMessage(alt_text="請輸入生日與性別", contents=container),
        TextMessage(text="📌 請依序完成以下步驟：\n1️⃣ 選擇生日\n2️⃣ 選擇出生時辰\n3️⃣ 點選性別")
    ])

# === 回覆確認卡片 ===
def confirm_user_input(reply_token, user_data):
    date = user_data.get("birthday_date", "未填")
    time = user_data.get("birthday_time", "未填")
    gender = "男" if user_data.get("gender") == 1 else "女" if user_data.get("gender") == 0 else "未填"
    confirm_text = f"✅ 你的輸入如下：\n📅 {date} {time}\n👤 性別：{gender}\n\n請輸入『分析八字』開始分析"
    reply_message(reply_token, [TextMessage(text=confirm_text)])

# === 儲存使用者資料欄位 ===
def save_user_data(user_id, field, value):
    user_ref = USERS_REF.child(user_id)
    user_ref.update({field: value})

# === 讀取使用者完整資料 ===
def get_user_data(user_id):
    return USERS_REF.child(user_id).get() or {}

# === 錯誤次數加一 ===
def increment_error(user_id):
    user_ref = USERS_REF.child(user_id)
    data = user_ref.get() or {}
    errors = data.get("errors", 0) + 1
    if errors >= MAX_ERRORS:
        user_ref.update({"step": None, "errors": 0})
        return True
    user_ref.update({"errors": errors})
    return False

# === 主處理器：處理文字訊息 ===
def handle_text_message(event):
    user_id = event.source.user_id
    msg = event.message.text.strip()
    reply_token = event.reply_token

    user_data = get_user_data(user_id)
    step = user_data.get("step")

    if msg in ["八字命盤", "開始"]:
        save_user_data(user_id, "step", "ask_input")
        save_user_data(user_id, "errors", 0)
        save_user_data(user_id, "birthday_date", None)
        save_user_data(user_id, "birthday_time", None)
        save_user_data(user_id, "gender", None)
        return ask_birthday_and_gender(reply_token)

    if step == "done":
        return reply_message(reply_token, [
            TextMessage(text="✅ 你已完成輸入並分析，如需重新開始請輸入『八字命盤』")
        ])

    if step in ["ask_input", "ask_gender"]:
        if msg.startswith("性別"):
            if not user_data.get("birthday_date") or not user_data.get("birthday_time"):
                if increment_error(user_id):
                    return reply_message(reply_token, [TextMessage(text="⚠️ 多次輸入錯誤，請重新輸入『八字命盤』開始")])
                return reply_message(reply_token, [TextMessage(text="⚠️ 請先完成出生日期與時辰的輸入")])
            gender_str = msg.replace("性別", "").strip()
            if gender_str not in ["男", "女"]:
                if increment_error(user_id):
                    return reply_message(reply_token, [TextMessage(text="⚠️ 多次輸入錯誤，請重新輸入『八字命盤』開始")])
                return reply_message(reply_token, [TextMessage(text="⚠️ 請輸入正確性別：性別 男 或 性別 女")])
            gender = 1 if gender_str == "男" else 0
            save_user_data(user_id, "gender", gender)
            save_user_data(user_id, "step", "confirm")
            return confirm_user_input(reply_token, get_user_data(user_id))

    if step == "confirm" and msg.startswith("分析八字"):
        if all(user_data.get(k) for k in ["birthday_date", "birthday_time", "gender"]):
            save_user_data(user_id, "step", "done")
            from bot.bazi import get_bazi_from_input
            dt_str = f"{user_data['birthday_date']} {user_data['birthday_time']}"
            result = get_bazi_from_input(dt_str, user_data["gender"])
            return reply_message(reply_token, [TextMessage(text=result)])
        return reply_message(reply_token, [TextMessage(text="⚠️ 請先完成所有輸入再進行分析")])

    return reply_message(reply_token, [TextMessage(text="⚠️ 請依指示操作，或輸入『八字命盤』重新開始")])

# === 處理 Flex Message 的 Postback 選擇 ===
def handle_postback(event: PostbackEvent):
    user_id = event.source.user_id
    data = event.postback.data
    reply_token = event.reply_token

    if data == "birthday_selected":
        date = event.postback.params.get("date")
        if date:
            save_user_data(user_id, "birthday_date", date.replace("-", "/"))
            save_user_data(user_id, "step", "ask_input")
            return reply_message(reply_token, [
                TextMessage(text=f"✅ 出生日期已設定為：{date.replace('-', '/')}\n請繼續選擇出生時辰")
            ])

    if data == "birthtime_selected":
        time = event.postback.params.get("time")
        if time:
            save_user_data(user_id, "birthday_time", time)
            user_data = get_user_data(user_id)
            if user_data.get("birthday_date"):
                save_user_data(user_id, "step", "ask_gender")
                return reply_message(reply_token, [TextMessage(text=f"✅ 出生時辰已設定為：{time}\n請點選性別")])
            else:
                if increment_error(user_id):
                    return reply_message(reply_token, [TextMessage(text="⚠️ 多次錯誤，請重新輸入『八字命盤』開始")])
                return reply_message(reply_token, [TextMessage(text="⚠️ 請先選擇出生日期")])
