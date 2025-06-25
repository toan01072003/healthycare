from neo4j import GraphDatabase
import json
from pathlib import Path
from tqdm import tqdm

ONTOLOGY_PATH = Path("C:/Users/Toan/Documents/LapTrinh/do_all_terms.json")
with open(ONTOLOGY_PATH, "r", encoding="utf-8") as f:
    all_data = json.load(f)

BATCH_SIZE = 500
uri = "bolt://localhost:7687"
auth = ("neo4j", "test12345")
driver = GraphDatabase.driver(uri, auth=auth)

def chunked(data, size):
    for i in range(0, len(data), size):
        yield data[i:i+size]

def bulk_import():
    with driver.session() as session:
        for batch in tqdm(chunked(all_data, BATCH_SIZE), total=(len(all_data)+BATCH_SIZE-1)//BATCH_SIZE, desc="🚀 Importing"):
            diseases, synonyms, parents, children = [], [], [], []

            for d in batch:
                diseases.append({"id": d["id"], "name": d["name"], "definition": d["definition"]})
                for s in d.get("synonyms", []):
                    synonyms.append({"did": d["id"], "syn": s})
                for p in d.get("parents", []):
                    parents.append({"src": d["id"], "pid": p["id"], "pname": p["name"]})
                for c in d.get("children", []):
                    children.append({"cid": c["id"], "cname": c["name"], "dst": d["id"]})

            session.run("""
            UNWIND $diseases AS d
            MERGE (x:Disease {id: d.id})
            SET x.name = d.name, x.definition = d.definition
            """, diseases=diseases)

            session.run("""
            UNWIND $synonyms AS row
            MERGE (s:Synonym {name: row.syn})
            WITH s, row
            MATCH (d:Disease {id: row.did})
            MERGE (d)-[:HAS_SYNONYM]->(s)
            """, synonyms=synonyms)

            session.run("""
            UNWIND $parents AS rel
            MERGE (p:Disease {id: rel.pid})
            SET p.name = rel.pname
            WITH p, rel
            MATCH (d:Disease {id: rel.src})
            MERGE (d)-[:IS_A]->(p)
            """, parents=parents)

            session.run("""
            UNWIND $children AS rel
            MERGE (c:Disease {id: rel.cid})
            SET c.name = rel.cname
            WITH c, rel
            MATCH (d:Disease {id: rel.dst})
            MERGE (c)-[:IS_A]->(d)
            """, children=children)

    print("✅ DONE: Imported with UNWIND")

if __name__ == "__main__":
    bulk_import()
