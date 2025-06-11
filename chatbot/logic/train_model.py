import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import MultiLabelBinarizer
import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "Disease and symptoms dataset.csv")

df = pd.read_csv(csv_path)
df.columns = df.columns.str.strip()
df.columns.values[0] = "Disease"  # 👈 Gán lại tên cột đầu tiên

# Loại bỏ bệnh nào không có triệu chứng
df = df.dropna()

# Lấy các cột triệu chứng
symptom_cols = df.columns[1:]
df["symptoms"] = df[symptom_cols].apply(lambda x: [col.strip().lower() for col, val in zip(symptom_cols, x) if val == 1], axis=1)

# Mã hoá
mlb = MultiLabelBinarizer()
X = mlb.fit_transform(df["symptoms"])
y = df["Disease"]

# Huấn luyện
clf = DecisionTreeClassifier()
clf.fit(X, y)

# Lưu mô hình
joblib.dump(clf, os.path.join(BASE_DIR, "chatbot_model.pkl"))
joblib.dump(mlb, os.path.join(BASE_DIR, "symptom_encoder.pkl"))

print("✅ Đã train xong và lưu mô hình.")
