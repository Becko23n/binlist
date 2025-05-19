
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8198164270:AAGpRymPmXUxPpeRbUYZC5maVSfJJmcLk-Q"
RAPIDAPI_KEY = "a08b0e3a2cmshec1e7d909ca702ep15a71bjsnb53e7970f357"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 ¡Hola! Envíame un número BIN (6 dígitos) y te diré lo que sé 🔍")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()
    if not texto.isdigit() or len(texto) < 6:
        await update.message.reply_text("❗ Envíame un BIN válido (6 dígitos)")
        return

    bin_code = texto[:6]

    url = "https://bin-ip-checker.p.rapidapi.com/" + bin_code
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "bin-ip-checker.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()

            if data.get("valid") and "vendor" in data:
                mensaje = (
                    f"💳 BIN: {bin_code}\n"
                    f"🏦 Banco: {data.get('bank_name', 'N/D')}\n"
                    f"🌐 Marca: {data.get('vendor', 'N/D')}\n"
                    f"💼 Tipo: {data.get('type', 'N/D')}\n"
                    f"🌍 País: {data.get('country_name', 'N/D')}\n"
                    f"🔒 Nivel: {data.get('level', 'N/D')}"
                )
            else:
                mensaje = "❌ No se encontró información para ese BIN."
        else:
            mensaje = f"⚠️ Error consultando la API (código {response.status_code})"

    except Exception as e:
        mensaje = f"🚨 Error de conexión con la API: {e}"

    await update.message.reply_text(mensaje)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
