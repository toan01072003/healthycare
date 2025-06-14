import pronto
import json

# Tải từ OBO Foundry hoặc dùng bản đã tải
OBO_URL = "http://purl.obolibrary.org/obo/doid.obo"
ONTO_FILE = "doid.obo"

def download_obo():
    import requests
    r = requests.get(OBO_URL)
    with open(ONTO_FILE, "wb") as f:
        f.write(r.content)
    print("✅ Downloaded doid.obo")

def parse_disease_ontology():
    print("📖 Đang đọc ontology...")
    ontology = pronto.Ontology(ONTO_FILE)
    results = []

    for term in ontology.terms():
        if not term.name or term.obsolete:
            continue

        results.append({
            "id": term.id,
            "name": term.name,
            "definition": term.definition if term.definition else "",
            "synonyms": [s.description for s in term.synonyms],
            "parents": [{"id": p.id, "name": p.name} for p in term.superclasses(with_self=False)],
            "children": [{"id": c.id, "name": c.name} for c in term.subclasses(with_self=False)]
        })

    with open("do_all_terms.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"✅ Đã lưu {len(results)} diseases vào do_all_terms.json")

if __name__ == "__main__":
    download_obo()
    parse_disease_ontology()
