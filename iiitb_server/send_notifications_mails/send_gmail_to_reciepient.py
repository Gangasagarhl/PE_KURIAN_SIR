from datetime import datetime
import smtplib
from email.message import EmailMessage
import os


class gmail: 
    def __init__(self,reciver_email,sender_email="hlgsagar.1@gmail.com", sender_password="dbzg qyrt fvpu euks",address="IIIT-B_CEEMS_LAB"):
        self.sender_email=sender_email
        self.sender_password =  sender_password
        self.address =  address
        
        
        # Get current datetime
        now = datetime.now()
        # Extract parts
        self.current_time = now.strftime("%H:%M:%S")        # Time in HH:MM:SS
        self.current_date = now.strftime("%Y-%m-%d")        # Date in YYYY-MM-DD
        self.current_day = now.strftime("%A")  
        self.reciver_mail = reciver_email             # Day of the week (e.g., Monday)
        print("In gmail: ", self.reciver_mail,"\n")
        

    def send_video_and_summary(self,video_path=None,summary=None,subject="Emergency Video And Summary"):
        body="Emergency Video\nTime: "+self.current_time+"\nDate: "+self.current_date+"\nDay: "+self.current_day
        body+="\nAddress: "+self.address+"\n"
        if  summary:
            body += "\n\nSummary: "+summary

        try:
            # Create the email message
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = self.reciver_mail
            msg.set_content(body)

            # Attach the video
            with open(video_path, "rb") as f:
                msg.add_attachment(f.read(), maintype="video", subtype="avi", filename=video_path)

            # SMTP configuration (Gmail example)
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            print(f"Email sent successfully to {self.reciver_mail}")
            

        except Exception as e:
            print(f"Failed to send email: {e}")

    


