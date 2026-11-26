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
    --bg-glow-1: rgba(61, 174, 233, 0.22);
    --bg-glow-2: rgba(61, 174, 233, 0.14);
    --glass: rgba(20, 24, 33, 0.72);
    --glass-strong: rgba(18, 22, 30, 0.94);
    --surface: rgba(255, 255, 255, 0.055);
    --surface-hover: rgba(255, 255, 255, 0.11);
    --border: rgba(255, 255, 255, 0.13);
    --text: #eff0f1;
    --muted: #9aa5b4;
    --accent: #3daee9;
    --accent-rgb: 61, 174, 233;
    --accent-glow: rgba(61, 174, 233, 0.36);
    --cue-color: #ef4444;
    --cue-glow: rgba(239, 68, 68, 0.9);
    --clock-color: #eff0f1;
    --clock-bg-alpha: 0.55;
    --clock-scale: 1;
    --clock-font: 'JetBrains Mono', monospace;
    --amber: #f67400;
    --amber-glow: rgba(246, 116, 0, 0.35);
    --green: #27ae60;
    --green-glow: rgba(39, 174, 96, 0.4);
    --red: #da4453;
    --panel-radius: 10px;
  }

  body[data-scene="clouds"] { --bg-core: #0d1f36; }
  body[data-scene="forest"] { --bg-core: #04100a; }
  body[data-scene="rain"]   { --bg-core: #060b14; }
  body[data-scene="snow"]   { --bg-core: #081220; }
  body[data-scene="galaxy"] { --bg-core: #060412; }
  body[data-scene="minimal"]{ --bg-core: #07090f; }

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

  /* KDE Plasma Breeze Panel Header */
  header {
    position: relative;
    z-index: 30;
    width: 100%;
    height: 54px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 16px;
    background: var(--glass);
    backdrop-filter: blur(22px) saturate(140%);
    border-bottom: 1px solid var(--border);
    box-shadow: 0 2px 16px rgba(0, 0, 0, 0.35);
    gap: 10px;
    transition: opacity 0.25s ease;
  }

  body.floating-panel header {
    width: calc(100% - 24px);
    margin: 10px auto 0 auto;
    border-radius: var(--panel-radius);
    border: 1px solid var(--border);
  }

  .brand {
    display: flex;
    align-items: center;
    gap: 9px;
    font-weight: 700;
    letter-spacing: 0.06em;
    font-size: 0.86rem;
  }
  .brand-dot {
    width: 11px;
    height: 11px;
    border-radius: 3px;
    background: var(--accent);
    box-shadow: 0 0 12px var(--accent-glow);
    transform: rotate(15deg);
  }

  .scramble-wrap {
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .scramble-box {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.94rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    padding: 7px 14px;
    border-radius: 8px;
    background: var(--surface);
    border: 1px solid var(--border);
    cursor: pointer;
    transition: all 0.16s ease;
  }
  .scramble-box:hover {
    background: var(--surface-hover);
    border-color: var(--accent);
    box-shadow: 0 0 16px var(--accent-glow);
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
    padding: 6px 10px;
    border-radius: 8px;
    font-size: 0.79rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s ease;
    display: inline-flex;
    align-items: center;
    gap: 6px;
  }
  .pill-btn:hover {
    background: var(--surface-hover);
    color: var(--text);
    border-color: rgba(255, 255, 255, 0.24);
  }
  .pill-btn.active {
    color: var(--text);
    border-color: var(--accent);
    background: rgba(var(--accent-rgb), 0.18);
    box-shadow: 0 0 12px var(--accent-glow);
  }

  .emoji-nav-btn {
    font-size: 1.02rem;
    padding: 6px 10px;
    line-height: 1.1;
    color: var(--text);
  }
  .nav-label {
    font-size: 0.78rem;
    font-weight: 500;
    color: var(--muted);
    display: none;
  }
  body.show-nav-labels .nav-label {
    display: inline;
  }
  .emoji-nav-btn:hover .nav-label,
  .emoji-nav-btn.active .nav-label {
    color: var(--text);
  }
  .count-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 700;
    padding: 1px 5px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.12);
    color: var(--accent);
  }

  /* Docked Header Clock Option */
  .docked-clock {
    display: none;
    align-items: center;
    gap: 8px;
    padding: 5px 11px;
    border-radius: 8px;
    background: var(--surface);
    border: 1px solid var(--border);
    font-family: var(--clock-font);
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--clock-color);
  }
  body.clock-docked .docked-clock {
    display: inline-flex;
  }
  body.clock-docked .clock-plasmoid {
    display: none !important;
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

  /* KDE Edit Mode Banner */
  .edit-mode-bar {
    position: fixed;
    top: 66px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 35;
    display: none;
    align-items: center;
    gap: 10px;
    padding: 7px 14px;
    border-radius: 10px;
    background: rgba(18, 22, 30, 0.92);
    border: 1px solid var(--accent);
    box-shadow: 0 8px 28px rgba(0, 0, 0, 0.55), 0 0 18px var(--accent-glow);
    font-size: 0.78rem;
    color: var(--text);
  }
  body.edit-mode .edit-mode-bar {
    display: flex;
  }

  /* Real-Life Clock Plasmoid Widget */
  .clock-plasmoid {
    position: fixed;
    z-index: 20;
    left: 24px;
    top: 74px;
    transform: scale(var(--clock-scale));
    transform-origin: top left;
    padding: 12px 18px;
    border-radius: 12px;
    background: rgba(18, 22, 30, var(--clock-bg-alpha));
    backdrop-filter: blur(18px);
    border: 1px solid var(--border);
    color: var(--clock-color);
    font-family: var(--clock-font);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    transition: border-color 0.15s ease, box-shadow 0.15s ease, opacity 0.2s ease;
  }
  .clock-plasmoid.no-border {
    border-color: transparent;
    box-shadow: none;
  }
  .clock-plasmoid.hidden {
    display: none;
  }

  body.edit-mode .clock-plasmoid {
    cursor: grab;
    border: 1.5px dashed var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(var(--accent-rgb), 0.18), 0 12px 32px rgba(0, 0, 0, 0.5) !important;
  }
  body.edit-mode .clock-plasmoid:active {
    cursor: grabbing;
  }

  .plasmoid-badge {
    display: none;
    position: absolute;
    top: -11px;
    left: 10px;
    padding: 1px 7px;
    border-radius: 5px;
    background: var(--accent);
    color: #060911;
    font-family: 'Inter', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.04em;
  }
  body.edit-mode .plasmoid-badge {
    display: inline-block;
  }

  .clock-analog-wrap {
    display: none;
    width: 112px;
    height: 112px;
  }
  .clock-plasmoid[data-style="analog"] .clock-analog-wrap,
  .clock-plasmoid[data-style="hybrid"] .clock-analog-wrap {
    display: block;
  }
  .clock-plasmoid[data-style="analog"] .clock-digital-time {
    display: none;
  }

  .clock-digital-time {
    font-size: 2.1rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.05;
    text-shadow: 0 2px 14px rgba(0, 0, 0, 0.45);
    white-space: nowrap;
  }
  .clock-ampm {
    font-size: 0.85rem;
    font-weight: 600;
    opacity: 0.8;
    margin-left: 4px;
  }
  .clock-date-line {
    font-family: 'Inter', sans-serif;
    font-size: 0.76rem;
    font-weight: 500;
    opacity: 0.78;
    letter-spacing: 0.02em;
    white-space: nowrap;
  }
  .clock-tz-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.66rem;
    opacity: 0.6;
    text-transform: uppercase;
  }

  .focus-banner {
    padding: 5px 14px;
    border-radius: 999px;
    background: rgba(246, 116, 0, 0.14);
    border: 1px solid rgba(246, 116, 0, 0.4);
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
    text-shadow: 0 8px 36px rgba(0, 0, 0, 0.5);
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
    background: rgba(246, 116, 0, 0.13);
    box-shadow: 0 0 18px var(--amber-glow);
  }
  .sensor.down .sensor-dot {
    background: var(--amber);
    box-shadow: 0 0 8px var(--amber);
  }
  .sensor.armed {
    border-color: var(--green);
    color: var(--green);
    background: rgba(39, 174, 96, 0.16);
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
    border-radius: var(--panel-radius);
    background: var(--glass);
    backdrop-filter: blur(18px);
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

  /* KDE Plasma Right-Side Slide-Out Drawers */
  .side-drawer {
    position: fixed;
    top: 54px;
    right: 0;
    bottom: 0;
    width: 365px;
    max-width: 94vw;
    background: var(--glass-strong);
    backdrop-filter: blur(24px) saturate(140%);
    border-left: 1px solid var(--border);
    box-shadow: -8px 0 32px rgba(0, 0, 0, 0.45);
    transform: translateX(100%);
    transition: transform 0.22s cubic-bezier(0.22, 1, 0.36, 1);
    display: flex;
    flex-direction: column;
    z-index: 25;
  }
  body.floating-panel .side-drawer {
    top: 72px;
    right: 12px;
    bottom: 12px;
    border-radius: var(--panel-radius);
    border: 1px solid var(--border);
  }
  .side-drawer.open { transform: translateX(0); }

  .drawer-head {
    padding: 13px 16px;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.88rem;
    font-weight: 600;
  }

  .drawer-body {
    flex: 1;
    overflow-y: auto;
    padding: 14px;
    display: flex;
    flex-direction: column;
    gap: 11px;
  }

  .section-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    color: var(--accent);
    font-weight: 700;
    margin-top: 4px;
  }

  .scene-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
  }
  .scene-card {
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 9px 11px;
    border-radius: 9px;
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--text);
    font-size: 0.81rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s ease;
    text-align: left;
  }
  .scene-card:hover {
    background: var(--surface-hover);
    border-color: rgba(255, 255, 255, 0.25);
  }
  .scene-card.active {
    border-color: var(--accent);
    background: rgba(var(--accent-rgb), 0.18);
    box-shadow: 0 0 14px var(--accent-glow);
  }

  .color-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 7px;
  }
  .color-swatch-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 5px;
    padding: 7px 5px;
    border-radius: 9px;
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--muted);
    font-size: 0.72rem;
    cursor: pointer;
    transition: all 0.15s ease;
  }
  .color-swatch-btn:hover {
    background: var(--surface-hover);
    color: var(--text);
  }
  .color-swatch-btn.active {
    border-color: var(--accent);
    color: var(--text);
    background: rgba(var(--accent-rgb), 0.16);
    box-shadow: 0 0 12px var(--accent-glow);
  }
  .swatch-dot {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    border: 2px solid rgba(255, 255, 255, 0.35);
  }

  .custom-color-row,
  .config-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 9px 12px;
    border-radius: 9px;
    background: var(--surface);
    border: 1px solid var(--border);
    font-size: 0.81rem;
    color: var(--muted);
    gap: 10px;
  }
  input[type="color"] {
    width: 34px;
    height: 24px;
    border: none;
    background: transparent;
    cursor: pointer;
  }

  select.breeze-select {
    background: rgba(10, 14, 22, 0.9);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 7px;
    padding: 5px 8px;
    font-size: 0.78rem;
    font-family: 'Inter', sans-serif;
    cursor: pointer;
    outline: none;
  }
  select.breeze-select:focus {
    border-color: var(--accent);
  }

  /* 3x3 Anchor Grid for Clock Placement */
  .anchor-grid {
    display: grid;
    grid-template-columns: repeat(3, 28px);
    gap: 4px;
  }
  .anchor-btn {
    width: 28px;
    height: 22px;
    border-radius: 5px;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid var(--border);
    color: var(--muted);
    font-size: 0.65rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .anchor-btn:hover {
    background: var(--surface-hover);
    color: var(--text);
  }
  .anchor-btn.active {
    background: var(--accent);
    color: #060911;
    border-color: var(--accent);
    font-weight: 700;
  }

  /* Sliders */
  .slider-card {
    display: flex;
    flex-direction: column;
    gap: 7px;
    padding: 9px 12px;
    border-radius: 9px;
    background: var(--surface);
    border: 1px solid var(--border);
  }
  .slider-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.8rem;
    color: var(--muted);
  }
  .slider-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: var(--accent);
    font-weight: 600;
  }
  input[type="range"] {
    width: 100%;
    accent-color: var(--accent);
    cursor: pointer;
    height: 4px;
  }

  /* Toggle Switch */
  .switch {
    position: relative;
    display: inline-block;
    width: 40px;
    height: 22px;
    flex-shrink: 0;
  }
  .switch input { opacity: 0; width: 0; height: 0; }
  .slider {
    position: absolute;
    cursor: pointer;
    inset: 0;
    background-color: rgba(255, 255, 255, 0.12);
    border: 1px solid var(--border);
    transition: 0.2s;
    border-radius: 999px;
  }
  .slider:before {
    position: absolute;
    content: "";
    height: 16px;
    width: 16px;
    left: 2px;
    bottom: 2px;
    background-color: var(--text);
    transition: 0.2s;
    border-radius: 50%;
  }
  input:checked + .slider {
    background-color: var(--accent);
    border-color: var(--accent);
  }
  input:checked + .slider:before {
    transform: translateX(18px);
    background-color: #060911;
  }

  .solve-list {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .solve-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 11px;
    border-radius: 8px;
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

  /* 3D Scramble Modal */
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
    width: 500px;
    max-width: 94vw;
    background: #12161f;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px;
    display: flex;
    flex-direction: column;
    gap: 13px;
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.65);
  }

  .cube-stage {
    position: relative;
    width: 100%;
    height: 260px;
    display: flex;
    align-items: center;
    justify-content: center;
    perspective: 820px;
    background: radial-gradient(circle at center, rgba(255,255,255,0.04), rgba(0,0,0,0.45));
    border-radius: 11px;
    border: 1px solid var(--border);
    cursor: grab;
    overflow: hidden;
  }
  .cube-stage:active { cursor: grabbing; }

  .move-cue-overlay {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    pointer-events: none;
    z-index: 50;
    opacity: 0;
    transform: translateZ(260px) scale(0.82);
    transition: opacity 0.22s ease, transform 0.22s cubic-bezier(0.22, 1, 0.36, 1);
  }
  .move-cue-overlay.visible {
    opacity: 1;
    transform: translateZ(260px) scale(1);
  }
  .move-cue-badge {
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.8rem;
    font-weight: 800;
    letter-spacing: -0.05em;
    line-height: 1;
    color: var(--cue-color);
    background: transparent;
    border: none;
    text-shadow:
      0 0 28px var(--cue-glow),
      0 6px 24px rgba(0, 0, 0, 0.96);
  }

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
  body.running .post-actions,
  body.running .edit-mode-bar {
    opacity: 0;
    pointer-events: none;
  }
  body.running.hide-clock-running .clock-plasmoid {
    opacity: 0;
    pointer-events: none;
  }
