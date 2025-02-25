import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# Load environment variables
load_dotenv()

# Secure API credentials
BOT_TOKEN = os.getenv("BOT_TOKEN")
MODIJIURL_API = os.getenv("MODIJIURL_API")
API_KEY = os.getenv("API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# File Storage Mapping (TeraBox File Links)
file_links = {
    "SAMPLE": "https://1024terabox.com/s/1fBRj1bH7pq7tMf9yhwd3Ow",
    "SAMPLE1": "https://1024terabox.com/s/1_cDqyr7PzTEys5JMLg9F_A",
}

# Function to shorten link using ModijiURL
async def shorten_link(long_url):
    response = requests.post(f"{MODIJIURL_API}/shorten", data={"api_key": API_KEY, "url": long_url})
    return response.json().get("shortenedUrl", long_url)

# Function to check if user is subscribed
async def is_subscribed(user_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember?chat_id={CHANNEL_ID}&user_id={user_id}"
    response = requests.get(url).json()
    status = response.get("result", {}).get("status", "left")
    return status in ["member", "administrator", "creator"]

# Function to handle messages (users type file name)
async def handle_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    text = update.message.text.strip().upper()

    if not await is_subscribed(user_id):
        await update.message.reply_text(f"🚨 Please subscribe to {CHANNEL_ID} first to use this bot!")
        return

    if text in file_links:
        original_link = file_links[text]
        short_link = await shorten_link(original_link)
        await update.message.reply_text(f"✅ Here is your file: [Click to Download]({short_link})", parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ File not found! Please check the filename.")

# Main function to run the bot
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
