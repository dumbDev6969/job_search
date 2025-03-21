
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get email credentials from environment variables


def my_send_email(subject: str, body: str, recipients: list[str]) -> None:
    """
    Send an HTML email using Gmail SMTP server.

    Args:
        subject (str): The subject line of the email
        body (str): The HTML body content of the email
        recipients (list[str]): List of recipient email addresses
    Returns:
        None: This function doesn't return anything, but prints a success message
    """
    sender = os.getenv('SENDER_EMAIL')
    password = os.getenv('SENDER_PASSWORD')
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")


# Example usage
# if __name__ == "__main__":
#     subject = "daily update"
#     body = "This is your daily update"
#     recipients = ["jemcarlo46@gmail.com", "recipient2@gmail.com"]

#     try:
#        # Use environment variables instead of decode_string
#        my_send_email(subject, body, SENDER_EMAIL, recipients, SENDER_PASSWORD)
#     except Exception as e:
#        print(str(e))
#        print("Failed to send email")