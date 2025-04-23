# Telegram Bot

A Telegram bot for handling premium content delivery and payment processing.

## Features

- Model selection
- Price plan selection
- Payment verification
- Google Sheets integration
- User feedback collection

## Setup Instructions

1. Create a `.env` file with the following variables:
```
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_BOT_TOKEN=your_bot_token
GOOGLE_SHEETS_WEBHOOK_URL=your_webhook_url
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the bot:
```bash
python bot.py
```

## Deployment to Railway

1. Sign up for a free account at [Railway](https://railway.app)

2. Install Railway CLI:
   - For Windows: Download from [Railway CLI Releases](https://github.com/railwayapp/cli/releases)
   - For Mac/Linux: `npm i -g @railway/cli`

3. Login to Railway:
```bash
railway login
```

4. Initialize your project:
```bash
railway init
```

5. Add your environment variables:
```bash
railway variables set TELEGRAM_API_ID=your_api_id
railway variables set TELEGRAM_API_HASH=your_api_hash
railway variables set TELEGRAM_BOT_TOKEN=your_bot_token
railway variables set GOOGLE_SHEETS_WEBHOOK_URL=your_webhook_url
```

6. Upload your images:
   - Go to Railway dashboard
   - Click on your project
   - Go to "Files" tab
   - Create an "images" folder
   - Upload all your images

7. Deploy your bot:
```bash
railway up
```

8. First-time setup:
   - After deployment, go to the "Logs" tab in Railway
   - You'll see prompts for phone number and OTP
   - Enter your phone number when prompted
   - Enter the OTP you receive
   - The bot will create a session file automatically

9. Keep the bot running:
   - Railway will automatically keep your bot running
   - If it crashes, it will automatically restart
   - You can monitor logs in the Railway dashboard

## Important Notes

- Make sure your `.env` file is properly configured
- Keep your API keys and tokens secure
- Monitor the bot's logs in Railway's "Logs" tab
- The free tier of Railway is sufficient for a Telegram bot
- Ensure all image paths in your code match the uploaded directory structure

## Troubleshooting

If the bot stops working:
1. Check the logs in Railway
2. Verify your API credentials
3. Make sure all dependencies are installed
4. Restart the deployment if needed
5. Verify that all images are properly uploaded and accessible 