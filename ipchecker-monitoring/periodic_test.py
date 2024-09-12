import subprocess
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# Email configuration
SENDER_EMAIL = "ipcheckermonitoringalerts@hotmail.com"
SENDER_PASSWORD = "ipchecker123"  
RECIPIENT_EMAIL = "ipcheckermonitoringalerts@hotmail.com"
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, text)
        server.quit()
        print("Alert email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

def monitor_and_alert():
    monitor_file = "monitoring_log.json"  # Name of the JSON log file

    while True:
        print(f"Running monitor.py at {datetime.now()}...")
        result = subprocess.run(["python", "monitor.py"], capture_output=True, text=True)
        output = result.stdout

        # Check if any function failed
        if "Correct: No" in output:
            subject = "IP Checker Monitoring Alert"
            body = f"One or more tests failed during the monitoring at {datetime.now()}:\n\n{output}"
            send_email(subject, body)

        # Wait for an hour before the next check
        time.sleep(3600)

if __name__ == "__main__":
    monitor_and_alert()
