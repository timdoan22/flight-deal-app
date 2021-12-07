from twilio.rest import Client
import os
import smtplib

TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUM = TWILIO_NUMBER
RECIPIENT_PHONE_NUM = RECIPIENT_PHONE_NUMBER
MY_EMAIL = YOUR_EMAIL
PASSWORD = YOUR_PASSWORD
RECIPIENT_EMAIL = RECIPIENT_EMAIL


class NotificationManager:
    def __init__(self):
        pass

    def send_sms(self, phone, body):
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages \
            .create(
                body=body,
                from_=TWILIO_PHONE_NUM,
                to=phone
                )
        print(message.sid)

    def send_email(self, first_name, recipient_email, body):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=RECIPIENT_EMAIL,
                msg=f"Subject:Amazing Flight Deal Alert!\n\nHi {first_name}, we've got an awesome deal for you! \n\n{body}"
            )
        print(f"Email sent successfully to {first_name}!")
