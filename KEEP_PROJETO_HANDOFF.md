# Keep — Plataforma de Inteligência SEO, GEO & Conteúdo (Handoff Técnico)

> **Propósito deste documento:** Guia completo de arquitetura, banco de dados, scripts de coleta, design system e descobertas técnicas do projeto **Keep**, pronto para continuidade em qualquer IDE ou agente de IA.

---

## 1. Visão Geral do Projeto

O **Keep** é uma plataforma de **SEO Técnico, GEO (Generative Engine Optimization) e Inteligência Editorial** construída para auditar, monitorar e escalar a autoridade orgânica e generativa de duas marcas B2B do agronegócio brasileiro pertencentes ao **Grupo Indorama**:

1. **Adfert** (`https://adfert.com.br/artigos/`) — Especialista em aditivos industriais para fertilizantes (antiempedrantes, antipó, revestimento NPK, micronutrientes e adjuvantes). Atua em **3 idiomas** (PT-BR, EN-US, ES).
2. **Intrivia** (`https://intrivia.com.br/artigos/`) — Especialista em fisiologia vegetal, nutrição especializada, biofertilizantes e redução de estresse abiótico no campo. Atua em **1 idioma** (PT-BR).

O projeto combina dados oficiais extraídos em tempo real das **APIs REST do WordPress (`wp-json`)** de ambas as marcas com conceitos e coletores inspirados em dois projetos open-source de referência:
- **[`every-app/open-seo`](https://github.com/every-app/open-seo):** Mapeamento de visibilidade em motores de IA generativa (ChatGPT, Perplexity, Gemini), classificação de intenção de funil (*Topo / Visitas*, *Meio / Intenções*, *Fundo / Produto*) e **AI Prompt Explorer**.
- **[`crawlseo/crawlseo`](https://github.com/crawlseo/crawlseo):** Crawler On-Page de HTML real (contagem de palavras, estrutura H2/H3, alt text de imagens, links internos para páginas de conversão `/nossas-solucoes/`), telemetria HTTP (TTFB, tamanho de payload, tempo de resposta) e minerador de **Google Autocomplete Brasil** (`suggestqueries.google.com`).

---

## 2. Localização e Estrutura de Pastas

O projeto principal está salvo em:
📂 **`/Users/matheus/Documents/Keep/`** *(com espelho de trabalho em `/Users/matheus/.gemini/antigravity/scratch/Keep/`)*

```text
/Users/matheus/Documents/Keep/
├── dashboard.html                     # Aplicação Web autocontida (4 telas, zero dependências externas de servidor)
├── build_dashboard.py                 # Gerador/compilador do dashboard.html a partir do knowledge_base.json
├── harvest_live_data.py               # Coletor em tempo real: WP-JSON (HTML completo), HTTP TTFB e Google Autocomplete
├── enrich_kb.py                       # Motor de análise On-Page (CrawlSEO) + AI Prompts (OpenSEO) -> atualiza JSON/DB
├── indexer_cli.py                     # CLI de consulta rápida e sincronizador de notícias ao vivo (Google News RSS)
├── PRODUCT.md                         # Especificação de produto, personas (25–42 anos) e regras de negócio
├── DESIGN.md                          # Design System Keep (cores, tipografia, grid, regras anti-slop da skill Impeccable)
├── README.md                          # Guia rápido de uso
├── assets/
│   └── keep-logo.png                  # Logotipo oficial geométrico do Keep
├── data/
│   ├── knowledge_base.json            # Base de dados unificada (artigos enriquecidos, scores, prompts IA, vitals, notícias)
│   └── seo_geo_agro.db                # Banco relacional SQLite (tabelas: articles, brand_audits, news_radar)
└── reports/
    ├── auditoria_seo_geo_adfert.md    # Dossiê técnico completo da Adfert (SEO, GEO, 6 Pilares e Polylang)
    └── auditoria_seo_geo_intrivia.md  # Dossiê técnico completo da Intrivia (SEO, GEO, 6 Pilares e Clones)
```

---

## 3. Como os Dados São Coletados e Transformados

### 3.1. Endpoints WordPress REST API (`wp-json`) Descobertos
Ambos os sites possuem a API REST nativa do WordPress aberta publicamente:
- **Adfert:** `https://adfert.com.br/wp-json/wp/v2/posts?per_page=100` (e `/categories`, `/pages`)
- **Intrivia:** `https://intrivia.com.br/wp-json/wp/v2/posts?per_page=100` (e `/categories`, `/pages`)

### 3.2. Pipeline de Enriquecimento (`harvest_live_data.py` + `enrich_kb.py`)
1. **Coleta Bruta (`harvest_live_data.py`):**
   - Puxa todos os posts publicados via `wp-json/wp/v2/posts`, incluindo o HTML completo renderizado (`content.rendered`), datas exatas (`date`, `modified`), slugs e idioma.
   - Mede a performance HTTP real (`ttfb_ms`, `total_ms`, `size_kb`, `server`, `cache_status`) de `adfert.com.br/artigos/` e `intrivia.com.br/artigos/`.
   - Consulta a API do Google Suggest (`http://suggestqueries.google.com/complete/search?client=firefox&hl=pt-BR&gl=br&q=...`) para dezenas de sementes do agronegócio e tecnologia de fertilizantes.
2. **Processamento On-Page & GEO (`enrich_kb.py`):**
   - Analisa o HTML de cada artigo individualmente e calcula:
     - `word_count`: Contagem real de palavras limpas.
     - `h2_count` e `h3_count`: Profundidade de escaneabilidade semântica.
     - `internal_links`: Total de links internos para o próprio domínio.
     - `product_links`: Quantos links apontam para páginas comerciais (`/nossas-solucoes/`, `/produtos/`, `/contato/`).
     - `images_missing_alt`: Imagens sem atributo `alt`.
     - `onpage_score` (`0–100`): Nota técnica calculada automaticamente por artigo.
     - `intent`: Classificação automática no funil (**Topo / Visitas**, **Meio / Intenções**, **Fundo / Produto**).
   - Classifica cada artigo em um dos **6 Pilares Editoriais**:
     1. `1. Aditivos`
     2. `2. Fertilizantes`
     3. `3. Agro`
     4. `4. Agro Global`
     5. `5. Clima e Bioma`
     6. `6. Complementares & Entretenimento`
3. **Radar de Notícias ao Vivo (`indexer_cli.py --sync-live`):**
   - Busca manchetes reais do Google News RSS Brasil para cada um dos 6 pilares e salva em `knowledge_base.json` e no banco SQLite `seo_geo_agro.db`.

---

## 4. Arquitetura de Interface (4 Telas na Sidebar)

Seguindo a identidade visual do **Keep** e as diretrizes da skill `impeccable` (voltada para decisores e analistas de **25 a 42 anos**), a interface foi dividida em **4 funções independentes** acionadas pelos 4 ícones SVG da barra lateral esquerda:

| Ícone / Aba | Nome da Função | O que exibe |
| :--- | :--- | :--- |
| **1. Painel** | **Dashboard Executivo** | • **3 Cards KPI Keep:** Cobalt Blue (`#4B6BFB` — Artigos/Visitas), Deep Indigo (`#221C7A` — Intenções Google + Prompts IA), Cool Gray (`#D6D6D6` — Artigos com Link p/ Soluções).<br>• **Evolução Temporal:** Gráfico spline com seletor entre **Cadência Real Publicada (WP-JSON)** e **Projeção Search Console (GSC)**.<br>• **Funil & Scorecard:** Donut de conversão interna + notas das 4 frentes (`SEO Técnico`, `Prontidão GEO`, `Autoridade 6 Pilares`, `Arquitetura Multilíngue`). |
| **2. Radar** | **Radar 6 Pilares & Catálogo** | • **Artigos Recomendados (Novembro):** Pautas prontas com H2/H3, FAQ GEO e linkagem comercial.<br>• **Grid dos 6 Pilares:** Cobertura atual da marca + notícias quentes do Google News RSS.<br>• **Catálogo Completo:** Tabela paginada/filtrável por pilar, idioma e busca textual com métricas de palavras, H2/H3, links para `/nossas-solucoes/` e nota On-Page. |
| **3. Prompts** | **Função OpenSEO (IA & Buscas)** | • **AI Prompt Explorer:** Perguntas reais de compradores e agrônomos no ChatGPT, Perplexity e Gemini, indicando o status da marca (*Citada*, *Parcial* ou *Invisível*) e o gap exato para produzir.<br>• **Google Autocomplete Explorer:** Termos cauda-longa buscados no Brasil e se já estão cobertos ou são oportunidades abertas. |
| **4. Auditoria** | **Função CrawlSEO (Engenharia)** | • **Telemetria HTTP & Web Vitals:** TTFB real (`168ms` Adfert / `269ms` Intrivia), peso do HTML e status de Schema.org.<br>• **5 Correções Críticas Priorizadas:** Problemas de código/servidor de cada marca.<br>• **Lista de Artigos Órfãos de Conversão:** Todos os artigos em PT-BR que têm `0 links` para `/nossas-solucoes/`. |

> **Comparador Lado a Lado:** No topo de qualquer tela, o botão **"Comparar Marcas"** abre um modal comparando Adfert vs. Intrivia em todas as dimensões.

---

## 5. Resumo das Descobertas Técnicas nas 2 Marcas

### 5.1. Adfert (`https://adfert.com.br/artigos/`)
- **Volume Indexado:** **114 artigos no total** (40 em PT-BR, 37 em EN-US, 37 em ES), média de **586 palavras/post**.
- **Gargalo Comercial (CrawlSEO):** Apenas **10 dos 40 artigos em PT (25,0%)** possuem link interno para `/nossas-solucoes/`. Há **30 artigos órfãos de conversão**.
- **Bugs Críticos de SEO & GEO:**
  1. **Canonical & `og:url` Hardcoded para a Home:** O header global do tema imprime `<link rel="canonical" href="https://adfert.com.br/">` fixo em todas as páginas, conflitando com a canonical individual dos artigos.
  2. **Zero Schema.org JSON-LD (`GEO: 35/100`):** Nenhuma marcação `Article`, `Organization` ou `FAQPage`, reduzindo drasticamente a citação em motores de IA.
  3. **Hierarquia H1 Invertida:** `<h1>` sendo usado em títulos de rodapé ("Menu", "Contato") enquanto os títulos dos artigos usam `<h2>`.
  4. **Contaminação de Categorias no Polylang:** Posts em inglês (`en-US`) estão categorizados sob `"Noticias Generales"` (espanhol) e posts em espanhol sob `"General News"` (inglês).

### 5.2. Intrivia (`https://intrivia.com.br/artigos/`)
- **Volume Indexado:** **18 artigos no total** (100% em PT-BR, sem versões EN/ES), média de **635 palavras/post**.
- **Gargalo Comercial (CrawlSEO):** Apenas **4 dos 18 artigos (22,2%)** linkam para `/nossas-solucoes/` (14 artigos órfãos).
- **Bugs Críticos de SEO & GEO:**
  1. **4 Artigos Clonados da Adfert no Ar:** Há 4 posts de 2025 herdados do banco da Adfert publicados dentro do domínio da Intrivia citando *"Adfert"* no título e na URL (risco de conteúdo duplicado entre domínios do mesmo grupo).
  2. **Duplo `<title>` e Duplo `<link rel="canonical">`:** O plugin RankMath está ativo, mas o `header.php` do tema também imprime tags estáticas duplicadas.
  3. **Schema.org `@type: Person` Incorreto:** O JSON-LD do RankMath declara a entidade publicadora da Intrivia como `Person` em vez de `Organization`.
  4. **Ausência de Versões EN/ES (`Multilíngue: 20/100`):** 100% restrita ao português.

---

## 6. Comandos para Operar na Nova IDE

Abra o terminal na pasta `/Users/matheus/Documents/Keep` e utilize:

```bash
# 1. Consultar estatísticas rápidas do banco de dados
python3 indexer_cli.py --stats

# 2. Sincronizar manchetes ao vivo do Google News RSS (6 Pilares)
python3 indexer_cli.py --sync-live

# 3. Rodar novamente o crawler completo (WP-JSON + TTFB + Google Autocomplete)
python3 harvest_live_data.py
python3 enrich_kb.py

# 4. Recompilar o dashboard.html após qualquer mudança de código ou dados
python3 build_dashboard.py
```

---

## 7. Visão Completa do Produto SaaS (Os 6 Pilares de Expansão do Keep)

O **Keep** deixa de ser apenas um painel de diagnóstico e passa a operar como um **Sistema Operacional Completo de Presença Digital, CMS Visual e Motor Autônomo de Conteúdo SEO/GEO**, estruturado em 6 frentes integradas:

### Módulo 1 — Conector WordPress Bidirecional (Leitura + Publicação Autenticada)
- Além de ler via `GET /wp-json/wp/v2/posts`, o cliente conecta sua conta WordPress (via **Application Passwords** nativo do WP ou JWT).
- O Keep passa a ter permissão de escrita (`POST /wp-json/wp/v2/posts`, `POST /wp-json/wp/v2/media`) para publicar artigos automaticamente, corrigir meta tags/canonicals, injetar Schema.org JSON-LD e inserir links internos nos artigos órfãos com 1 clique.

### Módulo 2 — Agente Gerador de Artigos Padrão "EbookGPT" (SEO + GEO Rico)
- Motor de geração de artigos sob demanda (controlado pela cota contratada no plano do cliente).
- Segue o **Padrão Editorial EbookGPT** (`https://ebookgpt.com/en/blog/youtube-shopping-for-ebook-discovery`):
  - Hierarquia semântica impecável (`H1` único, `H2` modulares, `H3` de resposta direta para motores de IA).
  - Mix visual rico ao longo do corpo: **imagens contextuais, GIFs demonstrativos, tabelas comparativas, blocos de destaque (callouts/key takeaways), listas estruturadas e FAQ Schema**.
  - Injeção automática de **hiperlinks internos** (apontando para as páginas comerciais do cliente, como `/nossas-solucoes/`) e **links externos de autoridade** (backlinks/citações de fontes confiáveis para elevar o score GEO no Perplexity, ChatGPT e Google AI Overviews).

### Módulo 3 — Editor Visual Simplificado ("Tempero Gourmet" / Headless CMS Visual)
- Uma aba dedicada na sidebar do Keep onde o dono do site edita **textos, galerias de imagens e vídeos** da sua página institucional sem nunca precisar abrir o painel confuso do WordPress ou mexer em código.
- Funciona lendo e gravando diretamente nos atributos padronizados do HTML do cliente.

### Módulo 4 — Motor de Assinaturas e Cobrança via Asaas
- Integração nativa com a API do **Asaas** (PIX, Boleto, Cartão Recorrente e Webhooks de status de assinatura).
- Controle automático de cotas por plano:
  - Quantidade de artigos SEO/GEO gerados por mês pelo Agente.
  - Quantidade de páginas/domínios monitorados no Radar e Auditoria.
  - Acesso ao Editor Visual e ao Pack de Design Systems.

### Módulo 5 — Ecossistema Methz (`methz.com.br` — 20 Design Systems Integrados)
- Unificação com a oferta do pack de **20 Design Systems (`methz.com.br`)**.
- Quem adquire o pack na Methz já recebe acesso integrado ao ecossistema Keep, podendo escolher qualquer um dos 20 Design Systems prontos e gerenciá-lo visualmente dentro da plataforma.

### Módulo 6 — Padronização de HTML & Onboarding dos Primeiros ~8 Clientes Reais
- Os **20 Design Systems** já possuem uma marcação padrão no `<body>` do HTML pensada para o Editor Visual do Keep reconhecer blocos editáveis (textos, imagens, galerias, vídeos).
- **Ação Imediata de Onboarding:** Auditar e refatorar o HTML das **~8 páginas dos primeiros clientes reais** que ainda estão fora desse padrão, normalizando a estrutura do `<body>` para que todas fiquem 100% gerenciáveis pelo Keep desde o dia 1.


