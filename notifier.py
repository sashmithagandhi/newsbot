import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date
from dotenv import load_dotenv
import os

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_APP_PASSWORD")

def send_morning_digest(users, fetched_summary):
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("⚠️ Email credentials not set, skipping email notifications")
        return

    for user in users:
        try:
            msg = MIMEMultipart()
            msg["From"] = SENDER_EMAIL
            msg["To"] = user.email
            msg["Subject"] = f"📰 Your Morning NewsBot Digest — {date.today().strftime('%d %B %Y')}"

            body = f"""
Good morning {user.name}! 🌅

Today's newspapers are ready on NewsBot.

{fetched_summary}

Open NewsBot to read and chat with AI about today's news.

— NewsBot Team
            """

            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.send_message(msg)

            print(f"✅ Email sent to {user.email}")

        except Exception as e:
            print(f"❌ Failed to send to {user.email}: {e}")