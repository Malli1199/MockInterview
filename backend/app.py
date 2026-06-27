import numpy as np
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from routers import evaluation

app = FastAPI(title="AI-Sentinel Core Multi-Modal Engine")

# Address SonarQube Security Vulnerabilities regarding Wildcard CORS with Credentials
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1", "http://localhost:5500", "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include the evaluation router explicitly so endpoints balance cleanly
app.include_router(evaluation.router)

# Initialize Modern Mediapipe Face Landmarker once globally to prevent memory leaks
base_options = python.BaseOptions(model_asset_path='face_landmarker.task')
options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    output_face_blendshapes=True,
    num_faces=1
)
face_detector = vision.FaceLandmarker.create_from_options(options)

# In-memory session logging tracking states
session_behavioral_flags: List[Dict] = []
session_start_time = time.time()

# Request schema for frontend authentication validation
class LoginRequest(BaseModel):
    registration_id: str
    password: str

# Expanded CBT Layout Question Banks
ROLE_QUESTION_BANKS = {
    "Software Engineer": [
        {"id": 1, "type": "DESCRIPTIVE", "question": "Explain the difference between a Convolutional Neural Network (CNN) and a Recurrent Neural Network (RNN) architecture."},
        {"id": 2, "type": "MCQ", "question": "Which data structure operates on a Last-In, First-Out (LIFO) basis?", "options": ["Queue", "Stack", "Linked List", "Binary Tree"], "answer": "Stack"},
        {"id": 3, "type": "MSQ", "question": "Select all languages that support primitive OOP structures natively:", "options": ["Python", "C++", "Java", "Pure HTML"], "answer": ["Python", "C++", "Java"]},
        {"id": 4, "type": "DESCRIPTIVE", "question": "What is the worst-case time complexity of searching an element inside a perfectly balanced Binary Search Tree (BST)?"},
        {"id": 5, "type": "DESCRIPTIVE", "question": "Explain how a deadlock condition occurs in multi-threaded software application spaces."}
    ],
    "AI / ML Engineer": [
        {"id": 1, "type": "DESCRIPTIVE", "question": "What is the primary role of an activation function in deep neural network nodes?"},
        {"id": 2, "type": "MCQ", "question": "Which optimization technique dynamically rescales learning rates per parameter?", "options": ["SGD", "Adam", "Momentum", "RMSprop"], "answer": "Adam"},
        {"id": 3, "type": "DESCRIPTIVE", "question": "What is the difference between L1 Regularization (Lasso) and L2 Regularization (Ridge) loss optimization profiles?"},
        {"id": 4, "type": "DESCRIPTIVE", "question": "Describe the phenomenon of exploding gradients and how Gradient Clipping mitigates it."},
        {"id": 5, "type": "DESCRIPTIVE", "question": "Explain the architecture and mechanical purpose of Multi-Head Attention mechanisms in Transformers."}
    ]
}

def analyze_student_behavior(image_bytes: bytes) -> Dict:
    nparr = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if frame is None:
        return {"status": "Error", "message": "Failed to decode frame bytes"}
        
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Convert OpenCV RGB array to the required MediaPipe Image format
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    results = face_detector.detect(mp_image)
    
    confidence_rate = 50.0
    attitude = "Distracted / Anxious"
    eye_gaze = "Looking Away"
    current_timestamp = round(time.time() - session_start_time, 1)
    gaze_deviation = 0.0

    # Process using the new Tasks API structural layer format
    if results.face_landmarks:
        landmarks = results.face_landmarks[0]
        
        # Extracted landmark indices matching the canonical face mesh profile
        left_pupil = landmarks[468]
        right_pupil = landmarks[473]
        head_center = landmarks[168]
        
        gaze_deviation = abs(((left_pupil.x + right_pupil.x) / 2) - head_center.x)
        
        if gaze_deviation < 0.025:
            eye_gaze = "Maintaining Direct Eye Contact"
            attitude = "Highly Focused, Attentive, and Professional"
            confidence_rate = 95.0
        elif gaze_deviation < 0.045:
            eye_gaze = "Intermittent/Drifting Eye Gaze"
            attitude = "Processing / Thinking About Response"
            confidence_rate = 75.0
        else:
            eye_gaze = "Frequent Shifting/Avoiding Focus"
            attitude = "Showing signs of Nervousness or High Anxiety"
            confidence_rate = 40.0
            
            session_behavioral_flags.append({
                "timestamp_seconds": current_timestamp,
                "event": "Distracted Eye Movement Spotted",
                "details": f"Gaze deviation index breached boundary limits with scale threshold metric {round(gaze_deviation, 4)}"
            })

        return {
            "status": "Success",
            "confidence_rate": confidence_rate,
            "behavioral_attitude": attitude,
            "eye_gaze_tracking": eye_gaze,
            "metric_deviation_delta": round(float(gaze_deviation), 5)
        }
        
    return {
        "status": "Face Not Found",
        "confidence_rate": 0.0,
        "behavioral_attitude": "Student completely out of camera bounds",
        "eye_gaze_tracking": "Unresolvable"
    }

