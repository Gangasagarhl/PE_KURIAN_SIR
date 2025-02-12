from flask import Flask, request, jsonify
from PIL import Image
import io
from image_descriptor import description

import os
os.environ["PYTHONWARNINGS"] = "ignore"
from datetime import datetime
import warnings


warnings.filterwarnings("ignore")
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    message="The `use_column_width` parameter has been deprecated"
)

app = Flask(__name__)
"""
This is like registering yourself within the big home, so any body who is coming to look after
you, will search for the directory of Flask and gets t know about address
, you are here I'll deliver the details you want and return 
the processed part in return or do something useful.

app  here is used to start if __main__ is checked.
"""


UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route("/process_image", methods=["POST", "GET"])
def process_image():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    for key, file in request.files.items():
        print(":Key:", key,"File Name::\n",file.filename)
    
    image_file = request.files["image"]
    # dictionary like extracts
    
    client_ip = request.remote_addr
    image = Image.open(io.BytesIO(image_file.read()))

    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_filename = f"{client_ip}_{timestamp}.jpg"
    image_path = os.path.join(UPLOAD_DIR, image_filename)
    image.save(image_path)

   
    caption =  description(image)
    return jsonify({"result": caption})


def run_server():
    
    app.run(host="0.0.0.0", port=5000, debug=True)
    """
    This 0.0.0.0 is used to bind to all the network interfaces of the device 
    on which flask is running. Currently whn connected to the wifi, I have 2 interfaces
    1.  loop back address
    2.  hotspot of mobile.
    
    If you have more interfaces it will bind to all the interfaces, hence 
    """

if __name__ == "__main__":
    print("Starting the server on the local Wi-Fi network...")
    run_server()
