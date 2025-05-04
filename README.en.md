📘 Language Selection｜語言選擇: [中文](README.md) | [English](README.en.md)

# 🤖 LINEBot JWT Starter

A Python Flask-based LINE Bot project that supports secure JWT signing and access token caching. Deployable with one click on [Render](https://render.com).

---

## 📁 Project Structure & Description

```plaintext
linebot_jwt_starter/
🔼 app.py                      # 🔁 Flask entry point (Webhook endpoint)
🔼 bot/
🔼 └─ handler.py              # 📉 Handles messages from LINE (simple echo logic)
🔼 auth/
🔼 ├─ generate_keys.py        # 🔐 Generates RSA keys (PEM + JWK)
🔼 ├─ generate_jwt.py         # 🔐 Generates JWT from private key
🔼 └─ access_token.py         # 🔑 Handles access token caching and renewal
🔼 keys/
🔼 └─ private_key.pem         # 🔐 RSA private key (should not be pushed to GitHub)
🔼 cache/
🔼 └─ access_token.json       # 🗾 Cached access token (should not be pushed to GitHub)
🔼 .env                        # ⚙️ Local environment variables (should not be committed)
🔼 .env.example                # 📄 Example for .env variables
🔼 requirements.txt            # 📦 Python dependencies
🔼 README.md
🔼 README.en.md
```

---

## 🚀 Quick Start

### 1. Install Dependencies

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

### 3. Register Public Key on LINE Developer Console

1. Log into [LINE Developers Console](https://developers.line.biz/console/)
2. Go to your channel → Messaging API → Assertion Signing Key
3. Paste the content of `public_key.jwk.json`
4. Save and note the generated `kid`

### 4. Set up `.env`

```env
LINE_CHANNEL_ID=YOUR_LINE_CHANNEL_ID
LINE_CHANNEL_KID=YOUR_KEY_ID
LINE_CHANNEL_SECRET=YOUR_CHANNEL_SECRET
LINE_PRIVATE_KEY_PATH=./keys/private_key.pem
```

> 📝 If you're using Secret Files on Render, change the last line to:
>
> ```env
> LINE_PRIVATE_KEY_PATH=/etc/secrets/private_key.pem
> ```

---

## 🌐 Deploying to Render (Free Hosting)

### 📌 Prerequisites

1. Push your project to GitHub (preferably public)
2. Create your LINE bot and get your Channel ID & Secret
3. Generate and store the `kid` and `private_key.pem`

### 1️⃣ Create a Web Service

* Log into [Render Dashboard](https://dashboard.render.com/)
* Click "New Web Service" → Connect your GitHub repo
* Select the `linebot_jwt_starter` project

### 2️⃣ Configure Build Settings

| Field         | Value                             |
| ------------- | --------------------------------- |
| Runtime       | Python 3.9 (or compatible)        |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app`                |

### 3️⃣ Set Environment Variables

Go to your Render project → Environment → Add Environment Variables:

```env
LINE_CHANNEL_ID=...
LINE_CHANNEL_KID=...
LINE_CHANNEL_SECRET=...
LINE_PRIVATE_KEY_PATH=/etc/secrets/private_key.pem
```

### 4️⃣ Upload Private Key with Secret Files

Render provides official secret file management:

> 🔒 **Secret Files**
> Store plaintext files containing secret data (such as a .env file or a private key).
> Access during builds and at runtime from your app's root, or from `/etc/secrets/<filename>`

**Steps:**

1. Go to the Advanced tab → `Secret Files`
2. Click "Add Secret File"
3. Upload `private_key.pem`, which Render will mount to:

   ```
   /etc/secrets/private_key.pem
   ```
4. Ensure your `.env` uses that same path.

✅ This ensures your key persists even after redeploys!

### 5️⃣ LINE Webhook Setup

In [LINE Developers Console](https://developers.line.biz/console):

* Webhook URL should be your Render domain, e.g.:

```
https://your-app-name.onrender.com/callback
```

* Click "Verify" to test
* Make sure "Use Webhook" is enabled

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

If you have suggestions, feel free to submit a PR, open an issue, or give this project a ⭐.