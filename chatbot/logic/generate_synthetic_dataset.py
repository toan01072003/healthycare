import pandas as pd
import random

SYMPTOMS = [
    "fever", "cough", "headache", "fatigue", "shortness_of_breath",
    "sore_throat", "nausea", "chest_pain", "runny_nose", "loss_of_smell",
    "vomiting", "diarrhea", "dizziness", "abdominal_pain", "muscle_pain",
    "rash", "joint_pain", "sneezing", "eye_pain", "back_pain"
]

DISEASES = ["Flu", "COVID-19", "Migraine", "Asthma", "Food Poisoning", "Dengue", "Allergy", "Cold", "Gastroenteritis"]

data = []
for _ in range(1000):  # 1000 samples
    row = [random.randint(0, 1) for _ in SYMPTOMS]
    label = random.choice(DISEASES)
    data.append(row + [label])

df = pd.DataFrame(data, columns=SYMPTOMS + ["disease"])
df.to_csv("disease_symptoms_dataset.csv", index=False)
