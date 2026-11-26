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
        #MainMenu, header, footer { visibility: hidden; }
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }
        iframe {
            display: block;
            width: 100vw !important;
            height: 100vh !important;
            border: none !important;
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
    --glass: rgba(15, 20, 32, 0.62);
    --glass-strong: rgba(12, 16, 26, 0.88);
    --surface: rgba(255, 255, 255, 0.045);
    --surface-hover: rgba(255, 255, 255, 0.09);
    --border: rgba(255, 255, 255, 0.11);
    --text: #f8fafc;
    --muted: #94a3b8;
    --accent: #38bdf8;
    --accent-glow: rgba(56, 189, 248, 0.35);
    --amber: #f59e0b;
    --amber-glow: rgba(245, 158, 11, 0.35);
    --green: #10b981;
    --green-glow: rgba(16, 185, 129, 0.4);
    --red: #ef4444;
    --gold: #fbbf24;
  }

  body[data-theme="galaxy"] {
    --bg-core: #060412;
    --bg-glow-1: rgba(168, 85, 247, 0.24);
    --bg-glow-2: rgba(59, 130, 246, 0.2);
    --accent: #c084fc;
    --accent-glow: rgba(192, 132, 252, 0.4);
  }

  body[data-theme="inferno"] {
    --bg-core: #110403;
    --bg-glow-1: rgba(249, 115, 22, 0.25);
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
    --bg-glow-1: rgba(236, 72, 153, 0.22);
    --bg-glow-2: rgba(16, 185, 129, 0.18);
    --accent: #f472b6;
    --accent-glow: rgba(244, 114, 182, 0.4);
  }

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    user-select: none;
  }

  body {
    height: 100vh;
    overflow: hidden;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: var(--bg-core);
    color: var(--text);
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
    width: 520px;
    height: 520px;
    background: var(--bg-glow-1);
    top: -120px;
    left: 15%;
  }
  .orb-2 {
    width: 480px;
    height: 480px;
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
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 24px;
    background: var(--glass);
    backdrop-filter: blur(18px);
    border-bottom: 1px solid var(--border);
    gap: 14px;
    transition: opacity 0.25s ease, transform 0.25s ease;
  }

  .brand {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 700;
    letter-spacing: 0.08em;
    font-size: 0.9rem;
    color: var(--text);
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
    gap: 8px;
  }

  .scramble-box {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.02rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    padding: 9px 18px;
    border-radius: 12px;
    background: var(--surface);
    border: 1px solid var(--border);
    cursor: pointer;
    transition: all 0.16s ease;
  }
  .scramble-box:hover {
    background: var(--surface-hover);
    border-color: var(--accent);
    box-shadow: 0 0 20px var(--accent-glow);
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
    padding: 7px 13px;
    border-radius: 10px;
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
    box-shadow: 0 0 14px var(--accent-glow);
  }

  main {
    position: relative;
    z-index: 5;
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
  }

  .focus-banner {
    padding: 6px 14px;
    border-radius: 999px;
    background: rgba(245, 158, 11, 0.14);
    border: 1px solid rgba(245, 158, 11, 0.4);
    color: var(--amber);
    font-size: 0.78rem;
    font-weight: 500;
    margin-bottom: 14px;
    opacity: 0;
    transform: translateY(-4px);
    transition: all 0.18s ease;
  }
  body.unfocused .focus-banner {
    opacity: 1;
    transform: translateY(0);
  }

  .timer-display {
    font-family: 'JetBrains Mono', monospace;
    font-size: clamp(4.6rem, 13vw, 9.2rem);
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
  .timer-display.dnf {
    color: var(--red);
  }

  .progress-track {
    width: 290px;
    height: 6px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 999px;
    overflow: hidden;
    margin-top: 22px;
    border: 1px solid rgba(255, 255, 255, 0.06);
  }
  .progress-fill {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #d97706, var(--amber));
    border-radius: 999px;
    transition: background 0.12s ease;
  }
  .progress-fill.armed {
    background: linear-gradient(90deg, #059669, var(--green));
    box-shadow: 0 0 16px var(--green-glow);
  }

  .sensors {
    display: flex;
    gap: 14px;
    margin-top: 20px;
  }

  .sensor {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 18px;
    border-radius: 999px;
    font-size: 0.82rem;
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
    transition: all 0.12s ease;
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
    margin-top: 14px;
    font-size: 0.82rem;
    color: var(--muted);
    letter-spacing: 0.01em;
  }

  .post-actions {
    display: flex;
    gap: 8px;
    margin-top: 20px;
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
    bottom: 22px;
    display: flex;
    gap: 22px;
    padding: 10px 22px;
    border-radius: 14px;
    background: var(--glass);
    backdrop-filter: blur(16px);
    border: 1px solid var(--border);
    font-size: 0.82rem;
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
    top: 63px;
    right: 0;
    bottom: 0;
    width: 340px;
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
    padding: 15px 18px;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.88rem;
    font-weight: 600;
  }

  .solve-list {
    flex: 1;
    overflow-y: auto;
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 7px;
  }

  .solve-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 9px 12px;
    border-radius: 10px;
    background: var(--surface);
    border: 1px solid transparent;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
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
    padding: 3px 6px;
    font-size: 0.72rem;
    cursor: pointer;
  }
  .mini-btn:hover { color: var(--text); border-color: var(--accent); }

  .modal-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(2, 6, 14, 0.72);
    backdrop-filter: blur(8px);
    display: none;
    align-items: center;
    justify-content: center;
    z-index: 40;
  }
  .modal-backdrop.open { display: flex; }

  .modal {
    width: 420px;
    max-width: 92vw;
    background: #0f1422;
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 15px;
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.65);
  }

  .modal-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.86rem;
    color: var(--muted);
  }

  /* 3D Cube Visualizer */
  .cube-stage {
    width: 100%;
    height: 230px;
    display: flex;
    align-items: center;
    justify-content: center;
    perspective: 700px;
    background: rgba(0, 0, 0, 0.28);
    border-radius: 12px;
    border: 1px solid var(--border);
    cursor: grab;
  }
  .cube-stage:active { cursor: grabbing; }

  .cube-3d {
    width: 132px;
    height: 132px;
    position: relative;
    transform-style: preserve-3d;
    transform: rotateX(-26deg) rotateY(-36deg);
  }

  .cube-face {
    position: absolute;
    width: 132px;
    height: 132px;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 4px;
    padding: 5px;
    background: #0b0d12;
    border-radius: 8px;
    border: 2px solid #050608;
  }
  .face-U { transform: rotateX(90deg) translateZ(66px); }
  .face-D { transform: rotateX(-90deg) translateZ(66px); }
  .face-F { transform: translateZ(66px); }
  .face-B { transform: rotateY(180deg) translateZ(66px); }
  .face-L { transform: rotateY(-90deg) translateZ(66px); }
  .face-R { transform: rotateY(90deg) translateZ(66px); }

  .sticker {
    border-radius: 4px;
    box-shadow: inset 0 1px 2px rgba(255, 255, 255, 0.35);
  }

  .move-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    justify-content: center;
  }
  .move-pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    padding: 4px 8px;
    border-radius: 6px;
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--muted);
    cursor: pointer;
  }
  .move-pill.done { color: var(--text); border-color: rgba(255, 255, 255, 0.22); }
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
    <button class="pill-btn theme-btn" data-theme="obsidian">Obsidian</button>
    <button class="pill-btn theme-btn active" data-theme="galaxy">Galaxy</button>
    <button class="pill-btn theme-btn" data-theme="inferno">Inferno</button>
    <button class="pill-btn theme-btn" data-theme="arctic">Arctic</button>
    <button class="pill-btn theme-btn" data-theme="cyber">Cyber</button>
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
  <div class="hint" id="hintText">Hold both keys together until green, release to start • Space to stop</div>

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
      <button class="pill-btn" id="filterStarBtn" style="padding:4px 8px;font-size:0.75rem;">★ Only</button>
      <button class="pill-btn" id="clearAllBtn" style="padding:4px 8px;font-size:0.75rem;">Clear All</button>
    </div>
  </div>
  <div class="solve-list" id="solveList"></div>
