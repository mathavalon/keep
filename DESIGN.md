# DESIGN.md — keep Design System (Operate Mode)

## Identidade Visual Pinned (keep)
- **Superfície:** Modo Claro Operacional (`--bg: #F6F7FB`, `--surface: #FFFFFF`, `--border: #E4E7EC`).
- **Paleta Semântica Keep:**
  - **Cobalt Blue (`#4B6BFB`):** Ação primária, seleção ativa na sidebar e Topo de Funil (`Visitas / Páginas`).
  - **Deep Indigo (`#221C7A`):** Contraste institucional secundário e Meio de Funil (`Intenções / Buscas`).
  - **Cool Gray (`#D6D6D6`):** Bloco de Fundo de Funil (`Conversão / Links de Produto`, com texto `#221C7A`).
  - **Estados:** Sucesso `#16A34A`, Alerta `#D97706`, Erro/Crítico `#E11D48`.

## Regras de Craft (Impeccable + Web Design Guidelines)
- **Zero Emojis como Ícones:** Todos os ícones de navegação e interface são SVGs autorais de traço uniforme (`stroke-width: 1.75`, `20x20px`).
- **Tipografia & Numerais:** Sans-serif limpa (`Inter` / sistema) com `font-variant-numeric: tabular-nums` em todos os KPIs, tabelas, scores e métricas de latência.
- **Sem Costumes de Template IA:** Proibido `border-left: 4px solid` em cards/alertas, textos em gradiente ou sombras duras. Hierarquia construída por espaçamento, bordas de `1px` e badges semânticos discretos.
- **1 Função por Tela:** Navegação lateral esquerda (`60px`) alterna instantaneamente entre 4 telas independentes sem empilhar relatórios longos na mesma visão.
