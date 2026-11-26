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
<style>
  :root {
    --bg-0: #090b10;
    --bg-1: #11151f;
    --surface: rgba(255, 255, 255, 0.04);
    --surface-hover: rgba(255, 255, 255, 0.08);
    --border: rgba(255, 255, 255, 0.1);
    --text: #f3f5f8;
    --muted: #8a94a6;
    --accent: #60a5fa;
    --amber: #f59e0b;
    --green: #10b981;
    --red: #ef4444;
    --gold: #fbbf24;
  }

  body[data-theme="galaxy"] {
    --bg-0: #080614;
    --bg-1: #160f30;
    --accent: #a78bfa;
  }
  body[data-theme="inferno"] {
    --bg-0: #120605;
    --bg-1: #260d09;
    --accent: #fb7185;
  }
  body[data-theme="arctic"] {
    --bg-0: #061218;
    --bg-1: #0c222c;
    --accent: #38bdf8;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }

  body {
    height: 100vh;
    overflow: hidden;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: radial-gradient(circle at 50% 35%, var(--bg-1), var(--bg-0) 75%);
    color: var(--text);
    display: flex;
    flex-direction: column;
  }

  header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 22px;
    border-bottom: 1px solid var(--border);
    background: rgba(0, 0, 0, 0.25);
    gap: 12px;
    z-index: 10;
  }

  .brand {
    font-weight: 700;
    letter-spacing: 0.06em;
    font-size: 0.9rem;
    color: var(--accent);
  }

  .scramble-box {
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size: 1.05rem;
    letter-spacing: 0.04em;
    padding: 8px 14px;
    border-radius: 10px;
    background: var(--surface);
    border: 1px solid var(--border);
    cursor: pointer;
    text-align: center;
  }
  .scramble-box:hover { background: var(--surface-hover); }

  .controls {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .btn {
    background: var(--surface);
    color: var(--text);
    border: 1px solid var(--border);
    padding: 7px 12px;
    border-radius: 9px;
    font-size: 0.82rem;
    cursor: pointer;
  }
  .btn:hover { background: var(--surface-hover); }
  .btn.active { border-color: var(--accent); color: var(--accent); }

  main {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    padding: 20px;
  }

  .focus-banner {
    font-size: 0.8rem;
    color: var(--amber);
    margin-bottom: 10px;
    opacity: 0;
    transition: opacity 0.15s;
  }
  body.unfocused .focus-banner { opacity: 1; }

  .timer-display {
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size: clamp(4.2rem, 12vw, 8.5rem);
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1;
    transition: color 0.1s ease;
  }
  .timer-display.holding { color: var(--amber); }
  .timer-display.armed { color: var(--green); }
  .timer-display.dnf { color: var(--red); }

  .progress-wrap {
    width: 260px;
    height: 6px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 999px;
    overflow: hidden;
    margin-top: 18px;
  }
  .progress-fill {
    height: 100%;
    width: 0%;
    background: var(--amber);
    transition: background 0.1s;
  }
  .progress-fill.armed { background: var(--green); }

  .sensors {
    display: flex;
    gap: 12px;
    margin-top: 18px;
  }

  .sensor {
    padding: 7px 16px;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 600;
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--muted);
    transition: all 0.1s ease;
  }
  .sensor.down {
    border-color: var(--amber);
    color: var(--amber);
    background: rgba(245, 158, 11, 0.12);
  }
  .sensor.armed {
    border-color: var(--green);
    color: var(--green);
    background: rgba(16, 185, 129, 0.15);
  }

  .hint {
    margin-top: 12px;
    font-size: 0.82rem;
    color: var(--muted);
  }

  .post-actions {
    display: flex;
    gap: 8px;
    margin-top: 18px;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.15s;
  }
  .post-actions.visible {
    opacity: 1;
    pointer-events: auto;
  }

  .stats-bar {
    position: absolute;
    bottom: 18px;
    display: flex;
    gap: 18px;
    padding: 9px 18px;
    border-radius: 12px;
    background: var(--surface);
    border: 1px solid var(--border);
    font-size: 0.82rem;
    color: var(--muted);
  }
  .stats-bar b { color: var(--text); margin-left: 4px; }

  .drawer {
    position: fixed;
    top: 57px;
    right: 0;
    bottom: 0;
    width: 320px;
    background: rgba(12, 15, 23, 0.96);
    border-left: 1px solid var(--border);
    transform: translateX(100%);
    transition: transform 0.2s ease;
    display: flex;
    flex-direction: column;
    z-index: 20;
  }
  .drawer.open { transform: translateX(0); }

  .drawer-head {
    padding: 14px 16px;
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
    padding: 10px;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .solve-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 10px;
    border-radius: 8px;
    background: var(--surface);
    border: 1px solid transparent;
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size: 0.86rem;
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
    border-radius: 5px;
    padding: 2px 6px;
    font-size: 0.72rem;
    cursor: pointer;
  }
  .mini-btn:hover { color: var(--text); border-color: var(--text); }

  .modal-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.65);
    display: none;
    align-items: center;
    justify-content: center;
    z-index: 30;
  }
  .modal-backdrop.open { display: flex; }

  .modal {
    width: 360px;
    background: #121622;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px;
    display: flex;
    flex-direction: column;
    gap: 14px;
  }
  .modal-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.86rem;
  }

  body.running header,
  body.running .stats-bar,
  body.running .post-actions {
    opacity: 0;
    pointer-events: none;
  }
