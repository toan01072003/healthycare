# chatbot/logic/neo4j_utils.py

from neo4j import GraphDatabase

# Cấu hình kết nối đến Neo4j
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "test123"  # Đổi nếu bạn đặt khác

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def get_disease_info_neo4j(disease_name):
    """
    Truy vấn mô tả, triệu chứng, chuyên khoa, hướng điều trị từ đồ thị Neo4j.
    """
    with driver.session() as session:
        result = session.run("""
            MATCH (d:Disease {name: $name})
            OPTIONAL MATCH (d)-[:HAS_SYMPTOM]->(s:Symptom)
            OPTIONAL MATCH (d)-[:TREATED_BY]->(t:Treatment)
            OPTIONAL MATCH (d)-[:BELONGS_TO]->(sp:Specialist)
            RETURN d.description AS description,
                   collect(DISTINCT s.name) AS symptoms,
                   collect(DISTINCT t.name) AS treatments,
                   sp.name AS specialist
        """, name=disease_name)

        record = result.single()
        if not record:
            return None

        return {
            "description": record["description"],
            "symptoms": record["symptoms"],
            "treatments": record["treatments"],
            "specialist": record["specialist"]
        }

def test_connection():
    with driver.session() as session:
        result = session.run("MATCH (n) RETURN count(n) AS total_nodes")
        count = result.single()["total_nodes"]
        print(f"✅ Connected to Neo4j. Total nodes: {count}")
