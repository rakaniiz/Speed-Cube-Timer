import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="ChronoCube",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        #MainMenu, header, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] {
            display: none !important;
        }
        html, body, [data-testid="stAppViewContainer"], .main, .block-container {
            padding: 0 !important;
            margin: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            max-width: 100vw !important;
            overflow: hidden !important;
        }
        iframe {
            position: fixed !important;
            inset: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            border: none !important;
            z-index: 9999 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

HTML_APP = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>ChronoCube</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root {
    --bg-core: #07090f;
    --bg-glow-1: rgba(56, 189, 248, 0.14);
    --bg-glow-2: rgba(99, 102, 241, 0.12);
    --glass: rgba(15, 20, 32, 0.65);
    --glass-strong: rgba(12, 16, 26, 0.92);
    --surface: rgba(255, 255, 255, 0.05);
    --surface-hover: rgba(255, 255, 255, 0.1);
    --border: rgba(255, 255, 255, 0.12);
    --text: #f8fafc;
    --muted: #94a3b8;
    --accent: #38bdf8;
    --accent-glow: rgba(56, 189, 248, 0.35);
    --amber: #f59e0b;
    --amber-glow: rgba(245, 158, 11, 0.35);
    --green: #10b981;
    --green-glow: rgba(16, 185, 129, 0.4);
    --red: #ef4444;
  }

  body[data-theme="galaxy"] {
    --bg-core: #060412;
    --bg-glow-1: rgba(168, 85, 247, 0.25);
    --bg-glow-2: rgba(59, 130, 246, 0.22);
    --accent: #c084fc;
    --accent-glow: rgba(192, 132, 252, 0.4);
  }

  body[data-theme="inferno"] {
    --bg-core: #110403;
    --bg-glow-1: rgba(249, 115, 22, 0.26);
    --bg-glow-2: rgba(225, 29, 72, 0.22);
    --accent: #fb923c;
    --accent-glow: rgba(251, 146, 60, 0.4);
  }

  body[data-theme="arctic"] {
    --bg-core: #041017;
    --bg-glow-1: rgba(34, 211, 238, 0.22);
    --bg-glow-2: rgba(56, 189, 248, 0.18);
    --accent: #22d3ee;
    --accent-glow: rgba(34, 211, 238, 0.38);
  }

  body[data-theme="cyber"] {
    --bg-core: #050811;
    --bg-glow-1: rgba(236, 72, 153, 0.24);
    --bg-glow-2: rgba(16, 185, 129, 0.18);
    --accent: #f472b6;
    --accent-glow: rgba(244, 114, 182, 0.4);
  }

  body[data-theme="emerald"] {
    --bg-core: #030e09;
    --bg-glow-1: rgba(16, 185, 129, 0.24);
    --bg-glow-2: rgba(5, 150, 105, 0.18);
    --accent: #34d399;
    --accent-glow: rgba(52, 211, 153, 0.38);
  }

  body[data-theme="solar"] {
    --bg-core: #100b03;
    --bg-glow-1: rgba(245, 158, 11, 0.24);
    --bg-glow-2: rgba(234, 179, 8, 0.18);
    --accent: #fbbf24;
    --accent-glow: rgba(251, 191, 36, 0.38);
  }

  body[data-theme="sakura"] {
    --bg-core: #12060c;
    --bg-glow-1: rgba(244, 114, 182, 0.24);
    --bg-glow-2: rgba(251, 113, 133, 0.2);
    --accent: #f9a8d4;
    --accent-glow: rgba(249, 168, 212, 0.38);
  }

  body[data-theme="void"] {
    --bg-core: #070410;
    --bg-glow-1: rgba(124, 58, 237, 0.26);
    --bg-glow-2: rgba(79, 70, 229, 0.2);
    --accent: #a78bfa;
    --accent-glow: rgba(167, 139, 250, 0.4);
  }

  body[data-theme="crimson"] {
    --bg-core: #120305;
    --bg-glow-1: rgba(220, 38, 38, 0.26);
    --bg-glow-2: rgba(153, 27, 27, 0.22);
    --accent: #f87171;
    --accent-glow: rgba(248, 113, 113, 0.4);
  }

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    user-select: none;
  }

  html, body {
    width: 100%;
    height: 100%;
    overflow: hidden;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: var(--bg-core);
    color: var(--text);
  }

  body {
    display: flex;
    flex-direction: column;
    position: relative;
  }

  #bgCanvas {
    position: fixed;
    inset: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    pointer-events: none;
  }

  .ambient-orb {
    position: fixed;
    border-radius: 50%;
    filter: blur(95px);
    pointer-events: none;
    z-index: 0;
    animation: drift 14s ease-in-out infinite alternate;
  }
  .orb-1 {
    width: 500px;
    height: 500px;
    background: var(--bg-glow-1);
    top: -120px;
    left: 14%;
  }
  .orb-2 {
    width: 460px;
    height: 460px;
    background: var(--bg-glow-2);
    bottom: -140px;
    right: 12%;
    animation-delay: -7s;
  }

  @keyframes drift {
    0% { transform: translate(0, 0) scale(1); }
    100% { transform: translate(35px, 25px) scale(1.08); }
  }

  header {
    position: relative;
    z-index: 15;
    width: 100%;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    padding: 12px 20px;
    background: var(--glass);
    backdrop-filter: blur(18px);
    border-bottom: 1px solid var(--border);
    gap: 10px;
    transition: opacity 0.25s ease;
  }

  .brand {
    display: flex;
    align-items: center;
    gap: 9px;
    font-weight: 700;
    letter-spacing: 0.08em;
    font-size: 0.88rem;
  }
  .brand-dot {
    width: 10px;
    height: 10px;
    border-radius: 3px;
    background: var(--accent);
    box-shadow: 0 0 14px var(--accent-glow);
    transform: rotate(15deg);
  }

  .scramble-wrap {
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .scramble-box {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.96rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    padding: 8px 14px;
    border-radius: 10px;
    background: var(--surface);
    border: 1px solid var(--border);
    cursor: pointer;
    transition: all 0.16s ease;
  }
  .scramble-box:hover {
    background: var(--surface-hover);
    border-color: var(--accent);
    box-shadow: 0 0 18px var(--accent-glow);
  }

  .nav-group {
    display: flex;
    align-items: center;
    gap: 7px;
  }

  .pill-btn {
    background: var(--surface);
    color: var(--muted);
    border: 1px solid var(--border);
    padding: 6px 11px;
    border-radius: 9px;
    font-size: 0.8rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s ease;
  }
  .pill-btn:hover {
    background: var(--surface-hover);
    color: var(--text);
  }
  .pill-btn.active {
    color: var(--text);
    border-color: var(--accent);
    background: rgba(255, 255, 255, 0.09);
    box-shadow: 0 0 12px var(--accent-glow);
  }

  .icon-btn {
    font-size: 1rem;
    padding: 5px 10px;
    line-height: 1.1;
  }

  main {
    position: relative;
    z-index: 5;
    flex: 1;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 16px;
  }

  .focus-banner {
    padding: 5px 14px;
    border-radius: 999px;
    background: rgba(245, 158, 11, 0.14);
    border: 1px solid rgba(245, 158, 11, 0.4);
    color: var(--amber);
    font-size: 0.76rem;
    margin-bottom: 12px;
    opacity: 0;
    transition: opacity 0.18s ease;
  }
  body.unfocused .focus-banner { opacity: 1; }

  .timer-display {
    font-family: 'JetBrains Mono', monospace;
    font-size: clamp(4.2rem, 12vw, 8.8rem);
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1;
    text-shadow: 0 8px 36px rgba(0, 0, 0, 0.45);
    transition: color 0.12s ease, text-shadow 0.12s ease, transform 0.12s ease;
  }
  .timer-display.holding {
    color: var(--amber);
    text-shadow: 0 0 34px var(--amber-glow);
    transform: scale(0.985);
  }
  .timer-display.armed {
    color: var(--green);
    text-shadow: 0 0 42px var(--green-glow);
    transform: scale(1.015);
  }
  .timer-display.dnf { color: var(--red); }

  .progress-track {
    width: 280px;
    max-width: 80vw;
    height: 6px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 999px;
    overflow: hidden;
    margin-top: 20px;
    border: 1px solid rgba(255, 255, 255, 0.06);
  }
  .progress-fill {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #d97706, var(--amber));
    border-radius: 999px;
  }
  .progress-fill.armed {
    background: linear-gradient(90deg, #059669, var(--green));
    box-shadow: 0 0 16px var(--green-glow);
  }

  .sensors {
    display: flex;
    gap: 12px;
    margin-top: 18px;
  }

  .sensor {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 7px 16px;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 600;
    background: var(--glass);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border);
    color: var(--muted);
    transition: all 0.12s ease;
  }
  .sensor-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--muted);
  }
  .sensor.down {
    border-color: var(--amber);
    color: var(--amber);
    background: rgba(245, 158, 11, 0.13);
    box-shadow: 0 0 18px var(--amber-glow);
  }
  .sensor.down .sensor-dot {
    background: var(--amber);
    box-shadow: 0 0 8px var(--amber);
  }
  .sensor.armed {
    border-color: var(--green);
    color: var(--green);
    background: rgba(16, 185, 129, 0.16);
    box-shadow: 0 0 22px var(--green-glow);
  }
  .sensor.armed .sensor-dot {
    background: var(--green);
    box-shadow: 0 0 10px var(--green);
  }

  .hint {
    margin-top: 13px;
    font-size: 0.8rem;
    color: var(--muted);
    text-align: center;
  }

  .post-actions {
    display: flex;
    gap: 8px;
    margin-top: 18px;
    opacity: 0;
    pointer-events: none;
    transform: translateY(6px);
    transition: all 0.18s ease;
  }
  .post-actions.visible {
    opacity: 1;
    pointer-events: auto;
    transform: translateY(0);
  }

  .stats-dock {
    position: absolute;
    bottom: 18px;
    display: flex;
    gap: 20px;
    padding: 9px 20px;
    border-radius: 13px;
    background: var(--glass);
    backdrop-filter: blur(16px);
    border: 1px solid var(--border);
    font-size: 0.8rem;
    color: var(--muted);
    transition: opacity 0.25s ease;
  }
  .stats-dock b {
    font-family: 'JetBrains Mono', monospace;
    color: var(--text);
    margin-left: 5px;
    font-weight: 700;
  }

  .drawer {
    position: fixed;
    top: 58px;
    right: 0;
    bottom: 0;
    width: 330px;
    max-width: 90vw;
    background: var(--glass-strong);
    backdrop-filter: blur(22px);
    border-left: 1px solid var(--border);
    transform: translateX(100%);
    transition: transform 0.22s cubic-bezier(0.22, 1, 0.36, 1);
    display: flex;
    flex-direction: column;
    z-index: 25;
  }
  .drawer.open { transform: translateX(0); }

  .drawer-head {
    padding: 14px 16px;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.86rem;
    font-weight: 600;
  }

  .solve-list {
    flex: 1;
    overflow-y: auto;
    padding: 10px;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .solve-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 11px;
    border-radius: 9px;
    background: var(--surface);
    border: 1px solid transparent;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.83rem;
  }
  .solve-item.star {
    border-color: rgba(251, 191, 36, 0.45);
    background: rgba(251, 191, 36, 0.08);
  }

  .solve-actions { display: flex; gap: 4px; }
  .mini-btn {
    background: transparent;
    border: 1px solid var(--border);
    color: var(--muted);
    border-radius: 6px;
    padding: 2px 6px;
    font-size: 0.7rem;
    cursor: pointer;
  }
  .mini-btn:hover { color: var(--text); border-color: var(--accent); }

  .modal-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(2, 6, 14, 0.74);
    backdrop-filter: blur(8px);
    display: none;
    align-items: center;
    justify-content: center;
    z-index: 40;
  }
  .modal-backdrop.open { display: flex; }

  .modal {
    width: 440px;
    max-width: 94vw;
    background: #0f1422;
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 18px;
    display: flex;
    flex-direction: column;
    gap: 13px;
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.65);
  }

  .modal-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.85rem;
    color: var(--muted);
  }

  /* Theme Grid */
  .theme-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
  }
  .theme-card {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 9px 12px;
    border-radius: 10px;
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--text);
    font-size: 0.82rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s ease;
    text-align: left;
  }
  .theme-card:hover {
    background: var(--surface-hover);
    border-color: rgba(255, 255, 255, 0.25);
  }
  .theme-card.active {
    border-color: var(--accent);
    background: rgba(255, 255, 255, 0.1);
    box-shadow: 0 0 14px var(--accent-glow);
  }
  .theme-swatch {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    flex-shrink: 0;
    border: 1px solid rgba(255, 255, 255, 0.35);
  }

  /* 27-Cubie Real 3D Rubik's Cube */
  .cube-stage {
    width: 100%;
    height: 260px;
    display: flex;
    align-items: center;
    justify-content: center;
    perspective: 820px;
    background: radial-gradient(circle at center, rgba(255,255,255,0.04), rgba(0,0,0,0.45));
    border-radius: 13px;
    border: 1px solid var(--border);
    cursor: grab;
    overflow: hidden;
  }
  .cube-stage:active { cursor: grabbing; }

  .cube-world {
    width: 0;
    height: 0;
    position: relative;
    transform-style: preserve-3d;
    transform: rotateX(-26deg) rotateY(-36deg);
  }

  .cubie {
    position: absolute;
    width: 46px;
    height: 46px;
    margin-left: -23px;
    margin-top: -23px;
    transform-style: preserve-3d;
  }

  .cubie-face {
    position: absolute;
    width: 46px;
    height: 46px;
    background: #0c0e14;
    border: 1px solid #050609;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    backface-visibility: hidden;
  }
  .cf-U { transform: rotateX(90deg) translateZ(23px); }
  .cf-D { transform: rotateX(-90deg) translateZ(23px); }
  .cf-F { transform: translateZ(23px); }
  .cf-B { transform: rotateY(180deg) translateZ(23px); }
  .cf-L { transform: rotateY(-90deg) translateZ(23px); }
  .cf-R { transform: rotateY(90deg) translateZ(23px); }

  .sticker-tile {
    width: 38px;
    height: 38px;
    border-radius: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 800;
    color: rgba(0, 0, 0, 0.55);
    box-shadow:
      inset 0 2px 3px rgba(255, 255, 255, 0.45),
      inset 0 -2px 4px rgba(0, 0, 0, 0.25);
  }

  .move-desc {
    text-align: center;
    font-size: 0.82rem;
    color: var(--accent);
    font-weight: 600;
    min-height: 18px;
  }

  .move-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    justify-content: center;
  }
  .move-pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.76rem;
    padding: 4px 8px;
    border-radius: 6px;
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--muted);
    cursor: pointer;
  }
  .move-pill.done { color: var(--text); border-color: rgba(255, 255, 255, 0.24); }
  .move-pill.current {
    background: var(--accent);
    color: #050811;
    font-weight: 700;
    border-color: var(--accent);
  }

  body.running header,
  body.running .stats-dock,
  body.running .post-actions {
    opacity: 0;
    pointer-events: none;
  }
