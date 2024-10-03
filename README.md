# 🚀 Telegram Message Forwarding Bot

Welcome to the **Telegram Message Forwarding Bot**, a robust solution for forwarding messages, videos, and other media from users directly to the owner. This bot not only helps you manage incoming messages efficiently but also allows you to respond seamlessly.

![Telegram Bot](https://example.com/your-image.png) <!-- Replace with an actual image link -->

---

## 📋 Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Running the Bot](#running-the-bot)
  - [Commands](#commands)
- [Logging](#logging)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## ⭐ Features

- **Forward Messages**: Automatically forwards all types of messages from users to the owner.
- **Reply Support**: Replies sent by the owner are forwarded back to the respective users.
- **Toggle Forwarding**: Easily enable or disable message forwarding with the `/switch` command.
- **Status Check**: Use the `/status` command to see if forwarding is currently enabled or disabled.
- **Logging**: All actions are logged for future reference in a `message_log.json` file.
- **Error Handling**: Automatically manages errors and attempts to reconnect if the bot crashes.
- **Multi-Format Support**: Handles text, photos, videos, documents, voice messages, and audio files.

---

## 🛠️ Getting Started

### Prerequisites

- **Python**: Version 3.7 or higher.
- **pip**: Python package installer.

### Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/telegram-bot.git
    cd telegram-bot
    ```

2. **Create a virtual environment** (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Configuration**:
   - Open the bot script file and replace the placeholders:
     - Set your Telegram user ID in `OWNER_CHAT_ID`.
     - Set your bot token in `BOT_TOKEN`.

---

## 🏃‍♂️ Usage

### Running the Bot

Run the bot using:

```bash
python your_bot_script.py
```
