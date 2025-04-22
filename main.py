import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Get API keys from environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# Function to get forex data
def get_forex_signal(pair):
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={pair[:3]}&to_currency={pair[3:]}&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url).json()

    try:
        rate = float(response["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
        signal = "BUY" if rate > 1 else "SELL"
        return f"📊 *{pair}*\n🌐 Rate: {rate}\n📈 Signal: *{signal}*"
    except:
        return "⚠️ Could not fetch data. Check the currency pair."


# Telegram command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to Forex Signal Bot! Send a currency pair like EURUSD to get signals.")

async def get_signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pair = update.message.text.strip().upper()
    if len(pair) == 6:
        msg = get_forex_signal(pair)
        await update.message.reply_markdown(msg)
    else:
        await update.message.reply_text("Please send a valid 6-letter currency pair like EURUSD.")

# Main function
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("signal", get_signal))
    app.add_handler(CommandHandler("signal", get_signal))
    app.run_polling()
