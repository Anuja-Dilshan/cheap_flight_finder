import smtplib
from user_registration import UserRegistration


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.user = 'anujadilshan8@gmail.com'
        self.password = 'iiachefiixaomrxv'
        self.smtp_address = 'smtp.gmail.com'

    def send_email(self, msg: str, email: str):

        with smtplib.SMTP(self.smtp_address) as connection:
            connection.starttls()
            connection.login(user=self.user, password=self.password)
            connection.sendmail(from_addr=self.user, to_addrs=email, msg=msg)
