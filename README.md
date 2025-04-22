# Telegram Bot

A Telegram bot for managing user interactions and payments.

## Features

- Model selection
- Price plan selection
- Payment verification
- Google Sheets integration
- User feedback collection

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your credentials:
   ```
   TELEGRAM_API_ID=your_api_id
   TELEGRAM_API_HASH=your_api_hash
   TELEGRAM_BOT_TOKEN=your_bot_token
   GOOGLE_SHEETS_WEBHOOK_URL=your_webhook_url
   ```

## Running the Bot

```
python bot.py
```

## Deployment

The bot can be deployed on Railway for 24/7 operation. 