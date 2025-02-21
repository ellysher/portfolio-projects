from flask import Flask, request, render_template, redirect, url_for
import os
import tensorflow as tf
import numpy as np
import cv2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Load the trained model
model = tf.keras.models.load_model("Model2 Final Brain Tumor.keras")

# Define class labels
class_labels = ['glioma', 'meningioma', 'notumor', 'pituitary']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def preprocess_image(image_path, img_size=224):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, (img_size, img_size))
    image = image / 255.0
    image = np.expand_dims(image, axis=-1)
    return np.expand_dims(image, axis=0)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            image = preprocess_image(file_path)
            predictions = model.predict(image)
            predicted_class = np.argmax(predictions, axis=1)[0]
            confidence = np.max(predictions)
            result = {
                'class': class_labels[predicted_class],
                'confidence': float(confidence),
                'filename': filename
            }
            return render_template('index.html', result=result)
    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)