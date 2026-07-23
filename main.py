import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# 1. Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Твой токен бота
TOKEN = "8685276551:AAHaWurnWMqaxPMx8_GhyqG9DQ4iQdtO06E"

# Команда /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 Добро пожаловать в игру!\n\n"
        "Введи команду **/gamerps**, чтобы сыграть в «Камень, ножницы, бумага».",
        parse_mode='Markdown'
    )


# Команда /gamerps — выводит игровую панель с тремя кнопками
async def gamerps_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🪨 Камень", callback_data="rps_rock"),
            InlineKeyboardButton("✂️ Ножницы", callback_data="rps_scissors"),
            InlineKeyboardButton("📄 Бумага", callback_data="rps_paper")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🎮 **Камень, ножницы, бумага**\n\nСделай свой выбор, нажав на кнопку ниже:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


# Обработчик выбора игрока
async def rps_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    choice_map = {
        "rps_rock": "🪨 Камень",
        "rps_scissors": "✂️ Ножницы",
        "rps_paper": "📄 Бумага"
    }

    user_choice = choice_map.get(query.data)
    
    # Бот делает свой случайный выбор
    bot_choice_key = random.choice(["rps_rock", "rps_scissors", "rps_paper"])
    bot_choice = choice_map[bot_choice_key]

    # Определяем победителя
    if user_choice == bot_choice:
        result = "🤝 Ничья!"
    elif (
        (user_choice == "🪨 Камень" and bot_choice == "✂️ Ножницы") or
        (user_choice == "✂️ Ножницы" and bot_choice == "📄 Бумага") or
        (user_choice == "📄 Бумага" and bot_choice == "🪨 Камень")
    ):
        result = f"🎉 Победил @{user.username or user.first_name}!"
    else:
        result = "🤖 Победил бот!"

    # Обновляем сообщение с результатами игры
    await query.edit_message_text(
        f"🎮 **Результаты игры**\n\n"
        f"Ты выбрал: **{user_choice}**\n"
        f"Бот выбрал: **{bot_choice}**\n\n"
        f"{result}",
        parse_mode='Markdown'
    )


# Главная функция запуска
if __name__ == '__main__':
    print("Бот Камень-Ножницы-Бумага запускается...")
    
    application = ApplicationBuilder().token(TOKEN).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('gamerps', gamerps_command))
    
    # Обработчик нажатий на кнопки с префиксом rps_
    application.add_handler(CallbackQueryHandler(rps_button_handler, pattern="^rps_"))

    print("Бот работает!")
    application.run_polling()
      
