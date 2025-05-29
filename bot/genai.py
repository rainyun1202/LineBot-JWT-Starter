import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

gemini_api = os.getenv("GEMINI_API")

client = genai.Client(api_key=gemini_api,
                      http_options={'api_version': 'v1alpha'})

def ask_gemini_ai(bazi_result: str) -> str:

    prompt = (
        "請根據以下使用者的生辰八字命盤內容，提供精簡清楚的命理分析：\n\n"
        f"{bazi_result}\n\n"
        "請以條列清單呈現分析重點，例如：\n"
        "- 出生年份與五行偏重\n"
        "- 日主強弱、格局解釋\n"
        "- 可能的職業方向與建議\n"
        "- 感情或健康注意事項\n"
    )
    
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt,
    )

    return response.text
