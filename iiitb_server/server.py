# server.py
from flask import Flask, request, jsonify
import csv
import os
from flask import Flask
from flask_socketio import SocketIO, disconnect
import os
from flask import Flask, request, render_template
from RAG.data_preprocessing import preprcoess
from RAG.persistant_RAG import PersistentRAGSystem
import time
from datetime import datetime
import threading

# Import the models to ensure they are loaded
from iiitb_server.model_manage import blip_model, blip_processor, t5_model, t5_tokenizer

# Import other modules (adjust paths as needed)
from iiitb_server.analysis.donwload_video_from_client import video_photo_analyzer
from iiitb_server.extreme_emergency_alerts.alert_neighbours import alert_neighbours
from  iiitb_server.analysis.summariser import Summarizer

app = Flask(__name__)

CSV_FILE = "iiitb_server/database/data.csv"

def initialize_csv():
    os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "description"])




initialize_csv()
rag = PersistentRAGSystem()

######################## SUmmary for the whole halh of the day*******
def add_summary_to_vector_store():
    summary_obj = Summarizer()
    li = preprcoess().execute()
    summary_text = summary_obj.refine_summarize(li)
    rag.add_text_data(summary_text)



def check_time_and_run():
    while True:
        now = datetime.now()
        if now.hour == 18:
            add_summary_to_vector_store()
            break  # remove this if you want it to run daily
        time.sleep(3000)  # sleep for 50 minutes or any interval you prefer

# Run the function in a background thread
thread = threading.Thread(target=check_time_and_run, daemon=True)
thread.start()




################################### Summary added here to vector store #########


@app.route("/", methods=["GET", "POST"])
def index():
    answer = None
    context = None
    if request.method == "POST":
        query = request.form.get("query")
        if query:
            response = rag.query(query)
            answer = response["answer"]
            context = response["context"]
    return render_template("index.html", answer=answer, context=context)





# Create instances for video/photo analysis as needed.
va = video_photo_analyzer()
app.add_url_rule('/upload_video', view_func=va.upload_video, methods=['POST'])
app.add_url_rule('/upload_photo_for_summary', view_func=va.upload_photo, methods=['POST'])
app.add_url_rule('/emergency_alert_neighbours', view_func=alert_neighbours().truly_alert, methods=['POST'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