</style>
</head>
<body data-scene="clouds">

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
    <div class="docked-clock" id="dockedClock">00:00</div>
    <button class="pill-btn emoji-nav-btn" id="editModeNavBtn" title="Edit Widgets">
      <span>🧩</span><span class="nav-label">Edit</span>
    </button>
    <button class="pill-btn emoji-nav-btn" id="themesNavBtn" data-drawer="themesDrawer" title="Themes">
      <span>🎨</span><span class="nav-label">Themes</span>
    </button>
    <button class="pill-btn emoji-nav-btn" id="configNavBtn" data-drawer="configDrawer" title="Config">
      <span>⚙️</span><span class="nav-label">Config</span>
    </button>
    <button class="pill-btn emoji-nav-btn" id="historyNavBtn" data-drawer="historyDrawer" title="History">
      <span>📜</span><span class="nav-label">History</span><span class="count-badge" id="solveCount">0</span>
    </button>
  </div>
</header>

<!-- KDE Edit Mode Floating Bar -->
<div class="edit-mode-bar" id="editModeBar">
  <span>🧩 <b>Desktop Edit Mode</b> — Drag the Clock widget anywhere on screen</span>
  <button class="pill-btn active" id="exitEditModeBtn" style="padding:3px 9px;">Done</button>
</div>

