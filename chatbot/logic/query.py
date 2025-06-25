# 📁 File: web_query_multi.py
import requests
from bs4 import BeautifulSoup
import re

HEADERS = {"User-Agent": "Mozilla/5.0"}

def clean_text(text):
    return re.sub(r'\[\d+\]', '', text).replace('\n', ' ').strip()

# 🧠 Wikipedia
def get_from_wikipedia(name):
    try:
        url = f"https://en.wikipedia.org/wiki/{name.replace(' ', '_')}"
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        desc = next(p.get_text() for p in soup.select("p") if len(p.get_text()) > 100)
        desc = clean_text(desc)
        return {"source": "Wikipedia", "description": desc}
    except:
        return None

# 🏥 MayoClinic
def get_from_mayo(name):
    try:
        search_url = f"https://www.mayoclinic.org/search/search-results?q={name}"
        r = requests.get(search_url, headers=HEADERS)
        soup = BeautifulSoup(r.text, "html.parser")
        link = soup.select_one(".results a")
        if not link:
            return None
        href = link['href']
        full_url = "https://www.mayoclinic.org" + href
        page = requests.get(full_url, headers=HEADERS)
        soup = BeautifulSoup(page.text, "html.parser")
        desc = soup.select_one("article p")
        return {
            "source": "MayoClinic",
            "description": clean_text(desc.get_text()) if desc else None
        }
    except:
        return None

# 💊 WebMD
def get_from_webmd(name):
    try:
        search_url = f"https://www.webmd.com/search/search_results/default.aspx?query={name}"
        r = requests.get(search_url, headers=HEADERS)
        soup = BeautifulSoup(r.text, "html.parser")
        link = soup.select_one("a.search-results-doc-link")
        if not link:
            return None
        page = requests.get(link['href'], headers=HEADERS)
        soup = BeautifulSoup(page.text, "html.parser")
        desc = soup.select_one("section p")
        return {
            "source": "WebMD",
            "description": clean_text(desc.get_text()) if desc else None
        }
    except:
        return None

# 🧬 MedlinePlus (NIH)
def get_from_medlineplus(name):
    try:
        search = requests.get(f"https://medlineplus.gov/search/?query={name}", headers=HEADERS)
        soup = BeautifulSoup(search.text, "html.parser")
        a_tag = soup.select_one("ul.search-results a")
        if not a_tag:
            return None
        href = "https://medlineplus.gov" + a_tag['href']
        page = requests.get(href, headers=HEADERS)
        soup = BeautifulSoup(page.text, "html.parser")
        desc = soup.select_one("div.section p")
        return {
            "source": "MedlinePlus",
            "description": clean_text(desc.get_text()) if desc else None
        }
    except:
        return None

# 🧾 Healthline
def get_from_healthline(name):
    try:
        url = f"https://www.healthline.com/search?q1={name.replace(' ', '+')}"
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text, "html.parser")
        first = soup.select_one("a.css-1dyz3hf")
        if not first:
            return None
        page = requests.get("https://www.healthline.com" + first['href'], headers=HEADERS)
        soup = BeautifulSoup(page.text, "html.parser")
        para = soup.select_one("section div p")
        return {
            "source": "Healthline",
            "description": clean_text(para.get_text()) if para else None
        }
    except:
        return None

# Tổng hợp tất cả nguồn
def get_disease_info_all_sources(disease_name):
    sources = [
        get_from_mayo,
        get_from_wikipedia,
        get_from_webmd,
        get_from_medlineplus,
        get_from_healthline,
    ]
    for source_func in sources:
        result = source_func(disease_name)
        if result and result.get("description"):
            return result
    return {"source": None, "description": None}
