from neo4j import GraphDatabase
import json
import os

KB_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base.json")
with open(KB_PATH, "r", encoding="utf-8") as f:
    knowledge = json.load(f)

uri = "bolt://127.0.0.1:7687"
auth = ("neo4j", "test12345")
  # thay bằng mật khẩu bạn đặt

driver = GraphDatabase.driver(uri, auth=auth)

def import_knowledge():
    with driver.session() as session:
        for disease, info in knowledge.items():
            session.run("MERGE (d:Disease {name: $name, description: $desc})", name=disease, desc=info.get("description"))

            for s in info.get("symptoms", []):
                session.run("MERGE (s:Symptom {name: $name})", name=s)
                session.run("""
                    MATCH (d:Disease {name: $disease}), (s:Symptom {name: $symptom})
                    MERGE (d)-[:HAS_SYMPTOM]->(s)
                """, disease=disease, symptom=s)

            for t in info.get("treatments", []):
                session.run("MERGE (t:Treatment {name: $name})", name=t)
                session.run("""
                    MATCH (d:Disease {name: $disease}), (t:Treatment {name: $treatment})
                    MERGE (d)-[:TREATED_BY]->(t)
                """, disease=disease, treatment=t)

            spec = info.get("specialist")
            if spec:
                session.run("MERGE (sp:Specialist {name: $name})", name=spec)
                session.run("""
                    MATCH (d:Disease {name: $disease}), (sp:Specialist {name: $specialist})
                    MERGE (d)-[:BELONGS_TO]->(sp)
                """, disease=disease, specialist=spec)

    print("✅ Đã import dữ liệu vào Neo4j")

if __name__ == "__main__":
    import_knowledge()