<!-- Customizable Real-Life Clock Plasmoid -->
<div class="clock-plasmoid" id="clockPlasmoid" data-style="digital">
  <span class="plasmoid-badge">CLOCK WIDGET</span>
  <div class="clock-analog-wrap">
    <svg viewBox="0 0 120 120" width="112" height="112">
      <circle cx="60" cy="60" r="54" fill="rgba(0,0,0,0.22)" stroke="currentColor" stroke-opacity="0.35" stroke-width="2.5"/>
      <g id="analogTicks" stroke="currentColor" stroke-opacity="0.55" stroke-width="2" stroke-linecap="round"></g>
      <line id="handHour" x1="60" y1="60" x2="60" y2="30" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
      <line id="handMin" x1="60" y1="60" x2="60" y2="18" stroke="currentColor" stroke-width="2.8" stroke-linecap="round"/>
      <line id="handSec" x1="60" y1="66" x2="60" y2="14" stroke="var(--accent)" stroke-width="1.6" stroke-linecap="round"/>
      <circle cx="60" cy="60" r="3.5" fill="var(--accent)"/>
    </svg>
  </div>
  <div class="clock-digital-time" id="clockDigitalTime">00:00:00</div>
  <div class="clock-date-line" id="clockDateLine">Thursday, Nov 26, 2026</div>
  <div class="clock-tz-tag" id="clockTzTag">LOCAL</div>
</div>

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

<!-- 1. Themes Side Drawer -->
<aside class="side-drawer" id="themesDrawer">
  <div class="drawer-head">
    <span>🎨 Themes</span>
    <button class="pill-btn close-drawer-btn" style="padding:3px 8px;">✕</button>
  </div>
  <div class="drawer-body">
    <div class="section-label">Animated Scenes</div>
    <div class="scene-grid">
      <button class="scene-card" data-scene="clouds"><span>☁️</span>Sky Clouds</button>
      <button class="scene-card" data-scene="forest"><span>🌲</span>Mist Forest</button>
      <button class="scene-card" data-scene="rain"><span>🌧️</span>Rainstorm</button>
      <button class="scene-card" data-scene="snow"><span>❄️</span>Snowfall</button>
      <button class="scene-card" data-scene="galaxy"><span>🌌</span>Galaxy</button>
      <button class="scene-card" data-scene="minimal"><span>🌑</span>Minimal</button>
    </div>

    <div class="section-label">Plasma Accent Color</div>
    <div class="color-grid">
      <button class="color-swatch-btn" data-color="#3daee9"><span class="swatch-dot" style="background:#3daee9;"></span>Breeze</button>
      <button class="color-swatch-btn" data-color="#c084fc"><span class="swatch-dot" style="background:#c084fc;"></span>Violet</button>
      <button class="color-swatch-btn" data-color="#fb923c"><span class="swatch-dot" style="background:#fb923c;"></span>Inferno</button>
      <button class="color-swatch-btn" data-color="#27ae60"><span class="swatch-dot" style="background:#27ae60;"></span>Emerald</button>
      <button class="color-swatch-btn" data-color="#fbbf24"><span class="swatch-dot" style="background:#fbbf24;"></span>Gold</button>
      <button class="color-swatch-btn" data-color="#f472b6"><span class="swatch-dot" style="background:#f472b6;"></span>Sakura</button>
      <button class="color-swatch-btn" data-color="#da4453"><span class="swatch-dot" style="background:#da4453;"></span>Crimson</button>
      <button class="color-swatch-btn" data-color="#eff0f1"><span class="swatch-dot" style="background:#eff0f1;"></span>Frost</button>
    </div>

    <div class="custom-color-row">
      <span>Custom Accent</span>
      <input type="color" id="customColorPicker" value="#3daee9" />
    </div>

    <div class="section-label">Scene Motion & Density</div>
    <div class="slider-card">
      <div class="slider-header">
        <span id="sizeSliderLabel">Size</span>
        <span class="slider-val" id="sizeSliderVal">1.0x</span>
      </div>
      <input type="range" id="sceneSizeSlider" min="0.4" max="2.2" step="0.1" value="1.0" />
    </div>

    <div class="slider-card">
      <div class="slider-header">
        <span id="speedSliderLabel">Speed</span>
        <span class="slider-val" id="speedSliderVal">1.0x</span>
      </div>
      <input type="range" id="sceneSpeedSlider" min="0.2" max="2.5" step="0.1" value="1.0" />
    </div>

    <div class="slider-card">
      <div class="slider-header">
        <span id="intensitySliderLabel">Intensity</span>
        <span class="slider-val" id="intensitySliderVal">100%</span>
      </div>
      <input type="range" id="sceneIntensitySlider" min="0.2" max="2.0" step="0.1" value="1.0" />
    </div>
  </div>
</aside>

