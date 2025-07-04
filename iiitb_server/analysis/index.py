from iiitb_server.analysis.image_descriptor import GetCaptions
from iiitb_server.analysis.summariser import Summarizer
from iiitb_server.send_notifications_mails.send_gmail_to_reciepient import gmail
from iiitb_server.send_notifications_mails.send_whatsapp_alerts import send_whatsapp_alert
import threading
import os
global blip_model, blip_processor, t5_model, t5_tokenizer
class make_it:
    def __init__(self,video_path, output_folder):
        
        self.captions =  GetCaptions()#this takes the captions for the uploaded vidoe
        self.summary =  Summarizer()#this takes the summary 
        self.video= video_path
        self.out = output_folder
        
      


    def generate_summary(self):
        print("\nNow started to make the summarisation\n")
        caption =  self.captions.extract_images_from_video_returns_list_of_captions(self.video, self.out)
        refined_summary = self.summary.map_reduce_summarize(captions=caption)
        return refined_summary
    
    ##the phone numbers and the gmail address should be mapped with the database and then it has to process
    def send_to_recepeints(self,to_mail,to_phone,address="IIITB_CEEMS_LAB"):
        print("\nreciever_email_: ", to_mail,"\n Phone: ",to_phone)
        self.reciever_email = to_mail
        self.phone_number =  to_phone
        gmailing = gmail(reciver_email=self.reciever_email ,address=address)
        print("The gmail_configuarations are set\n")

        summary =  self.generate_summary()
        print("\n\n**********Summary********\n",summary)

        gmailing.send_video_and_summary(video_path=self.video, summary=summary)
        send_whatsapp_alert(to_number=self.phone_number)
        os.remove (self.video)



if __name__ =="__main__": 
    obj = make_it(video_path="videos/videoplayback.mp4", output_folder="out")
    thread = threading.Thread(target=obj.send_to_recepeints, args=("hlgsagar.2@gmail.com", 8105114611, ))
    thread.start()