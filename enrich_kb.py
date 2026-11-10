#!/usr/bin/env python3
import json
import re
import sqlite3
from pathlib import Path

base_dir = Path(__file__).resolve().parent
kb = json.loads((base_dir / "data" / "knowledge_base.json").read_text(encoding="utf-8"))
harvest = json.loads(Path("/tmp/keep_harvest.json").read_text(encoding="utf-8"))


def analyze_article_html(a, html_body, domain):
    text = re.sub(r"<[^>]+>", " ", html_body)
    words = [w for w in text.split() if w.strip()]
    word_count = len(words)
    h2s = re.findall(r"<h2[^>]*>(.*?)</h2>", html_body, re.I | re.S)
    h3s = re.findall(r"<h3[^>]*>(.*?)</h3>", html_body, re.I | re.S)
    links = re.findall(r'href=["\']([^"\']+)["\']', html_body, re.I)
    internal_links = [l for l in links if domain in l or l.startswith("/")]
    product_links = [
        l
        for l in internal_links
        if any(k in l.lower() for k in ["solucoes", "produto", "fale-conosco", "contato", "uremax", "phosprotec", "coatmax", "protec"])
    ]
    imgs = re.findall(r"<img\s+[^>]*>", html_body, re.I)
    imgs_no_alt = sum(1 for img in imgs if not re.search(r'alt=["\'][^"\']+["\']', img, re.I))

    full_txt = (a["title"] + " " + a["excerpt"] + " " + text[:800]).lower()
    if any(k in full_txt for k in ["uremax", "phosprotec", "coatmax", "protec foli", "anticaking", "antidusting", "linha de inibidores", "soluções adfert", "nossas soluções"]):
        intent = "Fundo / Produto"
    elif any(k in full_txt for k in ["eficiência", "manejo", "como aumentar", "proteger seu investimento", "barter", "planejar a compra", "deficiência de enxofre", "calor extremo", "chuva em excesso"]):
        intent = "Meio / Intenção"
    else:
        intent = "Topo / Visitas"

    score = 55
    if word_count >= 500:
        score += 15
    elif word_count >= 300:
        score += 10
    if len(h2s) >= 2:
        score += 10
    if len(internal_links) >= 1:
        score += 8
    if len(product_links) >= 1:
        score += 7
    if imgs_no_alt == 0:
        score += 5
    if any("CRÍTICO: Artigo herdado" in an for an in a.get("seo_anomalies", [])):
        score -= 25

    a["crawl_metrics"] = {
        "word_count": word_count,
        "h2_count": len(h2s),
        "h3_count": len(h3s),
        "internal_links": len(internal_links),
        "product_links": len(product_links),
        "images_count": len(imgs),
        "images_missing_alt": imgs_no_alt,
        "title_len": len(a["title"]),
        "onpage_score": max(15, min(95, score)),
        "intent": intent,
    }
    if len(product_links) == 0 and a["lang"] == "pt":
        msg = "Sem link interno para /nossas-solucoes/ (artigo órfão de conversão)"
        if msg not in a["seo_anomalies"]:
            a["seo_anomalies"].append(msg)


for a in kb["brands"]["adfert"]["articles"]:
    body = harvest["adfert_content"].get(str(a["id"]), "")
    analyze_article_html(a, body, "adfert.com.br")

for a in kb["brands"]["intrivia"]["articles"]:
    body = harvest["intrivia_content"].get(str(a["id"]), "")
    analyze_article_html(a, body, "intrivia.com.br")

