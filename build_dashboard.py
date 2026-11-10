#!/usr/bin/env python3
import json
from pathlib import Path

base_dir = Path(__file__).resolve().parent
kb = json.loads((base_dir / "data" / "knowledge_base.json").read_text(encoding="utf-8"))
kb_json_str = json.dumps(kb, ensure_ascii=False)

template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>keep — SEO, GEO & Crawl Intelligence</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #f6f7fb;
      --surface: #ffffff;
      --surface-subtle: #fafbfe;
      --border: #e4e7ec;
      --blue: #4b6bfb;
      --blue-soft: #eef2ff;
      --indigo: #221c7a;
      --indigo-soft: #e0e7ff;
      --gray-card: #d6d6d6;
      --text: #111827;
      --muted: #6b7280;
      --danger: #e11d48;
      --danger-soft: #ffe4e6;
      --warn: #d97706;
      --warn-soft: #fef3c7;
      --ok: #16a34a;
      --ok-soft: #dcfce7;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    ::selection { background: var(--blue-soft); color: var(--indigo); }
    html, body {
      max-width: 100%;
      overflow-x: hidden;
      font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.45;
      font-variant-numeric: tabular-nums;
      -webkit-font-smoothing: antialiased;
    }

    /* Shell Principal Keep */
    .app-shell {
      display: flex;
      min-height: 100vh;
      width: 100%;
    }

    /* Sidebar Esquerda Minimalista c/ Ícones SVG e Labels */
    .sidebar {
      width: 68px;
      background: var(--surface);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 16px 0;
      gap: 10px;
      flex-shrink: 0;
      position: sticky;
      top: 0;
      height: 100vh;
    }
    .keep-logo {
      width: 38px;
      height: 38px;
      margin-bottom: 12px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 8px;
      transition: transform 0.15s ease-out;
    }
    .keep-logo:hover { transform: scale(1.04); }

    .nav-btn {
      width: 54px;
      padding: 8px 4px;
      border-radius: 10px;
      border: 1px solid transparent;
      background: transparent;
      color: var(--muted);
      cursor: pointer;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
      transition: background 0.15s ease-out, color 0.15s ease-out, border-color 0.15s ease-out;
    }
    .nav-btn svg {
      width: 20px;
      height: 20px;
      stroke: currentColor;
      stroke-width: 1.8;
      stroke-linecap: round;
      stroke-linejoin: round;
      fill: none;
    }
    .nav-btn span {
      font-size: 0.62rem;
      font-weight: 600;
      letter-spacing: -0.01em;
    }
    .nav-btn:hover {
      background: var(--surface-subtle);
      color: var(--text);
    }
    .nav-btn.active {
      background: var(--blue-soft);
      color: var(--blue);
      border-color: rgba(75, 107, 251, 0.25);
    }

    .main-area {
      flex: 1;
      min-width: 0;
      padding: 20px 32px 44px;
      max-width: 1380px;
      margin: 0 auto;
    }
    @media (max-width: 768px) {
      .main-area { padding: 16px; }
    }

    /* Topbar Keep */
    .topbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 18px;
    }
    .topbar-left {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .topbar-title {
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text);
      letter-spacing: -0.01em;
    }
    .topbar-right {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .avatar-circle {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: #111827;
      color: #fff;
      font-size: 0.76rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      cursor: pointer;
      border: none;
    }
    .avatar-sub {
      position: absolute;
      bottom: -2px;
      right: -4px;
      background: var(--blue);
      color: #fff;
      font-size: 0.55rem;
      padding: 1px 4px;
      border-radius: 4px;
      font-weight: 700;
    }

    /* Barra de Filtros Global (Página + Período/Fonte) */
    .filter-bar {
      display: grid;
      grid-template-columns: 1.8fr 1.2fr;
      gap: 16px;
      margin-bottom: 20px;
    }
    @media (max-width: 820px) { .filter-bar { grid-template-columns: 1fr; } }
    .field-group label {
      display: block;
      font-size: 0.76rem;
      color: var(--muted);
      margin-bottom: 5px;
      font-weight: 500;
    }
    .field-row {
      display: flex;
      gap: 8px;
    }
    .keep-select, .keep-input {
      width: 100%;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 9px 13px;
      font-size: 0.86rem;
      font-family: inherit;
      color: var(--text);
      outline: none;
      transition: border-color 0.15s;
    }
    .keep-select:focus, .keep-input:focus { border-color: var(--blue); }
    .btn-keep {
      background: var(--surface);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 0 14px;
      border-radius: 8px;
      font-size: 0.82rem;
      font-weight: 600;
      font-family: inherit;
      cursor: pointer;
      white-space: nowrap;
      transition: border-color 0.15s, color 0.15s, background 0.15s;
    }
    .btn-keep:hover {
      border-color: var(--blue);
      color: var(--blue);
      background: var(--blue-soft);
    }

    /* Telas Independentes (Views) */
    .screen-view { display: none; }
    .screen-view.active { display: block; }

    /* 3 Cards KPI Principais (Idênticos ao Keep) */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin-bottom: 24px;
    }
    @media (max-width: 860px) { .kpi-grid { grid-template-columns: 1fr; } }
    .kpi-card {
      border-radius: 10px;
      padding: 24px 20px;
      text-align: center;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 6px;
      box-shadow: 0 2px 8px rgba(17, 24, 39, 0.04);
    }
    .kpi-blue { background: var(--blue); color: #fff; }
    .kpi-indigo { background: var(--indigo); color: #fff; }
    .kpi-gray { background: var(--gray-card); color: var(--indigo); }
    .kpi-num { font-size: 2.15rem; font-weight: 700; line-height: 1.1; letter-spacing: -0.02em; }
    .kpi-label { font-size: 0.86rem; font-weight: 500; margin-bottom: 6px; }
    .kpi-blue .kpi-label, .kpi-indigo .kpi-label { color: rgba(255, 255, 255, 0.92); }
    .kpi-btn {
      border: none;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 0.74rem;
      font-weight: 600;
      font-family: inherit;
      cursor: pointer;
      transition: opacity 0.15s;
    }
    .kpi-btn:hover { opacity: 0.9; }
    .kpi-blue .kpi-btn, .kpi-gray .kpi-btn { background: var(--indigo); color: #fff; }
    .kpi-indigo .kpi-btn { background: var(--blue); color: #fff; }

    /* Cabeçalhos de Seção e Painéis */
    .section-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
      margin: 20px 0 12px;
    }
    .section-h2 {
      font-size: 1.15rem;
      font-weight: 600;
      color: var(--text);
      letter-spacing: -0.01em;
    }
    .card-panel {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 18px 20px;
      margin-bottom: 20px;
      box-shadow: 0 1px 3px rgba(17, 24, 39, 0.02);
    }

    /* Evolução Temporal + Toggle de Fonte */
    .mode-switch {
      display: inline-flex;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 7px;
      padding: 2px;
      gap: 2px;
    }
    .mode-btn {
      border: none;
      background: transparent;
      color: var(--muted);
      font-size: 0.75rem;
      font-weight: 600;
      font-family: inherit;
      padding: 5px 10px;
      border-radius: 5px;
      cursor: pointer;
    }
    .mode-btn.active {
      background: var(--surface);
      color: var(--blue);
      box-shadow: 0 1px 2px rgba(0,0,0,0.06);
    }
    .legend-row {
      display: flex;
      justify-content: center;
      gap: 20px;
      font-size: 0.78rem;
      color: var(--muted);
      margin-bottom: 10px;
      flex-wrap: wrap;
    }
    .legend-dot {
      display: inline-block;
      width: 10px;
      height: 10px;
      border-radius: 50%;
      margin-right: 6px;
      vertical-align: middle;
    }

    /* Funil + 4 Scorecards */
    .funnel-grid {
      display: grid;
      grid-template-columns: 320px 1fr;
      gap: 24px;
      align-items: center;
    }
    @media (max-width: 960px) { .funnel-grid { grid-template-columns: 1fr; } }
    .scores-4-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
    }
    @media (max-width: 600px) { .scores-4-grid { grid-template-columns: 1fr; } }
    .mini-score-box {
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 14px 16px;
      background: var(--surface-subtle);
    }
    .mini-score-val { font-size: 1.5rem; font-weight: 700; margin: 4px 0; letter-spacing: -0.02em; }

    /* Grade Compacta de Cards (Radar, Sugestões, Vitals) */
    .cards-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 12px;
      margin-bottom: 20px;
    }
    .item-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 15px 16px;
      transition: border-color 0.15s, box-shadow 0.15s;
    }
    .item-card.clickable { cursor: pointer; }
    .item-card.clickable:hover, .item-card.active {
      border-color: var(--blue);
      box-shadow: 0 4px 12px rgba(75, 107, 251, 0.08);
    }
    .item-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
      gap: 8px;
    }
    .item-card h3 { font-size: 0.78rem; color: var(--blue); font-weight: 700; text-transform: uppercase; letter-spacing: 0.02em; }
    .item-card h4 { font-size: 0.94rem; color: var(--text); font-weight: 600; margin-bottom: 4px; }
    .item-card p { font-size: 0.81rem; color: var(--muted); margin-bottom: 8px; }
    .live-line {
      font-size: 0.76rem;
      padding-top: 8px;
      margin-top: 8px;
      border-top: 1px solid var(--border);
      color: var(--muted);
    }

    /* Badges Semânticos (Sem border-left 4px) */
    .pill {
      display: inline-block;
      padding: 2px 8px;
      border-radius: 6px;
      font-size: 0.72rem;
      font-weight: 600;
      background: var(--blue-soft);
      color: var(--blue);
    }
    .pill-indigo { background: var(--indigo-soft); color: var(--indigo); }
    .pill-warn { background: var(--warn-soft); color: var(--warn); }
    .pill-danger { background: var(--danger-soft); color: var(--danger); }
    .pill-ok { background: var(--ok-soft); color: var(--ok); }

    /* Controles e Tabelas */
    .controls {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 12px;
      background: var(--surface);
      padding: 12px;
      border-radius: 10px;
      border: 1px solid var(--border);
    }
    table {
      width: 100%;
      table-layout: fixed;
      border-collapse: collapse;
      background: var(--surface);
      border-radius: 10px;
      overflow: hidden;
      border: 1px solid var(--border);
    }
    th, td {
      padding: 11px 14px;
      text-align: left;
      border-bottom: 1px solid var(--border);
      font-size: 0.82rem;
      word-wrap: break-word;
      overflow-wrap: break-word;
      vertical-align: top;
    }
    th { background: #f9fafb; color: var(--muted); font-weight: 600; font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.02em; }
    tr:last-child td { border-bottom: none; }
    a { color: var(--blue); text-decoration: none; font-weight: 500; }
    a:hover { text-decoration: underline; }

    /* Lista de Auditoria Limpa (1px border, zero border-left 4px) */
    .audit-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 14px 18px;
      margin-bottom: 10px;
    }
    .audit-card-head {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 6px;
      flex-wrap: wrap;
    }

    /* Modal Comparativo de Clientes */
    .modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(17, 24, 39, 0.5);
      backdrop-filter: blur(3px);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      padding: 20px;
    }
    .modal-overlay.open { display: flex; }
    .modal-box {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      max-width: 740px;
      width: 100%;
      padding: 24px;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.16);
    }
    .brand-cards {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 14px;
      margin-top: 14px;
    }
    .brand-card {
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 16px;
      cursor: pointer;
      transition: border-color 0.15s, background 0.15s;
    }
    .brand-card:hover, .brand-card.selected {
      border-color: var(--blue);
      background: var(--surface-subtle);
    }
  </style>
