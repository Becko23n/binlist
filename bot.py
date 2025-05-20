
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8198164270:AAGpRymPmXUxPpeRbUYZC5maVSfJJmcLk-Q"
RAPIDAPI_KEY = "a08b0e3a2cmshec1e7d909ca702ep15a71bjsnb53e7970f357"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 ¡Hola! Envíame un número BIN (6 dígitos) y te diré lo que sé 🧠")

def consultar_bin(bin_code):
    url = f"https://bin-ip-checker.p.rapidapi.com/bin/{bin_code}"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "bin-ip-checker.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error: {response.status_code} {response.text}")
        return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()
    if not texto.isdigit() or len(texto) < 6:
        await update.message.reply_text("❗ Envíame un BIN válido (6 dígitos)")
        return

    bin_code = texto[:6]
    data = consultar_bin(bin_code)
    print(data)  # <-- Aquí mostramos la respuesta en los logs

    if data and "BIN" in data:
        bin_data = data["BIN"]
        mensaje = (
    f"💳 Marca: {bin_data.get('scheme', 'N/A')}\n"
    f"🏦 Banco: {bin_data.get('issuer', {}).get('name', 'N/A')}\n"
    f"🌍 País: {bin_data.get('country', {}).get('name', 'N/A')} {bin_data.get('country', {}).get('flag', '')}\n"
    f"💰 Moneda: {bin_data.get('currency', 'N/A')}\n"
    f"🏷️ Tipo: {bin_data.get('type', 'N/A')} / {bin_data.get('brand', 'N/A')}"
)
    else:
        mensaje = "❌ No se encontró información para ese BIN."

    await update.message.reply_text(mensaje)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
