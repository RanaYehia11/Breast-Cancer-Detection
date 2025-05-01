import numpy as np 
import cv2
import tensorflow as tf
from django.http import JsonResponse
from django.shortcuts import render
import json 
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from tensorflow.keras.models import load_model  # type: ignore

# Load the trained model 
model = load_model(r"E:\my graduation project\django_form\notebook\BreastCancer.h5", compile=False)

# Define class labels for prediction output
class_labels = ["Benign", "Malignant", "Normal"]  

def predict_image(image):
    """Process the uploaded image and use the model to predict cancer type with advice."""
    
    # Convert image color from BGR (OpenCV default) to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Resize image to match model input size
    image = cv2.resize(image, (128, 128))
    
    # Normalize image pixels to the range [0, 1]
    image = image.astype("float32") / 255.0
    
    # Add batch dimension (1, 128, 128, 3)
    image = np.expand_dims(image, axis=0)

    # Make prediction using the loaded model
    prediction = model.predict(image)
    
    # Get the index of the class with the highest confidence
    class_index = np.argmax(prediction, axis=1)[0]
    
    # Get the class label
    result = class_labels[class_index]

    # Generate medical advice based on the prediction result
    advice = {
        "Malignant": "<b>A cancerous tumor</b> <span style='font-weight: lighter;'>that can grow and spread to other parts of the body if not treated promptly. <br>  <b style='color:#FF0059;'> Advice: </b> Please consult a doctor immediately.</span>",
        "Benign": "<b>A non-cancerous tumor</b> <span style='font-weight: lighter;'>that does not spread to other parts of the body. <br>  <b style='color:#FF0059;'> Advice:</b> Regular check-ups with a doctor are recommended for you.</span>",
        "Normal": "<b>Healthy breast tissue with no signs of cancer</b> <span style='font-weight: lighter;'> <br> <b style='color:#FF0059;'>Advice:</b> Keep up with self-checks and screenings.</span>"
    }

    return result, advice[result]

@csrf_exempt
def predict_breast_cancer(request):
    """Handle image upload, make prediction, and return advice + doctors list."""

    doctors = []  # Initialize doctors list

    try:
        # Read the doctor list from an Excel file and convert to a list of dictionaries
        df = pd.read_excel(r"E:\doctors-list.xlsx", dtype=str)
        doctors = df.to_dict(orient='records')
    except Exception as e:
        print(f"Error reading Excel file: {e}")  # Log error for debugging

    # Handle POST request and check if an image file was uploaded
    if request.method == "POST" and "image" in request.FILES:
        try:
            file = request.FILES["image"]  # Get uploaded image
            image_array = np.frombuffer(file.read(), np.uint8)  # Convert to NumPy array
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)  # Decode image with OpenCV

            # Predict result and get advice
            result, advice = predict_image(image)

            # Return prediction, advice, and doctor list as JSON
            return JsonResponse({"prediction": result, "advice": advice, "doctors": doctors})
        except Exception as e:
            # Handle and return any errors as a JSON response
            return JsonResponse({"error": str(e)}, status=400)

    return render(request, "pages/prediction.html")
