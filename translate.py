from telegram import (
    Update,
    ParseMode,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    CallbackQueryHandler,
)
from transformers import MarianTokenizer, MarianMTModel
import os
import sacremoses

models = {
    'German': 'Helsinki-NLP/opus-mt-en-de',
    'French': 'Helsinki-NLP/opus-mt-en-fr',
    'Spanish': 'Helsinki-NLP/opus-mt-en-es',
}
tokenizers = {lang: MarianTokenizer.from_pretrained(model_name) for lang, model_name in models.items()}
models = {lang: MarianMTModel.from_pretrained(model_name) for lang, model_name in models.items()}

def escape_markdown_v2(text):
    """
    Escape special characters for Telegram's MarkdownV2 format.
    """
    escape_chars = r'_[]()~`>#+-=|{}.!'
    return ''.join(f'\\{char}' if char in escape_chars else char for char in text)

def start(update: Update, context: CallbackContext) -> None:
    """
    Send a welcome message with options to choose a language for translation.
    """
    welcome_message = (
        "*Hello!*\n\n"
        "I can translate English text to different languages.\n"
        "Choose a language and send me the text!\n\n"
        "*Languages available:*\n"
    )
    
    keyboard = create_language_keyboard()
    
    update.message.reply_text(
        escape_markdown_v2(welcome_message),
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=keyboard
    )

def help_command(update: Update, context: CallbackContext) -> None:
    """
    Display help message with usage instructions.
    """
    help_message = (
        "*How to use this bot:*\n\n"
        "1. Select a language from the menu.\n"
        "2. Send me any English text.\n"
        "3. I'll translate it into the selected language!\n\n"
        "To change the translation language, use the menu to select a new one."
    )
    
    if update.message:
        update.message.reply_text(
            escape_markdown_v2(help_message),
            parse_mode=ParseMode.MARKDOWN_V2
        )
    elif update.callback_query:
        update.callback_query.message.reply_text(
            escape_markdown_v2(help_message),
            parse_mode=ParseMode.MARKDOWN_V2
        )

def perform_translation(text, language):
    """
    Translate text using the selected language model.
    """
    tokenizer = tokenizers[language]
    model = models[language]
    inputs = tokenizer(text, return_tensors="pt", padding=True)
    outputs = model.generate(**inputs)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def translate(update: Update, context: CallbackContext) -> None:
    """
    Handle text messages and translate them to the selected language.
    """
    # Get the language selection from user data
    language = context.user_data.get('language', 'German')
    
    text_to_translate = update.message.text
    translated_text = perform_translation(text_to_translate, language)
    
    response_message = f"{translated_text}"
    
    try:
        update.message.reply_text(
            escape_markdown_v2(response_message),
            parse_mode=ParseMode.MARKDOWN_V2
        )
    except Exception as e:
        print(f"Error sending message: {e}")
        # Fallback to plain text if Markdown fails
        update.message.reply_text(f"Translated Text:\n\n{translated_text}")

def button_handler(update: Update, context: CallbackContext) -> None:
    """
    Handle button clicks from inline keyboard.
    """
    query = update.callback_query
    query.answer()
    
    if query.data != 'help':
        context.user_data['language'] = query.data
    
    language_map = {
        'German': 'German',
        'French': 'French',
        'Spanish': 'Spanish',
        'help': 'Help'
    }
    selected_language = language_map.get(query.data, 'German')
    
    if query.data == 'help':
        help_message = (
            "*How to use this bot:*\n\n"
            "1. Select a language from the menu.\n"
            "2. Send me any English text.\n"
            "3. I'll translate it into the selected language!\n\n"
            "To change the translation language, use the menu to select a new one."
        )
        query.message.reply_text(
            escape_markdown_v2(help_message),
            parse_mode=ParseMode.MARKDOWN_V2
        )
    else:
        new_message_text = escape_markdown_v2(f"You have selected *{selected_language}*. Now send me the text to translate.")
        if query.message.text != new_message_text:
            query.edit_message_text(
                text=new_message_text,
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=create_language_keyboard()  # Persist the keyboard
            )

def create_language_keyboard():
    """
    Create an inline keyboard for language selection.
    """
    keyboard = [
        [
            InlineKeyboardButton("German", callback_data='German'),
            InlineKeyboardButton("French", callback_data='French'),
            InlineKeyboardButton("Spanish", callback_data='Spanish')
        ],
        [InlineKeyboardButton("Help", callback_data='help')],
    ]
    return InlineKeyboardMarkup(keyboard)

def error_handler(update, context):
    """
    Log errors caused by updates.
    """
    print(f"Update {update} caused error {context.error}")

def main() -> None:
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set.")
        return

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, translate))
    dp.add_handler(CallbackQueryHandler(button_handler))
    
    dp.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    print("Starting Telegram Translation Bot...")
    main()
