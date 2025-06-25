from neo4j import GraphDatabase
import joblib

# === Cấu hình ===
uri = "bolt://localhost:7687"
auth = ("neo4j", "test12345")
ENCODER_PATH = "c:/Users/Toan/Documents/LapTrinh/python/smartphc/chatbot/logic/label_encoder.pkl"

# === Load label từ mô hình BERT ===
label_encoder = joblib.load(ENCODER_PATH)
print("✅ Loại đối tượng:", type(label_encoder))  # Phải là LabelEncoder
bert_labels = set(label_encoder.classes_)
print("🧠 Số bệnh từ mô hình:", len(bert_labels))

# === Kết nối Neo4j ===
driver = GraphDatabase.driver(uri, auth=auth)

# === Truy vấn Neo4j để lấy các tên bệnh đã có ===
neo4j_diseases = set()
with driver.session() as session:
    result = session.run("MATCH (d:Disease) RETURN toLower(d.name) AS name")
    for r in result:
        neo4j_diseases.add(r["name"])

print(f"📦 Đã có trong Neo4j: {len(neo4j_diseases)} bệnh")

# === Tìm các bệnh còn thiếu ===
missing_diseases = [d for d in bert_labels if d.lower() not in neo4j_diseases]
print(f"⚠️ Còn thiếu {len(missing_diseases)} bệnh → sẽ được thêm mới.")

# === Thêm vào Neo4j ===
with driver.session() as session:
    for disease in missing_diseases:
        session.run("""
        MERGE (d:Disease {name: $name})
        SET d.description = "Chưa có mô tả.",
            d.id = $id
        """, name=disease, id=disease.replace(" ", "_"))

print("✅ Đã thêm toàn bộ bệnh còn thiếu vào Neo4j.")
