import streamlit as st
import requests
from PIL import Image
import io
import warnings
import os
os.environ["PYTHONWARNINGS"] = "ignore"

warnings.filterwarnings("ignore")

SERVER_URL = "http://192.168.86.36:5000/process_image"

st.write("Upload an image and get a caption!")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image")

    
    image = image.convert("RGB")

    
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="JPEG")
    img_bytes.seek(0)

    
    st.write("Processing...")
    try:
        response = requests.post(SERVER_URL, files={"image": img_bytes})
        if response.status_code == 200:
            result = response.json()["result"]
            st.success(f"Caption: {result}")
        else:
            st.error("Error processing the image")
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
