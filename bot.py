
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

with open("bins.json", encoding="utf-8") as f:
    bins = json.load(f)

BOT_TOKEN = "8198164270:AAGpRymPmXUxPpeRbUYZC5maVSfJJmcLk-Q"

def buscar_bin(bin_code):
    for entry in bins:
        if entry["bin"] == bin_code:
            return entry
    return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 ¡Hola! Envíame un número BIN (6 dígitos) y te diré lo que sé 💳")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()
    if not texto.isdigit() or len(texto) < 6:
        await update.message.reply_text("❗ Envíame un BIN válido (6 dígitos)")
        return

    bin_code = texto[:6]
    resultado = buscar_bin(bin_code)

    if resultado:
        mensaje = (
            f"💳 Marca: {resultado['scheme']}
"
            f"🏷️ Tipo: {resultado['type']}
"
            f"⭐ Nivel: {resultado['brand']}
"
            f"🏦 Banco: {resultado['bank']}
"
            f"🌍 País: {resultado['country']}"
        )
    else:
        mensaje = "❌ No se encontró información para ese BIN."

    await update.message.reply_text(mensaje)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot activo")
    app.run_polling()