<!-- 2. Config Side Drawer -->
<aside class="side-drawer" id="configDrawer">
  <div class="drawer-head">
    <span>⚙️ Config</span>
    <button class="pill-btn close-drawer-btn" style="padding:3px 8px;">✕</button>
  </div>
  <div class="drawer-body">
    <div class="section-label">Plasma Workspace</div>
    <div class="config-card">
      <span>Edit Widget Layout</span>
      <button class="pill-btn" id="toggleEditFromConfigBtn">🧩 Toggle</button>
    </div>
    <div class="config-card">
      <span>Floating Top Panel</span>
      <label class="switch">
        <input type="checkbox" id="toggleFloatingPanelChk">
        <span class="slider"></span>
      </label>
    </div>
    <div class="config-card">
      <span>Show Text Labels</span>
      <label class="switch">
        <input type="checkbox" id="toggleLabelsChk">
        <span class="slider"></span>
      </label>
    </div>

    <div class="section-label">🕒 Real-Life Clock Widget</div>
    <div class="config-card">
      <span>Show Clock</span>
      <label class="switch">
        <input type="checkbox" id="clockEnabledChk" checked>
        <span class="slider"></span>
      </label>
    </div>
    <div class="config-card">
      <span>Clock Mode</span>
      <div style="display:flex;gap:4px;">
        <button class="pill-btn clock-style-btn active" data-style="digital">Digital</button>
        <button class="pill-btn clock-style-btn" data-style="analog">Analog</button>
        <button class="pill-btn clock-style-btn" data-style="hybrid">Both</button>
      </div>
    </div>
    <div class="config-card">
      <span>Location</span>
      <div style="display:flex;align-items:center;gap:8px;">
        <button class="pill-btn" id="dockClockBtn" style="padding:4px 8px;font-size:0.74rem;">Dock Top</button>
        <div class="anchor-grid" id="clockAnchorGrid" title="Snap Clock Position">
          <button class="anchor-btn" data-pos="tl">↖</button>
          <button class="anchor-btn" data-pos="tc">↑</button>
          <button class="anchor-btn" data-pos="tr">↗</button>
          <button class="anchor-btn" data-pos="ml">←</button>
          <button class="anchor-btn" data-pos="mc">•</button>
          <button class="anchor-btn" data-pos="mr">→</button>
          <button class="anchor-btn" data-pos="bl">↙</button>
          <button class="anchor-btn" data-pos="bc">↓</button>
          <button class="anchor-btn" data-pos="br">↘</button>
        </div>
      </div>
    </div>
    <div class="config-card">
      <span>Timezone</span>
      <select class="breeze-select" id="clockTzSelect">
        <option value="local">Local System</option>
        <option value="UTC">UTC</option>
        <option value="Europe/Madrid">Madrid / CET</option>
        <option value="Europe/Istanbul">Istanbul / TRT</option>
        <option value="Europe/London">London / GMT</option>
        <option value="America/New_York">New York / EST</option>
        <option value="America/Los_Angeles">Los Angeles / PST</option>
        <option value="Asia/Tokyo">Tokyo / JST</option>
      </select>
    </div>
    <div class="config-card">
      <span>Font Style</span>
      <select class="breeze-select" id="clockFontSelect">
        <option value="'JetBrains Mono', monospace">JetBrains Mono</option>
        <option value="'Inter', sans-serif">Inter Sans</option>
        <option value="system-ui, sans-serif">System UI</option>
      </select>
    </div>
    <div class="config-card">
      <span>24-Hour Format</span>
      <label class="switch">
        <input type="checkbox" id="clock24hChk" checked>
        <span class="slider"></span>
      </label>
    </div>
    <div class="config-card">
      <span>Show Seconds</span>
      <label class="switch">
        <input type="checkbox" id="clockSecChk" checked>
        <span class="slider"></span>
      </label>
    </div>
    <div class="config-card">
      <span>Show Date</span>
      <label class="switch">
        <input type="checkbox" id="clockDateChk" checked>
        <span class="slider"></span>
      </label>
    </div>
    <div class="config-card">
      <span>Card Border</span>
      <label class="switch">
        <input type="checkbox" id="clockBorderChk" checked>
        <span class="slider"></span>
      </label>
    </div>
    <div class="config-card">
      <span>Hide While Solving</span>
      <label class="switch">
        <input type="checkbox" id="clockHideRunChk">
        <span class="slider"></span>
      </label>
    </div>
    <div class="config-card">
      <span>Clock Color</span>
      <input type="color" id="clockColorPicker" value="#eff0f1" />
    </div>
    <div class="slider-card">
      <div class="slider-header">
        <span>Clock Scale</span>
        <span class="slider-val" id="clockScaleVal">1.0x</span>
      </div>
      <input type="range" id="clockScaleSlider" min="0.6" max="1.8" step="0.05" value="1.0" />
    </div>
    <div class="slider-card">
      <div class="slider-header">
        <span>Card Background Opacity</span>
        <span class="slider-val" id="clockOpacityVal">55%</span>
      </div>
      <input type="range" id="clockOpacitySlider" min="0" max="0.95" step="0.05" value="0.55" />
    </div>

    <div class="section-label">3D Move Notation</div>
    <div class="config-card">
      <span>Show Notation</span>
      <label class="switch">
        <input type="checkbox" id="toggleNotationChk" checked>
        <span class="slider"></span>
      </label>
    </div>
    <div class="config-card">
      <span>Notation Color</span>
      <input type="color" id="notationColorPicker" value="#ef4444" />
    </div>

    <div class="section-label">Dual-Hand Trigger Keys</div>
    <div class="config-card">
      <span>Left Key</span>
      <button class="pill-btn" id="bindLeftBtn">AltLeft</button>
    </div>
    <div class="config-card">
      <span>Right Key</span>
      <button class="pill-btn" id="bindRightBtn">AltRight</button>
    </div>
    <div class="config-card">
      <span>Hold Delay</span>
      <div style="display:flex;gap:5px;">
        <button class="pill-btn delay-btn" data-ms="300">0.30s</button>
        <button class="pill-btn delay-btn active" data-ms="450">0.45s</button>
        <button class="pill-btn delay-btn" data-ms="650">0.65s</button>
      </div>
    </div>

    <button class="pill-btn" id="resetKeysBtn" style="justify-content:center;margin-top:4px;">Reset All Defaults</button>
  </div>
</aside>

<!-- 3. History Side Drawer -->
<aside class="side-drawer" id="historyDrawer">
  <div class="drawer-head">
    <span>📜 History</span>
    <div style="display:flex;gap:6px;">
      <button class="pill-btn" id="filterStarBtn" style="padding:4px 8px;font-size:0.74rem;">★ Only</button>
      <button class="pill-btn" id="clearAllBtn" style="padding:4px 8px;font-size:0.74rem;">Clear All</button>
      <button class="pill-btn close-drawer-btn" style="padding:3px 8px;">✕</button>
    </div>
  </div>
  <div class="drawer-body">
    <div class="solve-list" id="solveList"></div>
  </div>
</aside>

<!-- 3D Scramble Visualizer Modal -->
<div class="modal-backdrop" id="visModal">
  <div class="modal">
    <div style="display:flex;justify-content:space-between;align-items:center;">
      <span style="font-weight:600;font-size:0.92rem;">3D Scramble Guide (White Top, Green Front)</span>
      <button class="pill-btn" id="closeVisBtn" style="padding:4px 9px;">✕</button>
    </div>
    <div class="cube-stage" id="cubeStage">
      <div class="cube-world" id="cubeWorld"></div>
      <div class="move-cue-overlay" id="moveCueOverlay">
        <div class="move-cue-badge" id="moveCueBadge">R'</div>
      </div>
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
        <button class="pill-btn speed-btn" data-cue="760" data-turn="750" data-pause="950">0.5x</button>
        <button class="pill-btn speed-btn active" data-cue="580" data-turn="480" data-pause="650">1x</button>
        <button class="pill-btn speed-btn" data-cue="340" data-turn="260" data-pause="360">1.5x</button>
      </div>
    </div>
  </div>
</div>

