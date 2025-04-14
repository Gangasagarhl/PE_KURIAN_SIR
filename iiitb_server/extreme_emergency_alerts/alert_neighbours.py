from send_notifications_mails.send_gmail_to_reciepient import gmail
from send_notifications_mails import send_whatsapp_alerts
import requests
from datetime import datetime
import threading
import pandas as pd
import os

class alert_neighbours:
    def __init__(self):
        print("alert neighbours is initiated\n")

    def extract_emails(self, id):
        df = pd.read_csv('../database/email.csv')
        return df[df['id'] == id]['email'].tolist()

    def extract_numbers(self, id):
        df = pd.read_csv('../database/phone_numbers.csv')
        return df[df['id'] == id]['phone'].tolist()

    def extract_the_neighbours_info_from_database(self, id):
        emails = self.extract_emails(id)
        phone = self.extract_numbers(id)
        return emails, phone

    def truly_alert(self):
        # Generate a formatted timestamp if needed
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        id = "sag1" 
        print(id) # You might consider renaming this variable (e.g., alert_id) to avoid shadowing built-in id()
        address = "Visveswaraya@iiitb"
        print(address)
        video_name = "1.mp4"  # Or: f"{id}_{now}.mp4"
        print(video_name)

        
        # Correct thread instantiation: use keyword 'target' and proper args tuple
        t1 = threading.Thread(group=None,target=self.alerting_all, args=(video_name, id, address))
        t1.start()
        t1.join()

        return True

    def alerting_all_email_id(self, email_ids, video_name, address):
        for email in email_ids:
            # Create a new gmail object for each email and call its send_video_and_summary method
            t = threading.Thread(
                target=gmail(reciver_email=email, address=address).send_video_and_summary,
                args=(f"../extreme_emergency_alerts/{video_name}",)  # Note the trailing comma
            )
            t.start()

    def alerting_all_through_whatsapp(self, phone_numbers):
        for phone in phone_numbers:
            t = threading.Thread(
                target=send_whatsapp_alerts,
                args=(phone,)
            )
            t.start()

    def alerting_all(self, video_name, id, address="Visveswaraya@iiitb"):
        email_ids, phone_numbers = self.extract_the_neighbours_info_from_database(id)

        t1 = threading.Thread(
            target=self.alerting_all_email_id,
            args=(email_ids, video_name, address)
        )
        t2 = threading.Thread(
            target=self.alerting_all_through_whatsapp,
            args=(phone_numbers,)
        )

        t1.start()
        t2.start()
        t1.join()
        t2.join()

        try:
            os.remove(video_name)
            print(f"Deleted: {video_name}")
        except Exception as e:
            print(f"Failed to delete video: {e}")

# For testing extraction functionality
def checking():
    df = pd.read_csv('../database/phone_numbers.csv')
    phone_numbers = df[df['id'] == 'sag1']['phone'].tolist()
    print(phone_numbers)

if __name__ == "__main__":
    # Test the checking function first
    checking()
    
    # Test the alert_neighbours functionality
    from extreme_emergency_alerts.alert_neighbours import alert_neighbours
    obj = alert_neighbours()
    print(obj.truly_alert())
