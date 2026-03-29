# telegram_bot.py

import requests
import os
import matplotlib.pyplot as plt
import re

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    filters,
    ContextTypes,
)

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")
# ================= CONFIG =================

# BOT_TOKEN = "8285920911:AAG2IADPYm5QavsnkDjEJSdr1aOK11TnIk8"

# API_URL = "http://127.0.0.1:8000/predict/"


# ================= START COMMAND =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 Welcome to Energy Forecast Bot\n\n"
        "Upload your CSV file 📂\n"
        "I will generate prediction + PDF report for you."
    )


# ================= FORECAST CHART =================

def create_forecast_chart(forecast):

    x = [i["datetime"][-8:] for i in forecast]
    y = [i["predicted_energy_kWh"] for i in forecast]

    plt.figure(figsize=(10,4))

    plt.plot(x, y, marker="o")

    plt.title("24-Hour Energy Forecast")

    plt.xlabel("Time")

    plt.ylabel("Energy (kWh)")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig("forecast_chart.png")

    plt.close()


# ================= CLEAN AI TEXT =================

def clean_ai_text(text):

    text = re.sub(r"<.*?>", "", text)

    text = text.replace("■", "Rs ")

    text = text.replace("₹", "Rs ")

    text = text.replace("≈", "approx ")

    text = re.sub(r"\*\*", "", text)

    text = re.sub(r"\|", "", text)

    text = re.sub(r"---", "", text)

    return text


# ================= SPLIT INTO BULLETS =================

def split_points(text):

    sentences = re.split(r"\.\s+", text)

    bullets = []

    for s in sentences:

        if len(s.strip()) > 30:

            bullets.append("• " + s.strip())

    return bullets[:12]


# ================= PDF GENERATOR =================

def generate_pdf(data, filename):

    create_forecast_chart(data["next_24_hours_forecast"])

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=30
    )

    elements = []


    # TITLE

    elements.append(
        Paragraph("Energy Forecast Analytics Report",
                  styles["Heading1"])
    )

    elements.append(Spacer(1, 20))


    # SUMMARY SECTION

    elements.append(
        Paragraph("Summary Overview", styles["Heading2"])
    )

    summary = [

        f"Total rows analysed: {data['total_rows']}",

        f"Detected anomalies: {data['total_anomalies']}",

        f"Estimated current cost: Rs {data['estimated_total_cost']}",

        f"Predicted next month usage: {data['estimated_next_month_usage_kWh']} kWh",

        f"Predicted next month cost: Rs {data['estimated_next_month_cost']}"
    ]

    for item in summary:

        elements.append(
            Paragraph("• " + item, styles["Normal"])
        )

    elements.append(Spacer(1, 25))


    # FORECAST GRAPH

    elements.append(
        Paragraph("24-Hour Energy Forecast", styles["Heading2"])
    )

    if os.path.exists("forecast_chart.png"):

        img = Image("forecast_chart.png")

        img.drawHeight = 240

        img.drawWidth = 450

        elements.append(img)

    elements.append(Spacer(1, 25))


    # AI INSIGHTS

    elements.append(
        Paragraph("AI Generated Insights", styles["Heading2"])
    )

    cleaned_text = clean_ai_text(data["generated_report"])

    bullets = split_points(cleaned_text)

    for bullet in bullets:

        elements.append(
            Paragraph(bullet, styles["Normal"])
        )

    elements.append(Spacer(1, 20))


    # RECOMMENDATIONS

    elements.append(
        Paragraph("Energy Saving Recommendations", styles["Heading2"])
    )

    tips = [

        "Shift heavy appliance usage to night hours",

        "Maintain AC temperature between 24°C and 26°C",

        "Upgrade lighting systems to LED",

        "Install timers for heaters and pumps",

        "Monitor anomaly timestamps regularly"

    ]

    for tip in tips:

        elements.append(
            Paragraph("• " + tip, styles["Normal"])
        )

    doc.build(elements)


# ================= CSV HANDLER =================

async def handle_csv(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text("✅ CSV received")

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    file = await update.message.document.get_file()

    csv_path = "temp.csv"

    await file.download_to_drive(csv_path)

    await update.message.reply_text(
        "📊 Running energy forecast model..."
    )

    try:

        with open(csv_path, "rb") as f:

            response = requests.post(
                API_URL,
                files={"file": f}
            )

        result = response.json()

    except Exception:

        await update.message.reply_text(
            "❌ Error processing file."
        )

        return

    await update.message.reply_text(
        "🧠 Generating AI insights report..."
    )

    pdf_path = "energy_report.pdf"

    generate_pdf(result, pdf_path)

    await update.message.reply_text(
        "📄 Report ready! Sending now..."
    )

    await update.message.reply_document(
        document=open(pdf_path, "rb"),
        filename="Energy_Forecast_Report.pdf"
    )


    # CLEANUP

    if os.path.exists(csv_path):

        os.remove(csv_path)

    if os.path.exists(pdf_path):

        os.remove(pdf_path)

    if os.path.exists("forecast_chart.png"):

        os.remove("forecast_chart.png")


# ================= MAIN =================

def main():

    app = ApplicationBuilder().token(
        BOT_TOKEN
    ).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(filters.Document.ALL, handle_csv)
    )

    print("✅ Telegram bot running...")

    app.run_polling()


# ================= ENTRY =================

if __name__ == "__main__":

    main()