import os
import numpy as np
import cv2
try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    import tensorflow.lite as tflite

class RaspberryPiPredictor:
    def __init__(self, model_path="strp_model.tflite"):
        # Initialize TensorFlow Lite interpreter
        self.interpreter = tflite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        
        # Get input and output details
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        
        # Labels
        self.labels = ["NO", "SCI"]
        
        print("✅ Model loaded successfully on Raspberry Pi!")
        print(f"Input shape: {self.input_details[0]['shape']}")
        print(f"Input type: {self.input_details[0]['dtype']}")

    def predict_image(self, img):
        # Resize using OpenCV
        resized_img = cv2.resize(img, (224, 224))
        
        # Convert BGR to RGB
        resized_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
        
        # Normalize and prepare input
        img_array = resized_img.astype(np.float32) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # Set input tensor
        self.interpreter.set_tensor(self.input_details[0]['index'], img_array)
        
        # Run inference
        self.interpreter.invoke()
        
        # Get prediction
        predictions = self.interpreter.get_tensor(self.output_details[0]['index'])[0][0]
        
        # Determine predicted class
        predicted_class = self.labels[int(predictions > 0.5)]
        
        # Print result
        print(f"✅ Predicted Class: {predicted_class}")
        print(f"✅ Confidence Score: {predictions:.4f}")
        
        return predicted_class, predictions

# Usage
predictor = RaspberryPiPredictor("strp_model.tflite")

# Test with an image
img = cv2.imread("test_image.jpg")
if img is not None:
    result = predictor.predict_image(img)
else:
    print("❌ Could not load test image")