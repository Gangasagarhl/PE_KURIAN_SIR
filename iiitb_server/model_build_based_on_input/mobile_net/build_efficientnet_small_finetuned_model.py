import tensorflow as tf
import tensorflow_hub as hub

class DownloadAndFinetune:
    def __init__(self):
        print("Initiated")

    def download_model(self):
        """
        Downloads EfficientNet-Lite0 and builds a finetunable model using Functional API.
        """
        model_url = "https://tfhub.dev/tensorflow/efficientnet/lite0/feature-vector/2"
        
        try:
            # ✅ Create input tensor
            inputs = tf.keras.layers.Input(shape=(224, 224, 3))
            
            # ✅ Load Hub module with proper input handling
            hub_layer = hub.KerasLayer(model_url, trainable=False)
            x = hub_layer(inputs)
            
            # ✅ Add classification head
            outputs = tf.keras.layers.Dense(10, activation='softmax')(x)
            
            # ✅ Build model
            model = tf.keras.Model(inputs=inputs, outputs=outputs)
            return model
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return None

if __name__ == "__main__":
    obj = DownloadAndFinetune()
    model = obj.download_model()
    
    if model:
        model.summary()
        print("✅ Model loaded successfully!")
    else:
        print("❌ Model loading failed")
        