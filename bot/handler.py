from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage
)
from auth.access_token import get_access_token
from bot.bazi import get_bazi_from_input

# def reply_echo_message(event):
#     access_token = get_access_token()
#     configuration = Configuration(access_token=access_token)
#     with ApiClient(configuration) as api_client:
#         line_bot_api = MessagingApi(api_client)
#         line_bot_api.reply_message_with_http_info(
#             ReplyMessageRequest(
#                 reply_token=event.reply_token,
#                 messages=[TextMessage(text=event.message.text)]
#             )
#         )
        
def reply_echo_message(event):
    user_input = event.message.text.strip()

    # 偵測生日格式
    if ("/" in user_input or "-" in user_input) and ":" in user_input:
        reply_text = get_bazi_from_input(user_input)
    else:
        reply_text = "👋 請輸入生日時間，例如：1999/09/04 23:00"

    access_token = get_access_token()
    configuration = Configuration(access_token=access_token)
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_text)]
            )
        )