from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image
import base64
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# ====================== Flask App Setup ======================
app = Flask(__name__)
app.secret_key = "cervical_cancer_prediction_secret_key"

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'dib'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ====================== Load Keras Model ======================
try:
    model = load_model("deeplabv3_final.h5") 
except Exception as e:
    print("Model loading failed:", e)
    model = None

# ====================== Helper Functions ======================
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_path):
    """Prepare image for Keras model"""
    img = image.load_img(image_path, target_size=(224, 224))  # Match your model input
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0  # Normalize if model trained this way
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def get_prediction(image_path):
    """Get class prediction from model"""
    classes = ["Carcinoma", "Light Dyplastic", "Moderate Dyplastic", 
               "Normal columnar", "Normal intermediate", 
               "Normal Superficial", "Severe Dyplastic"]

    input_tensor = preprocess_image(image_path)
    predictions = model.predict(input_tensor)[0]
    predicted_class_index = np.argmax(predictions)
    predicted_class = classes[predicted_class_index]
    confidence = float(predictions[predicted_class_index])
    return predicted_class, confidence

# ====================== Routes ======================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                prediction, confidence = get_prediction(filepath)
            except Exception as e:
                flash(f'Prediction failed: {e}')
                return redirect(request.url)

            with open(filepath, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode('utf-8')

            return render_template('result.html',
                                   prediction=prediction,
                                   confidence="{:.2f}%".format(confidence * 100),
                                   image_data=img_data)

    return render_template('predict.html')

# ====================== Run ======================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
