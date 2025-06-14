# chatbot/logic/predictor.py

import joblib
import os
from .dummy_objs import DummyModel, DummyEncoder

MODEL_PATH = "chatbot/logic/chatbot_model.pkl"
ENCODER_PATH = "chatbot/logic/symptom_encoder.pkl"

if os.path.exists(MODEL_PATH) and os.path.exists(ENCODER_PATH):
    model = joblib.load(MODEL_PATH)
    symptom_encoder = joblib.load(ENCODER_PATH)
else:
    model = DummyModel()
    symptom_encoder = DummyEncoder()

def predict_disease(symptom_list):
    cleaned = [s.strip().lower() for s in symptom_list]
    vector = symptom_encoder.transform([cleaned])
    probs = model.predict_proba(vector)[0]

    top_predictions = sorted(
        zip(model.classes_, probs), key=lambda x: x[1], reverse=True
    )

    # Chỉ chọn những bệnh có xác suất > 0
    result = [{"disease": d, "confidence": round(p * 100, 2)} for d, p in top_predictions if p > 0]
    return result[:5]  # giới hạn top 5 kết quả
