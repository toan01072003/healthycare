# 📁 File: save_knowledge_base.py
import json
import time
from pathlib import Path
from tqdm import tqdm
from web_query_multi import get_disease_info_all_sources

DISEASE_LIST = ["Migraine", "Flu", "Asthma", "Hypertension", "Diabetes"]  # hoặc lấy từ ontology

OUTPUT_PATH = Path("knowledge_base.json")
knowledge = {}

for disease in tqdm(DISEASE_LIST, desc="🔍 Enriching diseases"):
    info = get_disease_info_all_sources(disease)
    knowledge[disease] = {
        "description": info.get("description"),
        "symptoms": [],
        "treatments": [],
        "specialist": None,
        "source": info.get("source")
    }
    time.sleep(1.0)  # tránh bị block

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(knowledge, f, indent=2, ensure_ascii=False)

print("✅ Saved to knowledge_base.json")
