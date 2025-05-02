
# LineBot JWT Starter

## Project Introduction
This is a simple LINE Bot example with the following features:
- Flask is used to set up the Webhook callback
- Automatically generates and caches JWT, then retrieves the access token
- Echoes back user text messages
- Provides a professional, modular structure that facilitates future development and expansion

## Technologies Used
- Python 3
- Flask
- line-bot-sdk v3
- jwcrypto

## Installation and Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set environment variables
Create a `.env` file (or set environment variables for your Render environment) and add the following entries:
```env
LINE_CHANNEL_ID=YOUR_LINE_CHANNEL_ID
LINE_CHANNEL_KID=YOUR_LINE_CHANNEL_KID
LINE_CHANNEL_SECRET=YOUR_CHANNEL_SECRET
PRIVATE_KEY_PATH=./keys/private_key.pem
```

### 3. Prepare private key
Place your `private_key.pem` file in the `./keys/` folder, ensuring it's in PEM format (RSA 2048):
```bash
-----BEGIN RSA PRIVATE KEY-----
...
-----END RSA PRIVATE KEY-----
```

### 4. Start the server (for local testing)
```bash
python app/main.py
```

### 5. Deploy on Render
To deploy your LINE Bot on Render, follow these steps:
1. Push your code to a GitHub repository.
2. Create a new web service on Render, linking your GitHub repository.
3. Set up environment variables in the Render dashboard (same as `.env` file).
4. Render will automatically build and deploy the service.
5. Once deployed, update the Webhook URL in your LINE official account with the URL provided by Render, for example:
```
https://your-app-name.onrender.com/callback
```
