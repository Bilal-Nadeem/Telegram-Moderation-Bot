# Telegram Moderation Bot

This is a Python-based Telegram bot that helps manage a Telegram group by setting daily message limits, locking/unlocking the group or individual users, and managing a whitelist for allowed URLs.

## Features

- **Group Lock/Unlock**: Admins can lock or unlock the entire group, restricting or allowing message sending.
- **User Lock/Unlock**: Automatically locks users when they exceed a specified message limit or posts unwhitelisted links.
- **Daily Reset**: Automatically resets message limits every day at a specific time.
- **Whitelist Management**: Admins can add or remove URLs from a whitelist, allowing certain links to bypass restrictions.
- **Welcome Message**: Sends a welcome message with links to YouTube and Instagram for new users.

## Requirements

- Python 3.x
- `python-telegram-bot` library
- `pytz` for timezone handling

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/telegram-group-bot.git
   ```

2. Navigate to the project directory:

   ```bash
   cd telegram-group-bot
   ```

3. Install the required dependencies:

   ```bash
   pip install python-telegram-bot pytz
   ```

4. Replace "Token" with your actual Telegram Bot API token in the code.
    
## Usage

1. Run the bot:

   ```bash
   python bot.py
   ```

2. Admin Commands

    - `/lock all` - Lock the group (prevent all users from sending messages).
    - `/unlock all` - Unlock the group (allow users to send messages).
    - `/whitelist <url>` - Add a URL to the whitelist.
    - `/rmwhitelist <url>` - Remove a URL from the whitelist.

## License

This project is licensed under the MIT License.