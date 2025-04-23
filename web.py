from flask import Flask
import threading
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_bot():
    try:
        import bot
        bot.main()
    except Exception as e:
        logger.error(f"Bot error: {str(e)}")

if __name__ == '__main__':
    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True  # Make thread daemon so it exits when main thread exits
    bot_thread.start()
    
    # Get port from environment variable
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"Starting web server on port {port}")
    
    # Run the web server
    app.run(host='0.0.0.0', port=port, debug=False) 