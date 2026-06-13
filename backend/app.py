import numpy as np
import cv2
import mediapipe as mp
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI - The core server gateway
app = FastAPI(title="AI-Sentinel Core Multi-Modal Engine")

# Configure CORS so your local dashboard.html can securely stream data to this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Mediapipe Face Mesh components for tracking behavior, eye gaze, and expressions
mp_face_mesh = mp.solutions.face_mesh

def analyze_student_behavior(image_bytes):
    """
    Evaluates raw frame bytes from the browser webcam. Tracks iris alignment, 
    facial posture stability, and computes an absolute behavioral confidence rate.
    """
    # Decode raw incoming browser image bytes into an OpenCV matrix array
    nparr = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if frame is None:
        return {"status": "Error", "message": "Failed to decode frame bytes"}

    # Setup the pre-trained Mediapipe machine learning model mesh
    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True, # Critical: Activates the high-precision 478 landmark iris tracking
        min_detection_confidence=0.5
    ) as face_mesh:
        
        # Convert BGR (OpenCV default color space) to RGB (Required by Mediapipe ML models)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)
        
        # Default baseline values if the student drops out of camera view
        confidence_rate = 50.0
        attitude = "Distracted / Anxious"
        eye_gaze = "Looking Away"

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            
            # --- MODEL ALGORITHM: EYE GAZE & FOCUS DEVIATION CALCULATION ---
            # Landmark 468 = Center of Left Pupil | Landmark 473 = Center of Right Pupil
            left_pupil = landmarks[468]
            right_pupil = landmarks[473]
            # Landmark 168 = The stable bone midpoint directly between eyebrows (Nasion)
            head_center = landmarks[168]
            
            # Compute the absolute horizontal pixel offset delta between pupils and head center
            gaze_deviation = abs(((left_pupil.x + right_pupil.x) / 2) - head_center.x)
            
            # --- REPORT LOGIC GENERATION MATRIX ---
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

@app.post("/api/analyze-behavior")
async def analyze_behavior_endpoint(file: UploadFile = File(...)):
    """
    Receives automated multi-modal frame payloads dispatched from dashboard.html,
    routes them into the machine learning engine, and feeds back the JSON report metrics.
    """
    frame_bytes = await file.read()
    report = analyze_student_behavior(frame_bytes)
    return report

@app.get("/api/health")
def system_health():
    return {"status": "AI Core Active", "port": 3000}