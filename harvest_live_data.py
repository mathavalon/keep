#!/usr/bin/env python3
"""
Coletor Ao Vivo Keep (OpenSEO + CrawlSEO):
1. Busca sugestões reais do Google Autocomplete Brasil (100% gratuito) para Adfert e Intrivia.
2. Busca o conteúdo HTML completo via WP-JSON (content.rendered) para calcular métricas reais
   de CrawlSEO/OpenSEO por artigo: contagem de palavras, links internos, links para página de produto,
   imagens sem atributo alt, H2/H3, intenção de busca e nota On-Page (0-100).
3. Mede TTFB e tamanho de payload das páginas principais (/artigos/).
"""
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) KeepSEOBot/2.0"}


def fetch_json(url: str):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8", errors="ignore"))


def measure_page_vitals(url: str):
    t0 = time.time()
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        first_byte = time.time() - t0
        body = r.read()
        total_time = time.time() - t0
        status = r.status
        headers = dict(r.info())
    html = body.decode("utf-8", errors="ignore")
    imgs = re.findall(r"<img\s+[^>]*>", html, re.I)
    imgs_no_alt = sum(1 for img in imgs if not re.search(r'alt=["\'][^"\']+["\']', img, re.I))
    scripts = len(re.findall(r"<script", html, re.I))
    stylesheets = len(re.findall(r"<link[^>]*rel=[\"']stylesheet[\"']", html, re.I))
    return {
        "url": url,
        "status_code": status,
        "ttfb_ms": round(first_byte * 1000),
        "total_load_ms": round(total_time * 1000),
        "html_size_kb": round(len(body) / 1024, 1),
        "cf_cache": headers.get("cf-cache-status", headers.get("CF-Cache-Status", "DYNAMIC")),
        "total_images": len(imgs),
        "images_missing_alt": imgs_no_alt,
        "scripts_count": scripts,
        "stylesheets_count": stylesheets,
    }


def harvest_autocomplete(seeds: list):
    results = []
    for seed_obj in seeds:
        q = seed_obj["seed"]
        pillar = seed_obj["pillar"]
        intent = seed_obj["intent"]
        url = f"https://suggestqueries.google.com/complete/search?client=firefox&hl=pt-BR&gl=BR&q={urllib.parse.quote(q)}"
        try:
            data = fetch_json(url)
            suggestions = data[1] if isinstance(data, list) and len(data) > 1 else []
        except Exception:
            suggestions = []
        results.append({
            "seed": q,
            "pillar": pillar,
            "intent": intent,
            "suggestions": suggestions[:8],
        })
    return results


def main():
    adfert_seeds = [
        {"seed": "inibidor de urease", "pillar": "1. Aditivos", "intent": "Fundo / Produto"},
        {"seed": "aditivo para fertilizante", "pillar": "1. Aditivos", "intent": "Fundo / Produto"},
        {"seed": "ureia protegida", "pillar": "2. Fertilizantes", "intent": "Meio / Comercial"},
        {"seed": "fixação de fósforo no solo", "pillar": "2. Fertilizantes", "intent": "Topo / Informacional"},
        {"seed": "empedramento de fertilizantes", "pillar": "1. Aditivos", "intent": "Meio / Comercial"},
        {"seed": "barter soja fertilizantes", "pillar": "3. Agro", "intent": "Meio / Comercial"},
        {"seed": "mercado de fertilizantes 2026", "pillar": "4. Agro Global", "intent": "Topo / Informacional"},
        {"seed": "el niño safra soja", "pillar": "5. Clima e Bioma", "intent": "Topo / Informacional"},
    ]
    intrivia_seeds = [
        {"seed": "estresse térmico na soja", "pillar": "1. Aditivos", "intent": "Meio / Comercial"},
        {"seed": "protetor solar foliar", "pillar": "1. Aditivos", "intent": "Fundo / Produto"},
        {"seed": "deficiência de enxofre na soja", "pillar": "2. Fertilizantes", "intent": "Meio / Comercial"},
        {"seed": "pegamento de florada café", "pillar": "3. Agro", "intent": "Meio / Comercial"},
        {"seed": "adubação foliar soja", "pillar": "2. Fertilizantes", "intent": "Fundo / Produto"},
        {"seed": "calor extremo lavoura", "pillar": "5. Clima e Bioma", "intent": "Topo / Informacional"},
    ]

    out = {
        "adfert_autocomplete": harvest_autocomplete(adfert_seeds),
        "intrivia_autocomplete": harvest_autocomplete(intrivia_seeds),
        "adfert_vitals": measure_page_vitals("https://adfert.com.br/artigos/"),
        "intrivia_vitals": measure_page_vitals("https://intrivia.com.br/artigos/"),
        "adfert_content": {},
        "intrivia_content": {},
    }

    # Fetch full content for PT posts (Adfert page 1 & 2, Intrivia page 1)
    for page in [1, 2, 3]:
        try:
            posts = fetch_json(f"https://adfert.com.br/wp-json/wp/v2/posts?per_page=50&page={page}&_fields=id,content")
            if isinstance(posts, list):
                for p in posts:
                    out["adfert_content"][str(p["id"])] = p.get("content", {}).get("rendered", "")
        except Exception:
            pass

    try:
        iposts = fetch_json("https://intrivia.com.br/wp-json/wp/v2/posts?per_page=50&_fields=id,content")
        if isinstance(iposts, list):
            for p in iposts:
                out["intrivia_content"][str(p["id"])] = p.get("content", {}).get("rendered", "")
    except Exception:
        pass

    Path("/tmp/keep_harvest.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print("Harvest complete! Adfert content count:", len(out["adfert_content"]), "Intrivia content count:", len(out["intrivia_content"]))


if __name__ == "__main__":
    main()

