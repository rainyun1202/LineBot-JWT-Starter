import os
from flask import Flask, request, abort
from dotenv import load_dotenv

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import (
    MessageEvent, TextMessageContent,
    FollowEvent, PostbackEvent
)
from bot.handler import handle_text_message

load_dotenv()

app = Flask(__name__)
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# ✅ 健康檢查用（給 uptime robot / render ping）
@app.route("/health", methods=["GET", "HEAD"])
def health_check():
    return "OK", 200

# ✅ 訊息處理（文字訊息）
@handler.add(MessageEvent, message=TextMessageContent)
def handle_text(event):
    handle_text_message(event)

@handler.add(PostbackEvent)
def handle_postback_event(event):
    from bot.handler import handle_postback
    handle_postback(event)

