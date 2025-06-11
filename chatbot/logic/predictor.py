# chatbot/logic/predictor.py

import joblib

model = joblib.load("chatbot/logic/chatbot_model.pkl")
symptom_encoder = joblib.load("chatbot/logic/symptom_encoder.pkl")

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
