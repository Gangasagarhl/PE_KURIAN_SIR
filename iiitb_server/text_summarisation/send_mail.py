import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_mail(message_text):
# Email credentials
    EMAIL_ADDRESS = "hlgsagar.1@gmail.com"  # Change this
    EMAIL_PASSWORD = "dbzg qyrt fvpu euks"  # Use an App Password
    RECEIVER_EMAIL = "hlgsagar.2@gmail.com"  # Change this

    # Create a 300-word text message
    

    # Set up the MIME email
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = "Test Email with 300-Word Text"

    # Attach the message body
    msg.attach(MIMEText(message_text, "plain"))

    try:
        # Connect to SMTP server and send email
        server = smtplib.SMTP("smtp.gmail.com", 587)  # For Gmail
        server.starttls()  # Secure the connection
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        
        print("Email sent successfully!")

    except Exception as e:
        print(f"Error: {e}")
