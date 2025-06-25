from neo4j import GraphDatabase
import os

# 🧠 Cấu hình Neo4j (đổi mật khẩu nếu cần)
uri = "bolt://localhost:7687"
auth = ("neo4j", "test12345")

driver = GraphDatabase.driver(uri, auth=auth)

def get_disease_info_neo4j(disease_name):
    with driver.session() as session:
        result = session.run("""
            MATCH (d:Disease)
            WHERE toLower(d.name) = toLower($name)
               OR EXISTS {
                   MATCH (d)-[:HAS_SYNONYM]->(s:Synonym)
                   WHERE toLower(s.name) = toLower($name)
               }
            OPTIONAL MATCH (d)-[:TREATED_WITH]->(t:Treatment)
            OPTIONAL MATCH (d)-[:TREATED_BY]->(s:Specialist)
            RETURN d.definition AS description,
                   COLLECT(DISTINCT t.name) AS treatments,
                   s.name AS specialist
            LIMIT 1
        """, name=disease_name)

        record = result.single()
        if not record:
            return None

        return {
            "description": record["description"] or "Không có mô tả.",
            "treatments": record["treatments"] or [],
            "specialist": record["specialist"] or "Chưa rõ"
        }
