import os
import logging
from telethon import TelegramClient, events, Button, types
from dotenv import load_dotenv
import asyncio
from datetime import datetime, timedelta
import random
import aiohttp
import json

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Webhook URL from Google Apps Script
WEBHOOK_URL = os.getenv("GOOGLE_SHEETS_WEBHOOK_URL")

# Store user journey data
user_journey = {}

# Function to format user journey details
def format_user_journey(user_id, action, details=None):
    if user_id not in user_journey:
        user_journey[user_id] = {
            "actions": [],
            "details": {}
        }
    
    # Add new action to history
    user_journey[user_id]["actions"].append(action)
    
    # Update details
    if details:
        user_journey[user_id]["details"].update(details)
    
    return {
        "action": " -> ".join(user_journey[user_id]["actions"]),
        "details": user_journey[user_id]["details"]
    }

# Function to log user data
async def log_user_data(user_id, username, first_name, last_name, action, details=None):
    try:
        async with aiohttp.ClientSession() as session:
            # Convert all values to strings and handle None values
            data = {
                "user_id": str(user_id),
                "username": str(username) if username else "",
                "first_name": str(first_name) if first_name else "",
                "last_name": str(last_name) if last_name else "",
                "action": action,
                "details": details if details else {}
            }
            
            async with session.post(WEBHOOK_URL, json=data) as response:
                if response.status != 200:
                    response_text = await response.text()
                    logger.error(f"Error sending data to webhook: {response.status} - {response_text}")
    except Exception as e:
        logger.error(f"Error logging user data: {str(e)}")

# Function to format price details
def format_price_details(model, duration, price):
    return {
        "Model": model["name"],
        "Duration": f"{duration} minutes",
        "Price": f"₹{price}"
    }

# Initialize the client
client = TelegramClient('bot_session', os.getenv("TELEGRAM_API_ID"), os.getenv("TELEGRAM_API_HASH")).start(bot_token=os.getenv("TELEGRAM_BOT_TOKEN"))

# Model information with enhanced details
MODELS = {
    "model1": {
        "name": "💋 Lucky Rajor",
        "description": """🔥 Nude Content Collection

💫 Original Price: ₹16000 for Recorded Nude Video

⭐️ Our Price: ₹349 for 30 minutes Nude Video

🎯 Instant Access

✨ Quick Delivery

━━━━━━━━━━━━━━━━━━━━━━━━
📊 Model Statistics
━━━━━━━━━━━━━━━━━━━━━━━━

⭐️ Rating: 4.9/5.0
👥 Orders in last 24 hours: 346
💯 Customer Satisfaction: 98%
🎯 Success Rate: 100%""",
        "price_30min": 349,
        "price_1hr": 579,
        "stats": "👁️ Premium Content | 💖 Instant Delivery",
        "specialties": "HD Videos | 4K Quality | Instant Access",
        "image": "images/luckyrajor.jpg",
        "hot_description": """💋 Lucky Rajor Nude Video Collection

🔥 Original Price: ₹16000 for 30 minutes Nude Recorded Video

💫 Our Price: ₹349 for 30 minutes Nude Video

✨ Instant Access After Payment

🎯 Quick Delivery

⭐️ HD Quality Content

💖 100% Satisfaction

━━━━━━━━━━━━━━━━━━━━━━━━
📊 Model Statistics
━━━━━━━━━━━━━━━━━━━━━━━━

⭐️ Rating: 4.9/5.0
👥 Orders in last 24 hours: 346
💯 Customer Satisfaction: 98%
🎯 Success Rate: 100%"""
    },
    "model2": {
        "name": "💝 Miss Pinky (Sana)",
        "description": """✨ Miss Pinky (Sana) Nude Video Collection

💫 Original Price: ₹17000 for 30 minutes Nude Recorded Video

💪 Our Price: ₹399 for 30 minutes Nude Video

🏆 Instant Access

🎯 Quick Delivery

━━━━━━━━━━━━━━━━━━━━━━━━
📊 Model Statistics
━━━━━━━━━━━━━━━━━━━━━━━━

⭐️ Rating: 4.8/5.0
👥 Orders in last 24 hours: 287
💯 Customer Satisfaction: 97%
🎯 Success Rate: 100%""",
        "price_30min": 399,
        "price_1hr": 639,
        "stats": "👁️ Premium Content | 💖 Instant Delivery",
        "specialties": "HD Videos | 4K Quality | Instant Access",
        "image": "images/Miss Pinky.jpg",
        "hot_description": """💋 Miss Pinky (Sana) Nude Video Collection

🔥 Original Price: ₹17000 for 30 minutes Nude Recorded Video

💫 Our Price: ₹399 for 30 minutes Nude Video

✨ Instant Access After Payment

🎯 Quick Delivery

⭐️ HD Quality Content

💖 100% Satisfaction

━━━━━━━━━━━━━━━━━━━━━━━━
📊 Model Statistics
━━━━━━━━━━━━━━━━━━━━━━━━

⭐️ Rating: 4.8/5.0
👥 Orders in last 24 hours: 287
💯 Customer Satisfaction: 97%
🎯 Success Rate: 100%"""
    },
    "model3": {
        "name": "✨ Shanaya Katiyan",
        "description": """💫 Shanaya Katiyan Nude Video Collection

⭐️ Original Price: ₹19500 for 30 minutes Nude Recorded Video

🎨 Our Price: ₹449 for 30 minutes Nude Video

🏆 Instant Access

✨ Quick Delivery

━━━━━━━━━━━━━━━━━━━━━━━━
📊 Model Statistics
━━━━━━━━━━━━━━━━━━━━━━━━

⭐️ Rating: 4.7/5.0
👥 Orders in last 24 hours: 529
💯 Customer Satisfaction: 96%
🎯 Success Rate: 100%""",
        "price_30min": 449,
        "price_1hr": 979,
        "stats": "👁️ Premium Content | 💖 Instant Delivery",
        "specialties": "HD Videos | 4K Quality | Instant Access",
        "image": "images/shanaya_katiyan.jpg",
        "hot_description": """💋 Shanaya Katiyan Nude Video Collection

🔥 Original Price: ₹19500 for 30 minutes Nude Recorded Video

💫 Our Price: ₹449 for 30 minutes Nude Video

✨ Instant Access After Payment

🎯 Quick Delivery

⭐️ HD Quality Content

💖 100% Satisfaction

━━━━━━━━━━━━━━━━━━━━━━━━
📊 Model Statistics
━━━━━━━━━━━━━━━━━━━━━━━━

⭐️ Rating: 4.7/5.0
👥 Orders in last 24 hours: 529
💯 Customer Satisfaction: 96%
🎯 Success Rate: 100%"""
    }
}

