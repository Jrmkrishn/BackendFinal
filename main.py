import numpy as np
import cv2
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.vgg16 import preprocess_input


model = load_model('facial_emotion_recognition_model.h5')  # Update with your model path

emotions = {0: 'neutral', 1: 'confident', 2: 'unconfident'}  # Assuming 0 is for neutral, 1 for confident, and 2 for unconfident



def predict_emotion(frame):
    img = preprocess_frame(frame)
    prediction = model.predict(img)
    predicted_class = np.argmax(prediction)
    max_probability = np.max(prediction)
    if max_probability < 0.3:  # Check if max probability is less than 0.3
        return 'neutral'
    else:
        return emotions[predicted_class], max_probability

def preprocess_frame(frame):
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (48, 48))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img

cap = cv2.VideoCapture(0)

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
    
    
    if predicted_emotion == 'neutral':
        print("Predicted Emotion: Neutral")
    else:
        print(f"Predicted Emotion: {predicted_emotion}, Probability: {max_probability:.2f}")

cap.release()
cv2.destroyAllWindows()