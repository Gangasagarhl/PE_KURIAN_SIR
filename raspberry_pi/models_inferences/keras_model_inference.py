import os
import numpy as np
import cv2
from tensorflow import keras
from tensorflow.keras.preprocessing.image import img_to_array
# Load the model
model = keras.models.load_model("model/model.keras")

# Labels
labels = ["BOTTLE", "NO"]

def predict_image(img):
    # Resize using OpenCV
    resized_img = cv2.resize(img, (224, 224))
    
    # Convert BGR (OpenCV format) to RGB (what the model expects)
    resized_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)

    # Convert to float32 and normalize
    img_array = img_to_array(resized_img) / 255.0  
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

    # Make prediction
    predictions = model.predict(img_array)[0][0]
    predictions_full = model.predict(img_array)

    print(predictions_full)

    # Determine predicted class
    predicted_class = labels[int(predictions > 0.5)]

    # Print result
    print(f"✅ Predicted Class: {predicted_class}")
    print(f"✅ Confidence Score: {predictions:.4f}")
    return predicted_class
