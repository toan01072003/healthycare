import pandas as pd

# Đọc file (update đường dẫn nếu cần)
df = pd.read_csv("C:/Users/Toan/Documents/LapTrinh/python/Disease and symptoms dataset.csv")

# Tách tên các triệu chứng (bỏ cột đầu là disease)
SYMPTOMS = df.columns.tolist()[1:]

sentences = []
labels = []

import random

PHRASES = [
    "I have",
    "I'm experiencing",
    "I'm suffering from",
    "My symptoms are",
    "I feel",
    "I've been having"
]

# ...

for idx, row in df.iterrows():
    present_symptoms = [s for s in SYMPTOMS if row[s] == 1 or row[s] == "1"]
    if not present_symptoms:
        continue
    prefix = random.choice(PHRASES)
    sentence = prefix + " " + ", ".join(present_symptoms) + "."
    sentences.append(sentence)
    labels.append(row["diseases"])


# Tạo DataFrame mới
processed = pd.DataFrame({
    "text": sentences,
    "label": labels
})

processed.to_csv("bert_dataset.csv", index=False)
print("✅ Dataset created: bert_dataset.csv")
