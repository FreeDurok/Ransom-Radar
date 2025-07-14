# 🕷 Ransom Radar

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)


<p align="center">
  <img src=".img/Ransom Radar.png" alt="Ransom Radar Logo" width="300"/>
</p>

## Description
Get 🚨 **real-time alerts** on new ransomware posts, leaks, and extortion attempts.  
This tool polls [RansomLook](https://www.ransomlook.io), [RansomFeed](https://ransomfeed.it), and [RansomLive](https://www.ransomware.live), sending alerts to a Telegram channel or group.

---

## 🚀 Features
- Polls RansomLook and RansomFeed API for new ransomware victims.
- Maintains a local `.cache` to avoid duplicate alerts.
- Sends rich notifications (with group, victim, date, description, screenshot, etc.) via Telegram.
- Lightweight and modular Python design.
- **Optional AI enrichment:** Automatically summarizes victim descriptions and generates insights using configurable AI models (e.g., Hugging Face, GPT-4, DeepSeek). AI features can be enabled or disabled in the configuration.

---

## ⚙ Requirements
- Python 3.8+
- Libraries listed in `requirements.txt`

```bash
git clone https://github.com/FreeDurok/Ransom-Radar.git
cd Ransom-Radar

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

---
## 🔑 Telegram Setup
1. Create a bot with [BotFather](https://t.me/BotFather) on Telegram.
2. Obtain your **bot token**.
3. Add the bot to your channel or group and give it permission to post messages.
4. Obtain your **chat ID**.  
 - For groups, you can use the `@RawDataBot` to get the chat ID.
---

## 📝 Configuration
Edit `config.py`:

```python
BASE_URL = "https://www.ransomlook.io"
POLL_INTERVAL = 150  # 2.5 minutes
TELEGRAM_TOKEN = "your_telegram_bot_token_here"
TELEGRAM_CHAT_ID = "your_channel_or_group_chat_id_here"
```

Alternatively, you can use a `.env` file for configuration.  
The project supports environment variables via the `python-dotenv` library.

Create a `.env` file in the project root with the following content:

This allows you to keep sensitive information out of your codebase and manage configuration more securely.

### 🤖 AI Module Configuration

Configuration for AI model selection and API access.

- `AI_ENABLED`: Enables or disables AI features.
- `AI_MODEL`: Specifies the model to use for inference. You can choose from public models on Hugging Face Model Hub (e.g., "moonshotai/kimi-k2-instruct", "gpt-4", "deepseek/deepseek-r1-0528").
- `API_KEY`: API key for authentication. By default, uses the Hugging Face token from the environment variable `HF_API_KEY`.
- `API_URL`: Endpoint for model inference. Defaults to Hugging Face Novita Inference API.
- `PROXY_URL`: Optional proxy URL, loaded from the environment variable `PROXY_URL`.

---


## 🚀 Run

```bash
python3 main.py
```

It will start polling immediately and notify your Telegram channel/group.

---

## 📂 Cache

Keeps a `.cache/state.json` file to track already notified posts.

---

## 📜 Create the systemd service file

Create a file at:
```
touch /etc/systemd/system/ransom-radar.service
```

with the following content:

```ini
[Unit]
Description=Ransom Radar - Ransomware Telegram Notifier
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/Ransom-Radar
ExecStart=/opt/Ransom-Radar/venv/bin/python3 /opt/Ransom-Radar/main.py
Restart=always
RestartSec=10
User=ubuntu

[Install]
WantedBy=multi-user.target
```

🔎 Note: replace User=ubuntu with the actual system user that owns the project directory.

🔎 Note: move or clone the project in `/opt` folder.

```bash
sudo systemctl daemon-reload
sudo systemctl enable ransom-radar
sudo systemctl start ransom-radar
sudo systemctl status ransom-radar
```

## 📄 License

MIT



