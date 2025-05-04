# 🤖 LINEBot JWT Starter

A Python Flask-based LINE Bot project that supports secure JWT signing and access token caching, with simple deployment on [Render](https://render.com).

---

## 📁 Project Structure & Description

```plaintext
linebot_jwt_starter/
🔼 app.py                      # 🔁 Flask application entry point (handles webhook)
🔼 bot/
🔼 └─ handler.py              # 📉 Handles LINE messages, currently a simple echo function for testing
🔼 auth/
🔼 ├─ generate_keys.py        # 🔐 Generates RSA keys (PEM + JWK)
🔼 ├─ generate_jwt.py         # 🔐 Generates JWT using the private key
🔼 └─ access_token.py         # 🔑 Caches and auto-renews LINE access tokens
🔼 keys/
🔼 └─ private_key.pem         # 🔐 Stores the private key (DO NOT commit to GitHub)
🔼 cache/
🔼 └─ access_token.json       # 🗾 Caches access tokens (DO NOT commit to GitHub)
🔼 .env                        # ⚙️ Stores secrets and configurations (DO NOT commit)
🔼 .env.example                # 📄 Environment variable example
🔼 requirements.txt            # 📆 Python dependencies
🔼 README.md
🔼 README.en.md
```

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate RSA Key Pair

```bash
python auth/generate_keys.py
```

This will generate:

* `private_key.pem`
* `private_key.jwk.json`
* `public_key.jwk.json`

### 3. Register the Public Key in LINE Developer Console

1. Go to [LINE Developers Console](https://developers.line.biz/console/)
2. Select your channel → Messaging API → Assertion Signing Key
3. Paste the contents of `public_key.jwk.json`
4. Save it and note down the returned `kid`

### 4. Set environment variables in `.env`

```env
LINE_CHANNEL_ID=YOUR_LINE_CHANNEL_ID
LINE_CHANNEL_KID=YOUR_KEY_ID
LINE_CHANNEL_SECRET=YOUR_CHANNEL_SECRET
LINE_PRIVATE_KEY_PATH=./keys/private_key.pem
```

### 5. Run the local Flask server

```bash
python app.py
```

---

## 🌐 Deploy on Render (Free Hosting for LINE Bot)

### 📌 Prerequisites

1. Push your project to GitHub (public recommended)
2. Create a LINE Bot and obtain Channel ID and Secret
3. Have the generated `kid` and `private_key.pem` ready

### 1️⃣ Create a Web Service

* Log in to [Render](https://dashboard.render.com/)
* Click "New Web Service" → Connect GitHub → Select your repo
* Choose `linebot_jwt_starter` repo

### 2️⃣ Configure Build and Start

| Item          | Value                               |
| ------------- | ----------------------------------- |
| Runtime       | Python 3.9 (or compatible version)  |
| Build Command | `pip install -r requirements.txt`   |
| Start Command | `python app.py`                     |

### 3️⃣ Add Environment Variables

Go to: Render Project → Environment → Add:

```
LINE_CHANNEL_ID=...
LINE_CHANNEL_KID=...
LINE_CHANNEL_SECRET=...
LINE_PRIVATE_KEY_PATH=./keys/private_key.pem
```

### 4️⃣ Upload `private_key.pem` Securely

* Use Render's Shell to create manually:

```bash
mkdir keys
nano keys/private_key.pem
# Paste the key, save with Ctrl + X
```

### 5️⃣ Configure LINE Webhook

Go to [LINE Developers Console](https://developers.line.biz/console):

* Set Webhook URL as the one provided by Render:

```
https://your-app-name.onrender.com/callback
```

* Click "Verify" to confirm success
* Make sure "Use Webhook" is ON

---

## 🔍 Dependencies

* Python >= 3.9
* Flask
* python-dotenv
* PyJWT
* jwcrypto
* requests
* line-bot-sdk==3.\*

---

## 🙏 Feedback

If you encounter issues or want to contribute, feel free to open an issue or submit a PR — and don't forget to ⭐ the repo!
