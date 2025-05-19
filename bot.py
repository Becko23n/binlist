import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8198164270:AAGpRymPmXUxPpeRbUYZC5maVSfJJmcLk-Q"
RAPIDAPI_KEY = "a08b0e3a2cmshec1e7d909ca702ep15a71bjsnb53e7970f357"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 ¡Hola! Envíame un número BIN (6 dígitos) y te diré lo que sé 🧠")

def consultar_bin(bin_code):
    url = "https://bin-ip-checker.p.rapidapi.com/"
    headers = {
        "Content-Type": "application/json",
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "bin-ip-checker.p.rapidapi.com"
    }
    payload = {
        "bin": bin_code,
        "ip": "2.56.188.79"
    }

    response = requests.post(url, json=payload, headers=headers)
    print("🔁 Código HTTP:", response.status_code)
    print("📦 JSON recibido:")
    try:
        print(response.json())
        return response.json()
    except Exception as e:
        print("❌ Error al parsear JSON:", e)
        return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()
    if not texto.isdigit() or len(texto) < 6:
        await update.message.reply_text("❗ Envíame un BIN válido (6 dígitos)")
        return

    bin_code = texto[:6]
    data = consultar_bin(bin_code)

    if data and data.get("BIN"):
        bin_data = data["BIN"]
        mensaje = (
            "💳 Marca: " + bin_data.get("scheme", "N/A") + "\n"
            "🧾 Tipo: " + bin_data.get("type", "N/A") + "\n"
            "🏦 Banco: " + bin_data.get("issuer", {}).get("name", "N/A") + "\n"
            "🌍 País: " + bin_data.get("country", {}).get("name", "N/A") + " " + bin_data.get("country", {}).get("flag", "")
        )
    else:
        mensaje = "❌ No se encontró información para ese BIN."

    await update.message.reply_text(mensaje.replace("\n", "\n"))

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()