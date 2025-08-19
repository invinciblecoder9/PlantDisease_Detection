import os
from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import numpy as np
import io # Make sure io is imported
from tensorflow.keras.preprocessing import image

# Initialize the Flask app. This line MUST come before any @app.route decorators.
app = Flask(__name__)

# Load the trained model
# Ensure 'plant_disease_model.h5' is in the same directory as app.py
model = tf.keras.models.load_model('plant_disease_model_v3.h5')

# Define the class names in the correct order as your model
# IMPORTANT: Replace these with your actual 15 class names
# The order here must match the order of class_indices from your train_generator
# Example (adjust based on your specific classes and their order):
class_names = [
    'Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy',
    'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
    'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight',
    'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites_Two_spotted_spider_mite', 'Tomato___Target_Spot',
    'Tomato___Tomato_mosaic_virus', 'Tomato___Tomato_YellowLeaf__Curl_Virus',
    'Tomato___healthy'
]

# Define the home page route
@app.route('/')
def home():
    return render_template('index.html')

# Define the prediction route
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file:
        try:
            # Read the image data from the FileStorage object into a BytesIO object
            # This fixes the TypeError you encountered previously
            img_bytes = io.BytesIO(file.read())
            
            # Preprocess the user's uploaded image from the in-memory data
            img = image.load_img(img_bytes, target_size=(224, 224))
            
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0) # Add a batch dimension
            img_array /= 255.0  # Normalize pixel values
            
            # Make a prediction
            predictions = model.predict(img_array)
            predicted_class_index = np.argmax(predictions)
            predicted_class_name = class_names[predicted_class_index]
            
            return jsonify({'prediction': predicted_class_name})
            
        except Exception as e:
            # Return any unexpected errors to the frontend for debugging
            return jsonify({'error': str(e)})

# Run the Flask app
# if __name__ == '__main__':
#     app.run(debug=True)