</style>
</head>
<body data-theme="obsidian">

<header>
  <div class="brand">CHRONOCUBE</div>
  <div class="scramble-box" id="scrambleDisplay" title="Click for new scramble"></div>
  <div class="controls">
    <button class="btn theme-btn active" data-theme="obsidian">Obsidian</button>
    <button class="btn theme-btn" data-theme="galaxy">Galaxy</button>
    <button class="btn theme-btn" data-theme="inferno">Inferno</button>
    <button class="btn theme-btn" data-theme="arctic">Arctic</button>
    <button class="btn" id="configBtn">Keys</button>
    <button class="btn" id="drawerBtn">Solves (<span id="solveCount">0</span>)</button>
  </div>
</header>

<main id="stage" tabindex="0">
  <div class="focus-banner">Click anywhere on the timer once to focus keyboard input</div>
  <div class="timer-display" id="timerDisplay">0.000</div>
  <div class="progress-wrap"><div class="progress-fill" id="progressFill"></div></div>
  <div class="sensors">
    <div class="sensor" id="sensorLeft">Left Alt</div>
    <div class="sensor" id="sensorRight">Right Alt</div>
  </div>
  <div class="hint" id="hintText">Hold Left Alt + Right Alt until green, release to start • Space to stop</div>

  <div class="post-actions" id="postActions">
    <button class="btn" id="btnPlus2">+2</button>
    <button class="btn" id="btnDnf">DNF</button>
    <button class="btn" id="btnStar">★ Highlight</button>
    <button class="btn" id="btnDeleteLast" style="color:#f87171;">Delete Run</button>
  </div>

  <div class="stats-bar">
    <span>PB:<b id="statPb">-</b></span>
    <span>Ao5:<b id="statAo5">-</b></span>
    <span>Ao12:<b id="statAo12">-</b></span>
    <span>Mean:<b id="statMean">-</b></span>
  </div>
</main>

<aside class="drawer" id="drawer">
  <div class="drawer-head">
    <span>Session Solves</span>
    <button class="btn" id="clearAllBtn" style="padding:4px 8px;font-size:0.75rem;">Clear All</button>
  </div>
  <div class="solve-list" id="solveList"></div>
</aside>

