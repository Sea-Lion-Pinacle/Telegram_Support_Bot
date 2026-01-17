import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Enable logging
logging.basicConfig(level=logging.INFO)
TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace after BotFather

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📋 Order Status", callback_data='status')],
        [InlineKeyboardButton("💰 Pricing", callback_data='pricing')],
        [InlineKeyboardButton("📞 Contact", callback_data='contact')],
        [InlineKeyboardButton("❓ FAQs", callback_data='faq')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Hello! How can I help you today?",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'status':
        await query.edit_message_text("📦 Your order #12345 ships tomorrow. Track: https://track.order.com/12345")
    elif query.data == 'pricing':
        await query.edit_message_text("💰 Plans:\n• Basic: $29/mo\n• Pro: $79/mo\n• Enterprise: $199/mo")
    elif query.data == 'contact':
        await query.edit_message_text("📞 Email: support@business.com\n📱 WhatsApp: +1234567890")
    elif query.data == 'faq':
        await query.edit_message_text("❓ Common questions:\n• Delivery: 3-5 days\n• Returns: 30 days\n• Support: 24/7")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    
    if any(word in text for word in ['order', 'tracking', 'ship']):
        await update.message.reply_text("📦 Check order status: /status")
    elif any(word in text for word in ['price', 'cost', 'plan']):
        await update.message.reply_text("💰 View pricing: /pricing")
    elif 'refund' in text or 'return' in text:
        await update.message.reply_text("🔄 30-day money back guarantee. Email support@business.com")
    else:
        await update.message.reply_text("Type /start for menu!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📋 Menu", callback_data='status')]]))

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot running...")
    app.run_polling()

if __name__ == '__main__':
    main()
