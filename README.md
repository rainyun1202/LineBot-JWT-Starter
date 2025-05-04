📘 語言選擇｜Language: [中文](README.md) | [English](README.en.md)

# 🤖 LINEBot JWT Starter

一個使用 Python Flask 快速部署的 LINE Bot 專案，支援 JWT 安全簽章與 Access Token 快取，並可一鍵部署到 [Render](https://render.com)。

---

## 📁 專案結構與說明

```plaintext
linebot_jwt_starter/
🔼 app.py                      # 🔁 Flask 應用進入點 (Webhook 的接收處)
🔼 bot/
🔼 └─ handler.py              # 📉 處理 LINE 傳來的訊息，簡易 echo 功能，目前僅為測試版本
🔼 auth/
🔼 ├─ generate_keys.py        # 🔐 產生 RSA 金鑰 (PEM + JWK)
🔼 ├─ generate_jwt.py         # 🔐 使用私鑰產生 JWT
🔼 └─ access_token.py         # 🔑 快取 + 自動換發 LINE Access Token
🔼 keys/
🔼 └─ private_key.pem         # 🔐 儲存私鑰 (勿上傳 GitHub)
🔼 cache/
🔼 └─ access_token.json       # 🗾 Access Token 快取檔案 (勿上傳 GitHub)
🔼 .env                        # ⚙️ 儲存秘密參數 (勿上傳 GitHub)
🔼 .env.example                # 📄 .env 格式參考
🔼 requirements.txt            # 📆 專案依賴套件
🔼 README.md
🔼 README.en.md
```

---

## 🚀 快速啟動

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 產生金鑰

```bash
python auth/generate_keys.py
```

將產生:

* `private_key.pem`
* `private_key.jwk.json`
* `public_key.jwk.json`

### 3. 新增公鑰到 LINE Developer Console

1. 登入 [LINE Developers Console](https://developers.line.biz/console/)
2. 選擇你的 channel → Messaging API → Assertion Signing Key
3. 貼上 `public_key.jwk.json` 的內容
4. 儲存後會獲得一組 `kid`，請記下

### 4. 設定 .env 環境變數

```env
LINE_CHANNEL_ID=YOUR_LINE_CHANNEL_ID
LINE_CHANNEL_KID=YOUR_KEY_ID
LINE_CHANNEL_SECRET=YOUR_CHANNEL_SECRET
LINE_PRIVATE_KEY_PATH=./keys/private_key.pem
```

### 5. 啟動 Flask Webhook 服務

```bash
python app.py
```

## 🌐 Render 部署教學（免費部署 LINE Bot）

### 📌 前置準備

1. 將專案 push 到 GitHub（建議公開 repo）
2. 建立 LINE Bot 並取得 Channel ID、Secret
3. 已產出並記下 `kid` 和 `private_key.pem`

### 1️⃣ 建立 Web Service

* 登入 [Render](https://dashboard.render.com/)
* 點選「New Web Service」 → 選擇 GitHub 並授權存取 repo
* 選擇 `linebot_jwt_starter` 專案

### 2️⃣ 設定建置方式

| 項目          | 設定值                            |
| ------------- | --------------------------------- |
| Runtime       | Python 3.9 (或相容版本)           |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python app.py`                   |

### 3️⃣ 設定環境變數（Environment Variables）

點選 Render 專案 → Environment → Add Environment Variables：

```
LINE_CHANNEL_ID=...
LINE_CHANNEL_KID=...
LINE_CHANNEL_SECRET=...
LINE_PRIVATE_KEY_PATH=./keys/private_key.pem
```

### 4️⃣ 手動上傳私鑰 `private_key.pem`

* 點選「Shell」或使用 `Deploy Script`

```bash
mkdir keys
nano keys/private_key.pem
# 貼上內容，Ctrl + X 儲存
```

### 5️⃣ LINE Webhook 設定

前往 [LINE Developers Console](https://developers.line.biz/console)

* Webhook URL 填入 Render 給你的 URL，例如：

```
https://your-app-name.onrender.com/callback
```

* 點選「Verify」測試是否成功
* 確保已啟用 Use Webhook

---

## 🔍 依賴套件

* Python >= 3.9
* Flask
* python-dotenv
* PyJWT
* jwcrypto
* requests
* line-bot-sdk==3.\*

---

## 🙏 Feedback

如有問題歡迎提交 PR、issue，或幫我們加星 ⭐。
