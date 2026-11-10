# Auditoria Técnica SEO & GEO — `https://adfert.com.br/artigos/`

> **Data da Indexação:** 10/11/2026  
> **Stack Detectada:** WordPress 7.1.4 + Elementor 4.4.0 + Google Site Kit 1.191.0 + Cloudflare CDN (GRU Edge)  
> **Base Indexada:** 114 artigos (40 em Português, 37 em Inglês, 37 em Espanhol) extraídos via HTML + WP REST API (`/wp-json/wp/v2/posts`).

---

## 1. Scorecard de Diagnóstico (SEO vs. GEO)

| Dimensão | Nota | Diagnóstico Resumido |
| :--- | :---: | :--- |
| **SEO Técnico & Indexação** | **48 / 100** | Crítico: tag `<link rel="canonical" href="https://adfert.com.br/">` hardcoded no cabeçalho global. |
| **GEO (Generative Engine Optimization)** | **35 / 100** | Crítico: **0 blocos JSON-LD** (`Schema.org`), sem marcação de entidades químicas/agronômicas (`NBPT`, `PhosProtec`, `CoatMax`). |
| **Autoridade Temática & Conteúdo** | **84 / 100** | Excelente cobertura técnica nos 6 pilares (Aditivos, Fertilizantes, Agro, Agro Global, Clima/Bioma e Cultura/ESG). |
| **Arquitetura Multilíngue (PT/EN/ES)** | **62 / 100** | `hreflang` presente, mas há cruzamento de categorias entre EN/ES e slugs clonados em traduções. |

---

## 2. Achados Críticos de Indexação & SEO

### 🔴 2.1. Conflito de Canonical e OpenGraph Hardcoded para a Home
- **Evidência em `/artigos/`:**
  ```html
  <link rel="canonical" href="https://adfert.com.br/">
  <meta property="og:url" content="https://adfert.com.br/">
  ```
- **Evidência nos Artigos Individuais (ex.: `/eficiencia-do-nitrogenio-.../`):**
  ```html
  <link rel="canonical" href="https://adfert.com.br/eficiencia-do-nitrogenio-tecnologia-e-conhecimento-para-proteger-seu-investimento/" />
  <link rel="canonical" href="https://adfert.com.br/">
  ```
- **Impacto:** O Googlebot ignora declarações canônicas quando encontra múltiplas tags `<link rel="canonical">` conflitantes ou desindexa `/artigos/` por entender que é cópia da Home (`/`).
- **Correção:** Remover as tags `<link rel="canonical" ...>`, `<meta property="og:url" ...>`, `<meta name="description" ...>` e `<meta name="keywords" ...>` que foram inseridas manualmente no `header.php` (ou nas configurações personalizadas do Elementor) e delegar ao plugin de SEO dinâmico.

### 🔴 2.2. Hierarquia Semântica Invertida (`<h1>` no Rodapé)
- **Evidência em `/artigos/`:**
  - `H1 #1`: `Política de Privacidade | © 2024 - Indorama Brasil Ltda | 42.602.384/0009-10`
  - `H1 #2`: `Fale com a gente Rua Lineu Anterino Mariano, 175, Distrito Industrial, Uberlândia-MG, CEP: 38.402-346`
  - O título real da página (`ARTIGOS` / `Confira nossos artigos e conteúdos especiais`) está marcado apenas como `<h2>`.
- **Correção:** Alterar os elementos de rodapé no template global do Elementor de `H1` para `<p>` ou `<h4>`, garantindo um único `<h1>` semântico por página.

### 🟠 2.3. Erro de Sintaxe HTML nas Meta Tags e Snippet Genérico
- **Evidência:**
  ```html
  <meta name="keywords" content=“”ADFERT, soluções sustentáveis, Nutrientes especiais, Agricultura"">
  ```
  O uso de aspas curvas tipográficas (`“”`) junto com aspas duplas quebra o parser de atributos no `<head>`. Além disso, a `meta description` é idêntica em todas as URLs do site.

### 🟡 2.4. Anomalias no Cluster Multilíngue (PT / EN / ES)
1. **Cruzamento de Taxonomias:** Todos os posts em **Inglês** estão categorizados na categoria em Espanhol `Noticias Generales` (ID `19`), enquanto os posts em **Espanhol** estão categorizados em Inglês `General News` (ID `23`).
2. **Slugs Clonados (15/04/2026):**
   - PT: `/recorde-nas-operacoes-de-barter-e-o-ajuste-no-acesso-a-insumos/`
   - EN: `/en/2026-agricultural-margins-will-be-defined-by-strategy-not-only-by-productivity/` *(slug copiado do artigo de 02/03/2026!)*
   - ES: `/es/2026-el-margen-en-el-agro-sera-definido-por-la-estrategia-no-solo-por-la-productividad/` *(slug copiado do artigo de 02/03/2026!)*

---

## 3. Estratégia GEO (Generative Engine Optimization) para Motores de IA

Para que **Google AI Overviews, Perplexity, ChatGPT Search e Gemini** citem a **Adfert** como fonte primária ao responderem perguntas sobre *aditivos para fertilizantes, inibidores de urease (NBPT), proteção de fósforo em solos tropicais e tendências do agro*, recomendamos:

1. **Injeção de Grafo de Entidades em `JSON-LD` (`Schema.org`):**
   - Conectar explicitamente `Adfert` (`parentOrganization: Indorama Corporation`) às entidades técnicas e produtos (`Uremax NBPT`, `PhosProtec`, `CoatMax`, `Anticaking`, `Antidusting`).
2. **Blocos de Resposta Direta ("Citation-Ready Summaries"):**
   - Iniciar artigos técnicos com um resumo estruturado de 40–60 palavras + tabela comparativa (ex.: % de redução de perdas por volatilização de $\text{NH}_3$ com NBPT vs. ureia convencional).
3. **Arquivo `/llms.txt` na Raiz do Domínio:**
   - Publicar `https://adfert.com.br/llms.txt` indexando os 6 pilares temáticos e as fichas técnicas das linhas de aditivos.

### Modelo JSON-LD Pronto para `/artigos/` e Artigos Técnicos

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://adfert.com.br/#organization",
      "name": "Adfert",
      "legalName": "Indorama Brasil Ltda",
      "url": "https://adfert.com.br/",
      "parentOrganization": {
        "@type": "Organization",
        "name": "Indorama Corporation"
      },
      "knowsAbout": [
        "Aditivos para Fertilizantes",
        "Inibidores de Urease (NBPT)",
        "Complexantes de Fósforo (PhosProtec)",
        "Anticaking e Antidusting",
        "Revestimento de Micronutrientes (CoatMax)",
        "Eficiência Nutricional no Agronegócio"
      ]
    },
    {
      "@type": "CollectionPage",
      "@id": "https://adfert.com.br/artigos/#webpage",
      "url": "https://adfert.com.br/artigos/",
      "name": "Artigos e Conteúdos Técnicos sobre Aditivos, Fertilizantes e Agronegócio | Adfert",
      "inLanguage": "pt-BR",
      "isPartOf": {
        "@id": "https://adfert.com.br/#website"
      },
      "about": [
        { "@type": "Thing", "name": "Aditivos para Fertilizantes" },
        { "@type": "Thing", "name": "Eficiência de Nitrogênio e Fósforo" },
        { "@type": "Thing", "name": "Mercado Global de Fertilizantes" },
        { "@type": "Thing", "name": "Clima, Biomas e Sustentabilidade no Agro" }
      ]
    }
  ]
}
```

