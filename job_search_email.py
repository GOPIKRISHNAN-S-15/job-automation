import os, smtplib, requests, datetime
from email.message import EmailMessage

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

SMTP_HOST = os.getenv("EMAIL_SMTP_HOST")
SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", "587"))
SMTP_USER = os.getenv("EMAIL_SMTP_USER")
SMTP_PASS = os.getenv("EMAIL_SMTP_PASS")

EMAIL_TO = os.getenv("EMAIL_TO")
EMAIL_FROM = os.getenv("EMAIL_FROM")

country = "in"
what = "entry level data analyst OR junior data analyst OR data analytics intern"

def fetch_jobs():
    url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": what,
        "results_per_page": 20
    }
    return requests.get(url, params=params).json()

def send_email(body):
    msg = EmailMessage()
    msg["Subject"] = "Daily Data Jobs"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.starttls()
        s.login(SMTP_USER, SMTP_PASS)
        s.send_message(msg)

data = fetch_jobs()

text = ""
for j in data.get("results", [])[:10]:
    text += f"{j['title']} - {j['company']['display_name']}\n{j['redirect_url']}\n\n"

send_email(text)