</style>
</head>
<body data-theme="galaxy">

<canvas id="bgCanvas"></canvas>
<div class="ambient-orb orb-1"></div>
<div class="ambient-orb orb-2"></div>

<header>
  <div class="brand"><span class="brand-dot"></span>CHRONOCUBE</div>
  <div class="scramble-wrap">
    <div class="scramble-box" id="scrambleDisplay" title="Click to preview 3D scramble"></div>
    <button class="pill-btn" id="newScrambleBtn" title="New Scramble">↻</button>
  </div>
  <div class="nav-group">
    <button class="pill-btn icon-btn" id="themesBtn" title="Themes">🎨</button>
    <button class="pill-btn" id="configBtn">⚙ Keys</button>
    <button class="pill-btn" id="drawerBtn">Solves (<span id="solveCount">0</span>)</button>
  </div>
</header>

<main id="stage" tabindex="0">
  <div class="focus-banner">Click anywhere on the timer once to focus keyboard input</div>
  <div class="timer-display" id="timerDisplay">0.000</div>
  <div class="progress-track"><div class="progress-fill" id="progressFill"></div></div>
  <div class="sensors">
    <div class="sensor" id="sensorLeft"><span class="sensor-dot"></span><span id="sensorLeftLabel">Left Alt</span></div>
    <div class="sensor" id="sensorRight"><span class="sensor-dot"></span><span id="sensorRightLabel">Right Alt</span></div>
  </div>
  <div class="hint" id="hintText">Hold both keys until green, release to start • Press both keys to stop</div>

  <div class="post-actions" id="postActions">
    <button class="pill-btn" id="btnPlus2">+2</button>
    <button class="pill-btn" id="btnDnf">DNF</button>
    <button class="pill-btn" id="btnStar">★ Highlight</button>
    <button class="pill-btn" id="btnDeleteLast" style="color:#f87171;">Delete Run</button>
  </div>

  <div class="stats-dock">
    <span>PB:<b id="statPb">-</b></span>
    <span>Ao5:<b id="statAo5">-</b></span>
    <span>Ao12:<b id="statAo12">-</b></span>
    <span>Mean:<b id="statMean">-</b></span>
  </div>
