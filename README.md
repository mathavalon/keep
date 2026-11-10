# 🧩 keep — SEO, GEO & Crawl Intelligence

Projeto separado da Avalon. Abra um **projeto novo no Lovable** a partir de `https://github.com/mathavalon/keep`. Não conecte o Lovable da Avalon e não use o banco dela.

O Lovable cria o Supabase deste repositório e aplica `supabase/migrations/20261110220000_keep_init.sql`. A entrada do app é o login com confirmação de e-mail. O painel que já existe fica em `public/painel.html`.



Motor e painel unificado inspirado em **OpenSEO** + **CrawlSEO**, com identidade visual **keep**, cobrindo as marcas **Adfert** e **Intrivia**.

## 📂 Estrutura da Pasta `Keep`

- `public/painel.html` — Painel interativo no visual **keep** (sidebar esquerda, seletor de página/período, 3 cards de funil Azul/Índigo/Cinza, gráfico de evolução temporal, donut de conversão e 3 abas do arsenal).
- `src/App.tsx` — Entrada do Lovable: login e confirmação de e-mail antes do painel.
- `supabase/migrations/20261110220000_keep_init.sql` — Banco próprio do Keep.
- `harvest_live_data.py` — Coletor ao vivo (Google Autocomplete Brasil + métricas de TTFB/payload + extração do corpo HTML de todos os artigos via WP-JSON).
- `enrich_kb.py` — Analisador On-Page (contagem de palavras, `H2`/`H3`, links internos para `/nossas-solucoes/`, imagens sem `alt`, classificação de estágio de funil e Prompts de IA/GEO).
- `indexer_cli.py` — Utilitário de linha de comando (`--stats`, `--sync-live`).
- `data/knowledge_base.json` & `data/seo_geo_agro.db` — Base consolidada Multi-Cliente.
- `reports/` — Relatórios técnicos de auditoria da Adfert e da Intrivia.
