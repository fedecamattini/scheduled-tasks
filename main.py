import datetime as dt
import pandas as pd
import random
import smtplib
import os

MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

df = pd.read_csv("birthdays.csv")

def check_birthdays():
    now = dt.datetime.now()
    day = now.day
    month = now.month
    birthdays = [
        {"name":row.name, "email":row.email}
        for row in df.itertuples()
        if row.month == month and row.day == day]
    return birthdays

def write_email(person_name):
    with open(f"letter_templates/letter_{random.randint(1, 3)}.txt", "r") as file:
        old_text = file.read()
        new_text = old_text.replace("[NAME]", person_name)
        return new_text

def send_email(email_address, email_body):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=email_address, msg=f"Subject:Happy Birthday!\n\n{email_body}")

today_birthdays = check_birthdays()
for person in today_birthdays:
    message = write_email(person["name"])
    send_email(person["email"], message)
