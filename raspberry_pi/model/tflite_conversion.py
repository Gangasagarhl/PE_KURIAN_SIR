import tensorflow as tf

# Load your existing model
model = tf.keras.models.load_model("raspberry_pi/model/strp.keras")

# Convert to TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]  # Optimize for size and speed
tflite_model = converter.convert()

# Save the TensorFlow Lite model
with open("strp_model.tflite", "wb") as f:
    f.write(tflite_model)