</aside>

<!-- Key Configuration Modal -->
<div class="modal-backdrop" id="configModal">
  <div class="modal">
    <div style="font-weight:600;font-size:0.96rem;">Trigger Key Settings</div>
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
  <div class="modal" style="width:480px;">
    <div style="display:flex;justify-content:space-between;align-items:center;">
      <span style="font-weight:600;font-size:0.95rem;">3D Scramble Guide (White Top, Green Front)</span>
      <button class="pill-btn" id="closeVisBtn" style="padding:4px 9px;">✕</button>
    </div>
    <div class="cube-stage" id="cubeStage">
      <div class="cube-3d" id="cube3d">
        <div class="cube-face face-U" id="faceU"></div>
        <div class="cube-face face-D" id="faceD"></div>
        <div class="cube-face face-F" id="faceF"></div>
        <div class="cube-face face-B" id="faceB"></div>
        <div class="cube-face face-L" id="faceL"></div>
        <div class="cube-face face-R" id="faceR"></div>
      </div>
    </div>
    <div class="move-pills" id="movePills"></div>
    <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;">
      <div style="display:flex;gap:6px;">
        <button class="pill-btn" id="visResetBtn">⏮</button>
        <button class="pill-btn" id="visPrevBtn">◀</button>
        <button class="pill-btn active" id="visPlayBtn">▶ Play</button>
        <button class="pill-btn" id="visNextBtn">▶|</button>
      </div>
      <div style="display:flex;gap:4px;">
        <button class="pill-btn speed-btn" data-ms="1400">0.5x</button>
        <button class="pill-btn speed-btn active" data-ms="950">1x</button>
        <button class="pill-btn speed-btn" data-ms="550">1.5x</button>
      </div>
    </div>
  </div>
