# Telegram Message Forwarding Bot

A Telegram bot that forwards messages, videos, and other media types to the owner. The bot also allows the owner to reply to users directly. It includes a command to toggle the forwarding feature on and off, along with built-in error handling and logging.

## Features

- **Forward Messages**: Automatically forwards all types of messages from users to the owner.
- **Reply Support**: Replies sent by the owner are forwarded back to the respective users.
- **Toggle Forwarding**: Use the `/switch` command to enable or disable message forwarding.
- **Status Check**: Use the `/status` command to check if forwarding is currently enabled or disabled.
- **Logging**: All actions are logged for future reference.
- **Error Handling**: Automatically handles errors and attempts to reconnect if the bot crashes.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- `pip` (Python package installer)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/telegram-bot.git
    cd telegram-bot
    ```

2. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Replace the placeholders in the script:
   - Set your Telegram user ID in `OWNER_CHAT_ID`.
   - Set your bot token in `BOT_TOKEN`.

### Running the Bot

Run the bot using:

```bash
python your_bot_script.py