</main>

<aside class="drawer" id="drawer">
  <div class="drawer-head">
    <span>Session Solves</span>
    <div style="display:flex;gap:6px;">
      <button class="pill-btn" id="filterStarBtn" style="padding:4px 8px;font-size:0.74rem;">★ Only</button>
      <button class="pill-btn" id="clearAllBtn" style="padding:4px 8px;font-size:0.74rem;">Clear All</button>
    </div>
  </div>
  <div class="solve-list" id="solveList"></div>
</aside>

<!-- Themes Modal -->
<div class="modal-backdrop" id="themesModal">
  <div class="modal" style="width:410px;">
    <div style="display:flex;justify-content:space-between;align-items:center;">
      <span style="font-weight:600;font-size:0.95rem;">🎨 Select Theme</span>
      <button class="pill-btn" id="closeThemesBtn" style="padding:4px 9px;">✕</button>
    </div>
    <div class="theme-grid" id="themeGrid">
      <button class="theme-card" data-theme="obsidian"><span class="theme-swatch" style="background:linear-gradient(135deg,#0f172a,#38bdf8);"></span>Obsidian</button>
      <button class="theme-card" data-theme="galaxy"><span class="theme-swatch" style="background:linear-gradient(135deg,#3b0764,#c084fc);"></span>Galaxy</button>
      <button class="theme-card" data-theme="inferno"><span class="theme-swatch" style="background:linear-gradient(135deg,#7c2d12,#fb923c);"></span>Inferno</button>
      <button class="theme-card" data-theme="arctic"><span class="theme-swatch" style="background:linear-gradient(135deg,#083344,#22d3ee);"></span>Arctic</button>
      <button class="theme-card" data-theme="cyber"><span class="theme-swatch" style="background:linear-gradient(135deg,#831843,#10b981);"></span>Cyberpunk</button>
      <button class="theme-card" data-theme="emerald"><span class="theme-swatch" style="background:linear-gradient(135deg,#064e3b,#34d399);"></span>Emerald Matrix</button>
      <button class="theme-card" data-theme="solar"><span class="theme-swatch" style="background:linear-gradient(135deg,#78350f,#fbbf24);"></span>Solar Gold</button>
      <button class="theme-card" data-theme="sakura"><span class="theme-swatch" style="background:linear-gradient(135deg,#701a75,#f9a8d4);"></span>Sakura</button>
      <button class="theme-card" data-theme="void"><span class="theme-swatch" style="background:linear-gradient(135deg,#2e1065,#8b5cf6);"></span>Void Purple</button>
      <button class="theme-card" data-theme="crimson"><span class="theme-swatch" style="background:linear-gradient(135deg,#7f1d1d,#f87171);"></span>Crimson Blood</button>
    </div>
  </div>