kb["brands"]["adfert"]["ai_prompts"] = [
    {
        "prompt": "Qual o melhor inibidor de urease (NBPT) e aditivo para evitar volatilização da ureia no Brasil?",
        "pillar": "1. Aditivos",
        "intent": "Fundo / Produto",
        "status": "Cobertura Parcial",
        "detail": "O artigo de 30/10/2026 cita a Linha de Inibidores Adfert, mas falta Schema Product (Uremax NBPT/Plus/Coat/Pro) e tabela comparativa direta para IAs citarem.",
        "action": "Injetar JSON-LD Product + tabela de redução de perdas de NH3.",
    },
    {
        "prompt": "Como reduzir a fixação de fósforo no solo do Cerrado e aumentar a eficiência do MAP/DAP?",
        "pillar": "2. Fertilizantes",
        "intent": "Meio / Intenção",
        "status": "Citado / Coberto",
        "detail": "Coberto pelos artigos de 01/09/2026 e 17/09/2026 sobre eficiência do fósforo e PhosProtec.",
        "action": "Adicionar link interno direto para a ficha técnica do PhosProtec.",
    },
    {
        "prompt": "Como evitar o empedramento (caking) e geração de pó (dusting) no armazenamento de fertilizantes granulados?",
        "pillar": "1. Aditivos",
        "intent": "Fundo / Produto",
        "status": "Gap Crítico (Oportunidade)",
        "detail": "A Adfert possui linhas Anticaking e Antidusting, mas tem ZERO artigos dedicados a essas dores industriais no blog.",
        "action": "Publicar Artigo Sugerido #2 de Novembro (Tecnologias Anticaking e Antidusting).",
    },
    {
        "prompt": "Como proteger a adubação da soja e safrinha de milho em anos de El Niño forte e janela curta?",
        "pillar": "5. Clima e Bioma",
        "intent": "Meio / Intenção",
        "status": "Gap Crítico (Oportunidade)",
        "detail": "Existe alerta sobre Super El Niño (17/08/2026), mas sem conectar o risco climático ao uso de fertilizantes estabilizados.",
        "action": "Publicar Artigo Sugerido #1 de Novembro (Plantio sob El Niño + Aditivos de Eficiência).",
    },
    {
        "prompt": "Como enriquecer fertilizantes granulados NPK com micronutrientes líquidos sem segregação?",
        "pillar": "1. Aditivos",
        "intent": "Fundo / Produto",
        "status": "Citado / Coberto",
        "detail": "Coberto pelo artigo técnico sobre CoatMax (21/02/2025).",
        "action": "Atualizar data/dados para 2026 e corrigir tag canonical duplicada.",
    },
]

kb["brands"]["intrivia"]["ai_prompts"] = [
    {
        "prompt": "Como reduzir o abortamento de flores e vagens na soja causado por ondas de calor extremo e El Niño?",
        "pillar": "1. Aditivos",
        "intent": "Fundo / Produto",
        "status": "Gap Crítico (Oportunidade)",
        "detail": "O post de 19/10/2026 explica o dano do calor na soja, mas não apresenta o escudo fisiológico (Protec Foli) como solução técnica.",
        "action": "Publicar Artigo Sugerido #1 de Novembro (Escudo fisiológico na soja e no café com Protec Foli).",
    },
    {
        "prompt": "Como proteger a florada e o chumbinho do café contra seca e altas temperaturas na safra 2026/27?",
        "pillar": "3. Agro",
        "intent": "Meio / Intenção",
        "status": "Cobertura Parcial",
        "detail": "Abordado em 29/10/2026, porém sem link interno para a linha de Proteção Essencial da Intrivia.",
        "action": "Conectar artigo de café à página /nossas-solucoes/ e adicionar FAQ estruturado.",
    },
    {
        "prompt": "Quais micronutrientes e manejo foliar destravam o enchimento de grãos na soja e arranque do milho safrinha?",
        "pillar": "2. Fertilizantes",
        "intent": "Fundo / Produto",
        "status": "Gap Crítico (Oportunidade)",
        "detail": "O blog só possui 2 artigos de nutrição (ambos de abril/2026 focados apenas em Enxofre).",
        "action": "Publicar Artigo Sugerido #2 de Novembro (Equilíbrio nutricional e micronutrientes no enchimento de grãos).",
    },
    {
        "prompt": "Quais os sintomas de deficiência de enxofre na soja e impacto na nodulação e produtividade?",
        "pillar": "2. Fertilizantes",
        "intent": "Meio / Intenção",
        "status": "Citado / Coberto",
        "detail": "Bem coberto pelos artigos de 22/04/2026 (milho) e 30/04/2026 (soja).",
        "action": "Mudar permalink datado (/2026/04/30/...) para slug evergreen e corrigir Schema Person -> Organization.",
    },
]

