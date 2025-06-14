import json
import os

KB_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base.json")

with open(KB_PATH, "r", encoding="utf-8") as f:
    KB = json.load(f)

def get_disease_info(disease_name):
    info = KB.get(disease_name)
    if not info:
        return None
    return {
        "description": info.get("description", "Không có mô tả."),
        "specialist": info.get("specialist", "Không rõ chuyên khoa."),
        "treatments": info.get("treatments", []),
        "symptoms": info.get("symptoms", [])
    }
