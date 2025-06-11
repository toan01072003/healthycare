# chatbot/logic/symptom_utils.py

def normalize_symptoms(user_input):
    keyword_map = {
        "high temperature": "fever",
        "temperature": "fever",
        "tired": "fatigue",
        "tiredness": "fatigue",
        "throwing up": "vomiting",
        "stomach ache": "abdominal pain",
        "upset stomach": "nausea",
        "can’t sleep": "insomnia",
        "dizzy": "dizziness",
        "hard to breathe": "shortness of breath",
        "tight chest": "chest tightness",
        # Add more mappings here...
    }

    cleaned = user_input.lower()
    for phrase, standard in keyword_map.items():
        cleaned = cleaned.replace(phrase, standard)

    symptoms = [s.strip() for s in cleaned.split(",") if s.strip()]
    return symptoms
