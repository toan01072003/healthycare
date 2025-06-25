import wikipedia
from neo4j import GraphDatabase

# === Neo4j config ===
uri = "bolt://localhost:7687"
auth = ("neo4j", "test12345")
driver = GraphDatabase.driver(uri, auth=auth)

# === Lấy danh sách các bệnh chưa có mô tả ===
def get_diseases_without_description():
    with driver.session() as session:
        result = session.run("""
        MATCH (d:Disease)
        WHERE d.description IS NULL OR d.description = "" OR d.description = "Chưa có mô tả."
        RETURN d.name AS name
        """)
        return [record["name"] for record in result]

# === Cập nhật mô tả cho từng bệnh ===
def update_description_in_neo4j(disease_name, description):
    with driver.session() as session:
        session.run("""
        MATCH (d:Disease {name: $name})
        SET d.description = $desc
        """, name=disease_name, desc=description)

# === Main ===
def main():
    diseases = get_diseases_without_description()
    print(f"📋 Đang cập nhật mô tả cho {len(diseases)} bệnh...")

    for name in diseases:
        try:
            summary = wikipedia.summary(name, sentences=2, auto_suggest=False)
            update_description_in_neo4j(name, summary)
            print(f"✅ {name}: Đã cập nhật mô tả.")
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"⚠️ {name}: Có nhiều kết quả. Bỏ qua.")
        except wikipedia.exceptions.PageError:
            print(f"❌ {name}: Không tìm thấy trang.")
        except Exception as e:
            print(f"❌ {name}: Lỗi không xác định: {e}")

    print("🎉 Hoàn tất cập nhật mô tả.")

if __name__ == "__main__":
    main()