kb["brands"]["adfert"]["autocomplete"] = harvest["adfert_autocomplete"]
kb["brands"]["intrivia"]["autocomplete"] = harvest["intrivia_autocomplete"]
kb["brands"]["adfert"]["vitals"] = harvest["adfert_vitals"]
kb["brands"]["intrivia"]["vitals"] = harvest["intrivia_vitals"]

kb["brands"]["adfert"]["november_articles"] = [
    {
        "slot": "Artigo 1 (Meio do Mês)",
        "title": "Plantio sob El Niño e janela curta da Safrinha: como proteger o investimento na adubação em cenários de estresse climático",
        "pillars": ["5. Clima e Bioma", "1. Aditivos", "2. Fertilizantes"],
        "intent": "Meio / Intenção",
        "target_product": "Linha Uremax (NBPT/Plus/Coat/Pro) & PhosProtec",
        "rationale": "Conecta o atraso na compra de nitrogenados para a safrinha 2027 e o calor no Cerrado ao papel dos inibidores e protetores como seguro agronômico.",
    },
    {
        "slot": "Artigo 2 (Fim do Mês)",
        "title": "Da fábrica ao campo sem perdas: o papel das tecnologias Anticaking e Antidusting na fluidez e qualidade dos fertilizantes",
        "pillars": ["1. Aditivos", "3. Agro", "6. Complementares & Entretenimento"],
        "intent": "Fundo / Produto",
        "target_product": "Linhas Anticaking & Antidusting Adfert",
        "rationale": "Preenche o maior gap de SEO/GEO do blog da Adfert: zero artigos explicando controle de empedramento e poeira para misturadoras e indústria.",
    },
]

kb["brands"]["intrivia"]["november_articles"] = [
    {
        "slot": "Artigo 1 (Meio do Mês)",
        "title": "Escudo fisiológico na soja e no café: como mitigar o estresse térmico e proteger o pegamento de florada no pico do El Niño",
        "pillars": ["1. Aditivos", "5. Clima e Bioma", "3. Agro"],
        "intent": "Fundo / Produto",
        "target_product": "Linha Proteção Essencial (Protec Foli)",
        "rationale": "Conecta os alertas de calor extremo (outubro) e pico do El Niño (novembro) diretamente à solução fisiológica da Intrivia.",
    },
    {
        "slot": "Artigo 2 (Fim do Mês)",
        "title": "Equilíbrio nutricional e micronutrientes no enchimento de grãos: como destravar o teto produtivo da safra 2026/27",
        "pillars": ["2. Fertilizantes", "1. Aditivos", "3. Agro"],
        "intent": "Meio / Intenção",
        "target_product": "Portfólio de Nutrição de Alta Performance Intrivia",
        "rationale": "Expande a autoridade nutricional da Intrivia (hoje restrita a 2 posts de enxofre) para absorção foliar e enchimento de grãos.",
    },
]

(base_dir / "data" / "knowledge_base.json").write_text(json.dumps(kb, ensure_ascii=False, indent=2), encoding="utf-8")

for b in ["adfert", "intrivia"]:
    pt_arts = [a for a in kb["brands"][b]["articles"] if a["lang"] == "pt"]
    avg_words = round(sum(a["crawl_metrics"]["word_count"] for a in pt_arts) / len(pt_arts))
    with_prod_link = sum(1 for a in pt_arts if a["crawl_metrics"]["product_links"] > 0)
    ttfb = kb["brands"][b]["vitals"]["ttfb_ms"]
    print(f"[{b.upper()}] PT posts: {len(pt_arts)} | Avg words: {avg_words} | Posts linking to product pages: {with_prod_link}/{len(pt_arts)} | TTFB: {ttfb}ms")

