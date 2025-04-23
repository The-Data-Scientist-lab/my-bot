# Telegram Bot

A Telegram bot for handling premium content delivery and payment processing.

## Features

- Model selection
- Price plan selection
- Payment verification
- Google Sheets integration
- User feedback collection
- Automatic OTP verification
- 24/7 operation on Railway

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

2. Create a `.env` file with the following variables:
```
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_BOT_TOKEN=your_bot_token
GOOGLE_SHEETS_WEBHOOK_URL=your_webhook_url
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the bot locally (for testing):
```bash
python bot.py
```

## Deployment to Railway

1. Sign up for a free account at [Railway.app](https://railway.app)

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

# Telegram Bot on Google Colab

This repository contains a Telegram bot that can run continuously on Google Colab.

## Setup Instructions

1. **Create a new Google Colab notebook**
   - Go to [Google Colab](https://colab.research.google.com)
   - Create a new notebook

2. **Upload your files**
   - Upload `colab_bot.py` and `.env` files to your Colab notebook
   - Make sure your `.env` file contains:
     ```
     API_ID=your_api_id
     API_HASH=your_api_hash
     BOT_TOKEN=your_bot_token
     ```

3. **Install required packages**
   ```python
   !pip install telethon python-dotenv
   ```

4. **Run the bot**
   ```python
   !python colab_bot.py
   ```

## Important Notes

- Google Colab sessions will disconnect after a period of inactivity. To keep your bot running:
  1. Use the "Runtime" menu
  2. Select "Change runtime type"
  3. Set "Hardware accelerator" to "None"
  4. Enable "Keep runtime alive when idle"

- For continuous operation, you might want to use a service like [UptimeRobot](https://uptimerobot.com/) to ping your Colab notebook periodically.

## Troubleshooting

If you encounter any issues:
1. Make sure all environment variables are correctly set in your `.env` file
2. Check that you have the correct API credentials from Telegram
3. Ensure all required packages are installed
4. Restart the runtime if needed 