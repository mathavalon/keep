# 🧩 keep — SEO, GEO & Crawl Intelligence

Projeto separado da Avalon. Abra um **projeto novo no Lovable** a partir de `https://github.com/mathavalon/keep`. Não conecte o Lovable da Avalon e não use o banco dela.

O Lovable cria o Supabase deste repositório e aplica as migrations em `supabase/migrations`. A entrada `/` é a homepage de captura. O login fica em `/login`. Visão geral, radar, editor e as outras telas ficam em `/app` e só abrem com o e-mail confirmado.



Motor e painel unificado inspirado em **OpenSEO** + **CrawlSEO**, com identidade visual **keep**, cobrindo as marcas **Adfert** e **Intrivia**.

## 📂 Estrutura da Pasta `Keep`

- `public/keep-app.js` — Homepage, login e telas internas no design system novo.
- `src/main.tsx` — Liga o login e a captura de leads ao Supabase deste projeto.
- `supabase/migrations/` — Banco próprio do Keep, incluindo os contatos da homepage.
- `harvest_live_data.py` — Coletor ao vivo (Google Autocomplete Brasil + métricas de TTFB/payload + extração do corpo HTML de todos os artigos via WP-JSON).
- `enrich_kb.py` — Analisador On-Page (contagem de palavras, `H2`/`H3`, links internos para `/nossas-solucoes/`, imagens sem `alt`, classificação de estágio de funil e Prompts de IA/GEO).
- `indexer_cli.py` — Utilitário de linha de comando (`--stats`, `--sync-live`).
- `data/knowledge_base.json` & `data/seo_geo_agro.db` — Base consolidada Multi-Cliente.
- `reports/` — Relatórios técnicos de auditoria da Adfert e da Intrivia.
