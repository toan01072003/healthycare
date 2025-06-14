from neo4j import GraphDatabase
import json
import os

# File chứa ontology dạng list các bệnh
ONTOLOGY_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base.json")

with open(ONTOLOGY_PATH, "r", encoding="utf-8") as f:
    disease_terms = json.load(f)

uri = "bolt://127.0.0.1:7687"
auth = ("neo4j", "test12345")  # thay bằng mật khẩu thật

driver = GraphDatabase.driver(uri, auth=auth)

def import_doid_data():
    with driver.session() as session:
        for disease in disease_terms:
            session.run("""
                MERGE (d:Disease {id: $id})
                SET d.name = $name, d.definition = $definition
            """, id=disease["id"], name=disease["name"], definition=disease["definition"])

            for syn in disease.get("synonyms", []):
                session.run("""
                    MERGE (s:Synonym {name: $syn})
                    WITH s
                    MATCH (d:Disease {id: $d_id})
                    MERGE (d)-[:HAS_SYNONYM]->(s)
                """, syn=syn, d_id=disease["id"])

            for parent in disease.get("parents", []):
                session.run("""
                    MERGE (p:Disease {id: $p_id})
                    SET p.name = $p_name
                    WITH p
                    MATCH (d:Disease {id: $d_id})
                    MERGE (d)-[:IS_A]->(p)
                """, p_id=parent["id"], p_name=parent["name"], d_id=disease["id"])

            for child in disease.get("children", []):
                session.run("""
                    MERGE (c:Disease {id: $c_id})
                    SET c.name = $c_name
                    WITH c
                    MATCH (d:Disease {id: $d_id})
                    MERGE (c)-[:IS_A]->(d)
                """, c_id=child["id"], c_name=child["name"], d_id=disease["id"])

    print("✅ Đã import toàn bộ dữ liệu DOID vào Neo4j")

if __name__ == "__main__":
    import_doid_data()
