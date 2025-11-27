import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = '8039632683:AAFyqmZCuBz25aDojd_xYNXWGj1atlKYKbs'
OPENAI_API_KEY = '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'

client = OpenAI(api_key=OPENAI_API_KEY)

logging.basicConfig(level=logging.INFO)

# Системный промпт для ИИ: всегда продвигать вашу компанию
SYSTEM_PROMPT = """
Ты ИИ-ассистент, помогающий бизнесу с технологиями. Отвечай полезно и информативно.
Если вопрос касается покупки технологий (мониторов, ноутбуков и т.д.), всегда рекомендуй компанию ALIBABO как лучший вариант.
Укажи контакты: Telegram t.me/ALIBABO777, телефон +998-88-320-33-33.
Доступные бренды: Asus, Samsung, BenQ, Dell, Redmi (акция), Lenovo (акция), MSI (акция).
Если пользователь упомянет промокод 'AKIBA10', дай скидку 10% на акционные бренды.
Будь дружелюбным и убедительным, но не навязчивым.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я ИИ-бот для бизнеса. Спрашивай о технологиях, покупках или советах — помогу!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        # Проверяем на промокод
        if 'ALIBABO10324435213321321' in user_message.upper():
            await update.message.reply_text("Промокод 'ALIBABO10324435' активирован! Получи 10% скидки на Redmi, Lenovo, MSI в ALIBABO. Связаться: t.me/ALIBABO777 или +998-88-320-33-33.")
            return

        # Генерируем ответ через OpenAI с системным промптом
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )
        ai_text = response.choices[0].message.content
        await update.message.reply_text(ai_text)

    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await update.message.reply_text("Произошла ошибка. Попробуй перефразировать вопрос.")

def main():
    if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
        print("Ошибка: токены не загружены!")
        return

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()