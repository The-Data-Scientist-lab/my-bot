from flask import Flask
import threading
import os
import logging
import asyncio
import nest_asyncio
from waitress import serve
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enable nested event loops
nest_asyncio.apply()

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_bot():
    try:
        # Create new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        import bot
        # Run the bot in the event loop
        loop.run_until_complete(bot.start_bot())
    except Exception as e:
        logger.error(f"Bot error: {str(e)}")
        # Wait for 5 seconds before retrying
        time.sleep(5)
        # Restart the bot
        run_bot()
    finally:
        loop.close()

if __name__ == '__main__':
    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True  # Make thread daemon so it exits when main thread exits
    bot_thread.start()
    
    # Get port from environment variable
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"Starting web server on port {port}")
    
    # Use waitress instead of Flask's development server
    serve(app, host='0.0.0.0', port=port, threads=4) 