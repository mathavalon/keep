#!/usr/bin/env python3
"""
SEO-GEO Lab CLI & Real-Time Indexer
Permite consultar a base local (SQLite/JSON), filtrar pelos 6 temas,
sincronizar manchetes reais via Google News RSS (--sync-live) e auditar URLs.
"""
import argparse
import json
import re
import sqlite3
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "seo_geo_agro.db"
KB_PATH = BASE_DIR / "data" / "knowledge_base.json"

LIVE_QUERIES = {
    "1. Aditivos": "aditivos fertilizantes OR inibidor urease OR bioinsumos solo",
    "2. Fertilizantes": "mercado fertilizantes ureia fosfato MAP ANDA Brasil",
    "3. Agro": "agronegocio safra soja milho safrinha barter Brasil",
    "4. Agro Global": "fertilizantes global exportacao graos China India EUA",
    "5. Clima e Bioma": "El Nino La Nina clima safra Cerrado Amazonia chuva",
    "6. Complementares & Entretenimento": "inovacao agrotech carreira agronegocio sustentabilidade campo",
}


def sync_live_news():
    kb = json.loads(KB_PATH.read_text(encoding="utf-8"))
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS live_headlines (theme TEXT, title TEXT, link TEXT, pub_date TEXT, source TEXT)")
    cur.execute("DELETE FROM live_headlines")

    for ins in kb["realtime_insights"]:
        theme = ins["theme"]
        q = urllib.parse.quote(LIVE_QUERIES.get(theme, "agronegocio fertilizantes"))
        rss_url = f"https://news.google.com/rss/search?q={q}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
        headlines = []
        try:
            req = urllib.request.Request(rss_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                xml_data = resp.read()
            root = ET.fromstring(xml_data)
            for item in root.findall(".//item")[:3]:
                title = item.findtext("title", "")
                link = item.findtext("link", "")
                pub_date = item.findtext("pubDate", "")[:16]
                source_el = item.find("source")
                source = source_el.text if source_el is not None else "Google News"
                headlines.append({"title": title, "link": link, "pub_date": pub_date, "source": source})
                cur.execute("INSERT INTO live_headlines VALUES (?, ?, ?, ?, ?)", (theme, title, link, pub_date, source))
        except Exception as e:
            print(f"[Aviso] Falha ao buscar RSS de {theme}: {e}")
        ins["live_headlines"] = headlines

    kb["generated_at"] = datetime.now().isoformat()
    KB_PATH.write_text(json.dumps(kb, ensure_ascii=False, indent=2), encoding="utf-8")
    conn.commit()
    conn.close()
    print(f"[OK] Feed ao vivo atualizado em {kb['generated_at']}")


def list_stats():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    print("\n=== ESTATÍSTICAS DA BASE SEO-GEO LAB ===")
    cur.execute("SELECT lang, COUNT(*) FROM articles GROUP BY lang")
    for lang, count in cur.fetchall():
        print(f"  Idioma [{lang.upper()}]: {count} artigos indexados")
    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SEO-GEO Lab CLI")
    parser.add_argument("--stats", action="store_true", help="Exibe estatísticas da base")
    parser.add_argument("--sync-live", action="store_true", help="Busca manchetes em tempo real via RSS para os 6 temas")
    args = parser.parse_args()

    if args.sync_live:
        sync_live_news()
    else:
        list_stats()
