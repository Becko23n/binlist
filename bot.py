import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8198164270:AAGpRymPmXUxPpeRbUYZC5maVSfJJmcLk-Q"
RAPIDAPI_KEY = "a08b0e3a2cmshec1e7d909ca702ep15a71bjsnb53e7970f357"
STATIC_IP = "2.56.188.79"  # IP requerida por la API

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 ¡Hola! Envíame un número BIN (6 dígitos) y te diré lo que sé 🧠")

def consultar_bin(bin_code):
    url = f"https://bin-ip-checker.p.rapidapi.com/?bin={bin_code}&ip={STATIC_IP}"
    headers = {
        "Content-Type": "application/json",
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "bin-ip-checker.p.rapidapi.com"
    }
    payload = {
        "bin": bin_code,
        "ip": STATIC_IP
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error consultando API: {response.status_code}")
        return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()
    if not texto.isdigit() or len(texto) < 6:
        await update.message.reply_text("❗ Envíame un BIN válido (6 dígitos)")
        return

    bin_code = texto[:6]
    data = consultar_bin(bin_code)

    if data and any(data.get(k) for k in ["vendor", "type", "bank", "country"]):
        mensaje = (
            f"💳 Marca: {data.get('vendor', 'N/A')}
"
            f"🧾 Tipo: {data.get('type', 'N/A')}
"
            f"🏦 Banco: {data.get('bank', 'N/A')}
"
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