# Trust indicators
TRUST_INDICATORS = [
    "🔒 Secure Payment Processing",
    "✅ Instant Access After Payment",
    "🛡️ HD Quality Content",
    "📞 Quick Response"
]

# Payment methods
PAYMENT_METHODS = [
    "💳 UPI",
    "🏦 Bank Transfer",
    "📱 PhonePe",
    "💰 Google Pay",
    "💸 Paytm"
]

# Store user selections
user_selections = {}

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    """Send a welcome message when the command /start is issued."""
    user = await event.get_sender()
    current_time = datetime.now().strftime("%H:%M")
    
    # Initialize user's selection history
    user_selections[user.id] = []
    
    # Log user start
    await log_user_data(
        user.id,
        user.username,
        user.first_name,
        user.last_name,
        "Bot Started"
    )
    
    welcome_message = f"""
👋 Hey {user.first_name}!

🎀 Welcome to Premium Content Hub 🎀
🕒 {current_time} | ⭐️ Premium Content Access

💝 Get Access to Exclusive Content
✨ Instant Delivery
🔥 HD Quality Videos
🎯 4K Resolution Content

━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ IMPORTANT DISCLAIMER ⚠️
━━━━━━━━━━━━━━━━━━━━━━━━

🔞 Age Restriction: 18+ Only
📜 Content: For Personal Use Only
💫 All Content: Professional Quality
🎬 Quick Access: After Payment
✨ Instant Delivery: Guaranteed

━━━━━━━━━━━━━━━━━━━━━━━━
📢 IMPORTANT NOTICE 📢
━━━━━━━━━━━━━━━━━━━━━━━━

💫 I am not the original seller of these videos
💰 Original price is very high 
✨ I am reselling at affordable prices
🎯 Same premium content, lower price


━━━━━━━━━━━━━━━━━━━━━━━━
🚨 URGENT WARNING 🚨
━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ This bot was created on 23rd April 2025
⚠️ Can be banned anytime by Telegram officials
⚠️ Please complete your order as soon as possible
⚠️ Get your content before it's too late

━━━━━━━━━━━━━━━━━━━━━━━━

💋 Choose Your Favorite Collection Below 👇
"""
    buttons = [
        [Button.inline(MODELS["model1"]["name"], b"model1"),
         Button.inline(MODELS["model2"]["name"], b"model2")],
        [Button.inline(MODELS["model3"]["name"], b"model3")]
    ]
    await event.respond(welcome_message, buttons=buttons, parse_mode='markdown')