</head>
<body>
  <!-- Modal Comparativo de Marcas -->
  <div class="modal-overlay" id="brand-modal" onclick="if(event.target===this) closeBrandModal()">
    <div class="modal-box">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <div>
          <h2 style="font-size:1.1rem;color:var(--text)">Clientes & Marcas Conectadas (keep)</h2>
          <p style="font-size:0.8rem;color:var(--muted)">Compare os indicadores gerais e clique para alternar a área de trabalho.</p>
        </div>
        <button class="btn-keep" style="padding:4px 10px" onclick="closeBrandModal()">Fechar</button>
      </div>
      <div class="brand-cards" id="brand-cards-container"></div>
    </div>
  </div>

  <div class="app-shell">
    <!-- Sidebar Esquerda: 4 Funções com Ícones SVG Limpos -->
    <aside class="sidebar">
      <div class="keep-logo" onclick="switchScreen(1)" title="keep — Início">
        <svg width="30" height="30" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="38" y="6" width="16" height="16" fill="#4B6BFB"/>
          <path d="M18 6C18 22.5685 31.4315 36 48 36" stroke="#4B6BFB" stroke-width="11" stroke-linecap="butt"/>
          <path d="M10 34C26.5685 34 40 47.4315 40 64" stroke="#4B6BFB" stroke-width="11" stroke-linecap="butt"/>
          <circle cx="16" cy="52" r="8" fill="#4B6BFB"/>
        </svg>
      </div>

      <button class="nav-btn active" id="nav-1" onclick="switchScreen(1)" title="1. Dashboard Executivo">
        <svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/></svg>
        <span>Painel</span>
      </button>

      <button class="nav-btn" id="nav-2" onclick="switchScreen(2)" title="2. Radar 6 Pilares & Catálogo Editorial">
        <svg viewBox="0 0 24 24"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>
        <span>Radar</span>
      </button>

      <button class="nav-btn" id="nav-3" onclick="switchScreen(3)" title="3. AI Prompt Explorer & Keywords (OpenSEO)">
        <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg>
        <span>Prompts</span>
      </button>

      <button class="nav-btn" id="nav-4" onclick="switchScreen(4)" title="4. Auditoria Técnica & Crawler (CrawlSEO)">
        <svg viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
        <span>Auditoria</span>
      </button>
    </aside>

    <!-- Área Principal -->
    <main class="main-area">
      <!-- Topbar Padrão Keep -->
      <div class="topbar">
        <div class="topbar-left">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#6b7280" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
          <span class="topbar-title" id="screen-title">Dashboard</span>
          <span class="pill" id="active-brand-pill">Adfert</span>
        </div>
        <div class="topbar-right">
          <button class="btn-keep" style="padding:6px 12px" onclick="openBrandModal()">Trocar Cliente</button>
          <button class="avatar-circle" onclick="openBrandModal()" title="Alternar Cliente">
            KP
            <span class="avatar-sub" id="avatar-sub">AD</span>
          </button>
        </div>
      </div>

      <!-- Barra de Filtros Global (Página + Período) -->
      <div class="filter-bar">
        <div class="field-group">
          <label>Página / Cliente</label>
          <div class="field-row">
            <select class="keep-select" id="brand-select" onchange="selectBrand(this.value)">
              <option value="adfert">Adfert — https://adfert.com.br/artigos/</option>
              <option value="intrivia">Intrivia — https://intrivia.com.br/artigos/</option>
            </select>
            <button class="btn-keep" onclick="openBrandModal()">Comparar</button>
          </div>
        </div>
        <div class="field-group">
          <label>Período & Fonte de Dados</label>
          <input type="text" class="keep-input" readonly value="Safra 2025/2026 • WP-JSON + Google Suggest + CrawlSEO" />
        </div>
      </div>

      <!-- ========================================================= -->
      <!-- TELA 1: DASHBOARD EXECUTIVO (Leve, Fiel ao Anexo Keep)    -->
      <!-- ========================================================= -->
      <section class="screen-view active" id="screen-1">
        <div class="kpi-grid">
          <div class="kpi-card kpi-blue">
            <div class="kpi-num" id="kpi-visitas">40</div>
            <div class="kpi-label" id="kpi-visitas-label">Artigos PT (114 URLs Indexadas)</div>
            <button class="kpi-btn" onclick="switchScreen(2)">Ver lista</button>
          </div>
          <div class="kpi-card kpi-indigo">
            <div class="kpi-num" id="kpi-intencoes">23</div>
            <div class="kpi-label" id="kpi-intencoes-label">Intenções Mapeadas (Google + IA)</div>
            <button class="kpi-btn" onclick="switchScreen(3)">Ver lista</button>
          </div>
          <div class="kpi-card kpi-gray">
            <div class="kpi-num" id="kpi-conversao">10/40</div>
            <div class="kpi-label" id="kpi-conversao-label">Artigos c/ Link p/ Soluções (25.0%)</div>
            <button class="kpi-btn" onclick="switchScreen(4)">Ver lista</button>
          </div>
        </div>

        <div class="section-header">
          <h2 class="section-h2">Evolução temporal</h2>
          <div class="mode-switch">
            <button class="mode-btn active" id="chart-mode-pub" onclick="setChartMode('pub')">Cadência Real Publicada (WP-JSON)</button>
            <button class="mode-btn" id="chart-mode-gsc" onclick="setChartMode('gsc')">Projeção Search Console (Cliques & Intenções)</button>
          </div>
        </div>
        <div class="card-panel">
          <div class="legend-row" id="chart-legend"></div>
          <div id="timeline-svg-wrap" style="width:100%;overflow:hidden"></div>
          <div style="font-size:0.75rem;color:var(--muted);text-align:center;margin-top:8px" id="chart-footnote"></div>
        </div>

        <div class="section-header">
          <h2 class="section-h2">Funil por origem, taxa de conversão e Scorecard das 4 Frentes</h2>
        </div>
        <div class="card-panel funnel-grid">
          <div style="text-align:center">
            <div style="margin-bottom:8px">
              <span style="border:1px solid var(--text);padding:3px 9px;border-radius:4px;font-size:0.72rem;font-weight:700">ORGANIC + GEO</span>
            </div>
            <div style="font-size:0.86rem;font-weight:600;margin-bottom:8px" id="donut-title"></div>
            <div id="donut-svg-wrap"></div>
          </div>
          <div class="scores-4-grid" id="scores-4"></div>
        </div>
      </section>

      <!-- ========================================================= -->
      <!-- TELA 2: RADAR 6 PILARES, PAUTAS DO MÊS & CATÁLOGO         -->
      <!-- ========================================================= -->
      <section class="screen-view" id="screen-2">
        <div class="section-header" style="margin-top:4px">
          <h2 class="section-h2">Sugestão Editorial — Os 2 Novos Artigos deste Mês</h2>
          <span class="pill pill-indigo">Planejamento Novembro</span>
        </div>
        <div class="cards-grid" id="november-cards" style="grid-template-columns:repeat(auto-fit,minmax(400px,1fr))"></div>

        <div class="section-header">
          <h2 class="section-h2">Radar em Tempo Real — Os 6 Pilares (Clique para filtrar catálogo)</h2>
          <span style="font-size:0.78rem;color:var(--muted)">Resumo executivo + última manchete RSS</span>
        </div>
        <div class="cards-grid" id="pillars"></div>

        <div class="section-header">
          <h2 class="section-h2">Catálogo de Artigos Indexados (<span id="count-label">0</span>)</h2>
        </div>
        <div class="controls">
          <input type="text" class="keep-input" style="flex:1;min-width:220px" id="search" placeholder="Buscar artigo por título, palavra-chave ou slug..." />
          <select class="keep-select" style="width:auto" id="theme-filter">
            <option value="ALL">Todos os 6 Pilares</option>
            <option value="1. Aditivos">1. Aditivos</option>
            <option value="2. Fertilizantes">2. Fertilizantes</option>
            <option value="3. Agro">3. Agro</option>
            <option value="4. Agro Global">4. Agro Global</option>
            <option value="5. Clima e Bioma">5. Clima e Bioma</option>
            <option value="6. Complementares & Entretenimento">6. Complementares & Entretenimento</option>
          </select>
          <select class="keep-select" style="width:auto" id="intent-filter">
            <option value="ALL">Todos os Estágios</option>
            <option value="Topo / Visitas">Topo / Visitas</option>
            <option value="Meio / Intenção">Meio / Intenção</option>
            <option value="Fundo / Produto">Fundo / Produto</option>
          </select>
          <select class="keep-select" style="width:auto" id="lang-filter">
            <option value="pt" selected>Português (PT-BR)</option>
            <option value="en">Inglês (EN)</option>
            <option value="es">Espanhol (ES)</option>
            <option value="ALL">Todos os Idiomas</option>
          </select>
          <button class="btn-keep" onclick="resetFilters()">Limpar</button>
        </div>

        <table>
          <thead>
            <tr>
              <th style="width:95px">Data</th>
              <th>Artigo & URL Indexada</th>
              <th style="width:140px">Funil & Conversão</th>
              <th style="width:170px">Métricas On-Page</th>
              <th style="width:90px">Score</th>
            </tr>
          </thead>
          <tbody id="articles-body"></tbody>
        </table>
      </section>

      <!-- ========================================================= -->
      <!-- TELA 3: FUNÇÃO AI PROMPT EXPLORER & GOOGLE SUGGEST        -->
      <!-- ========================================================= -->
      <section class="screen-view" id="screen-3">
        <div class="section-header" style="margin-top:4px">
          <div>
            <h2 class="section-h2">AI Prompt Explorer & Visibilidade Generativa (Motor OpenSEO)</h2>
            <p style="font-size:0.82rem;color:var(--muted)">Perguntas reais feitas por compradores e agrônomos no ChatGPT, Perplexity, Gemini e Google AI Overviews.</p>
          </div>
          <span class="pill">GEO Intelligence</span>
        </div>

        <table style="margin-bottom:24px">
          <thead>
            <tr>
              <th>Prompt / Pergunta Real nas IAs</th>
              <th style="width:145px">Pilar & Estágio</th>
              <th style="width:155px">Status de Citação</th>
              <th style="width:300px">Diagnóstico & Ação p/ Ganhar a Resposta</th>
            </tr>
          </thead>
          <tbody id="prompts-body"></tbody>
        </table>

        <div class="section-header">
          <div>
            <h2 class="section-h2">Google Autocomplete Harvester (Motor CrawlSEO)</h2>
            <p style="font-size:0.82rem;color:var(--muted)">Buscas de cauda longa extraídas gratuitamente da API oficial de sugestões do Google Brasil.</p>
          </div>
          <span class="pill pill-indigo">Tempo Real</span>
        </div>
        <div class="cards-grid" id="autocomplete-grid"></div>
      </section>

      <!-- ========================================================= -->
      <!-- TELA 4: FUNÇÃO AUDITORIA TÉCNICA, WEB VITALS & CRAWLER    -->
      <!-- ========================================================= -->
      <section class="screen-view" id="screen-4">
        <div class="section-header" style="margin-top:4px">
          <div>
            <h2 class="section-h2">Core Web Vitals & Diagnóstico HTTP (Motor CrawlSEO + web-perf)</h2>
            <p style="font-size:0.82rem;color:var(--muted)">Medição direta de latência de servidor (TTFB), peso de documento, cache de borda e links internos.</p>
          </div>
          <span class="pill pill-ok">Auditoria Ativa</span>
        </div>
        <div class="cards-grid" id="vitals-grid"></div>

        <div class="section-header">
          <h2 class="section-h2">As 5 Correções Prioritárias de Engenharia SEO & GEO</h2>
        </div>
        <div id="audit-list" style="margin-bottom:24px"></div>

        <div class="section-header">
          <div>
            <h2 class="section-h2">Artigos Órfãos de Conversão (Sem Link Interno para Produto/Solução)</h2>
            <p style="font-size:0.82rem;color:var(--muted)">Artigos em Português que atraem tráfego orgânico, mas não possuem nenhum link apontando para <code>/nossas-solucoes/</code> ou contato.</p>
          </div>
          <span class="pill pill-danger" id="orphan-count-pill">0 artigos</span>
        </div>
        <table>
          <thead>
            <tr>
              <th style="width:95px">Data</th>
              <th>Artigo sem Link de Conversão</th>
              <th style="width:140px">Palavras & H2</th>
              <th style="width:220px">Recomendação de Link Interno</th>
            </tr>
          </thead>
          <tbody id="orphans-body"></tbody>
        </table>
      </section>
    </main>
  </div>

  <script>
    const KB = __KB_JSON__;
    let currentBrand = "adfert";
    let currentScreen = 1;
    let chartMode = "pub";

    const SCREEN_TITLES = {
      1: "Dashboard Executivo",
      2: "Radar 6 Pilares & Catálogo Editorial",
      3: "AI Prompt Explorer & Buscas (OpenSEO)",
      4: "Auditoria Técnica & Crawler (CrawlSEO)"
    };

    const SHORT_RADAR = {
      adfert: {
        "1. Aditivos": ["Inibidores NBPT & Proteção de Fósforo", "Foco em Uremax, PhosProtec, CoatMax, Anticaking e Antidusting."],
        "2. Fertilizantes": ["Eficiência NPK & Fertilizantes Líquidos", "Redução de perdas por volatilização e fixação (queda de 10,4% na ANDA)."],
        "3. Agro": ["Recorde em Barter & Margem da Safrinha", "Produtor trava custos via Barter; foco em eficiência por hectare."],
        "4. Agro Global": ["Geopolítica: Egito, EUA, Índia e China", "Projeto Indorama no Egito, subsídios nos EUA e pressão na ureia."],
        "5. Clima e Bioma": ["El Niño Ativo, Biomas & Baixo Carbono", "Risco climático no Cerrado/MATOPIBA, chuva no Sul e créditos de carbono."],
        "6. Complementares & Entretenimento": ["Cultura AgroTech, ESG & Carreira", "Next Impact, equidade salarial, Maio Amarelo e bastidores químicos."]
      },
      intrivia: {
        "1. Aditivos": ["Proteção Fisiológica (Protec Foli) & Foliar", "Escudo contra estresse térmico e abortamento floral na lavoura."],
        "2. Fertilizantes": ["Manejo de Enxofre (S) na Soja e Milho", "Síntese proteica, nodulação e equilíbrio nutricional de alta absorção."],
        "3. Agro": ["Multiculturas: Soja, Café, Milho, Cana e Trigo", "Pauta diversificada cobrindo florada do café, soja, cana e trigo."],
        "4. Agro Global": ["Exportação Recorde de Café & Custos Globais", "Brasil lidera embarques de café e soja em meio a investimentos nos EUA."],
        "5. Clima e Bioma": ["Pico do El Niño: Calor, Seca e Chuva", "Principal pilar atual: manejo de extremos térmicos e hídricos 2026/27."],
        "6. Complementares & Entretenimento": ["Alerta de Clone: 4 Posts da Adfert no Domínio", "Limpeza urgente dos 4 artigos de 2025 herdados do clone da Adfert."]
      }
    };

    function esc(str) {
      return String(str || "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
    }

    function getBrandData() { return KB.brands[currentBrand]; }

    function switchScreen(num) {
      currentScreen = num;
      [1, 2, 3, 4].forEach(n => {
        document.getElementById("screen-" + n).classList.toggle("active", n === num);
        document.getElementById("nav-" + n).classList.toggle("active", n === num);
      });
      document.getElementById("screen-title").textContent = SCREEN_TITLES[num];
      window.scrollTo({ top: 0, behavior: "smooth" });
    }

    function setChartMode(mode) {
      chartMode = mode;
      document.getElementById("chart-mode-pub").classList.toggle("active", mode === "pub");
      document.getElementById("chart-mode-gsc").classList.toggle("active", mode === "gsc");
      renderTimelineChart();
    }

    function openBrandModal() {
      renderBrandModalCards();
      document.getElementById("brand-modal").classList.add("open");
    }

    function closeBrandModal() {
      document.getElementById("brand-modal").classList.remove("open");
    }

    function selectBrand(brandId) {
      currentBrand = brandId;
      document.getElementById("brand-select").value = brandId;
      closeBrandModal();
      resetFilters();
      renderAll();
    }

    function renderBrandModalCards() {
      document.getElementById("brand-cards-container").innerHTML = Object.values(KB.brands).map(b => {
        const sc = b.seo_geo_audit.scores;
        const isSel = b.id === currentBrand;
        return `
          <div class="brand-card ${isSel ? "selected" : ""}" onclick="selectBrand('${b.id}')">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
              <strong style="font-size:1.05rem">${esc(b.name)}</strong>
              <span class="pill">${b.stats.pt_posts} Artigos PT (${b.stats.total_indexed_posts} URLs)</span>
            </div>
            <div style="font-size:0.8rem;color:var(--muted);margin-bottom:10px">${esc(b.tagline)}<br><span style="color:var(--blue)">${esc(b.url)}</span></div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:0.78rem;background:var(--bg);padding:10px;border-radius:8px">
              <div>1. SEO & Canonical: <strong style="color:var(--danger)">${sc.seo_technical}/100</strong></div>
              <div>2. Prontidão GEO: <strong style="color:var(--warn)">${sc.geo_ai_readiness}/100</strong></div>
              <div>3. Autoridade: <strong style="color:var(--ok)">${sc.content_authority}/100</strong></div>
              <div>4. Multilíngue: <strong style="color:var(--blue)">${sc.multilingual_architecture}/100</strong></div>
            </div>
          </div>
        `;
      }).join("");
    }

    function renderTimelineChart() {
      const b = getBrandData();
      const ptArts = b.articles.filter(a => a.lang === "pt");
      const months = ["2025-Q2", "2025-Q3", "2025-Q4", "2026-Q1", "2026-Q2", "2026-Q3", "2026-Q4"];

      function bucket(dateStr) {
        const y = dateStr.slice(0, 4);
        const m = parseInt(dateStr.slice(5, 7), 10);
        const q = Math.ceil(m / 3);
        const key = `${y}-Q${q}`;
        return months.includes(key) ? key : "2025-Q2";
      }

      let s1, s2, s3;
      if (chartMode === "pub") {
        s1 = months.map(m => ptArts.filter(a => bucket(a.date) === m && a.crawl_metrics.intent === "Topo / Visitas").length);
        s2 = months.map(m => ptArts.filter(a => bucket(a.date) === m && a.crawl_metrics.intent === "Meio / Intenção").length);
        s3 = months.map(m => ptArts.filter(a => bucket(a.date) === m && a.crawl_metrics.intent === "Fundo / Produto").length);
        document.getElementById("chart-legend").innerHTML = `
          <span><i class="legend-dot" style="background:var(--blue)"></i>Artigos Topo / Visitas</span>
          <span><i class="legend-dot" style="background:var(--indigo)"></i>Artigos Meio / Intenções</span>
          <span><i class="legend-dot" style="background:#b0b5c0"></i>Artigos Fundo / Produto</span>
        `;
        document.getElementById("chart-footnote").textContent = "Fonte 100% real: histórico trimestral de publicações extraído via API WP-JSON da marca.";
      } else {
        // Curva acumulada proporcional às páginas indexadas + conectores GSC (CrawlSEO)
        let cum = 0;
        s1 = months.map(m => { cum += ptArts.filter(a => bucket(a.date) === m).length; return cum * 38; });
        s2 = s1.map(v => Math.round(v * 0.24));
        s3 = s1.map(v => Math.round(v * 0.06));
        document.getElementById("chart-legend").innerHTML = `
          <span><i class="legend-dot" style="background:var(--blue)"></i>Visitas Orgânicas Estimadas</span>
          <span><i class="legend-dot" style="background:var(--indigo)"></i>Intenções / Cliques Qualificados</span>
          <span><i class="legend-dot" style="background:#b0b5c0"></i>Cliques p/ Soluções (Conversão)</span>
        `;
        document.getElementById("chart-footnote").textContent = "Projeção proporcional ao estoque indexado — conecte a API gratuita do Google Search Console (GSC) no CrawlSEO para substituir pelos cliques diários reais.";
      }

      const maxY = Math.max(6, ...s1, ...s2, ...s3);
      const W = 920, H = 180, padL = 42, padR = 24, padT = 16, padB = 28;
      const plotW = W - padL - padR;
      const plotH = H - padT - padB;

      function smoothPath(arr, color) {
        const pts = arr.map((v, i) => [
          padL + (i / (arr.length - 1)) * plotW,
          padT + plotH - (v / maxY) * plotH
        ]);
        let d = `M ${pts[0][0]} ${pts[0][1]}`;
        for (let i = 0; i < pts.length - 1; i++) {
          const p0 = pts[i], p1 = pts[i + 1];
          const cx = (p0[0] + p1[0]) / 2;
          d += ` C ${cx} ${p0[1]}, ${cx} ${p1[1]}, ${p1[0]} ${p1[1]}`;
        }
        const circles = pts.map(p => `<circle cx="${p[0]}" cy="${p[1]}" r="3.5" fill="${color}" />`).join("");
        return `<path d="${d}" fill="none" stroke="${color}" stroke-width="2.2" />${circles}`;
      }

      const gridLines = [0, 0.25, 0.5, 0.75, 1].map(f => {
        const y = padT + plotH * (1 - f);
        const val = Math.round(maxY * f);
        return `<line x1="${padL}" y1="${y}" x2="${W - padR}" y2="${y}" stroke="#eef0f4" stroke-width="1"/>
                <text x="${padL - 8}" y="${y + 4}" font-size="10" fill="#9ca3af" text-anchor="end">${val}</text>`;
      }).join("");

      const xLabels = months.map((m, i) => {
        const x = padL + (i / (months.length - 1)) * plotW;
        return `<text x="${x}" y="${H - 6}" font-size="10" fill="#6b7280" text-anchor="middle">${m}</text>`;
      }).join("");

      document.getElementById("timeline-svg-wrap").innerHTML = `
        <svg viewBox="0 0 ${W} ${H}" style="width:100%;height:180px;display:block">
          ${gridLines}
          ${smoothPath(s1, "#4b6bfb")}
          ${smoothPath(s2, "#221c7a")}
          ${smoothPath(s3, "#b0b5c0")}
          ${xLabels}
        </svg>
      `;
    }

    function renderScreen1() {
      const b = getBrandData();
      const ptArts = b.articles.filter(a => a.lang === "pt");
      const withProd = ptArts.filter(a => a.crawl_metrics && a.crawl_metrics.product_links > 0).length;
      const prodPct = ptArts.length ? ((withProd / ptArts.length) * 100).toFixed(1) : "0.0";

      const suggestCount = (b.autocomplete || []).reduce((acc, item) => acc + (item.suggestions ? item.suggestions.length : 0), 0);
      const promptCount = (b.ai_prompts || []).length;

      document.getElementById("active-brand-pill").textContent = b.name;
      document.getElementById("avatar-sub").textContent = b.id === "adfert" ? "AD" : "IN";
      document.getElementById("kpi-visitas").textContent = ptArts.length;
      document.getElementById("kpi-visitas-label").textContent = `Artigos PT (${b.stats.total_indexed_posts} URLs Indexadas)`;
      document.getElementById("kpi-intencoes").textContent = suggestCount + promptCount;
      document.getElementById("kpi-intencoes-label").textContent = `Intenções Mapeadas (${suggestCount} Google + ${promptCount} Prompts IA)`;
      document.getElementById("kpi-conversao").textContent = `${withProd}/${ptArts.length}`;
      document.getElementById("kpi-conversao-label").textContent = `Artigos c/ Link p/ Soluções (${prodPct}%)`;

      renderTimelineChart();

      // Donut Chart Funil
      const cTopo = ptArts.filter(a => a.crawl_metrics.intent === "Topo / Visitas").length;
      const cMeio = ptArts.filter(a => a.crawl_metrics.intent === "Meio / Intenção").length;
      const cFundo = ptArts.filter(a => a.crawl_metrics.intent === "Fundo / Produto").length;
      const total = Math.max(1, ptArts.length);
      const r = 54, C = 2 * Math.PI * r;
      const l1 = (cTopo / total) * C;
      const l2 = (cMeio / total) * C;

      document.getElementById("donut-title").innerHTML = `CONVERSÃO P/ PRODUTO <span class="pill pill-danger">!</span> ${prodPct}%`;
      document.getElementById("donut-svg-wrap").innerHTML = `
        <svg width="160" height="160" viewBox="0 0 160 160" style="margin:0 auto;display:block">
          <circle cx="80" cy="80" r="${r}" fill="none" stroke="#d6d6d6" stroke-width="22" />
          <circle cx="80" cy="80" r="${r}" fill="none" stroke="#4b6bfb" stroke-width="22"
            stroke-dasharray="${l1} ${C}" stroke-dashoffset="0" transform="rotate(-90 80 80)" />
          <circle cx="80" cy="80" r="${r}" fill="none" stroke="#221c7a" stroke-width="22"
            stroke-dasharray="${l2} ${C}" stroke-dashoffset="${-l1}" transform="rotate(-90 80 80)" />
          <text x="80" y="76" text-anchor="middle" font-size="18" font-weight="700" fill="#111827">${ptArts.length}</text>
          <text x="80" y="94" text-anchor="middle" font-size="10" fill="#6b7280">Artigos PT</text>
        </svg>
        <div style="font-size:0.76rem;color:var(--muted);margin-top:6px">
          Topo: <strong>${cTopo}</strong> • Meio: <strong>${cMeio}</strong> • Fundo: <strong>${cFundo}</strong>
        </div>
      `;

      const s = b.seo_geo_audit.scores;
      const notes = b.id === "adfert" ? {
        s1: "Canonical hardcoded p/ Home em todas as URLs",
        s2: "0 blocos JSON-LD Schema.org detectados",
        s3: "40 artigos PT + 74 traduções EN/ES",
        s4: "Hreflang ativo; categorias EN/ES trocadas"
      } : {
        s1: "Duplo <title>/canonical + 4 posts clonados da Adfert",
        s2: "Schema como @type: Person em vez de Organization",
        s3: "18 artigos PT (forte em Clima e Multiculturas)",
        s4: "Apenas PT-BR (sem EN/ES e sem hreflang)"
      };
      const scItems = [
        { label: "1. SEO Técnico & Canonical", val: s.seo_technical + "/100", color: "var(--danger)", note: notes.s1 },
        { label: "2. Prontidão GEO (IA Generativa)", val: s.geo_ai_readiness + "/100", color: "var(--warn)", note: notes.s2 },
        { label: "3. Autoridade Temática (6 Pilares)", val: s.content_authority + "/100", color: "var(--ok)", note: notes.s3 },
        { label: "4. Arquitetura Multilíngue", val: s.multilingual_architecture + "/100", color: "var(--blue)", note: notes.s4 }
      ];
      document.getElementById("scores-4").innerHTML = scItems.map(i => `
        <div class="mini-score-box">
          <div style="font-size:0.76rem;color:var(--muted);font-weight:600">${esc(i.label)}</div>
          <div class="mini-score-val" style="color:${i.color}">${esc(i.val)}</div>
          <div style="font-size:0.74rem;color:var(--muted)">${esc(i.note)}</div>
        </div>
      `).join("");
    }

    function renderScreen2() {
      const b = getBrandData();
      document.getElementById("november-cards").innerHTML = (b.november_articles || []).map(na => `
        <div class="item-card">
          <div class="item-top">
            <h3>${esc(na.slot)}</h3>
            <span class="pill pill-indigo">${esc(na.intent)}</span>
          </div>
          <h4>${esc(na.title)}</h4>
          <p>${esc(na.rationale)}</p>
          <div style="font-size:0.76rem;color:var(--indigo);font-weight:600">Produto conectado: ${esc(na.target_product)}</div>
        </div>
      `).join("");

      const currentTheme = document.getElementById("theme-filter").value;
      const ptArticles = b.articles.filter(a => a.lang === "pt");

      document.getElementById("pillars").innerHTML = b.realtime_insights.map(ins => {
        const count = ptArticles.filter(a => a.themes.includes(ins.theme)).length;
        const topLive = (ins.live_headlines && ins.live_headlines.length) ? ins.live_headlines[0] : null;
        const pair = (SHORT_RADAR[b.id] && SHORT_RADAR[b.id][ins.theme]) || [ins.title.slice(0, 45), ins.summary.slice(0, 95)];
        return `
          <div class="item-card clickable ${currentTheme === ins.theme ? "active" : ""}" onclick="selectTheme('${ins.theme}')">
            <div class="item-top">
              <h3>${esc(ins.theme)}</h3>
              <span class="pill">${count} posts</span>
            </div>
            <h4>${esc(pair[0])}</h4>
            <p>${esc(pair[1])}</p>
            <div>${ins.geo_keywords.slice(0, 3).map(k => `<span class="pill pill-indigo" style="margin-right:4px">${esc(k)}</span>`).join("")}</div>
            ${topLive ? `
              <div class="live-line">
                <span style="color:var(--danger);font-weight:700">Ao vivo:</span> <a href="${topLive.link}" target="_blank" rel="noopener" onclick="event.stopPropagation()">${esc(topLive.title.slice(0, 70))}...</a>
              </div>
            ` : ""}
          </div>
        `;
      }).join("");

      renderArticles();
    }

    function selectTheme(theme) {
      const sel = document.getElementById("theme-filter");
      sel.value = (sel.value === theme) ? "ALL" : theme;
      renderScreen2();
    }

    function resetFilters() {
      document.getElementById("search").value = "";
      document.getElementById("theme-filter").value = "ALL";
      document.getElementById("intent-filter").value = "ALL";
      document.getElementById("lang-filter").value = "pt";
      renderScreen2();
    }

    function renderArticles() {
      const b = getBrandData();
      const q = document.getElementById("search").value.toLowerCase();
      const tf = document.getElementById("theme-filter").value;
      const inf = document.getElementById("intent-filter").value;
      const lf = document.getElementById("lang-filter").value;

      const filtered = b.articles.filter(a => {
        if (lf !== "ALL" && a.lang !== lf) return false;
        if (tf !== "ALL" && !a.themes.includes(tf)) return false;
        if (inf !== "ALL" && (!a.crawl_metrics || a.crawl_metrics.intent !== inf)) return false;
        if (q && !(a.title.toLowerCase().includes(q) || a.excerpt.toLowerCase().includes(q) || a.slug.toLowerCase().includes(q))) return false;
        return true;
      });

      document.getElementById("count-label").textContent = filtered.length;
      document.getElementById("articles-body").innerHTML = filtered.map(a => {
        const cm = a.crawl_metrics || { word_count: 0, h2_count: 0, internal_links: 0, product_links: 0, onpage_score: 50, intent: "Topo / Visitas" };
        const intentClass = cm.intent.includes("Fundo") ? "pill-ok" : (cm.intent.includes("Meio") ? "pill-indigo" : "pill");
        const prodBadge = cm.product_links > 0
          ? `<span class="pill pill-ok">${cm.product_links} link produto</span>`
          : `<span class="pill pill-danger">Sem link produto</span>`;
        return `
          <tr>
            <td>
              <div style="font-weight:600">${esc(a.date)}</div>
              <span class="pill" style="margin-top:4px">${esc(a.lang.toUpperCase())}</span>
            </td>
            <td>
              <div style="font-weight:600;margin-bottom:3px"><a href="${a.url}" target="_blank" rel="noopener">${esc(a.title)}</a></div>
              <div style="color:var(--muted);font-size:0.76rem;margin-bottom:5px">${esc(a.excerpt.slice(0, 125))}...</div>
              <div>${a.themes.map(t => `<span class="pill" style="margin-right:4px">${esc(t)}</span>`).join("")}</div>
            </td>
            <td>
              <span class="pill ${intentClass}">${esc(cm.intent)}</span>
              <div style="margin-top:6px">${prodBadge}</div>
            </td>
            <td style="font-size:0.76rem;color:var(--muted)">
              <strong>${cm.word_count}</strong> palavras • <strong>${cm.h2_count}</strong> H2<br>
              <strong>${cm.internal_links}</strong> links int. • <strong>${cm.images_missing_alt || 0}</strong> img s/ alt
            </td>
            <td style="text-align:center">
              <div style="font-size:1.15rem;font-weight:700;color:${cm.onpage_score >= 75 ? 'var(--ok)' : (cm.onpage_score >= 60 ? 'var(--blue)' : 'var(--danger)')}">${cm.onpage_score}</div>
              <div style="font-size:0.68rem;color:var(--muted)">/ 100</div>
            </td>
          </tr>
        `;
      }).join("");
    }

    function renderScreen3() {
      const b = getBrandData();
      document.getElementById("prompts-body").innerHTML = (b.ai_prompts || []).map(p => {
        const stClass = p.status.includes("Gap") ? "pill-danger" : (p.status.includes("Parcial") ? "pill-warn" : "pill-ok");
        return `
          <tr>
            <td style="font-weight:600">${esc(p.prompt)}</td>
            <td>
              <span class="pill">${esc(p.pillar)}</span><br>
              <span class="pill pill-indigo" style="margin-top:4px">${esc(p.intent)}</span>
            </td>
            <td><span class="pill ${stClass}">${esc(p.status)}</span></td>
            <td style="font-size:0.78rem">
              <div style="color:var(--muted);margin-bottom:4px">${esc(p.detail)}</div>
              <div style="color:var(--blue);font-weight:600">${esc(p.action)}</div>
            </td>
          </tr>
        `;
      }).join("");

      document.getElementById("autocomplete-grid").innerHTML = (b.autocomplete || []).map(ac => `
        <div class="item-card">
          <div class="item-top">
            <h3>Busca Base: "${esc(ac.seed)}"</h3>
            <span class="pill pill-indigo">${esc(ac.intent)}</span>
          </div>
          <div style="margin-top:6px">
            ${(ac.suggestions && ac.suggestions.length)
              ? ac.suggestions.map(s => `<div style="font-size:0.8rem;padding:4px 0;border-bottom:1px solid var(--border);color:var(--text)">${esc(s)}</div>`).join("")
              : `<div style="font-size:0.8rem;color:var(--muted)">Sem sugestões retornadas</div>`
            }
          </div>
        </div>
      `).join("");
    }

    function renderScreen4() {
      const b = getBrandData();
      const v = b.vitals || {};
      const ptArts = b.articles.filter(a => a.lang === "pt");
      const avgWords = ptArts.length ? Math.round(ptArts.reduce((s, a) => s + (a.crawl_metrics ? a.crawl_metrics.word_count : 0), 0) / ptArts.length) : 0;
      const orphans = ptArts.filter(a => !a.crawl_metrics || a.crawl_metrics.product_links === 0);

      document.getElementById("vitals-grid").innerHTML = `
        <div class="item-card">
          <h3>Latência de Servidor (TTFB)</h3>
          <div style="font-size:1.65rem;font-weight:700;color:var(--blue);margin:4px 0">${v.ttfb_ms || 0} ms</div>
          <p>Download HTML: ${v.total_load_ms || 0} ms • Borda Cloudflare: <strong>${esc(v.cf_cache)}</strong> (Bom &lt; 800 ms)</p>
        </div>
        <div class="item-card">
          <h3>Peso do Documento & Assets</h3>
          <div style="font-size:1.65rem;font-weight:700;color:var(--indigo);margin:4px 0">${v.html_size_kb || 0} KB</div>
          <p>${v.scripts_count || 0} scripts JS • ${v.stylesheets_count || 0} arquivos CSS • ${v.images_missing_alt || 0}/${v.total_images || 0} imagens sem alt na listagem</p>
        </div>
        <div class="item-card">
          <h3>Artigos Órfãos de Conversão</h3>
          <div style="font-size:1.65rem;font-weight:700;color:var(--danger);margin:4px 0">${orphans.length} de ${ptArts.length}</div>
          <p>Artigos PT sem link para <code>/nossas-solucoes/</code> • Média de <strong>${avgWords} palavras</strong> por post</p>
        </div>
      `;

      document.getElementById("audit-list").innerHTML = b.seo_geo_audit.critical_findings.map(f => {
        const pillClass = f.severity === "CRITICAL" ? "pill-danger" : (f.severity === "HIGH" ? "pill-warn" : "pill");
        return `
          <div class="audit-card">
            <div class="audit-card-head">
              <span class="pill ${pillClass}">${esc(f.severity)}</span>
              <span class="pill pill-indigo">${esc(f.category)}</span>
              <strong style="font-size:0.9rem;color:var(--text)">${esc(f.title)}</strong>
            </div>
            <div style="font-size:0.81rem;color:var(--muted);margin-bottom:4px"><strong>Evidência no código:</strong> ${esc(f.evidence)}</div>
            <div style="font-size:0.81rem;color:var(--ok)"><strong>Plano de ação:</strong> ${esc(f.fix)}</div>
          </div>
        `;
      }).join("");

      document.getElementById("orphan-count-pill").textContent = `${orphans.length} artigos órfãos`;
      document.getElementById("orphans-body").innerHTML = orphans.map(a => {
        const cm = a.crawl_metrics || { word_count: 0, h2_count: 0 };
        const rec = b.id === "adfert"
          ? "Inserir âncora contextual para /nossas-solucoes/ (Uremax / PhosProtec)"
          : "Inserir âncora contextual para /nossas-solucoes/ (Protec Foli / Nutrição)";
        return `
          <tr>
            <td style="font-weight:600">${esc(a.date)}</td>
            <td><a href="${a.url}" target="_blank" rel="noopener">${esc(a.title)}</a></td>
            <td style="color:var(--muted)">${cm.word_count} palavras • ${cm.h2_count} H2</td>
            <td style="color:var(--blue);font-weight:500">${rec}</td>
          </tr>
        `;
      }).join("");
    }

    function renderAll() {
      renderScreen1();
      renderScreen2();
      renderScreen3();
      renderScreen4();
    }

    document.getElementById("search").addEventListener("input", renderArticles);
    document.getElementById("theme-filter").addEventListener("change", () => { renderScreen2(); });
    document.getElementById("intent-filter").addEventListener("change", renderArticles);
    document.getElementById("lang-filter").addEventListener("change", renderArticles);

    renderAll();
  </script>
</body>
</html>
"""

(base_dir / "dashboard.html").write_text(template.replace("__KB_JSON__", kb_json_str), encoding="utf-8")
print("4-screen Keep dashboard with Impeccable craft rules built successfully!")
