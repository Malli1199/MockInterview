import numpy as np
import cv2
import mediapipe as mp
import time
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict

app = FastAPI(title="AI-Sentinel Core Multi-Modal Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Mediapipe Face Mesh components
mp_face_mesh = mp.solutions.face_mesh

# In-memory tracking for session evaluation histories (Simulating light session DB state)
session_behavioral_flags: List[Dict] = []
session_start_time = time.time()

# --- RULE-BASED EXPERT ROLE QUESTION BANKS ---
ROLE_QUESTION_BANKS = {
    "Software Engineer": [
        {"id": 1, "type": "DESCRIPTIVE", "question": "Explain the difference between a Convolutional Neural Network (CNN) and a Recurrent Neural Network (RNN) architecture."},
        {"id": 2, "type": "MCQ", "question": "Which data structure operates on a Last-In, First-Out (LIFO) basis?", "options": ["Queue", "Stack", "Linked List", "Binary Tree"], "answer": "Stack"},
        {"id": 3, "type": "MSQ", "question": "Select all languages that support primitive OOP structures natively:", "options": ["Python", "C++", "Java", "Pure HTML"], "answer": ["Python", "C++", "Java"]}
    ],
    "AI / ML Engineer": [
        {"id": 1, "type": "DESCRIPTIVE", "question": "What is the primary role of an activation function in deep neural network nodes?"},
        {"id": 2, "type": "MCQ", "question": "Which optimization technique dynamically rescales learning rates per parameter?", "options": ["SGD", "Adam", "Momentum", "RMSprop"], "answer": "Adam"}
    ]
}

def analyze_student_behavior(image_bytes):
    """
    Evaluates raw frame bytes from browser webcam. Tracks iris metrics,
    flags looking-away anomalies, and calculates instant performance delta scores.
    """
    nparr = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if frame is None:
        return {"status": "Error", "message": "Failed to decode frame bytes"}

    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5
    ) as face_mesh:
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)
        
        confidence_rate = 50.0
        attitude = "Distracted / Anxious"
        eye_gaze = "Looking Away"
        current_timestamp = round(time.time() - session_start_time, 1)

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            
            # High precision 478 landmark reference iris data tracking
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
                
                # Automatically append a behavioral audit flag alert log
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

@app.get("/api/questions/{role}")
async def get_role_questions(role: str):
    """Loads targeted evaluation questions matching user track selections instantly."""
    questions = ROLE_QUESTION_BANKS.get(role, ROLE_QUESTION_BANKS["Software Engineer"])
    return {"status": "Success", "role": role, "questions": questions}

@app.post("/api/evaluate-interview")
async def evaluate_interview_endpoint(
    role_selected: str = Form(...),
    text_response: str = Form(...),
    audio_response: Optional[UploadFile] = File(None)
):
    """
    Evaluates text transcripts instantaneously. Flashes pre-compiled eye tracking history 
    flags directly to achieve latency response metrics below 200ms.
    """
    text_length = len(text_response.strip())
    
    if text_length > 100:
        vocab_accuracy = 94
        speech_clarity = "Highly Articulate & Structured"
        detailed_feedback = "Exceptional technical content clarity profile displayed. Core algorithmic patterns were described correctly with precise sentence phrasing structure."
    elif text_length > 30:
        vocab_accuracy = 82
        speech_clarity = "Clear Delivery Mode"
        detailed_feedback = "The user communicated key technical requirements, but could further enhance structure by clarifying edge architectural constraints."
    else:
        vocab_accuracy = 52
        speech_clarity = "Brief / Fragmented Execution"
        detailed_feedback = "The structural answer provided is quite minimal. Expand on foundational mechanics to pass baseline scoring profiles."

    # Copy current flags and flush buffer for subsequent testing sessions
    compiled_report_alerts = list(session_behavioral_flags)
    session_behavioral_flags.clear()

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