</div>

<script>
(() => {
  const STORAGE_SOLVES = "cc_v4_solves";
  const STORAGE_CFG = "cc_v4_cfg";

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

  for (let i = 0; i < 42; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      r: Math.random() * 1.8 + 0.6,
      vx: (Math.random() - 0.5) * 0.25,
      vy: (Math.random() - 0.5) * 0.25,
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
      cyber: "244, 114, 182"
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

  // State machine: IDLE | HOLDING | ARMED | RUNNING
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
    document.querySelectorAll(".theme-btn").forEach(b => {
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

  // Multi-signal detection so Left Alt + Right Alt (and Windows/Turkish Q AltGr) work simultaneously
  function detectKeysOnDown(e) {
    let hitLeft = false;
    let hitRight = false;

    if (e.code === cfg.leftKey) hitLeft = true;
    if (e.code === cfg.rightKey) hitRight = true;

    // Fallback by physical key location for Alt keys when OS swaps AltGr / Alt codes
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
    const isAltOrSpace = hitLeft || hitRight || e.code === "Space" || e.key === "Alt" || e.key === "AltGraph";

    if (isAltOrSpace) {
      e.preventDefault();
      e.stopPropagation();
    }

    if (phase === "RUNNING") {
      if (!e.repeat && (e.code === "Space" || hitLeft || hitRight)) {
        stopRun();
      }
      return;
    }

    if (blockUntilRelease) return;

    // Ignore Windows synthetic ControlLeft generated by Right Alt (AltGr)
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

    // Also sync modifier state in case first Alt event was swallowed while focusing
    if (cfg.leftKey === "AltLeft" && cfg.rightKey === "AltRight" && e.getModifierState) {
      if (e.getModifierState("AltGraph")) rightDown = true;
    }

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
      if (!leftDown && !rightDown && e.code !== "Space") {
        blockUntilRelease = false;
      }
      updateSensors();
      return;
    }

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

  // 3D Cube State Engine (WCA: U=White, D=Yellow, F=Green, B=Blue, L=Orange, R=Red)
  const COLORS = {
    U: "#f8fafc",
    D: "#facc15",
    F: "#22c55e",
    B: "#3b82f6",
    L: "#f97316",
    R: "#ef4444"
  };

  function solvedCube() {
    return {
      U: Array(9).fill("U"),
      D: Array(9).fill("D"),
      F: Array(9).fill("F"),
      B: Array(9).fill("B"),
      L: Array(9).fill("L"),
      R: Array(9).fill("R")
    };
  }

  function rotCW(arr) {
    return [arr[6], arr[3], arr[0], arr[7], arr[4], arr[1], arr[8], arr[5], arr[2]];
  }

  function applyQuarter(c, face) {
    c[face] = rotCW(c[face]);
    const t = [0, 0, 0];
    if (face === "U") {
      for (let i = 0; i < 3; i++) t[i] = c.F[i];
      for (let i = 0; i < 3; i++) c.F[i] = c.R[i];
      for (let i = 0; i < 3; i++) c.R[i] = c.B[i];
      for (let i = 0; i < 3; i++) c.B[i] = c.L[i];
      for (let i = 0; i < 3; i++) c.L[i] = t[i];
    } else if (face === "D") {
      for (let i = 0; i < 3; i++) t[i] = c.F[6 + i];
      for (let i = 0; i < 3; i++) c.F[6 + i] = c.L[6 + i];
      for (let i = 0; i < 3; i++) c.L[6 + i] = c.B[6 + i];
      for (let i = 0; i < 3; i++) c.B[6 + i] = c.R[6 + i];
      for (let i = 0; i < 3; i++) c.R[6 + i] = t[i];
    } else if (face === "R") {
      const idx = [2, 5, 8], bIdx = [6, 3, 0];
      for (let i = 0; i < 3; i++) t[i] = c.U[idx[i]];
      for (let i = 0; i < 3; i++) c.U[idx[i]] = c.F[idx[i]];
      for (let i = 0; i < 3; i++) c.F[idx[i]] = c.D[idx[i]];
      for (let i = 0; i < 3; i++) c.D[idx[i]] = c.B[bIdx[i]];
      for (let i = 0; i < 3; i++) c.B[bIdx[i]] = t[i];
    } else if (face === "L") {
      const idx = [0, 3, 6], bIdx = [8, 5, 2];
      for (let i = 0; i < 3; i++) t[i] = c.U[idx[i]];
      for (let i = 0; i < 3; i++) c.U[idx[i]] = c.B[bIdx[i]];
      for (let i = 0; i < 3; i++) c.B[bIdx[i]] = c.D[idx[i]];
      for (let i = 0; i < 3; i++) c.D[idx[i]] = c.F[idx[i]];
      for (let i = 0; i < 3; i++) c.F[idx[i]] = t[i];
    } else if (face === "F") {
      const u = [6, 7, 8], r = [0, 3, 6], d = [2, 1, 0], l = [8, 5, 2];
      for (let i = 0; i < 3; i++) t[i] = c.U[u[i]];
      for (let i = 0; i < 3; i++) c.U[u[i]] = c.L[l[i]];
      for (let i = 0; i < 3; i++) c.L[l[i]] = c.D[d[i]];
      for (let i = 0; i < 3; i++) c.D[d[i]] = c.R[r[i]];
      for (let i = 0; i < 3; i++) c.R[r[i]] = t[i];
    } else if (face === "B") {
      const u = [2, 1, 0], l = [0, 3, 6], d = [6, 7, 8], r = [8, 5, 2];
      for (let i = 0; i < 3; i++) t[i] = c.U[u[i]];
      for (let i = 0; i < 3; i++) c.U[u[i]] = c.R[r[i]];
      for (let i = 0; i < 3; i++) c.R[r[i]] = c.D[d[i]];
      for (let i = 0; i < 3; i++) c.D[d[i]] = c.L[l[i]];
      for (let i = 0; i < 3; i++) c.L[l[i]] = t[i];
    }
  }

  function applyMove(c, mv) {
    const face = mv[0];
    const turns = mv.endsWith("2") ? 2 : mv.endsWith("'") ? 3 : 1;
    for (let i = 0; i < turns; i++) applyQuarter(c, face);
  }

  let visMoves = [];
  let visStep = 0;
  let visTimer = null;
  let visSpeed = 950;
  let rotX = -26;
  let rotY = -36;

  function render3DCube() {
    const c = solvedCube();
    for (let i = 0; i < visStep; i++) applyMove(c, visMoves[i]);
    for (const f of ["U", "D", "F", "B", "L", "R"]) {
      const el = document.getElementById("face" + f);
      el.innerHTML = c[f]
        .map(code => `<div class="sticker" style="background:${COLORS[code]}"></div>`)
        .join("");
    }
    document.querySelectorAll(".move-pill").forEach((p, idx) => {
      p.classList.toggle("done", idx < visStep);
      p.classList.toggle("current", idx === visStep - 1);
    });
  }

  function stopVisPlay() {
    if (visTimer) {
      clearInterval(visTimer);
      visTimer = null;
    }
    document.getElementById("visPlayBtn").textContent = "▶ Play";
  }

  function openVisualizer() {
    stopVisPlay();
    visMoves = currentScramble.split(" ").filter(Boolean);
    visStep = 0;
    const pillsEl = document.getElementById("movePills");
    pillsEl.innerHTML = visMoves
      .map((m, idx) => `<span class="move-pill" data-idx="${idx + 1}">${m}</span>`)
      .join("");
    pillsEl.querySelectorAll(".move-pill").forEach(p => {
      p.addEventListener("click", () => {
        stopVisPlay();
        visStep = Number(p.dataset.idx);
        render3DCube();
      });
    });
    render3DCube();
    document.getElementById("visModal").classList.add("open");
  }

  const cubeStage = document.getElementById("cubeStage");
  const cube3d = document.getElementById("cube3d");
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
    cube3d.style.transform = `rotateX(${rotX}deg) rotateY(${rotY}deg)`;
  });
  window.addEventListener("pointerup", () => (dragging = false));

  document.getElementById("visResetBtn").addEventListener("click", () => {
    stopVisPlay();
    visStep = 0;
    render3DCube();
  });
  document.getElementById("visPrevBtn").addEventListener("click", () => {
    stopVisPlay();
    visStep = Math.max(0, visStep - 1);
    render3DCube();
  });
  document.getElementById("visNextBtn").addEventListener("click", () => {
    stopVisPlay();
    visStep = Math.min(visMoves.length, visStep + 1);
    render3DCube();
  });
  document.getElementById("visPlayBtn").addEventListener("click", () => {
    if (visTimer) {
      stopVisPlay();
      return;
    }
    if (visStep >= visMoves.length) visStep = 0;
    document.getElementById("visPlayBtn").textContent = "⏸ Pause";
    visTimer = setInterval(() => {
      if (visStep >= visMoves.length) {
        stopVisPlay();
        return;
      }
      visStep++;
      render3DCube();
    }, visSpeed);
  });

  document.querySelectorAll(".speed-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      visSpeed = Number(btn.dataset.ms);
      document.querySelectorAll(".speed-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      if (visTimer) {
        stopVisPlay();
        document.getElementById("visPlayBtn").click();
      }
    });
  });

  document.getElementById("closeVisBtn").addEventListener("click", () => {
    stopVisPlay();
    document.getElementById("visModal").classList.remove("open");
  });

  // UI Wiring
  document.querySelectorAll("button").forEach(btn => btn.addEventListener("focus", () => btn.blur()));
  scrambleEl.addEventListener("click", openVisualizer);
  document.getElementById("newScrambleBtn").addEventListener("click", newScramble);

  document.querySelectorAll(".theme-btn").forEach(btn => {
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
