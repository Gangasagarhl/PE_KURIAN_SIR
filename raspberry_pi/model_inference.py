import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
import cv2


class Inference:
    def __init__(self):
        self.model = tf.keras.models.load_model("model/model.keras")  # Load your model
        print("Model Loaded Successfully\n")

    def inference(self, img):
        img = cv2.resize(img, (224, 224))

        # Convert image to array and normalize pixel values to [0,1]
        img_array = img_to_array(img) / 255.0  
        img_array = np.expand_dims(img_array, axis=0)  # Expand dimensions to match model input

        # ✅ Step 3: Make prediction
        prediction = self.model.predict(img_array)  # Get the output prediction

        # ✅ Step 4: Interpret the prediction result
        class_labels = ["NO", "pen"]  # Modify based on your class labels
        predicted_class = class_labels[int(prediction[0][0] > 0.5)]  # Assuming binary classification
        print("Class:", predicted_class)

        if predicted_class == "pen":
            return "record"
            

