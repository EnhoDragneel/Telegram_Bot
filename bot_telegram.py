import csv
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TOKEN = "Seu Token" #Coloque aqui o token do seu bot
CSV_FILE = "mensagens_telegram.csv"


if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["chat_id", "usuario_id", "usuario", "primeiro_nome", "mensagem", "data"])

async def start(update: Update, context: CallbackContext) -> None:
    """Responde quando o usuário envia /start"""
    await update.message.reply_text(f"Olá, {update.message.from_user.first_name}! Eu sou o Enho, um bot de teste.")

async def save_message(update: Update, context: CallbackContext) -> None:
    """Salva as mensagens dos usuários em um arquivo CSV"""
    user = update.message.from_user
    chat_id = update.message.chat_id  
    message_text = update.message.text
    message_date = update.message.date.strftime("%Y-%m-%d %H:%M:%S")

    print(f"Mensagem recebida de {chat_id}: {message_text}") 

    # Salvar no CSV
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([chat_id, user.id, user.username, user.first_name, message_text, message_date])

    await update.message.reply_text("Mensagem registrada!")

def main():
    """Configura o bot e começa a escutar mensagens"""
    app = Application.builder().token(TOKEN).build()

    
    app.add_handler(CommandHandler("start", start))

    # Captura todas as mensagens e salva no CSV
    app.add_handler(MessageHandler(filters.ALL, save_message))

    # Inicia o bot
    app.run_polling()

if __name__ == "__main__":
    main()
