# app.py
from flask import Flask, request, jsonify
from send_notifications_mails.send_gmail_to_reciepient import gmail
from send_notifications_mails.send_whatsapp_alerts import send_whatsapp_alert
from datetime import datetime
import threading
import pandas as pd
import os
import time

app = Flask(__name__)

class alert_neighbours:
    def __init__(self):
        print("alert neighbours is initiated\n")

    def extract_emails(self, id):
        print("extract emails\n")
        df = pd.read_csv('database/email.csv')
        return df[df['id'] == id]['email'].tolist()

    def extract_numbers(self, id):
        print("extract numbers\n")
        df = pd.read_csv('database/phone_numbers.csv')
        return df[df['id'] == id]['phone'].tolist()

    def extract_the_neighbours_info_from_database(self, id):
        emails = self.extract_emails(id)
        phone = self.extract_numbers(id)
        return emails, phone





    def truly_alert(self):
        try:
            id = request.form.get('id')
            address = request.form.get('address')
            video = request.files['video']

            video.seek(0, 2)  # 2 means "from the end"
            size = video.tell()  # This returns the size in bytes
            # Reset the cursor back to the beginning so it can be saved later
            video.seek(0)
            print(f"Video size: {size} bytes ({size / 1024:.2f} KB)")



            print(f"\n\n***\n{id}\n{address}\n{video.filename} ***\n\n")
            #now = datetime.now().strftime("%Y%m%d%H%M%S")
            video_name = video.filename
            video.save(str("extreme_emergency_alerts/")+video_name)



            t1 = threading.Thread(target=self.alerting_all, args=(video_name, id, address))
            t1.start()
            t1.join()
            print("Calling to delete the file since the emergency video is sent\n\n\n")
            print("Video_name:",video_name)
            self.delete_the_file(video_name)

            return jsonify({"status": "success", "message": "Alert initiated"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
        






    def alerting_all_email_id(self, email_ids, video_name, address):
        for email in email_ids:
            #print("email: ",email,"\n")
            t = threading.Thread(
                target=gmail(reciver_email=email, address=address).send_video_and_summary,
                args=(f"extreme_emergency_alerts/{video_name}",f"Very Serious EMergency is detected at address\n{address}\n COnfirm through video and Start\n","SERIOUS CASED EMERGENCY START AS SOON AS POSSIBLE")
            )
            t.start()
        print("alerting through mail\n")








    def alerting_all_through_whatsapp(self, phone_numbers):
        for phone in phone_numbers:
            t = threading.Thread(
                target=send_whatsapp_alert,
                args=(phone,"EXTEREME EMERGENCY HAVE A LOOK AT MAIL AND HELP PLEASE")
            )
            t.start()






    def delete_the_file(self,file_name):
        
        try:
            os.remove(file_name)
            print("video deleted")
        except:
            print("file alreday deleted")


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



# Initialize object
an = alert_neighbours()

@app.route("/trigger-alert", methods=["POST"])
def trigger_alert():
    return an.truly_alert()

if __name__ == "__main__":
    app.run(debug=True)
