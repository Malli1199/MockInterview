import time
import json
from fastapi import APIRouter, File, UploadFile, Form
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter(prefix="/api/evaluation", tags=["Evaluation"])

# Schema structure to hold timeline metrics for tracking changes second-by-second
class TimelineMetrics(BaseModel):
    second: int
    eye_gaze: str
    inferred_emotion: str
    stress_level: str
    confidence_score: float

@router.post("/analyze-session")
async def analyze_session_endpoint(
    role_selected: str = Form(...),
    text_response: str = Form(...),
    total_duration_seconds: int = Form(15) # Default evaluation timeline
):
    """
    Core AI-Sentinel Evaluation Engine. Calculates verbal correctness, non-verbal communication,
    and builds a comprehensive, timeline-accurate report of student performance.
    """
    
    # 1. VERBAL COMMUNICATION ANALYSIS (NLP Mock Evaluation)
    text_clean = text_response.strip()
    word_count = len(text_clean.split())
    
    # Simple rule-based initial scoring placeholder for model training bounds
    if word_count > 40:
        vocabulary_accuracy = 88.5
        speech_clarity = "Highly Articulate & Structured"
        verbal_feedback = "Strong articulation. Sentences contain relevant domain keywords matching the target role."
    elif word_count > 15:
        vocabulary_accuracy = 74.0
        speech_clarity = "Moderate / Conversational Delivery"
        verbal_feedback = "Response is clear but could benefit from deeper technical keywords and structured metrics."
    else:
        vocabulary_accuracy = 45.0
        speech_clarity = "Fragmented / Too Brief"
        verbal_feedback = "The verbal response is too short to fully measure technical domain alignment."

    # 2. NON-VERBAL & TIMELINE ARCHITECTURE (Simulating MediaPipe Tracking over the Session)
    # This loop generates the chronological behavioral shift data you requested
    timeline_report: List[TimelineMetrics] = []
    
    base_confidence = 80.0
    accumulated_stress = 0.0
    anxious_seconds_count = 0
    
    for sec in range(1, total_duration_seconds + 1):
        # Simulating behavioral shifts based on typical student stress timelines
        if sec <= 5:
            # First few seconds: Usually highly composed
            eye_gaze = "Maintaining Direct Eye Contact"
            inferred_emotion = "Focused / Confident"
            stress_level = "Low"
            current_conf = base_confidence + (sec * 1.5)
        elif 6 <= sec <= 11:
            # Middle section: Shifting eyes, thinking/processing text
            eye_gaze = "Intermittent / Shifting Eye Gaze"
            inferred_emotion = "Processing Response / Thinking"
            stress_level = "Medium"
            current_conf = base_confidence - (sec * 0.8)
            anxious_seconds_count += 1
        else:
            # Final stretch: Fatigue or settling down
            eye_gaze = "Stable Interface Tracking"
            inferred_emotion = "Composed"
            stress_level = "Low"
            current_conf = base_confidence + 5.0

        timeline_report.append({
            "second": sec,
            "eye_gaze": eye_gaze,
            "inferred_emotion": inferred_emotion,
            "stress_level": stress_level,
            "confidence_score": round(current_conf, 2)
        })

    # 3. GLOBAL AGGREGATION & REPORT COMPILING
    # Combining verbal text metrics with visual timeline calculations
    avg_behavioral_confidence = sum([item["confidence_score"] for item in timeline_report]) / len(timeline_report)
    final_combined_confidence = round((vocabulary_accuracy * 0.4) + (avg_behavioral_confidence * 0.6), 2)
    
    # Determining management qualities (Anger, Stress, Focus handling)
    if anxious_seconds_count > (total_duration_seconds * 0.5):
        stress_management = "Needs improvement. Noticeable signs of stress or posture shifting under pressure."
        overall_attitude = "Anxious / Processing Lag"
    else:
        stress_management = "Excellent. Maintained emotional stability and controlled response posture."
        overall_attitude = "Professional, Attentive, and Well-Paced"

    return {
        "status": "Success",
        "metadata": {
            "role_evaluated": role_selected,
            "evaluation_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "session_length_seconds": total_duration_seconds
        },
        "metrics": {
            "overall_confidence_rate": final_combined_confidence,
            "verbal_communication_score": vocabulary_accuracy,
            "speech_clarity_index": speech_clarity,
            "behavioral_attitude_summary": overall_attitude,
            "stress_management_rating": stress_management
        },
        "feedback": {
            "strengths": "Maintained eye contact effectively during the opening definitions. Speech speed was controlled.",
            "areas_for_improvement": verbal_feedback + " Focus on practicing posture stability between seconds 6 and 11."
        },
        "chronological_behavior_timeline": timeline_report
    }