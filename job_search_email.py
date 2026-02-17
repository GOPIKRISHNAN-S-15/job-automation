import os
import smtplib
import requests
import datetime
from email.message import EmailMessage

# ===== ENV VARIABLES =====
APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

SMTP_HOST = os.getenv("EMAIL_SMTP_HOST")
SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", "587"))
SMTP_USER = os.getenv("EMAIL_SMTP_USER")
SMTP_PASS = os.getenv("EMAIL_SMTP_PASS")

EMAIL_TO = os.getenv("EMAIL_TO")
EMAIL_FROM = os.getenv("EMAIL_FROM")

# ===== SEARCH SETTINGS =====
country = "in"

roles = [
    "data analyst",
    "data analyst intern",
    "full stack developer",
    "full stack developer intern",
    "python developer",
    "python developer intern",
    "java developer",
    "java developer intern"
]

# ===== FETCH JOBS =====
def fetch_jobs(role):
    url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"

    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": role,
        "results_per_page": 10
    }

    response = requests.get(url, params=params)
    return response.json()

# ===== EMAIL FUNCTION =====
def send_email(body):
    msg = EmailMessage()
    msg["Subject"] = "Daily Tech Jobs Update 🚀"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.starttls()
        s.login(SMTP_USER, SMTP_PASS)
        s.send_message(msg)

# ===== MAIN =====
all_text = ""
job_found = False

today = datetime.date.today()

for role in roles:
    data = fetch_jobs(role)
    jobs = data.get("results", [])

    if jobs:
        job_found = True
        all_text += f"\n========== {role.upper()} ==========\n\n"

        for j in jobs[:5]:
            title = j.get("title", "N/A")
            company = j.get("company", {}).get("display_name", "N/A")
            url = j.get("redirect_url", "")

            all_text += f"{title} — {company}\nApply: {url}\n\n"

# ===== NO JOB MESSAGE =====
if not job_found:
    all_text = "No jobs found today 🙂\nTry again tomorrow!"

# ===== SEND =====
send_email(all_text)

print("Email sent successfully!")
