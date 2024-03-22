import cv2
import numpy as np
from fastapi import FastAPI, BackgroundTasks,Form
from fastapi.responses import JSONResponse
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.vgg16 import preprocess_input
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Header
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

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

terminate_video_capture = False

# Function to store interview result in MongoDB
def store_interview_result(username: str, confidence_percentage: float, final_result: str):
    interview_result = {
        'username': username,
        'confidence_percentage': confidence_percentage,
        'final_result': final_result
    }
    collection.insert_one(interview_result)

# Modified video_capture function to include username and store result
def video_capture( username: str = Header(...)):
    global terminate_video_capture
    predicted_emotions = []

    # Capture video from webcam
    cap = cv2.VideoCapture(0)

    while not terminate_video_capture:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (300, 300))

        # Preprocess the frame and predict emotion
        predicted_emotion, max_probability = predict_emotion(frame)
        predicted_emotions.append(predicted_emotion)

    # Release video capture
    cap.release()

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
    store_interview_result(username, confidence_percentage, final_result)

@app.post("/analyze_emotion")
async def analyze_emotion(background_tasks: BackgroundTasks, username: str = Header(...)):
    global terminate_video_capture
    terminate_video_capture = False
    background_tasks.add_task(video_capture, username=username)
    return JSONResponse(content={"message": "Interview started."})

@app.post("/shutdown")
async def shutdown_server():
    global terminate_video_capture
    terminate_video_capture = True
    return JSONResponse(content={"message": "Interview Finished"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
