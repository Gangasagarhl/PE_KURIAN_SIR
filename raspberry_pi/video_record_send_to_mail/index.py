"""
First record the video for the duration
Then send the video
Then delete the file. 
"""
from video_record_send_to_mail.delete_file import delete_file
#from video_record_send_to_mail.record_video import capture_with_ffmpeg
from video_record_send_to_mail.send_video_to_mail import send_email
from video_record_send_to_mail.whatsapp_message import send_whatsapp_alert

def execute_record(reciever_email):
    #capture_with_ffmpeg()
    send_email(reciever_email)
    
    _ = send_whatsapp_alert("Emergency at my end")
    delete_file()
    
    
    
    