</div>

<!-- Key Configuration Modal -->
<div class="modal-backdrop" id="configModal">
  <div class="modal" style="width:380px;">
    <div style="font-weight:600;font-size:0.95rem;">Trigger Key Settings</div>
    <div class="modal-row">
      <span>Left Key</span>
      <button class="pill-btn" id="bindLeftBtn">AltLeft</button>
    </div>
    <div class="modal-row">
      <span>Right Key</span>
      <button class="pill-btn" id="bindRightBtn">AltRight</button>
    </div>
    <div class="modal-row">
      <span>Hold Delay</span>
      <div style="display:flex;gap:6px;">
        <button class="pill-btn delay-btn" data-ms="300">0.30s</button>
        <button class="pill-btn delay-btn active" data-ms="450">0.45s</button>
        <button class="pill-btn delay-btn" data-ms="650">0.65s</button>
      </div>
    </div>
    <div style="display:flex;justify-content:space-between;margin-top:6px;">
      <button class="pill-btn" id="resetKeysBtn">Reset Defaults</button>
      <button class="pill-btn active" id="closeConfigBtn">Done</button>
    </div>
  </div>
</div>

<!-- 3D Scramble Visualizer Modal -->
<div class="modal-backdrop" id="visModal">
  <div class="modal" style="width:500px;">
    <div style="display:flex;justify-content:space-between;align-items:center;">
      <span style="font-weight:600;font-size:0.92rem;">3D Scramble Guide (White Top, Green Front)</span>
      <button class="pill-btn" id="closeVisBtn" style="padding:4px 9px;">✕</button>
    </div>
    <div class="cube-stage" id="cubeStage">
      <div class="cube-world" id="cubeWorld"></div>
    </div>
    <div class="move-desc" id="moveDesc">Solved — Press Play or Step Forward</div>
    <div class="move-pills" id="movePills"></div>
    <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;">
      <div style="display:flex;gap:6px;">
        <button class="pill-btn" id="visResetBtn">⏮</button>
        <button class="pill-btn" id="visPrevBtn">◀</button>
        <button class="pill-btn active" id="visPlayBtn">▶ Play</button>
        <button class="pill-btn" id="visNextBtn">▶|</button>
      </div>
      <div style="display:flex;gap:4px;">
        <button class="pill-btn speed-btn" data-turn="750" data-pause="1400">0.5x</button>
        <button class="pill-btn speed-btn active" data-turn="480" data-pause="950">1x</button>
        <button class="pill-btn speed-btn" data-turn="260" data-pause="520">1.5x</button>
      </div>
    </div>
  </div>
</div>