<div class="modal-backdrop" id="configModal">
  <div class="modal">
    <div style="font-weight:600;font-size:0.95rem;">Trigger Keys</div>
    <div class="modal-row">
      <span>Left Key</span>
      <button class="btn" id="bindLeftBtn">AltLeft</button>
    </div>
    <div class="modal-row">
      <span>Right Key</span>
      <button class="btn" id="bindRightBtn">AltRight</button>
    </div>
    <div class="modal-row">
      <span>Hold Delay</span>
      <div style="display:flex;gap:6px;">
        <button class="btn delay-btn" data-ms="300">0.30s</button>
        <button class="btn delay-btn active" data-ms="450">0.45s</button>
        <button class="btn delay-btn" data-ms="650">0.65s</button>
      </div>
    </div>
    <div style="display:flex;justify-content:space-between;margin-top:6px;">
      <button class="btn" id="resetKeysBtn">Reset Defaults</button>
      <button class="btn active" id="closeConfigBtn">Done</button>
    </div>
  </div>
</div>

<script>
(() => {
  const STORAGE_SOLVES = "cc_st_solves_v1";
  const STORAGE_CFG = "cc_st_cfg_v1";

  let cfg = { leftKey: "AltLeft", rightKey: "AltRight", holdMs: 450, theme: "obsidian" };
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_CFG));
    if (saved) cfg = { ...cfg, ...saved };
  } catch (e) {}

  let solves = [];
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_SOLVES));
    if (Array.isArray(saved)) solves = saved;
  } catch (e) {}

  // State machine: IDLE | HOLDING | ARMED | RUNNING
  let phase = "IDLE";
  let leftDown = false;
  let rightDown = false;
  let holdStart = 0;
  let runStart = 0;
  let rafId = null;
  let lastRunId = null;
  let currentScramble = "";
  let bindingTarget = null;
  let blockUntilRelease = false;

  const timerEl = document.getElementById("timerDisplay");
  const fillEl = document.getElementById("progressFill");
  const sensorLeftEl = document.getElementById("sensorLeft");
  const sensorRightEl = document.getElementById("sensorRight");
  const scrambleEl = document.getElementById("scrambleDisplay");
  const postActionsEl = document.getElementById("postActions");
  const solveListEl = document.getElementById("solveList");
  const solveCountEl = document.getElementById("solveCount");

  function prettyKey(code) {
    if (code === "AltLeft") return "Left Alt";
    if (code === "AltRight") return "Right Alt";
    if (code === "ControlLeft") return "Left Ctrl";
    if (code === "ControlRight") return "Right Ctrl";
    if (code === "ShiftLeft") return "Left Shift";
    if (code === "ShiftRight") return "Right Shift";
    return code;
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
    sensorLeftEl.textContent = prettyKey(cfg.leftKey);
    sensorRightEl.textContent = prettyKey(cfg.rightKey);
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
    rafId = requestAnimationFrame(tick);
  }

  // Normalize AltGr (Windows/Turkish Q sends ControlLeft + AltRight together)
  function isLeftTrigger(e) {
    return e.code === cfg.leftKey;
  }

  function isRightTrigger(e) {
    if (e.code === cfg.rightKey) return true;
    if (cfg.rightKey === "AltRight" && e.key === "AltGraph") return true;
    return false;
  }

  function handleKeyDown(e) {
    if (bindingTarget) {
      e.preventDefault();
      if (bindingTarget === "left") cfg.leftKey = e.code;
      if (bindingTarget === "right") cfg.rightKey = e.code;
      bindingTarget = null;
      saveCfg();
      return;
    }

    const leftMatch = isLeftTrigger(e);
    const rightMatch = isRightTrigger(e);

    if (leftMatch || rightMatch || e.code === "Space" || e.key === "Alt" || e.key === "AltGraph") {
      e.preventDefault();
    }

    if (e.repeat) return;

    if (phase === "RUNNING") {
      if (e.code === "Space" || leftMatch || rightMatch) {
        stopRun();
      }
      return;
    }

    if (blockUntilRelease) return;

    // If Right Alt is pressed on Windows/Turkish Q, ignore synthetic ControlLeft
    if (e.code === "ControlLeft" && cfg.leftKey !== "ControlLeft" && e.getModifierState("AltGraph")) {
      return;
    }

    if (leftMatch) leftDown = true;
    if (rightMatch) rightDown = true;

    // Step 1 -> Step 2: Once BOTH keys are held down, start charging the bar
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
    const leftMatch = isLeftTrigger(e);
    // On AltGr release, Windows often emits ControlLeft keyup while dropping AltGraph
    const rightMatch = isRightTrigger(e) || (
      cfg.rightKey === "AltRight" &&
      e.code === "ControlLeft" &&
      rightDown &&
      !e.getModifierState("AltGraph")
    );

    if (leftMatch || rightMatch || e.code === "Space" || e.key === "Alt" || e.key === "AltGraph") {
      e.preventDefault();
    }

    if (leftMatch) leftDown = false;
    if (rightMatch) rightDown = false;

    if (blockUntilRelease) {
      if (!leftDown && !rightDown && e.code !== "Space") {
        blockUntilRelease = false;
      }
      if (!leftDown && !rightDown) blockUntilRelease = false;
      updateSensors();
      return;
    }

    // Step 3: If armed and either key is released, immediately start the timer
    if (phase === "ARMED" && (!leftDown || !rightDown)) {
      startRun();
      return;
    }

    // If released too early before green, cancel hold
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

  window.addEventListener("focus", () => {
    document.body.classList.remove("unfocused");
  });

  document.addEventListener("pointerdown", () => {
    document.body.classList.remove("unfocused");
  });

  function calcAvg(list, n) {
    if (list.length < n) return "-";
    const slice = list.slice(0, n).map(s => s.penalty === "DNF" ? Infinity : s.ms + (s.penalty === "+2" ? 2000 : 0));
    const dnfs = slice.filter(v => !Number.isFinite(v)).length;
    if (dnfs >= 2) return "DNF";
    slice.sort((a, b) => a - b);
    const trimmed = slice.slice(1, n - 1);
    const sum = trimmed.reduce((a, b) => a + b, 0);
    return formatMs(sum / trimmed.length, null);
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

    solveListEl.innerHTML = solves.map((s, idx) => `
      <div class="solve-item ${s.star ? "star" : ""}">
        <span>#${solves.length - idx} &nbsp;<b>${formatMs(s.ms, s.penalty)}</b></span>
        <div class="solve-actions">
          <button class="mini-btn" onclick="window._ccAct(${s.id}, 'plus2')">+2</button>
          <button class="mini-btn" onclick="window._ccAct(${s.id}, 'dnf')">DNF</button>
          <button class="mini-btn" onclick="window._ccAct(${s.id}, 'star')">★</button>
          <button class="mini-btn" onclick="window._ccAct(${s.id}, 'del')">×</button>
        </div>
      </div>
    `).join("");
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

  // Button wiring (blur immediately so Space never re-clicks focused buttons)
  document.querySelectorAll("button").forEach(btn => {
    btn.addEventListener("focus", () => btn.blur());
  });

  scrambleEl.addEventListener("click", newScramble);

  document.querySelectorAll(".theme-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      cfg.theme = btn.dataset.theme;
      saveCfg();
    });
  });

  document.getElementById("drawerBtn").addEventListener("click", () => {
    document.getElementById("drawer").classList.toggle("open");
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

  document.getElementById("bindLeftBtn").addEventListener("click", (e) => {
    bindingTarget = "left";
    e.target.textContent = "Press any key...";
  });

  document.getElementById("bindRightBtn").addEventListener("click", (e) => {
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
  rafId = requestAnimationFrame(tick);
})();
</script>
</body>
</html>
"""

components.html(HTML_APP, height=900, scrolling=False)