@client.on(events.CallbackQuery())
async def callback_handler(event):
    """Handle button presses."""
    data = event.data.decode('utf-8')
    user = await event.get_sender()
    
    if data.startswith("model"):
        # If user already has a model selected, don't show another one
        if user_selections[user.id] and any(selection.startswith("Selected:") for selection in user_selections[user.id]):
            # Just show their current selection
            current_model = next((s for s in user_selections[user.id] if s.startswith("Selected:")), None)
            if current_model:
                model_name = current_model.replace("Selected: ", "")
                model_id = next((k for k, v in MODELS.items() if v["name"] == model_name), None)
                if model_id:
                    model = MODELS[model_id]
                    buttons = [
                        [Button.inline(f"30 Minutes - ₹{model['price_30min']}", f"plan_{model_id}_30".encode()),
                         Button.inline(f"1 Hour - ₹{model['price_1hr']}", f"plan_{model_id}_60".encode())],
                        [Button.inline("🔙 Back to Collections", b"back")]
                    ]
                    await event.respond(
                        f"{current_model}\n\n{model['hot_description']}\n\nChoose your plan:",
                        buttons=buttons,
                        parse_mode='markdown'
                    )
            return
        
        # If no model selected yet, proceed with new selection
        model_id = data
        model = MODELS[model_id]
        
        # Log model selection - creates new row
        await log_user_data(
            user.id,
            user.username,
            user.first_name,
            user.last_name,
            "Model Selected",
            {
                "Model": model["name"],
                "Selection_Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )
        
        # Store current selection
        user_selections[user.id] = [f"Selected: {model['name']}"]
        
        buttons = [
            [Button.inline(f"30 Minutes - ₹{model['price_30min']}", f"plan_{model_id}_30".encode()),
             Button.inline(f"1 Hour - ₹{model['price_1hr']}", f"plan_{model_id}_60".encode())],
            [Button.inline("🔙 Back to Collections", b"back")]
        ]
        
        try:
            # Get absolute path of the image
            image_path = os.path.abspath(model["image"])
            
            if os.path.exists(image_path):
                # Create a single message with image and description
                model_info = f"""
{user_selections[user.id][0]}

{model['hot_description']}

Choose your plan:
"""
                # Send image with caption
                await event.respond(
                    model_info,
                    file=image_path,
                    buttons=buttons,
                    parse_mode='markdown'
                )
            else:
                # If image not found, send text description only
                await event.respond(
                    f"{user_selections[user.id][0]}\n\n{model['hot_description']}\n\nChoose your plan:",
                    buttons=buttons,
                    parse_mode='markdown'
                )
        except Exception as e:
            # If any error occurs, send text description only
            await event.respond(
                f"{user_selections[user.id][0]}\n\n{model['hot_description']}\n\nChoose your plan:",
                buttons=buttons,
                parse_mode='markdown'
            )
    elif data == "back":
        # Clear all selections when going back
        user_selections[user.id] = []
        await start(event)
    elif data.startswith("plan_"):
        _, model_id, duration = data.split("_")
        model = MODELS[model_id]
        price = model[f"price_{duration}min"] if duration == "30" else model["price_1hr"]
        
        # Log package selection - creates new row
        await log_user_data(
            user.id,
            user.username,
            user.first_name,
            user.last_name,
            "Package Selected",
            {
                "Model": model["name"],
                "Duration": f"{duration} minutes",
                "Price": f"₹{price}",
                "Selection_Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )
        
        # Different package descriptions based on model and duration
        if model_id == "model1":  # Lucky Rajor
            if duration == "30":
                package_desc = "✅ 30 minutes Lucky Rajor Full Nude video"
                original_price = "16000"
            else:
                package_desc = "✅ 1 hour recorded Full Nude video\n✅ 30 Nude Photos"
                original_price = "18500"
        elif model_id == "model2":  # Miss Pinky
            if duration == "30":
                package_desc = "✅ 30 minutes Miss Pinky Full Nude video"
                original_price = "16000"
            else:
                package_desc = "✅ 1 hour recorded Full Nude video\n✅ 70 Nude Photos"
                original_price = "18500"
        else:  # Shanaya Katiyan
            if duration == "30":
                package_desc = "✅ 30 minutes Shanaya Katiyan Full Nude video"
                original_price = "16000"
            else:
                package_desc = "✅ 1 hour recorded Full Nude video\n✅ 100 Nude Photos"
                original_price = "18500"
        
        # Add selection to history
        user_selections[user.id].append(f"{model['name']} - {duration} minutes video - ₹{price}")
        
        # Show selection history
        history = "\n".join(user_selections[user.id])
        
        confirmation_message = f"""
{history}

{package_desc}
💰 Price: ₹{price} (Original: ₹{original_price})

━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ IMPORTANT DISCLAIMER ⚠️
━━━━━━━━━━━━━━━━━━━━━━━━

🔞 These videos are for personal use only
💫 We are not the original owner of these videos
💰 We are selling these videos at very low prices
✨ Same premium content, much cheaper price
🎯 100% satisfaction guaranteed

Please confirm your order to proceed to payment.
"""
        buttons = [
            [Button.inline("✅ Confirm Order", f"confirm_{model_id}_{duration}".encode())],
            [Button.inline("🔙 Back to Collections", b"back")]
        ]
        await event.respond(confirmation_message, buttons=buttons, parse_mode='markdown')
    
    elif data.startswith("confirm_"):
        # Clear previous selections except model and plan
        if len(user_selections[user.id]) > 2:
            user_selections[user.id] = user_selections[user.id][:2]  # Keep only model and plan selections
            
        _, model_id, duration = data.split("_")
        model = MODELS[model_id]
        price = model[f"price_{duration}min"] if duration == "30" else model["price_1hr"]
        
        # Log order confirmation
        await log_user_data(
            user.id,
            user.username,
            user.first_name,
            user.last_name,
            "Order Confirmed",
            {
                "Model": model["name"],
                "Duration": f"{duration} minutes",
                "Price": f"₹{price}"
            }
        )
        
        # Different package descriptions based on model and duration
        if model_id == "model1":  # Lucky Rajor
            if duration == "30":
                package_desc = "✅ 30 minutes Lucky Rajor Full Nude video"
            else:
                package_desc = "✅ 1 hour recorded Full Nude video\n✅ 30 exclusive photos"
        elif model_id == "model2":  # Miss Pinky
            if duration == "30":
                package_desc = "✅ 30 minutes Miss Pinky Full Nude video"
            else:
                package_desc = "✅ 1 hour recorded Full Nude video\n✅ 70 exclusive photos"
        else:  # Shanaya Katiyan
            if duration == "30":
                package_desc = "✅ 30 minutes Shanaya Katiyan Full Nude video"
            else:
                package_desc = "✅ 1 hour recorded Full Nude video\n✅ 100 exclusive photos"
        
        payment_message = f"""
{package_desc}
💰 Amount to Pay: ₹{price}

💝 Scan the QR code below to complete payment
✨ Get instant access to Google Drive link
🎯 Download your content easily

━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ IMPORTANT NOTE ⚠️
━━━━━━━━━━━━━━━━━━━━━━━━

💫 We are not the original owner of these videos
💰 We are selling these videos at very low prices
✨ Same premium content, much cheaper price
🎯 100% satisfaction guaranteed

Click 'I have paid' after completing the payment.
"""
        buttons = [
            [Button.inline("💳 I have paid", b"payment_done")],
            [Button.inline("🔙 Back to Collections", b"back")]
        ]
        
        try:
            # Get absolute path of the QR code
            qr_path = os.path.abspath("images/QR.jpg")
            
            if os.path.exists(qr_path):
                # Send QR code with payment message
                await event.respond(
                    payment_message,
                    file=qr_path,
                    buttons=buttons,
                    parse_mode='markdown'
                )
            else:
                await event.respond("⚠️ QR code not found. Please contact support.")
        except Exception as e:
            await event.respond(f"⚠️ Error displaying QR code: {str(e)}")
    elif data == "payment_done":
        # Log payment initiation
        await log_user_data(
            user.id,
            user.username,
            user.first_name,
            user.last_name,
            "Payment Initiated"
        )
        
        # Add selection to history
        user_selections[user.id].append("Payment Initiated")
        
        verification_message = f"""
Payment Verification Process
━━━━━━━━━━━━━━━━━━━━━━━━

📸 Please upload your payment screenshot

🔍 Verification Steps:
1️⃣ Upload clear payment screenshot
2️⃣ Wait for few second verification
3️⃣ Get instant access to content
4️⃣ Receive Google Drive link

⚠️ Note: 
- Make sure screenshot is clear
- Include transaction ID if possible
- Quick response guaranteed

💫 After verification, you'll get:
✨ Instant access to Google Drive
🎯 Easy download process
💖 Enjoy your content
"""
        await event.respond(verification_message, parse_mode='markdown')

@client.on(events.NewMessage(func=lambda e: e.photo))
async def handle_photo(event):
    """Handle the payment screenshot."""
    user = await event.get_sender()
    
    # Log screenshot received
    await log_user_data(
        user.id,
        user.username,
        user.first_name,
        user.last_name,
        "Screenshot Sent"
    )
    
    # Send verification started message
    verification_started = f"""
Payment Verification Started 💫
━━━━━━━━━━━━━━━━━━━━━━━━

✅ Payment screenshot received successfully!
⏳ Starting verification process...

🔍 Status: Processing
🕒 Time: {datetime.now().strftime("%H:%M:%S")}

✨ Please wait while we verify your payment
🎯 We'll notify you in just a few seconds
💖 Thank you for your patience
"""
    await event.respond(verification_started, parse_mode='markdown')
    
    # Wait for 16 seconds
    await asyncio.sleep(16)
    
    # Log verification failed
    await log_user_data(
        user.id,
        user.username,
        user.first_name,
        user.last_name,
        "Payment Failed"
    )
    
    # Send failed verification message with feedback request
    failed_message = f"""
❌ Verification Failed
━━━━━━━━━━━━━━━━━━━━━━━━

Please check:
✅ Your payment has been debited
✅ You have entered correct amount
✅ Screenshot is clear and has transaction ID/UTR number

What to do next:
1️⃣ Check your payment status
2️⃣ Take a clear screenshot
3️⃣ Try again

━━━━━━━━━━━━━━━━━━━━━━━━
💫 IMPORTANT NOTE 💫
━━━━━━━━━━━━━━━━━━━━━━━━

If everything is fine and money was debited from your account, don't worry! We will check your payment and let you know within 3 hours.

Please share your feedback about this experience:
"""
    await event.respond(failed_message, parse_mode='markdown')
    
    # Wait for user feedback using event handler
    feedback_event = await client.wait_for(events.NewMessage(from_users=user.id))
    feedback = feedback_event.message.text
    
    # Log user feedback
    await log_user_data(
        user.id,
        user.username,
        user.first_name,
        user.last_name,
        "User Feedback After Failed Verification",
        {
            "Feedback": feedback
        }
    )
    
    # Wait for 3 hours (10800 seconds)
    await asyncio.sleep(10800)
    
    # Send follow-up message after 3 hours
    follow_up_message = f"""
🔍 Payment Verification Update
━━━━━━━━━━━━━━━━━━━━━━━━

Dear {user.first_name},

We have reviewed your payment and found that it was not successful. Here's what you can do:

1️⃣ Check your bank statement
2️⃣ Verify the transaction ID
3️⃣ Take a new screenshot
4️⃣ Try the payment again

━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ IMPORTANT ⚠️
━━━━━━━━━━━━━━━━━━━━━━━━

If your payment was successful but not verified:
1. Send us your transaction ID
2. Include your bank statement
3. We'll manually verify within 24 hours

Please share your feedback about this experience:
"""
    await event.respond(follow_up_message, parse_mode='markdown')
    
    # Wait for user feedback using event handler
    feedback_event = await client.wait_for(events.NewMessage(from_users=user.id))
    feedback = feedback_event.message.text
    
    # Log user feedback
    await log_user_data(
        user.id,
        user.username,
        user.first_name,
        user.last_name,
        "User Feedback After 3 Hours",
        {
            "Feedback": feedback
        }
    )
    
    # Wait for 21 more hours (total 24 hours)
    await asyncio.sleep(75600)
    
    # Send refund message after 24 hours
    refund_message = f"""
💫 Payment Update
━━━━━━━━━━━━━━━━━━━━━━━━

Dear {user.first_name},

We're sorry we couldn't proceed with your Order. Your money will be refunded to your account within the next 3 working days.

Don't worry, you will receive your refund automatically. If you have any questions, feel free to leave a message below.

Thank you for your patience and understanding.
"""
    await event.respond(refund_message, parse_mode='markdown')
    
    # Wait for user message using event handler
    message_event = await client.wait_for(events.NewMessage(from_users=user.id))
    user_message = message_event.message.text
    
    # Log user message
    await log_user_data(
        user.id,
        user.username,
        user.first_name,
        user.last_name,
        "User Message After Refund Notification",
        {
            "Message": user_message
        }
    )

async def main():
    """Start the bot."""
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main()) 