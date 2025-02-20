import torch
from torchvision import models, transforms
from torchvision.models import ResNet101_Weights
from flask import Flask, request, jsonify, render_template
from PIL import Image
import requests
import base64
import io

app = Flask(__name__)

# Load the pre-trained ResNet model and set to evaluation mode
model = models.resnet101(weights=ResNet101_Weights.DEFAULT)
model.eval()

# Load ImageNet labels dynamically
def load_labels():
    url = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

labels = load_labels()

# Preprocessing function for images
def preprocess_image(image):
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    return transform(image).unsqueeze(0)  # Add batch dimension

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Check if image is uploaded
    if 'image' not in request.files:
        return jsonify({"error": "No file uploaded"})

    # Open and preprocess the image
    file = request.files['image']
    image = Image.open(file).convert('RGB')
    input_tensor = preprocess_image(image)

    # Encode the image to Base64
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # Make prediction
    with torch.no_grad():
        outputs = model(input_tensor)
        _, predicted_idx = outputs.max(1)  # Get the index of the highest probability
        predicted_label = labels[predicted_idx.item()]  # Map to ImageNet label

    return jsonify({"label": predicted_label, "image": base64_image})

if __name__ == "__main__":
    app.run()
