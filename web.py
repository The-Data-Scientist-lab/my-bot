from flask import Flask
import threading
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_bot():
    import bot
    bot.main()

if __name__ == '__main__':
    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    
    # Run the web server on the port provided by Render
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port) 