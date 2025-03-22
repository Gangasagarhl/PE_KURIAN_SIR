import smtplib
from email.message import EmailMessage
import os



def send_email(receiver_email,video_path="video_record_send_to_mail/recording.avi", sender_email="hlgsagar.1@gmail.com", sender_password="dbzg qyrt fvpu euks", subject="Emergency Video", body="Emergency Video"):
    
    try:
        # Create the email message
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg.set_content(body)

        # Attach the video
        with open(video_path, "rb") as f:
            msg.add_attachment(f.read(), maintype="video", subtype="avi", filename=video_path)

        # SMTP configuration (Gmail example)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)

        print(f"Email sent successfully to {receiver_email}")
        

    except Exception as e:
        print(f"Failed to send email: {e}")



