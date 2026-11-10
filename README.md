# 🧩 keep — SEO, GEO & Crawl Intelligence

Motor e painel unificado inspirado em **OpenSEO** + **CrawlSEO**, com identidade visual **keep**, cobrindo as marcas **Adfert** e **Intrivia**.

## 📂 Estrutura da Pasta `Keep`

- `dashboard.html` — Painel interativo no visual **keep** (sidebar esquerda, seletor de página/período, 3 cards de funil Azul/Índigo/Cinza, gráfico de evolução temporal, donut de conversão e 3 abas do arsenal).
- `harvest_live_data.py` — Coletor ao vivo (Google Autocomplete Brasil + métricas de TTFB/payload + extração do corpo HTML de todos os artigos via WP-JSON).
- `enrich_kb.py` — Analisador On-Page (contagem de palavras, `H2`/`H3`, links internos para `/nossas-solucoes/`, imagens sem `alt`, classificação de estágio de funil e Prompts de IA/GEO).
- `indexer_cli.py` — Utilitário de linha de comando (`--stats`, `--sync-live`).
- `data/knowledge_base.json` & `data/seo_geo_agro.db` — Base consolidada Multi-Cliente.
- `reports/` — Relatórios técnicos de auditoria da Adfert e da Intrivia.
