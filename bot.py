import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8198164270:AAGpRymPmXUxPpeRbUYZC5maVSfJJmcLk-Q"
API_NINJAS_KEY = "ZUf2OqY4iWaDZDmKVvx7xw==LCmu0KhGW95Cnjb4"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 ¡Hola! Envíame un número BIN (6 dígitos) para obtener detalles del emisor.")

def consultar_bin(bin_code):
    url = f"https://api.api-ninjas.com/v1/binlookup?bin={bin_code}"
    headers = {
        "X-Api-Key": API_NINJAS_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()
    if not texto.isdigit() or len(texto) < 6:
        await update.message.reply_text("❗ Envíame un BIN válido (mínimo 6 dígitos).")
        return

    bin_code = texto[:6]
    data = consultar_bin(bin_code)

    if data and "bank" in data:
        mensaje = (
    f"💳 Marca: {data.get('scheme', 'N/A')}\n"
    f"🏦 Banco: {data.get('bank', 'N/A')}\n"
    f"💳 Tipo: {data.get('type', 'N/A')}\n"
    f"🌍 País: {data.get('country', 'N/A')}"
)
    else:
        mensaje = "❌ No se encontró información para ese BIN."

    await update.message.reply_text(mensaje)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