# OPTIONS route for login preflight routing configurations
@app.options("/api/auth/login")
async def login_preflight():
    return {"success": True, "message": "Preflight routing configuration validated"}

# Process session tokens upon successful validation matching auth parameters
@app.post("/api/auth/login")
async def login(data: LoginRequest):
    if data.registration_id == "malli" and data.password == "malli1199":
        return {
            "success": True,
            "message": "Authentication verified cleanly",
            "token": "mock-sentinel-jwt-payload-xyz"
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid user credentials. Access Denied."
    )

@app.get("/api/questions/{role}")
async def get_role_questions(role: str):
    questions = ROLE_QUESTION_BANKS.get(role, ROLE_QUESTION_BANKS["Software Engineer"])
    return {"status": "Success", "role": role, "questions": questions}

# Enhanced to integrate CBT contextual structures tracking questions smoothly
@app.post("/api/evaluate-interview")
async def evaluate_interview_endpoint(
    role_selected: str = Form(...),
    text_response: str = Form(...),
    question_index: Optional[int] = Form(0),  # Accepts the question counter state directly
    audio_response: Optional[UploadFile] = File(None)
):
    text_length = len(text_response.strip())
    
    if text_length > 100:
        vocab_accuracy = 94
        speech_clarity = "Highly Articulate & Structured"
        detailed_feedback = f"Exceptional technical content clarity profile displayed for Question {question_index + 1}. Core algorithmic patterns described cleanly."
    elif text_length > 30:
        vocab_accuracy = 82
        speech_clarity = "Clear Delivery Mode"
        detailed_feedback = f"The user communicated requirements for Question {question_index + 1}, but could enhance structure by clarifying edge constraints."
    else:
        vocab_accuracy = 52
        speech_clarity = "Brief / Fragmented Execution"
        detailed_feedback = "The structural answer provided is minimal. Expand on foundational mechanics."

    # Shallow-copy the logs for this specific question evaluation submission
    compiled_report_alerts = list(session_behavioral_flags)
    session_behavioral_flags.clear()  # Flushes local cache cleanly for subsequent test items

    return {
        "status": "Success",
        "confidence_rate": vocab_accuracy,
        "behavioral_attitude": "Professional, Engaged, and Controlled" if len(compiled_report_alerts) < 3 else "High Visual Disregard Flags Triggered",
        "eye_gaze_tracking": "Stable Interface Tracking",
        "vocabulary_accuracy": vocab_accuracy,
        "speech_clarity": speech_clarity,
        "detailed_feedback": detailed_feedback,
        "behavioral_audit_flags": compiled_report_alerts
    }

@app.post("/api/analyze-behavior")
async def analyze_behavior_endpoint(file: UploadFile = File(...)):
    frame_bytes = await file.read()
    return analyze_student_behavior(frame_bytes)

@app.get("/api/health")
def system_health():
    return {"status": "AI Core Active", "port": 3000}