<script>
(() => {
  const STORAGE_SOLVES = "cc_v13_solves";
  const STORAGE_CFG = "cc_v13_cfg";

  const DEFAULT_CFG = {
    leftKey: "AltLeft",
    rightKey: "AltRight",
    holdMs: 450,
    scene: "clouds",
    accentColor: "#3daee9",
    floatingPanel: false,
    showLabels: false,
    showNotation: true,
    notationColor: "#ef4444",
    sceneSize: 1.0,
    sceneSpeed: 1.0,
    sceneIntensity: 1.0,
    clockEnabled: true,
    clockStyle: "digital",
    clockDocked: false,
    clockXRatio: 0.02,
    clockYRatio: 0.1,
    clockAnchor: "tl",
    clockTz: "local",
    clockFont: "'JetBrains Mono', monospace",
    clock24h: true,
    clockSeconds: true,
    clockDate: true,
    clockBorder: true,
    clockHideRunning: false,
    clockColor: "#eff0f1",
    clockScale: 1.0,
    clockOpacity: 0.55
  };

  let cfg = { ...DEFAULT_CFG };
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_CFG));
    if (saved) cfg = { ...cfg, ...saved };
  } catch (e) {}

  let solves = [];
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_SOLVES));
    if (Array.isArray(saved)) solves = saved;
  } catch (e) {}

  function hexToRgb(hex) {
    const clean = hex.replace("#", "");
    const num = parseInt(clean.length === 3 ? clean.split("").map(c => c + c).join("") : clean, 16);
    return {
      r: (num >> 16) & 255,
      g: (num >> 8) & 255,
      b: num & 255
    };
  }

  let accentRgb = hexToRgb(cfg.accentColor);

  // Build Analog Clock Dial Ticks
  const analogTicksEl = document.getElementById("analogTicks");
  for (let i = 0; i < 12; i++) {
    const angle = i * 30;
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", "60");
    line.setAttribute("y1", i % 3 === 0 ? "9" : "11");
    line.setAttribute("x2", "60");
    line.setAttribute("y2", i % 3 === 0 ? "17" : "15");
    line.setAttribute("transform", `rotate(${angle} 60 60)`);
    analogTicksEl.appendChild(line);
  }

  // Real-Life Clock Engine & Drag Placement
  const clockEl = document.getElementById("clockPlasmoid");
  const dockedClockEl = document.getElementById("dockedClock");
  const clockDigitalEl = document.getElementById("clockDigitalTime");
  const clockDateEl = document.getElementById("clockDateLine");
  const clockTzEl = document.getElementById("clockTzTag");
  const handHourEl = document.getElementById("handHour");
  const handMinEl = document.getElementById("handMin");
  const handSecEl = document.getElementById("handSec");

  function positionClockFromRatios() {
    const w = window.innerWidth;
    const h = window.innerHeight;
    const rect = clockEl.getBoundingClientRect();
    const maxX = Math.max(8, w - (rect.width || 180) - 8);
    const maxY = Math.max(64, h - (rect.height || 90) - 8);
    const px = Math.min(maxX, Math.max(8, cfg.clockXRatio * w));
    const py = Math.min(maxY, Math.max(64, cfg.clockYRatio * h));
    clockEl.style.left = px + "px";
    clockEl.style.top = py + "px";
  }

  function snapClockToAnchor(pos) {
    cfg.clockDocked = false;
    cfg.clockAnchor = pos;
    const w = window.innerWidth;
    const h = window.innerHeight;
    const rect = clockEl.getBoundingClientRect();
    const cw = rect.width || 190;
    const ch = rect.height || 90;
    const padX = 22;
    const topY = 74;
    const botY = Math.max(topY, h - ch - 24);
    const midY = Math.max(topY, (h - ch) / 2);

    let x = padX;
    let y = topY;
    if (pos.endsWith("c")) x = Math.max(padX, (w - cw) / 2);
    if (pos.endsWith("r")) x = Math.max(padX, w - cw - padX);
    if (pos.startsWith("m")) y = midY;
    if (pos.startsWith("b")) y = botY;

    cfg.clockXRatio = x / w;
    cfg.clockYRatio = y / h;
    saveCfg();
  }

  function updateRealLifeClock() {
    const now = new Date();
    const tzOption = cfg.clockTz === "local" ? undefined : cfg.clockTz;

    let partsMap = {};
    try {
      const fmt = new Intl.DateTimeFormat("en-US", {
        timeZone: tzOption,
        hour12: !cfg.clock24h,
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        weekday: "short",
        month: "short",
        day: "numeric",
        year: "numeric"
      });
      for (const p of fmt.formatToParts(now)) {
        partsMap[p.type] = p.value;
      }
    } catch (e) {
      partsMap = {
        hour: String(now.getHours()).padStart(2, "0"),
        minute: String(now.getMinutes()).padStart(2, "0"),
        second: String(now.getSeconds()).padStart(2, "0"),
        weekday: "Day",
        month: "Mon",
        day: String(now.getDate()),
        year: String(now.getFullYear())
      };
    }

    const hh = partsMap.hour || "00";
    const mm = partsMap.minute || "00";
    const ss = partsMap.second || "00";
    const dayPeriod = !cfg.clock24h && partsMap.dayPeriod ? `<span class="clock-ampm">${partsMap.dayPeriod}</span>` : "";

    const timeStr = cfg.clockSeconds ? `${hh}:${mm}:${ss}` : `${hh}:${mm}`;
    clockDigitalEl.innerHTML = timeStr + dayPeriod;
    dockedClockEl.textContent = cfg.clockSeconds ? `${hh}:${mm}:${ss}` : `${hh}:${mm}`;

    clockDateEl.style.display = cfg.clockDate ? "block" : "none";
    clockDateEl.textContent = `${partsMap.weekday}, ${partsMap.month} ${partsMap.day}, ${partsMap.year}`;

    clockTzEl.style.display = cfg.clockTz === "local" ? "none" : "block";
    clockTzEl.textContent = cfg.clockTz.replace("_", " ");

    // Analog hands
    const hNum = parseInt(hh, 10) % 12;
    const mNum = parseInt(mm, 10);
    const sNum = parseInt(ss, 10);
    const secDeg = sNum * 6;
    const minDeg = mNum * 6 + sNum * 0.1;
    const hourDeg = hNum * 30 + mNum * 0.5;

    handSecEl.style.display = cfg.clockSeconds ? "block" : "none";
    handSecEl.setAttribute("transform", `rotate(${secDeg} 60 60)`);
    handMinEl.setAttribute("transform", `rotate(${minDeg} 60 60)`);
    handHourEl.setAttribute("transform", `rotate(${hourDeg} 60 60)`);
  }

  // Drag Clock Plasmoid in Edit Mode
  let editMode = false;
  let draggingClock = false;
  let dragOffsetX = 0;
  let dragOffsetY = 0;

  clockEl.addEventListener("pointerdown", e => {
    if (!editMode) return;
    draggingClock = true;
    const rect = clockEl.getBoundingClientRect();
    dragOffsetX = e.clientX - rect.left;
    dragOffsetY = e.clientY - rect.top;
    clockEl.setPointerCapture(e.pointerId);
  });

  window.addEventListener("pointermove", e => {
    if (!draggingClock) return;
    const w = window.innerWidth;
    const h = window.innerHeight;
    const rect = clockEl.getBoundingClientRect();
    const nx = Math.min(w - rect.width - 8, Math.max(8, e.clientX - dragOffsetX));
    const ny = Math.min(h - rect.height - 8, Math.max(62, e.clientY - dragOffsetY));
    clockEl.style.left = nx + "px";
    clockEl.style.top = ny + "px";
    cfg.clockXRatio = nx / w;
    cfg.clockYRatio = ny / h;
    cfg.clockAnchor = "custom";
  });

  window.addEventListener("pointerup", () => {
    if (!draggingClock) return;
    draggingClock = false;
    saveCfg();
  });

  function setEditMode(active) {
    editMode = active;
    document.body.classList.toggle("edit-mode", editMode);
    document.getElementById("editModeNavBtn").classList.toggle("active", editMode);
  }

  // Procedural Scenic & Atmospheric Background Canvas
  const canvas = document.getElementById("bgCanvas");
  const ctx = canvas.getContext("2d");

  let particles = [];
  let clouds = [];
  let rainDrops = [];
  let ripples = [];
  let treesFar = [];
  let treesNear = [];
  let lightningAlpha = 0;

  function initSceneEntities() {
    const w = canvas.width;
    const h = canvas.height;

    particles = Array.from({ length: 120 }, () => ({
      x: Math.random() * w,
      y: Math.random() * h,
      r: Math.random() * 2 + 0.7,
      vx: (Math.random() - 0.5) * 0.3,
      vy: (Math.random() - 0.5) * 0.3,
      phase: Math.random() * Math.PI * 2,
      a: Math.random() * 0.5 + 0.15
    }));

    clouds = Array.from({ length: 18 }, (_, i) => ({
      x: (i / 18) * (w + 500) - 250,
      y: 45 + Math.random() * (h * 0.65),
      scale: 0.65 + Math.random() * 0.85,
      speed: 0.14 + Math.random() * 0.22,
      alpha: 0.08 + Math.random() * 0.1
    }));

    rainDrops = Array.from({ length: 280 }, () => ({
      x: Math.random() * (w + 260),
      y: Math.random() * h,
      len: 14 + Math.random() * 18,
      speed: 9 + Math.random() * 7,
      alpha: 0.16 + Math.random() * 0.25
    }));

    treesFar = [];
    for (let x = -40; x < w + 80; x += 48 + Math.random() * 28) {
      treesFar.push({
        x,
        height: 110 + Math.random() * 85,
        width: 34 + Math.random() * 18
      });
    }

    treesNear = [];
    for (let x = -40; x < w + 80; x += 64 + Math.random() * 34) {
      treesNear.push({
        x,
        height: 155 + Math.random() * 110,
        width: 48 + Math.random() * 22
      });
    }
  }

  function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    initSceneEntities();
    positionClockFromRatios();
  }
  window.addEventListener("resize", resizeCanvas);
  resizeCanvas();

  function drawCloudShape(x, y, scale, alpha) {
    const { r, g, b } = accentRgb;
    ctx.save();
    ctx.translate(x, y);
    ctx.scale(scale, scale);
    ctx.fillStyle = `rgba(${Math.round((r + 255) / 2)}, ${Math.round((g + 255) / 2)}, ${Math.round((b + 255) / 2)}, ${Math.min(0.45, alpha)})`;
    ctx.beginPath();
    ctx.arc(0, 0, 42, 0, Math.PI * 2);
    ctx.arc(38, -10, 50, 0, Math.PI * 2);
    ctx.arc(84, -4, 44, 0, Math.PI * 2);
    ctx.arc(118, 8, 32, 0, Math.PI * 2);
    ctx.arc(-34, 10, 30, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  }

  function drawPineTree(x, baseY, width, height, color) {
    ctx.fillStyle = color;
    const tiers = 4;
    for (let t = 0; t < tiers; t++) {
      const ratio = t / tiers;
      const tierTop = baseY - height + ratio * (height * 0.55);
      const tierBottom = tierTop + height * 0.42;
      const halfW = (width * 0.5) * (0.45 + ratio * 0.65);
      ctx.beginPath();
      ctx.moveTo(x, tierTop);
      ctx.lineTo(x - halfW, tierBottom);
      ctx.lineTo(x + halfW, tierBottom);
      ctx.closePath();
      ctx.fill();
    }
  }

  function drawBackgroundScene(now) {
    const w = canvas.width;
    const h = canvas.height;
    const { r, g, b } = accentRgb;
    const sz = cfg.sceneSize;
    const sp = cfg.sceneSpeed;
    const inten = cfg.sceneIntensity;

    ctx.clearRect(0, 0, w, h);

    if (cfg.scene === "clouds") {
      const grad = ctx.createLinearGradient(0, 0, 0, h);
      grad.addColorStop(0, `rgba(${r}, ${g}, ${b}, ${Math.min(0.35, 0.15 * inten)})`);
      grad.addColorStop(1, "rgba(7, 17, 32, 0.2)");
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, w, h);

      const activeCount = Math.max(2, Math.min(clouds.length, Math.round(9 * inten)));
      for (let i = 0; i < activeCount; i++) {
        const c = clouds[i];
        c.x += c.speed * sp;
        if (c.x > w + 260) c.x = -260;
        drawCloudShape(c.x, c.y, c.scale * sz, c.alpha * Math.min(1.5, 0.7 + inten * 0.3));
      }
      return;
    }

    if (cfg.scene === "forest") {
      const mist = ctx.createLinearGradient(0, h - 220 * sz, 0, h);
      mist.addColorStop(0, `rgba(${r}, ${g}, ${b}, 0)`);
      mist.addColorStop(1, `rgba(${r}, ${g}, ${b}, ${Math.min(0.35, 0.16 * inten)})`);
      ctx.fillStyle = mist;
      ctx.fillRect(0, h - 220 * sz, w, 220 * sz);

      for (const t of treesFar) {
        drawPineTree(
          t.x,
          h,
          t.width * (0.7 + sz * 0.3),
          t.height * (0.65 + sz * 0.35),
          `rgba(${Math.round(r * 0.14)}, ${Math.round(g * 0.22)}, ${Math.round(b * 0.18)}, 0.72)`
        );
      }
      for (const t of treesNear) {
        drawPineTree(
          t.x,
          h,
          t.width * (0.7 + sz * 0.3),
          t.height * (0.65 + sz * 0.35),
          `rgba(${Math.round(r * 0.08)}, ${Math.round(g * 0.14)}, ${Math.round(b * 0.11)}, 0.94)`
        );
      }

      const fireflyCount = Math.max(10, Math.min(particles.length, Math.round(50 * inten)));
      for (let i = 0; i < fireflyCount; i++) {
        const p = particles[i];
        p.x += (p.vx + Math.sin(now * 0.001 + p.phase) * 0.18) * sp;
        p.y += (p.vy - 0.12) * sp;
        if (p.x < 0) p.x = w;
        if (p.x > w) p.x = 0;
        if (p.y < 0) p.y = h - 40;
        const glow = Math.min(0.95, (0.25 + 0.45 * Math.abs(Math.sin(now * 0.002 + p.phase))) * inten);
        ctx.beginPath();
        ctx.arc(p.x, p.y, (p.r + 0.6) * sz, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${r}, ${g}, ${b}, ${glow})`;
        ctx.fill();
      }
      return;
    }

    if (cfg.scene === "rain") {
      if (Math.random() < 0.0025 * inten) lightningAlpha = Math.min(0.26, 0.14 * inten);
      if (lightningAlpha > 0.002) {
        ctx.fillStyle = `rgba(${r}, ${g}, ${b}, ${lightningAlpha})`;
        ctx.fillRect(0, 0, w, h);
        lightningAlpha *= 0.88;
      }

      ctx.lineWidth = Math.max(0.8, 1.15 * sz);
      const dropCount = Math.max(25, Math.min(rainDrops.length, Math.round(135 * inten)));
      for (let i = 0; i < dropCount; i++) {
        const d = rainDrops[i];
        const vy = d.speed * sp;
        d.x -= vy * 0.24;
        d.y += vy;
        if (d.y > h - 8) {
          if (Math.random() < 0.25 && ripples.length < Math.round(35 * inten)) {
            ripples.push({ x: d.x, y: h - 6 - Math.random() * 14, r: 1, a: 0.35 });
          }
          d.y = -20;
          d.x = Math.random() * (w + 260);
        }
        const scaledLen = d.len * sz;
        ctx.strokeStyle = `rgba(${r}, ${g}, ${b}, ${Math.min(0.85, d.alpha * (0.65 + inten * 0.35))})`;
        ctx.beginPath();
        ctx.moveTo(d.x, d.y);
        ctx.lineTo(d.x + scaledLen * 0.24, d.y - scaledLen);
        ctx.stroke();
      }

      for (let i = ripples.length - 1; i >= 0; i--) {
        const rp = ripples[i];
        rp.r += 0.65 * sp;
        rp.a *= 0.93;
        ctx.strokeStyle = `rgba(${r}, ${g}, ${b}, ${rp.a})`;
        ctx.beginPath();
        ctx.ellipse(rp.x, rp.y, rp.r * 2.2 * sz, rp.r * 0.55 * sz, 0, 0, Math.PI * 2);
        ctx.stroke();
        if (rp.a < 0.02) ripples.splice(i, 1);
      }
      return;
    }

    if (cfg.scene === "snow") {
      const flakeCount = Math.max(15, Math.min(particles.length, Math.round(60 * inten)));
      for (let i = 0; i < flakeCount; i++) {
        const p = particles[i];
        p.y += (0.65 + p.r * 0.35) * sp;
        p.x += Math.sin(now * 0.0012 + p.phase) * 0.45 * sp;
        if (p.y > h) {
          p.y = -10;
          p.x = Math.random() * w;
        }
        ctx.beginPath();
        ctx.arc(p.x, p.y, (p.r + 0.8) * sz, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${Math.round((r + 255) / 2)}, ${Math.round((g + 255) / 2)}, ${Math.round((b + 255) / 2)}, ${Math.min(0.95, p.a + 0.2)})`;
        ctx.fill();
      }
      return;
    }

    if (cfg.scene === "galaxy") {
      const starCount = Math.max(15, Math.min(particles.length, Math.round(60 * inten)));
      for (let i = 0; i < starCount; i++) {
        const p = particles[i];
        p.x += p.vx * sp;
        p.y += p.vy * sp;
        if (p.x < 0) p.x = w;
        if (p.x > w) p.x = 0;
        if (p.y < 0) p.y = h;
        if (p.y > h) p.y = 0;
        const twinkle = Math.min(0.95, p.a * (0.65 + 0.35 * Math.sin(now * 0.003 * sp + p.phase)) * inten);
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r * sz, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${r}, ${g}, ${b}, ${twinkle})`;
        ctx.fill();
      }
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

  function updateSliderLabels() {
    const labelMap = {
      rain: ["Drop Size", "Fall Speed", "Rain Intensity"],
      clouds: ["Cloud Size", "Drift Speed", "Cloud Density"],
      snow: ["Flake Size", "Fall Speed", "Snow Intensity"],
      forest: ["Tree & Firefly Size", "Drift Speed", "Mist & Fireflies"],
      galaxy: ["Star Size", "Drift Speed", "Star Density"],
      minimal: ["Glow Scale", "Motion Speed", "Glow Intensity"]
    };
    const labels = labelMap[cfg.scene] || ["Size", "Speed", "Intensity"];
    document.getElementById("sizeSliderLabel").textContent = labels[0];
    document.getElementById("speedSliderLabel").textContent = labels[1];
    document.getElementById("intensitySliderLabel").textContent = labels[2];

    document.getElementById("sceneSizeSlider").value = cfg.sceneSize;
    document.getElementById("sceneSpeedSlider").value = cfg.sceneSpeed;
    document.getElementById("sceneIntensitySlider").value = cfg.sceneIntensity;

    document.getElementById("sizeSliderVal").textContent = cfg.sceneSize.toFixed(1) + "x";
    document.getElementById("speedSliderVal").textContent = cfg.sceneSpeed.toFixed(1) + "x";
    document.getElementById("intensitySliderVal").textContent = Math.round(cfg.sceneIntensity * 100) + "%";
  }

  function syncLabels() {
    document.body.dataset.scene = cfg.scene;
    document.body.classList.toggle("floating-panel", Boolean(cfg.floatingPanel));
    document.body.classList.toggle("show-nav-labels", Boolean(cfg.showLabels));
    document.body.classList.toggle("clock-docked", Boolean(cfg.clockEnabled && cfg.clockDocked));
    document.body.classList.toggle("hide-clock-running", Boolean(cfg.clockHideRunning));

    document.getElementById("toggleFloatingPanelChk").checked = Boolean(cfg.floatingPanel);
    document.getElementById("toggleLabelsChk").checked = Boolean(cfg.showLabels);
    document.getElementById("toggleNotationChk").checked = Boolean(cfg.showNotation);
    document.getElementById("notationColorPicker").value = cfg.notationColor;

    // Clock UI sync
    document.getElementById("clockEnabledChk").checked = Boolean(cfg.clockEnabled);
    document.getElementById("clock24hChk").checked = Boolean(cfg.clock24h);
    document.getElementById("clockSecChk").checked = Boolean(cfg.clockSeconds);
    document.getElementById("clockDateChk").checked = Boolean(cfg.clockDate);
    document.getElementById("clockBorderChk").checked = Boolean(cfg.clockBorder);
    document.getElementById("clockHideRunChk").checked = Boolean(cfg.clockHideRunning);
    document.getElementById("clockTzSelect").value = cfg.clockTz;
    document.getElementById("clockFontSelect").value = cfg.clockFont;
    document.getElementById("clockColorPicker").value = cfg.clockColor;
    document.getElementById("clockScaleSlider").value = cfg.clockScale;
    document.getElementById("clockScaleVal").textContent = Number(cfg.clockScale).toFixed(2) + "x";
    document.getElementById("clockOpacitySlider").value = cfg.clockOpacity;
    document.getElementById("clockOpacityVal").textContent = Math.round(cfg.clockOpacity * 100) + "%";

    clockEl.classList.toggle("hidden", !cfg.clockEnabled);
    clockEl.classList.toggle("no-border", !cfg.clockBorder);
    clockEl.dataset.style = cfg.clockStyle;
    document.getElementById("dockClockBtn").classList.toggle("active", Boolean(cfg.clockDocked));

    document.querySelectorAll(".clock-style-btn").forEach(btn => {
      btn.classList.toggle("active", btn.dataset.style === cfg.clockStyle);
    });
    document.querySelectorAll(".anchor-btn").forEach(btn => {
      btn.classList.toggle("active", !cfg.clockDocked && btn.dataset.pos === cfg.clockAnchor);
    });

    accentRgb = hexToRgb(cfg.accentColor);
    const { r, g, b } = accentRgb;
    const inten = cfg.sceneIntensity;
    const cueRgb = hexToRgb(cfg.notationColor);
    const root = document.documentElement.style;
    root.setProperty("--accent", cfg.accentColor);
    root.setProperty("--accent-rgb", `${r}, ${g}, ${b}`);
    root.setProperty("--accent-glow", `rgba(${r}, ${g}, ${b}, 0.38)`);
    root.setProperty("--bg-glow-1", `rgba(${r}, ${g}, ${b}, ${Math.min(0.45, 0.24 * inten)})`);
    root.setProperty("--bg-glow-2", `rgba(${r}, ${g}, ${b}, ${Math.min(0.35, 0.14 * inten)})`);
    root.setProperty("--cue-color", cfg.notationColor);
    root.setProperty("--cue-glow", `rgba(${cueRgb.r}, ${cueRgb.g}, ${cueRgb.b}, 0.9)`);
    root.setProperty("--clock-color", cfg.clockColor);
    root.setProperty("--clock-bg-alpha", cfg.clockOpacity);
    root.setProperty("--clock-scale", cfg.clockScale);
    root.setProperty("--clock-font", cfg.clockFont);
    document.getElementById("customColorPicker").value = cfg.accentColor;

    document.querySelectorAll(".scene-card").forEach(btn => {
      btn.classList.toggle("active", btn.dataset.scene === cfg.scene);
    });
    document.querySelectorAll(".color-swatch-btn").forEach(btn => {
      btn.classList.toggle("active", btn.dataset.color.toLowerCase() === cfg.accentColor.toLowerCase());
    });

    updateSliderLabels();
    positionClockFromRatios();
    updateRealLifeClock();

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
    setEditMode(false);
    closeAllDrawers();
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

  let lastClockSec = -1;
  function tick(now) {
    drawBackgroundScene(now);
    const secNow = Math.floor(now / 250);
    if (secNow !== lastClockSec) {
      lastClockSec = secNow;
      updateRealLifeClock();
    }
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

    if (phase === "RUNNING") {
      if (leftDown && rightDown) stopRun();
      return;
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

  // True 27-Cubie 3D Rubik's Cube Engine with Configurable Borderless Notation Cue
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
  const moveCueOverlay = document.getElementById("moveCueOverlay");
  const moveCueBadge = document.getElementById("moveCueBadge");
  const SPACING = 47;
  let cubies = [];
  let visMoves = [];
  let visStep = 0;
  let isAnimating = false;
  let autoTimer = null;
  let cueTimer = null;
  let cueMs = 580;
  let turnMs = 480;
  let pauseMs = 650;
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

  function clearMoveCue() {
    if (cueTimer) {
      clearTimeout(cueTimer);
      cueTimer = null;
    }
    moveCueOverlay.classList.remove("visible");
  }

  function performLayerTurn(mv, onDone) {
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

  function executeMoveWithNotationCue(mv, stepNumber, onDone) {
    if (isAnimating) return;
    isAnimating = true;

    moveDescEl.textContent = `Step ${stepNumber}/${visMoves.length}: ${mv} — ${MOVE_TEXT[mv] || ""}`;

    if (!cfg.showNotation) {
      performLayerTurn(mv, onDone);
      return;
    }

    moveCueBadge.textContent = mv;
    moveCueOverlay.classList.add("visible");

    cueTimer = setTimeout(() => {
      cueTimer = null;
      moveCueOverlay.classList.remove("visible");
      performLayerTurn(mv, onDone);
    }, cueMs);
  }

  function stopAutoPlay() {
    if (autoTimer) {
      clearTimeout(autoTimer);
      autoTimer = null;
    }
    clearMoveCue();
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
    executeMoveWithNotationCue(mv, visStep, () => {
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
    executeMoveWithNotationCue(mv, visStep);
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
      cueMs = Number(btn.dataset.cue);
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

  // Right-Side Drawer Navigation (Themes, Config, History)
  const drawers = document.querySelectorAll(".side-drawer");
  const navBtns = document.querySelectorAll(".emoji-nav-btn[data-drawer]");

  function closeAllDrawers() {
    bindingTarget = null;
    drawers.forEach(d => d.classList.remove("open"));
    navBtns.forEach(b => b.classList.remove("active"));
    syncLabels();
  }

  navBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const targetId = btn.dataset.drawer;
      const targetDrawer = document.getElementById(targetId);
      const wasOpen = targetDrawer.classList.contains("open");
      closeAllDrawers();
      if (!wasOpen) {
        targetDrawer.classList.add("open");
        btn.classList.add("active");
      }
    });
  });

  document.querySelectorAll(".close-drawer-btn").forEach(btn => {
    btn.addEventListener("click", closeAllDrawers);
  });

  // Edit Mode Wiring
  document.getElementById("editModeNavBtn").addEventListener("click", () => setEditMode(!editMode));
  document.getElementById("toggleEditFromConfigBtn").addEventListener("click", () => setEditMode(!editMode));
  document.getElementById("exitEditModeBtn").addEventListener("click", () => setEditMode(false));

  // UI Wiring
  document.querySelectorAll("button").forEach(btn => btn.addEventListener("focus", () => btn.blur()));
  scrambleEl.addEventListener("click", openVisualizer);
  document.getElementById("newScrambleBtn").addEventListener("click", newScramble);

  // Scene, Color & Physics Sliders
  document.querySelectorAll(".scene-card").forEach(btn => {
    btn.addEventListener("click", () => {
      cfg.scene = btn.dataset.scene;
      saveCfg();
    });
  });

  document.querySelectorAll(".color-swatch-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      cfg.accentColor = btn.dataset.color;
      saveCfg();
    });
  });

  document.getElementById("customColorPicker").addEventListener("input", e => {
    cfg.accentColor = e.target.value;
    saveCfg();
  });

  document.getElementById("sceneSizeSlider").addEventListener("input", e => {
    cfg.sceneSize = parseFloat(e.target.value);
    saveCfg();
  });

  document.getElementById("sceneSpeedSlider").addEventListener("input", e => {
    cfg.sceneSpeed = parseFloat(e.target.value);
    saveCfg();
  });

  document.getElementById("sceneIntensitySlider").addEventListener("input", e => {
    cfg.sceneIntensity = parseFloat(e.target.value);
    saveCfg();
  });

  // Clock Customization Controls
  document.getElementById("clockEnabledChk").addEventListener("change", e => {
    cfg.clockEnabled = e.target.checked;
    saveCfg();
  });

  document.querySelectorAll(".clock-style-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      cfg.clockStyle = btn.dataset.style;
      saveCfg();
    });
  });

  document.getElementById("dockClockBtn").addEventListener("click", () => {
    cfg.clockDocked = !cfg.clockDocked;
    saveCfg();
  });

  document.querySelectorAll(".anchor-btn").forEach(btn => {
    btn.addEventListener("click", () => snapClockToAnchor(btn.dataset.pos));
  });

  document.getElementById("clockTzSelect").addEventListener("change", e => {
    cfg.clockTz = e.target.value;
    saveCfg();
  });

  document.getElementById("clockFontSelect").addEventListener("change", e => {
    cfg.clockFont = e.target.value;
    saveCfg();
  });

  document.getElementById("clock24hChk").addEventListener("change", e => {
    cfg.clock24h = e.target.checked;
    saveCfg();
  });

  document.getElementById("clockSecChk").addEventListener("change", e => {
    cfg.clockSeconds = e.target.checked;
    saveCfg();
  });

  document.getElementById("clockDateChk").addEventListener("change", e => {
    cfg.clockDate = e.target.checked;
    saveCfg();
  });

  document.getElementById("clockBorderChk").addEventListener("change", e => {
    cfg.clockBorder = e.target.checked;
    saveCfg();
  });

  document.getElementById("clockHideRunChk").addEventListener("change", e => {
    cfg.clockHideRunning = e.target.checked;
    saveCfg();
  });

  document.getElementById("clockColorPicker").addEventListener("input", e => {
    cfg.clockColor = e.target.value;
    saveCfg();
  });

  document.getElementById("clockScaleSlider").addEventListener("input", e => {
    cfg.clockScale = parseFloat(e.target.value);
    saveCfg();
  });

  document.getElementById("clockOpacitySlider").addEventListener("input", e => {
    cfg.clockOpacity = parseFloat(e.target.value);
    saveCfg();
  });

  // History Controls
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

  // Config Controls
  document.getElementById("toggleFloatingPanelChk").addEventListener("change", e => {
    cfg.floatingPanel = e.target.checked;
    saveCfg();
  });

  document.getElementById("toggleLabelsChk").addEventListener("change", e => {
    cfg.showLabels = e.target.checked;
    saveCfg();
  });

  document.getElementById("toggleNotationChk").addEventListener("change", e => {
    cfg.showNotation = e.target.checked;
    if (!cfg.showNotation) clearMoveCue();
    saveCfg();
  });

  document.getElementById("notationColorPicker").addEventListener("input", e => {
    cfg.notationColor = e.target.value;
    saveCfg();
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
    cfg = { ...DEFAULT_CFG };
    bindingTarget = null;
    setEditMode(false);
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
