import json
import smtplib
import random
import requests
from dotenv import dotenv_values

config = dotenv_values(".env")

my_email = config["email"]
password = config["password"]
recipient_emails = config["recipient_emails"]
gmail_smtp_address = "smtp.gmail.com"
url = config["url"]


def get_verses():
    try:
        with open("verses.json") as file:
            verses = json.load(file)
            return verses
    except FileNotFoundError:
        data = requests.get(url)
        json_data = data.json()
        with open("verses.json", mode="w") as file:
            json.dump(json_data, file, indent=4)
            verses = json_data
            return verses


def get_verse(verse_list):
    chapter_num = random.randint(1, 114)
    chapter = verse_list[f"{chapter_num}"]
    verse_data = random.choice(chapter)
    verse_num = verse_data["verse"]
    verse_text = verse_data["text"]
    return f"({chapter_num}:{verse_num}) {verse_text}"


def send_email(msg):
    with smtplib.SMTP(gmail_smtp_address) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=recipient_emails,
            msg=msg
        )


def main():
    verses = get_verses()
    verse = get_verse(verses)
    send_email(msg=f"Subject:Verse of the day\n\n{verse}")


main()
