import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from time import strftime, gmtime
from email.mime.text import MIMEText
from scraper import *

def sent_working_email():
    df2 = scraping_web_prices_day_by_day()
    name = "Report_"+ str(dt.datetime.today().date().strftime("%d-%m"))+".xlsx"
    df2.to_excel(name, encoding="utf-8")
    msg = MIMEMultipart()
    msg["From"] = "gabriele.ghisleni01@gmail.com"
    msg["To"] = "pr05@live.it"
    msg["Subject"] = "Daily Report "+str(dt.datetime.today().date().strftime("%d-%m"))
    row = len(df2)
    body= f"""This email is proudly generated automatically via Python.
    Every day at 6pm you will receive this excel file containing all the cars that have been uploaded in the last 24 hours.
    Today {row} new cars have been uploaded\n\nGabriele"""
    body = MIMEText(body)  # convert the body to a MIME compatible string
    msg.attach(body)  # attach it to your main message
    part = MIMEBase("application", "octet-stream")
    part.set_payload(open(name, "rb").read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment", filename=name)  # or
    msg.attach(part)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("gabriele.ghisleni01@gmail.com", os.environ.get("GMAIL_GABRY"))
        smtp.send_message(msg)

def send_wrong_email():
    msg = MIMEMultipart()
    msg["From"] = "gabriele.ghisleni01@gmail.com"
    msg["To"] = "pr05@live.it"
    msg["Subject"] = "Error occured at: " + str(dt.datetime.now())[0:16]
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("gabriele.ghisleni01@gmail.com", os.environ.get("GMAIL_GABRY"))
        smtp.send_message(msg)