<script>
(() => {
  const STORAGE_SOLVES = "cc_v6_solves";
  const STORAGE_CFG = "cc_v6_cfg";

  let cfg = { leftKey: "AltLeft", rightKey: "AltRight", holdMs: 450, theme: "galaxy" };
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_CFG));
    if (saved) cfg = { ...cfg, ...saved };
  } catch (e) {}

  let solves = [];
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_SOLVES));
    if (Array.isArray(saved)) solves = saved;
  } catch (e) {}

  // Ambient Particle Canvas
  const canvas = document.getElementById("bgCanvas");
  const ctx = canvas.getContext("2d");
  let particles = [];
  function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  window.addEventListener("resize", resizeCanvas);
  resizeCanvas();

  for (let i = 0; i < 48; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      r: Math.random() * 1.8 + 0.6,
      vx: (Math.random() - 0.5) * 0.28,
      vy: (Math.random() - 0.5) * 0.28,
      a: Math.random() * 0.45 + 0.1
    });
  }

  function drawParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const colorMap = {
      obsidian: "148, 163, 184",
      galaxy: "192, 132, 252",
      inferno: "251, 146, 60",
      arctic: "34, 211, 238",
      cyber: "244, 114, 182",
      emerald: "52, 211, 153",
      solar: "251, 191, 36",
      sakura: "249, 168, 212",
      void: "167, 139, 250",
      crimson: "248, 113, 113"
    };
    const rgb = colorMap[cfg.theme] || colorMap.galaxy;
    for (const p of particles) {
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0) p.x = canvas.width;
      if (p.x > canvas.width) p.x = 0;
      if (p.y < 0) p.y = canvas.height;
      if (p.y > canvas.height) p.y = 0;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${rgb}, ${p.a})`;
      ctx.fill();
    }
  }

  // Timer State Machine
  let phase = "IDLE";
  let leftDown = false;
  let rightDown = false;
  let holdStart = 0;
  let runStart = 0;
  let lastRunId = null;
  let currentScramble = "";
  let bindingTarget = null;
  let blockUntilRelease = false;
  let starOnly = false;

  const timerEl = document.getElementById("timerDisplay");
  const fillEl = document.getElementById("progressFill");
  const sensorLeftEl = document.getElementById("sensorLeft");
  const sensorRightEl = document.getElementById("sensorRight");
  const scrambleEl = document.getElementById("scrambleDisplay");
  const postActionsEl = document.getElementById("postActions");
  const solveListEl = document.getElementById("solveList");
  const solveCountEl = document.getElementById("solveCount");

  function prettyKey(code) {
    const map = {
      AltLeft: "Left Alt",
      AltRight: "Right Alt",
      ControlLeft: "Left Ctrl",
      ControlRight: "Right Ctrl",
      ShiftLeft: "Left Shift",
      ShiftRight: "Right Shift"
    };
    return map[code] || code;
  }

  function formatMs(ms, penalty) {
    if (penalty === "DNF") return "DNF";
    const total = Math.max(0, Math.floor(ms + (penalty === "+2" ? 2000 : 0)));
    const mins = Math.floor(total / 60000);
    const secs = Math.floor((total % 60000) / 1000);
    const millis = String(total % 1000).padStart(3, "0");
    if (mins > 0) {
      return mins + ":" + String(secs).padStart(2, "0") + "." + millis + (penalty === "+2" ? "+" : "");
    }
    return secs + "." + millis + (penalty === "+2" ? "+" : "");
  }

  function newScramble() {
    const faces = ["U", "D", "L", "R", "F", "B"];
    const axis = { U: 0, D: 0, L: 1, R: 1, F: 2, B: 2 };
    const mods = ["", "'", "2"];
    const out = [];
    let lastFace = "";
    let prevAxis = -1;
    while (out.length < 20) {
      const f = faces[Math.floor(Math.random() * faces.length)];
      if (f === lastFace) continue;
      if (out.length >= 2 && axis[f] === prevAxis && axis[f] === axis[lastFace]) continue;
      prevAxis = axis[lastFace] ?? -1;
      lastFace = f;
      out.push(f + mods[Math.floor(Math.random() * mods.length)]);
    }
    currentScramble = out.join(" ");
    scrambleEl.textContent = currentScramble;
  }

  function syncLabels() {
    document.body.dataset.theme = cfg.theme;
    document.querySelectorAll(".theme-card").forEach(b => {
      b.classList.toggle("active", b.dataset.theme === cfg.theme);
    });
    document.getElementById("sensorLeftLabel").textContent = prettyKey(cfg.leftKey);
    document.getElementById("sensorRightLabel").textContent = prettyKey(cfg.rightKey);
    document.getElementById("bindLeftBtn").textContent = cfg.leftKey;
    document.getElementById("bindRightBtn").textContent = cfg.rightKey;
    document.querySelectorAll(".delay-btn").forEach(b => {
      b.classList.toggle("active", Number(b.dataset.ms) === cfg.holdMs);
    });
  }

  function saveCfg() {
    localStorage.setItem(STORAGE_CFG, JSON.stringify(cfg));
    syncLabels();
  }

  function saveSolves() {
    localStorage.setItem(STORAGE_SOLVES, JSON.stringify(solves));
    renderSolves();
  }

  function updateSensors() {
    const armed = phase === "ARMED";
    sensorLeftEl.className = "sensor" + (leftDown ? (armed ? " armed" : " down") : "");
    sensorRightEl.className = "sensor" + (rightDown ? (armed ? " armed" : " down") : "");
  }

  function resetHoldUI() {
    phase = "IDLE";
    holdStart = 0;
    fillEl.style.width = "0%";
    fillEl.classList.remove("armed");
    timerEl.classList.remove("holding", "armed");
    updateSensors();
  }

  function startRun() {
    phase = "RUNNING";
    runStart = performance.now();
    document.body.classList.add("running");
    postActionsEl.classList.remove("visible");
    fillEl.style.width = "0%";
    fillEl.classList.remove("armed");
    timerEl.classList.remove("holding", "armed", "dnf");
    leftDown = false;
    rightDown = false;
    updateSensors();
  }

  function stopRun() {
    const elapsed = performance.now() - runStart;
    phase = "IDLE";
    blockUntilRelease = true;
    document.body.classList.remove("running");
    timerEl.textContent = formatMs(elapsed, null);
    updateSensors();

    const id = Date.now();
    lastRunId = id;
    solves.unshift({
      id,
      ms: elapsed,
      penalty: null,
      star: false,
      scramble: currentScramble
    });
    saveSolves();
    postActionsEl.classList.add("visible");
    newScramble();
  }

  function tick(now) {
    drawParticles();
    if (phase === "HOLDING") {
      const pct = Math.min(100, ((now - holdStart) / cfg.holdMs) * 100);
      fillEl.style.width = pct + "%";
      if (pct >= 100) {
        phase = "ARMED";
        fillEl.classList.add("armed");
        timerEl.classList.remove("holding");
        timerEl.classList.add("armed");
        updateSensors();
      }
    } else if (phase === "RUNNING") {
      timerEl.textContent = formatMs(now - runStart, null);
    }
    requestAnimationFrame(tick);
  }

  function detectKeysOnDown(e) {
    let hitLeft = e.code === cfg.leftKey;
    let hitRight = e.code === cfg.rightKey;

    if (cfg.leftKey === "AltLeft" && e.key === "Alt" && e.location === 1) hitLeft = true;
    if (cfg.rightKey === "AltRight") {
      if ((e.key === "Alt" && e.location === 2) || e.key === "AltGraph") hitRight = true;
      if (e.getModifierState && e.getModifierState("AltGraph")) hitRight = true;
    }
    return { hitLeft, hitRight };
  }

  function handleKeyDown(e) {
    if (bindingTarget) {
      e.preventDefault();
      e.stopPropagation();
      if (bindingTarget === "left") cfg.leftKey = e.code;
      if (bindingTarget === "right") cfg.rightKey = e.code;
      bindingTarget = null;
      saveCfg();
      return;
    }

    const { hitLeft, hitRight } = detectKeysOnDown(e);
    if (hitLeft || hitRight || e.code === "Space" || e.key === "Alt" || e.key === "AltGraph") {
      e.preventDefault();
      e.stopPropagation();
    }

    if (blockUntilRelease) return;

    // Update leftDown / rightDown consistently in both IDLE and RUNNING states
    if (
      e.code === "ControlLeft" &&
      cfg.leftKey !== "ControlLeft" &&
      (hitRight || (e.getModifierState && e.getModifierState("AltGraph")))
    ) {
      if (hitRight) rightDown = true;
    } else {
      if (hitLeft) leftDown = true;
      if (hitRight) rightDown = true;
    }

    if (cfg.leftKey === "AltLeft" && cfg.rightKey === "AltRight" && e.getModifierState) {
      if (e.getModifierState("AltGraph")) rightDown = true;
    }

    // Dual-hand stop: require BOTH keys down to end the run
    if (phase === "RUNNING") {
      if (leftDown && rightDown) {
        stopRun();
      }
      return;
    }

    // Dual-hand start: require BOTH keys down to arm
    if (leftDown && rightDown && phase === "IDLE") {
      phase = "HOLDING";
      holdStart = performance.now();
      timerEl.textContent = "0.000";
      timerEl.classList.remove("dnf");
      timerEl.classList.add("holding");
    }

    updateSensors();
  }

  function handleKeyUp(e) {
    let relLeft = e.code === cfg.leftKey || (cfg.leftKey === "AltLeft" && e.key === "Alt" && e.location === 1);
    let relRight =
      e.code === cfg.rightKey ||
      (cfg.rightKey === "AltRight" &&
        ((e.key === "Alt" && e.location === 2) ||
          e.key === "AltGraph" ||
          (e.code === "ControlLeft" && rightDown && !(e.getModifierState && e.getModifierState("AltGraph")))));

    if (relLeft || relRight || e.code === "Space" || e.key === "Alt" || e.key === "AltGraph") {
      e.preventDefault();
      e.stopPropagation();
    }

    if (relLeft) leftDown = false;
    if (relRight) rightDown = false;

    if (blockUntilRelease) {
      if (!leftDown && !rightDown) blockUntilRelease = false;
      updateSensors();
      return;
    }

    if (phase === "RUNNING") return;

    if (phase === "ARMED" && (!leftDown || !rightDown)) {
      startRun();
      return;
    }

    if (phase === "HOLDING" && (!leftDown || !rightDown)) {
      resetHoldUI();
      return;
    }

    updateSensors();
  }

  window.addEventListener("keydown", handleKeyDown, true);
  window.addEventListener("keyup", handleKeyUp, true);

  window.addEventListener("blur", () => {
    document.body.classList.add("unfocused");
    leftDown = false;
    rightDown = false;
    blockUntilRelease = false;
    if (phase === "HOLDING" || phase === "ARMED") resetHoldUI();
  });

  window.addEventListener("focus", () => document.body.classList.remove("unfocused"));
  document.addEventListener("pointerdown", () => document.body.classList.remove("unfocused"));

  // Stats & History
  function calcAvg(list, n) {
    if (list.length < n) return "-";
    const slice = list.slice(0, n).map(s => (s.penalty === "DNF" ? Infinity : s.ms + (s.penalty === "+2" ? 2000 : 0)));
    const dnfs = slice.filter(v => !Number.isFinite(v)).length;
    if (dnfs >= 2) return "DNF";
    slice.sort((a, b) => a - b);
    const trimmed = slice.slice(1, n - 1);
    return formatMs(trimmed.reduce((a, b) => a + b, 0) / trimmed.length, null);
  }

  function renderSolves() {
    solveCountEl.textContent = solves.length;
    const valid = solves.filter(s => s.penalty !== "DNF").map(s => s.ms + (s.penalty === "+2" ? 2000 : 0));
    document.getElementById("statPb").textContent = valid.length ? formatMs(Math.min(...valid), null) : "-";
    document.getElementById("statAo5").textContent = calcAvg(solves, 5);
    document.getElementById("statAo12").textContent = calcAvg(solves, 12);
    document.getElementById("statMean").textContent = valid.length
      ? formatMs(valid.reduce((a, b) => a + b, 0) / valid.length, null)
      : "-";

    const shown = starOnly ? solves.filter(s => s.star) : solves;
    solveListEl.innerHTML = shown
      .map(s => {
        const realIdx = solves.findIndex(x => x.id === s.id);
        return `
          <div class="solve-item ${s.star ? "star" : ""}">
            <span>#${solves.length - realIdx} &nbsp;<b>${formatMs(s.ms, s.penalty)}</b></span>
            <div class="solve-actions">
              <button class="mini-btn" onclick="window._ccAct(${s.id}, 'plus2')">+2</button>
              <button class="mini-btn" onclick="window._ccAct(${s.id}, 'dnf')">DNF</button>
              <button class="mini-btn" onclick="window._ccAct(${s.id}, 'star')">★</button>
              <button class="mini-btn" onclick="window._ccAct(${s.id}, 'del')">×</button>
            </div>
          </div>
        `;
      })
      .join("");
  }

  window._ccAct = (id, action) => {
    const idx = solves.findIndex(s => s.id === id);
    if (idx === -1) return;
    if (action === "del") {
      solves.splice(idx, 1);
      if (id === lastRunId) {
        lastRunId = null;
        timerEl.textContent = "0.000";
        postActionsEl.classList.remove("visible");
      }
    } else if (action === "plus2") {
      solves[idx].penalty = solves[idx].penalty === "+2" ? null : "+2";
      if (id === lastRunId) timerEl.textContent = formatMs(solves[idx].ms, solves[idx].penalty);
    } else if (action === "dnf") {
      solves[idx].penalty = solves[idx].penalty === "DNF" ? null : "DNF";
      if (id === lastRunId) {
        timerEl.textContent = formatMs(solves[idx].ms, solves[idx].penalty);
        timerEl.classList.toggle("dnf", solves[idx].penalty === "DNF");
      }
    } else if (action === "star") {
      solves[idx].star = !solves[idx].star;
    }
    saveSolves();
  };

  // True 27-Cubie 3D Rubik's Cube Engine with Layer Turn Animations
  const FACE_HEX = {
    U: "#f8fafc",
    D: "#facc15",
    F: "#22c55e",
    B: "#3b82f6",
    L: "#f97316",
    R: "#ef4444"
  };

  const MOVE_TEXT = {
    U: "Top Layer (White) — 90° Clockwise",
    "U'": "Top Layer (White) — 90° Counter-Clockwise",
    U2: "Top Layer (White) — 180° Half Turn",
    D: "Bottom Layer (Yellow) — 90° Clockwise",
    "D'": "Bottom Layer (Yellow) — 90° Counter-Clockwise",
    D2: "Bottom Layer (Yellow) — 180° Half Turn",
    R: "Right Layer (Red) — 90° Clockwise",
    "R'": "Right Layer (Red) — 90° Counter-Clockwise",
    R2: "Right Layer (Red) — 180° Half Turn",
    L: "Left Layer (Orange) — 90° Clockwise",
    "L'": "Left Layer (Orange) — 90° Counter-Clockwise",
    L2: "Left Layer (Orange) — 180° Half Turn",
    F: "Front Layer (Green) — 90° Clockwise",
    "F'": "Front Layer (Green) — 90° Counter-Clockwise",
    F2: "Front Layer (Green) — 180° Half Turn",
    B: "Back Layer (Blue) — 90° Clockwise",
    "B'": "Back Layer (Blue) — 90° Counter-Clockwise",
    B2: "Back Layer (Blue) — 180° Half Turn"
  };

  const cubeWorld = document.getElementById("cubeWorld");
  const moveDescEl = document.getElementById("moveDesc");
  const SPACING = 47;
  let cubies = [];
  let visMoves = [];
  let visStep = 0;
  let isAnimating = false;
  let autoTimer = null;
  let turnMs = 480;
  let pauseMs = 950;
  let rotX = -26;
  let rotY = -36;

  function buildSolvedCubies() {
    cubeWorld.innerHTML = "";
    cubies = [];
    for (let x = -1; x <= 1; x++) {
      for (let y = -1; y <= 1; y++) {
        for (let z = -1; z <= 1; z++) {
          const el = document.createElement("div");
          el.className = "cubie";
          const stickers = {};
          if (y === -1) stickers.U = "U";
          if (y === 1) stickers.D = "D";
          if (z === 1) stickers.F = "F";
          if (z === -1) stickers.B = "B";
          if (x === -1) stickers.L = "L";
          if (x === 1) stickers.R = "R";

          const isCenter = Math.abs(x) + Math.abs(y) + Math.abs(z) === 1;
          for (const f of ["U", "D", "F", "B", "L", "R"]) {
            const faceDiv = document.createElement("div");
            faceDiv.className = "cubie-face cf-" + f;
            if (stickers[f]) {
              const tile = document.createElement("div");
              tile.className = "sticker-tile";
              tile.style.background = FACE_HEX[stickers[f]];
              if (isCenter) tile.textContent = f;
              faceDiv.appendChild(tile);
            }
            el.appendChild(faceDiv);
          }

          const cubieObj = {
            x,
            y,
            z,
            mat: [1, 0, 0, 0, 1, 0, 0, 0, 1],
            el
          };
          updateCubieTransform(cubieObj);
          cubeWorld.appendChild(el);
          cubies.push(cubieObj);
        }
      }
    }
  }

  function updateCubieTransform(c) {
    const m = c.mat;
    const tx = c.x * SPACING;
    const ty = c.y * SPACING;
    const tz = c.z * SPACING;
    c.el.style.transform =
      `matrix3d(${m[0]},${m[3]},${m[6]},0, ${m[1]},${m[4]},${m[7]},0, ${m[2]},${m[5]},${m[8]},0, ${tx},${ty},${tz},1)`;
  }

  function matMul(a, b) {
    return [
      a[0]*b[0] + a[1]*b[3] + a[2]*b[6],
      a[0]*b[1] + a[1]*b[4] + a[2]*b[7],
      a[0]*b[2] + a[1]*b[5] + a[2]*b[8],
      a[3]*b[0] + a[4]*b[3] + a[5]*b[6],
      a[3]*b[1] + a[4]*b[4] + a[5]*b[7],
      a[3]*b[2] + a[4]*b[5] + a[5]*b[8],
      a[6]*b[0] + a[7]*b[3] + a[8]*b[6],
      a[6]*b[1] + a[7]*b[4] + a[8]*b[7],
      a[6]*b[2] + a[7]*b[5] + a[8]*b[8]
    ];
  }

  function rotMatrix(axis, deg) {
    const rad = (deg * Math.PI) / 180;
    const c = Math.round(Math.cos(rad));
    const s = Math.round(Math.sin(rad));
    if (axis === "x") return [1, 0, 0, 0, c, -s, 0, s, c];
    if (axis === "y") return [c, 0, s, 0, 1, 0, -s, 0, c];
    return [c, -s, 0, s, c, 0, 0, 0, 1];
  }

  function parseMoveSpec(mv) {
    const f = mv[0];
    const dir = mv.endsWith("'") ? -1 : 1;
    const mult = mv.endsWith("2") ? 2 : 1;
    if (f === "U") return { axis: "y", filter: c => c.y === -1, deg: -90 * dir * mult };
    if (f === "D") return { axis: "y", filter: c => c.y === 1, deg: 90 * dir * mult };
    if (f === "R") return { axis: "x", filter: c => c.x === 1, deg: 90 * dir * mult };
    if (f === "L") return { axis: "x", filter: c => c.x === -1, deg: -90 * dir * mult };
    if (f === "F") return { axis: "z", filter: c => c.z === 1, deg: 90 * dir * mult };
    return { axis: "z", filter: c => c.z === -1, deg: -90 * dir * mult };
  }

  function commitMoveInstant(mv) {
    const spec = parseMoveSpec(mv);
    const R = rotMatrix(spec.axis, spec.deg);
    for (const c of cubies) {
      if (!spec.filter(c)) continue;
      const nx = Math.round(R[0] * c.x + R[1] * c.y + R[2] * c.z);
      const ny = Math.round(R[3] * c.x + R[4] * c.y + R[5] * c.z);
      const nz = Math.round(R[6] * c.x + R[7] * c.y + R[8] * c.z);
      c.x = nx;
      c.y = ny;
      c.z = nz;
      c.mat = matMul(R, c.mat);
      updateCubieTransform(c);
    }
  }

  function syncMovePills() {
    document.querySelectorAll(".move-pill").forEach((p, idx) => {
      p.classList.toggle("done", idx < visStep);
      p.classList.toggle("current", idx === visStep - 1);
    });
    if (visStep === 0) {
      moveDescEl.textContent = "Solved — Press Play or Step Forward";
    } else {
      const m = visMoves[visStep - 1];
      moveDescEl.textContent = `Step ${visStep}/${visMoves.length}: ${m} — ${MOVE_TEXT[m] || ""}`;
    }
  }

  function animateSingleMove(mv, onDone) {
    if (isAnimating) return;
    isAnimating = true;
    const spec = parseMoveSpec(mv);
    const layer = cubies.filter(spec.filter);

    const pivot = document.createElement("div");
    pivot.style.position = "absolute";
    pivot.style.transformStyle = "preserve-3d";
    pivot.style.transition = `transform ${turnMs}ms cubic-bezier(0.25, 0.85, 0.35, 1)`;
    pivot.style.transform = "rotate3d(0,0,0,0deg)";
    cubeWorld.appendChild(pivot);
    layer.forEach(c => pivot.appendChild(c.el));

    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        if (spec.axis === "x") pivot.style.transform = `rotateX(${spec.deg}deg)`;
        else if (spec.axis === "y") pivot.style.transform = `rotateY(${spec.deg}deg)`;
        else pivot.style.transform = `rotateZ(${spec.deg}deg)`;
      });
    });

    setTimeout(() => {
      layer.forEach(c => cubeWorld.appendChild(c.el));
      pivot.remove();
      commitMoveInstant(mv);
      isAnimating = false;
      if (onDone) onDone();
    }, turnMs + 25);
  }

  function stopAutoPlay() {
    if (autoTimer) {
      clearTimeout(autoTimer);
      autoTimer = null;
    }
    document.getElementById("visPlayBtn").textContent = "▶ Play";
  }

  function jumpToStep(target) {
    stopAutoPlay();
    if (isAnimating) return;
    buildSolvedCubies();
    for (let i = 0; i < target; i++) commitMoveInstant(visMoves[i]);
    visStep = target;
    syncMovePills();
  }

  function scheduleNextAuto() {
    if (visStep >= visMoves.length) {
      stopAutoPlay();
      return;
    }
    const mv = visMoves[visStep];
    visStep++;
    syncMovePills();
    animateSingleMove(mv, () => {
      if (!autoTimer) return;
      autoTimer = setTimeout(scheduleNextAuto, pauseMs);
    });
  }

  function openVisualizer() {
    stopAutoPlay();
    visMoves = currentScramble.split(" ").filter(Boolean);
    visStep = 0;
    buildSolvedCubies();
    const pillsEl = document.getElementById("movePills");
    pillsEl.innerHTML = visMoves
      .map((m, idx) => `<span class="move-pill" data-idx="${idx + 1}">${m}</span>`)
      .join("");
    pillsEl.querySelectorAll(".move-pill").forEach(p => {
      p.addEventListener("click", () => jumpToStep(Number(p.dataset.idx)));
    });
    syncMovePills();
    document.getElementById("visModal").classList.add("open");
  }

  // Drag-to-orbit 3D Cube
  const cubeStage = document.getElementById("cubeStage");
  let dragging = false;
  let lastX = 0;
  let lastY = 0;
  cubeStage.addEventListener("pointerdown", e => {
    dragging = true;
    lastX = e.clientX;
    lastY = e.clientY;
  });
  window.addEventListener("pointermove", e => {
    if (!dragging) return;
    rotY += (e.clientX - lastX) * 0.6;
    rotX -= (e.clientY - lastY) * 0.6;
    lastX = e.clientX;
    lastY = e.clientY;
    cubeWorld.style.transform = `rotateX(${rotX}deg) rotateY(${rotY}deg)`;
  });
  window.addEventListener("pointerup", () => (dragging = false));

  document.getElementById("visResetBtn").addEventListener("click", () => jumpToStep(0));
  document.getElementById("visPrevBtn").addEventListener("click", () => {
    if (visStep > 0) jumpToStep(visStep - 1);
  });
  document.getElementById("visNextBtn").addEventListener("click", () => {
    stopAutoPlay();
    if (isAnimating || visStep >= visMoves.length) return;
    const mv = visMoves[visStep];
    visStep++;
    syncMovePills();
    animateSingleMove(mv);
  });

  document.getElementById("visPlayBtn").addEventListener("click", () => {
    if (autoTimer) {
      stopAutoPlay();
      return;
    }
    if (isAnimating) return;
    if (visStep >= visMoves.length) jumpToStep(0);
    document.getElementById("visPlayBtn").textContent = "⏸ Pause";
    autoTimer = setTimeout(scheduleNextAuto, 120);
  });

  document.querySelectorAll(".speed-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      turnMs = Number(btn.dataset.turn);
      pauseMs = Number(btn.dataset.pause);
      document.querySelectorAll(".speed-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
    });
  });

  document.getElementById("closeVisBtn").addEventListener("click", () => {
    stopAutoPlay();
    document.getElementById("visModal").classList.remove("open");
  });

  // UI Wiring
  document.querySelectorAll("button").forEach(btn => btn.addEventListener("focus", () => btn.blur()));
  scrambleEl.addEventListener("click", openVisualizer);
  document.getElementById("newScrambleBtn").addEventListener("click", newScramble);

  // Themes Modal
  const themesModal = document.getElementById("themesModal");
  document.getElementById("themesBtn").addEventListener("click", () => themesModal.classList.add("open"));
  document.getElementById("closeThemesBtn").addEventListener("click", () => themesModal.classList.remove("open"));
  themesModal.addEventListener("click", e => {
    if (e.target === themesModal) themesModal.classList.remove("open");
  });

  document.querySelectorAll(".theme-card").forEach(btn => {
    btn.addEventListener("click", () => {
      cfg.theme = btn.dataset.theme;
      saveCfg();
    });
  });

  document.getElementById("drawerBtn").addEventListener("click", () => {
    document.getElementById("drawer").classList.toggle("open");
  });

  document.getElementById("filterStarBtn").addEventListener("click", e => {
    starOnly = !starOnly;
    e.target.classList.toggle("active", starOnly);
    renderSolves();
  });

  document.getElementById("clearAllBtn").addEventListener("click", () => {
    solves = [];
    lastRunId = null;
    timerEl.textContent = "0.000";
    postActionsEl.classList.remove("visible");
    saveSolves();
  });

  document.getElementById("btnPlus2").addEventListener("click", () => lastRunId && window._ccAct(lastRunId, "plus2"));
  document.getElementById("btnDnf").addEventListener("click", () => lastRunId && window._ccAct(lastRunId, "dnf"));
  document.getElementById("btnStar").addEventListener("click", () => lastRunId && window._ccAct(lastRunId, "star"));
  document.getElementById("btnDeleteLast").addEventListener("click", () => lastRunId && window._ccAct(lastRunId, "del"));

  const modal = document.getElementById("configModal");
  document.getElementById("configBtn").addEventListener("click", () => modal.classList.add("open"));
  document.getElementById("closeConfigBtn").addEventListener("click", () => {
    bindingTarget = null;
    modal.classList.remove("open");
    syncLabels();
  });

  document.getElementById("bindLeftBtn").addEventListener("click", e => {
    bindingTarget = "left";
    e.target.textContent = "Press any key...";
  });

  document.getElementById("bindRightBtn").addEventListener("click", e => {
    bindingTarget = "right";
    e.target.textContent = "Press any key...";
  });

  document.querySelectorAll(".delay-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      cfg.holdMs = Number(btn.dataset.ms);
      saveCfg();
    });
  });

  document.getElementById("resetKeysBtn").addEventListener("click", () => {
    cfg.leftKey = "AltLeft";
    cfg.rightKey = "AltRight";
    cfg.holdMs = 450;
    bindingTarget = null;
    saveCfg();
  });

  syncLabels();
  newScramble();
  renderSolves();
  requestAnimationFrame(tick);
})();
</script>
</body>
</html>
"""

components.html(HTML_APP, height=900, scrolling=False)
