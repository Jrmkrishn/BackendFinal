import numpy as np
import cv2
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.vgg16 import preprocess_input
from pymongo import MongoClient

# Load the model
model = load_model('facial_emotion_recognition_model.h5')

# Define emotions dictionary
emotions = {0: 'neutral', 1: 'confident', 2: 'unconfident'}

# Function to preprocess frame
def preprocess_frame(frame):
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (48, 48))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img

# Function to predict emotion
def predict_emotion(frame):
    img = preprocess_frame(frame)
    prediction = model.predict(img)
    predicted_class = np.argmax(prediction)
    max_probability = np.max(prediction)
    if max_probability < 0.3:
        return 'neutral'
    else:
        return emotions[predicted_class], max_probability

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['emotion_results']
collection = db['interview_results']

# Capture video from webcam
cap = cv2.VideoCapture(0)
predicted_emotions = []

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (300, 300))

    # Display captured frame
    cv2.imshow('Webcam', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Preprocess the frame and predict emotion
    predicted_emotion, max_probability = predict_emotion(frame)
    predicted_emotions.append(predicted_emotion)

# Release video capture and close OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Calculate confidence metric
confident_count = sum(1 for emotion in predicted_emotions if emotion == 'confident')
total_emotions = len(predicted_emotions)
confidence_percentage = (confident_count / total_emotions) * 100

# Provide final determination
if confidence_percentage >= 70:
    final_result = "The interviewee is confident."
else:
    final_result = "The interviewee is not confident."

# Store final determination in MongoDB
interview_result = {
    'confidence_percentage': confidence_percentage,
    'final_result': final_result
}
collection.insert_one(interview_result)
