import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="ぽよぽよ電車ジャンプ！", layout="wide")

# タイトル
st.title("🍄 激闘！特攻カラスと回転列車 🚂🌀🆚🦅")
st.write("ボス戦の操作が変わったよ！【スワイプ：移動】【タップ：発射】だっち！先頭車両だけになっても諦めるな！")

# HTML/CSS/JSコード
html_code = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style>
    /* --- CSS (スタイル設定) --- */
    :root {
        --sky-top-day: #87CEEB; --sky-bottom-day: #E0F7FA;
        --water-top-day: #40a4df; --water-bottom-day: #0077be;
        --bridge-base-day: #A0522D; --bridge-top-day: #5D4037;
        
        --sky-top-night: #0a0a2a; --sky-bottom-night: #2a0a5a;
        --water-top-night: #050520; --water-bottom-night: #1a0a3a;
        --bridge-base-night: #4a5b6c; --bridge-top-night: #2a3b4c;

        --current-sky-top: var(--sky-top-day); --current-sky-bottom: var(--sky-bottom-day);
        --current-water-top: var(--water-top-day); --current-water-bottom: var(--water-bottom-day);
        --current-bridge-base: var(--bridge-base-day); --current-bridge-top: var(--bridge-top-day);
        --bridge-height: 280px;
    }

    #game-screen {
        width: 100%; height: 600px;
        background: linear-gradient(to bottom, var(--current-sky-top) 0%, var(--current-sky-bottom) 70%, var(--current-water-top) 70%, var(--current-water-bottom) 100%);
        position: relative; overflow: hidden; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        user-select: none; cursor: pointer; transition: background 1s ease;
        touch-action: none; /* スワイプ時の画面スクロール防止 */
    }

    /* 雲・星・月 */
    .cloud { position: absolute; background: rgba(255, 255, 255, 0.9); border-radius: 50px; z-index: 1; transition: opacity 1s ease; opacity: 1; }
    .cloud::after, .cloud::before { content: ''; position: absolute; background: inherit; border-radius: 50%; }
    .cloud.c1 { width: 120px; height: 40px; top: 60px; left: 10%; } .cloud.c1::after { width: 50px; height: 50px; top: -20px; left: 15px; } .cloud.c1::before { width: 40px; height: 40px; top: -15px; left: 50px; }
    .cloud.c2 { width: 80px; height: 30px; top: 150px; left: 60%; } .cloud.c2::after { width: 35px; height: 35px; top: -15px; left: 10px; }
    .star { position: absolute; background: #FFF; border-radius: 50%; z-index: 0; opacity: 0; display: none; box-shadow: 0 0 4px #FFF; }
    .star.drawn { width: 10px; height: 10px; background: #FFD700; clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%); animation: twinkle 2s infinite alternate; }
    .moon { position: absolute; top: 40px; right: 60px; width: 60px; height: 60px; background: transparent; border-radius: 50%; box-shadow: -15px 15px 0 0 #FFD700; opacity: 0; display: none; z-index: 0; transform: rotate(-10deg); animation: floatMoon 3s ease-in-out infinite alternate; }
    @keyframes floatMoon { from { transform: rotate(-10deg) translateY(0); } to { transform: rotate(-10deg) translateY(-10px); } }
    @keyframes twinkle { from { transform: scale(0.8); opacity: 0.7; } to { transform: scale(1.1); opacity: 1; } }

    #game-screen.galaxy-mode .cloud { opacity: 0; display: none; }
    #game-screen.galaxy-mode .star, #game-screen.galaxy-mode .moon { display: block; opacity: 1; }
    #game-screen.galaxy-mode .train-body { box-shadow: 0 0 15px #00BFFF, inset 0 0 5px #E0FFFF; border-color: #00BFFF; }

    /* ボス戦アラート */
    #boss-alert {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(255, 0, 0, 0.3); z-index: 40; display: none;
        justify-content: center; align-items: center;
        font-size: 60px; font-weight: bold; color: yellow; text-shadow: 4px 4px 0 red;
        animation: flashAlert 0.5s infinite alternate; pointer-events: none;
    }
    @keyframes flashAlert { from { opacity: 0.2; } to { opacity: 0.8; } }

    /* ★ボスキャラ：メカ・キングクロウ★ */
    .boss {
        position: absolute; width: 120px; height: 120px; z-index: 20;
        right: 20px; top: 50%; display: none;
        animation: bossFloat 2s ease-in-out infinite alternate;
    }
    .boss-body { position: absolute; width: 100px; height: 80px; top: 20px; left: 10px; background: #222; border-radius: 50%; border: 4px solid #aaa; box-shadow: inset 0 0 20px #000; }
    .boss-eye { position: absolute; width: 20px; height: 20px; background: #f00; border-radius: 50%; top: 20px; left: 20px; box-shadow: 0 0 10px #f00; animation: blink 0.2s infinite alternate; }
    .boss-beak { position: absolute; width: 0; height: 0; border-top: 15px solid transparent; border-bottom: 15px solid transparent; border-right: 30px solid #FFD700; top: 40px; left: -20px; }
    .boss-crown { position: absolute; top: -20px; left: 30px; font-size: 40px; }
    .boss-wing { position: absolute; width: 60px; height: 40px; background: #444; border-radius: 50% 50% 0 0; top: -10px; left: 20px; animation: flapBoss 0.5s infinite alternate; }
    .boss-hp-bar { position: absolute; top: -30px; left: 0; width: 100%; height: 10px; background: #333; border: 2px solid #fff; }
    .boss-hp-current { width: 100%; height: 100%; background: #f00; transition: width 0.2s; }
    @keyframes bossFloat { from { transform: translateY(-10px); } to { transform: translateY(10px); } }
    @keyframes blink { from { opacity: 0.5; } to { opacity: 1; } }
    @keyframes flapBoss { from { transform: rotate(0deg); } to { transform: rotate(-20deg); } }

    /* プレイヤーの弾（車両ミサイル） */
    .train-missile { position: absolute; z-index: 15; pointer-events: none; }
    .train-missile .train-unit { transform: rotate(0deg); }

    /* 爆発エフェクト */
    .explosion { position: absolute; font-size: 40px; pointer-events: none; z-index: 50; animation: fadeOut 0.5s forwards; }
    @keyframes fadeOut { from { opacity: 1; transform: scale(1); } to { opacity: 0; transform: scale(2); } }

    /* 背景要素 */
    #obstacles-container { position: absolute; bottom: 0; left: 0; width: 100%; height: var(--bridge-height); z-index: 5; }
    .bridge-part {
        position: absolute; bottom: 0; height: 100%; background-color: var(--current-bridge-base);
        background-image: radial-gradient(circle at bottom center, transparent 60%, var(--current-bridge-base) 61%), linear-gradient(rgba(0,0,0,0.1) 2px, transparent 2px);
        background-size: 200px 280px, 100% 20px; background-repeat: repeat-x, repeat; background-position: bottom left; box-sizing: border-box; transition: background-color 1s ease;
    }
    .bridge-part::after { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 15px; background: var(--current-bridge-top); transition: background 1s ease; z-index: 2; }
    .bridge-part::before {
        content: ''; position: absolute; top: -5px; left: 0; width: 100%; height: 15px;
        background: repeating-linear-gradient(45deg, #ff0000, #ff0000 10px, #ff7f00 10px, #ff7f00 20px, #ffff00 20px, #ffff00 30px, #00ff00 30px, #00ff00 40px, #0000ff 40px, #0000ff 50px, #4b0082 50px, #4b0082 60px, #9400d3 60px, #9400d3 70px);
        z-index: 3; opacity: 0; transition: opacity 1s ease; background-size: 200% 100%; animation: rainbowMove 2s linear infinite;
    }
    @keyframes rainbowMove { 0% { background-position: 0 0; } 100% { background-position: 100px 0; } }
    #game-screen.galaxy-mode .bridge-part::before { opacity: 1; } #game-screen.galaxy-mode .bridge-part::after { opacity: 0; }

    .item { position: absolute; bottom: 50px; width: 30px; height: 20px; background: #FFD700; border: 2px solid #FFA000; border-radius: 4px; z-index: 6; display: flex; justify-content: center; align-items: center; box-shadow: 0 0 10px rgba(255, 215, 0, 0.6); animation: floatItem 1s ease-in-out infinite alternate; } .item::after { content: '+1'; font-size: 12px; font-weight: bold; color: #8B4500; } @keyframes floatItem { from { transform: translateY(0); } to { transform: translateY(-10px); } }
    
    /* ロケット */ .rocket { position: absolute; width: 60px; height: 30px; z-index: 2; } .rocket-body { position: absolute; top: 5px; left: 10px; width: 40px; height: 20px; background: #f0f0f0; border-radius: 10% 50% 50% 10%; border: 2px solid #ccc; } .rocket-fin { position: absolute; width: 15px; height: 15px; background: #ff4500; } .rocket-fin.top { top: 0; left: 5px; clip-path: polygon(100% 100%, 0 0, 0 100%); } .rocket-fin.bottom { bottom: 0; left: 5px; clip-path: polygon(100% 0, 0 0, 0 100%); } .rocket-window { position: absolute; top: 8px; right: 15px; width: 8px; height: 8px; background: #87CEEB; border-radius: 50%; border: 2px solid #555; } .rocket-fire { position: absolute; top: 10px; left: -15px; width: 20px; height: 10px; background: linear-gradient(to right, #ffff00, #ff4500); border-radius: 50% 0 0 50%; animation: flicker 0.2s infinite alternate; } @keyframes flicker { from { transform: scaleX(1); opacity: 1; } to { transform: scaleX(0.8); opacity: 0.7; } }
    .rocket-right { animation: flyRight 8s linear forwards; } @keyframes flyRight { from { left: -100px; top: 20%; transform: rotate(0deg); } to { left: 120%; top: 20%; transform: rotate(0deg); } }
    .rocket-left { animation: flyLeft 8s linear forwards; } @keyframes flyLeft { from { left: 120%; top: 50%; transform: rotate(180deg); } to { left: -100px; top: 50%; transform: rotate(180deg); } }
    .rocket-up { animation: flyUp 8s linear forwards; } @keyframes flyUp { from { left: 50%; top: 120%; transform: rotate(-90deg); } to { left: 50%; top: -100px; transform: rotate(-90deg); } }
    .rocket-down { animation: flyDown 8s linear forwards; } @keyframes flyDown { from { left: 30%; top: -100px; transform: rotate(90deg); } to { left: 30%; top: 120%; transform: rotate(90deg); } }
    .rocket-up-right { animation: flyUpRight 8s linear forwards; } @keyframes flyUpRight { from { left: -100px; top: 120%; transform: rotate(-45deg); } to { left: 120%; top: -100px; transform: rotate(-45deg); } }
    .rocket-down-right { animation: flyDownRight 8s linear forwards; } @keyframes flyDownRight { from { left: -100px; top: -100px; transform: rotate(45deg); } to { left: 120%; top: 120%; transform: rotate(45deg); } }
    .rocket-up-left { animation: flyUpLeft 8s linear forwards; } @keyframes flyUpLeft { from { left: 120%; top: 120%; transform: rotate(-135deg); } to { left: -100px; top: -100px; transform: rotate(-135deg); } }
    .rocket-down-left { animation: flyDownLeft 8s linear forwards; } @keyframes flyDownLeft { from { left: 120%; top: -100px; transform: rotate(135deg); } to { left: -100px; top: 120%; transform: rotate(135deg); } }
    .shooting-star { position: absolute; width: 100px; height: 2px; background: linear-gradient(to right, rgba(255,255,255,0), #fff, rgba(255,255,255,0)); z-index: 0; transform: rotate(-30deg); animation: shoot 3s ease-out forwards; } @keyframes shoot { from { transform: translate(0, 0) rotate(-30deg) scale(0.5); opacity: 1; } to { transform: translate(-500px, 300px) rotate(-30deg) scale(1); opacity: 0; } }

    /* カラス（共通） */
    .crow { position: absolute; width: 50px; height: 30px; z-index: 20; } .crow-body { position: absolute; top: 5px; left: 10px; width: 35px; height: 20px; background: #333; border-radius: 50%; } .crow-head { position: absolute; top: 0; left: 0; width: 18px; height: 18px; background: #333; border-radius: 50%; } .crow-beak { position: absolute; top: 5px; left: -8px; width: 0; height: 0; border-top: 5px solid transparent; border-bottom: 5px solid transparent; border-right: 10px solid #FFD700; } .crow-eye { position: absolute; top: 5px; left: 5px; width: 4px; height: 4px; background: white; border-radius: 50%; } .crow-wing { position: absolute; top: -5px; left: 15px; width: 25px; height: 15px; background: #222; border-radius: 50% 50% 0 0; transform-origin: bottom center; animation: flap 0.2s infinite alternate; } @keyframes flap { from { transform: rotate(0deg) scaleY(1); } to { transform: rotate(-20deg) scaleY(0.5); } }
    .crow-helmet { position: absolute; top: -7px; left: -12px; width: 34px; height: 34px; border-radius: 50%; z-index: 25; display: none; background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.9), rgba(200,240,255,0.3) 60%, transparent 90%); border: 1px solid rgba(255, 255, 255, 0.4); box-shadow: inset -3px -3px 8px rgba(200,240,255,0.2), 0 0 5px rgba(255,255,255,0.3); } .crow.space-mode .crow-helmet { display: block; }
    .stolen-scene { position: absolute; z-index: 30; pointer-events: none; } .stolen-scene .train-unit { transform: rotate(10deg); }

    /* プレイヤー */
    #player-train { position: absolute; left: 100px; height: 40px; z-index: 10; transform-origin: bottom center; display: flex; flex-direction: row-reverse; align-items: flex-end; gap: 2px; transition: top 0.1s ease-out; } 
    #player-train.poyo { animation: poyoPoyo 0.6s steps(3) infinite alternate; }
    
    /* ★きりきり舞い（スタン状態）★ */
    #player-train.stunned {
        animation: spin 0.2s linear infinite !important;
        transition: none; /* 回転中は移動の滑らかさ無効 */
    }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

    .train-unit { position: relative; width: 54px; height: 40px; flex-shrink: 0; } 
    .train-body { width: 100%; height: 28px; background-color: #4DB6AC; border-radius: 6px; border: 2px solid #004D40; position: absolute; bottom: 4.5px; left: 0; display: flex; justify-content: space-evenly; align-items: center; box-shadow: 2px 2px 0px rgba(0,0,0,0.2); box-sizing: border-box; z-index: 2; transition: box-shadow 1s ease, border-color 1s ease; } 
    .train-body::before { content: ''; position: absolute; top: -5px; left: 2px; width: 46px; height: 5px; background-color: #004D40; border-radius: 3px 3px 0 0; } 
    .window { width: 8px; height: 8px; background-color: #FFF9C4; border: 1px solid #004D40; border-radius: 2px; } 
    .wheels-container { position: absolute; bottom: 0; width: 100%; height: 9px; display: flex; justify-content: space-between; padding: 0 8px; box-sizing: border-box; z-index: 1; } 
    .wheel { width: 9px; height: 9px; background-color: #FFC107; border: 1.5px solid #FF6F00; border-radius: 50%; } 
    .smoke { position: absolute; top: -15px; right: 5px; width: 10px; height: 10px; background: white; border-radius: 50%; opacity: 0; z-index: 0; display: none; } 
    .train-unit.head .smoke { display: block; } 
    #player-train.poyo .head .smoke { animation: smokeAnim 1s ease-out infinite; } 
    @keyframes poyoPoyo { 0% { transform: scale(1, 1); } 100% { transform: scale(0.95, 1.05); } } 
    @keyframes smokeAnim { 0% { opacity: 0.8; transform: scale(0.5) translate(0, 0); } 100% { opacity: 0; transform: scale(1.5) translate(-10px, -20px); } } 
    @keyframes landBounce { 0% { transform: scale(1, 1); } 30% { transform: scale(1.1, 0.9); } 60% { transform: scale(0.95, 1.05); } 100% { transform: scale(1, 1); } } 
    .landing { animation: landBounce 0.4s ease-out !important; } 
    .get-effect { position: absolute; color: #FFD700; font-weight: bold; font-size: 20px; animation: floatUp 0.8s ease-out forwards; pointer-events: none; z-index: 20; text-shadow: 1px 1px 0 #000; } 
    @keyframes floatUp { 0% { opacity: 1; transform: translateY(0); } 100% { opacity: 0; transform: translateY(-50px); } }

    #carriage-count-display { position: absolute; top: 20px; left: 20px; font-size: 20px; font-weight: bold; color: #333; z-index: 20; background: rgba(255,255,255,0.8); padding: 5px 15px; border-radius: 10px; }
</style>
</head>
<body>
<div id="game-screen">
    <div class="cloud c1"></div><div class="cloud c2"></div><div id="stars-container"></div><div class="moon"></div>
    <div id="carriage-count-display">車両: 1</div>
    <div id="obstacles-container"></div><div id="sky-container"></div>
    
    <div id="player-train" class="poyo"></div>
    
    <div id="boss-alert">WARNING!</div>
    <div id="boss" class="boss">
        <div class="boss-hp-bar"><div class="boss-hp-current" id="boss-hp"></div></div>
        <div class="boss-wing"></div><div class="boss-body"></div><div class="boss-eye"></div><div class="boss-beak"></div><div class="boss-crown">👑</div>
    </div>
</div>
<script>
    const gameScreen = document.getElementById('game-screen'); const playerTrain = document.getElementById('player-train'); const obstaclesContainer = document.getElementById('obstacles-container'); const skyContainer = document.getElementById('sky-container'); const starsContainer = document.getElementById('stars-container'); const carriageCountDisplay = document.getElementById('carriage-count-display'); const root = document.documentElement;
    const bossAlert = document.getElementById('boss-alert'); const bossElement = document.getElementById('boss'); const bossHpBar = document.getElementById('boss-hp');

    const BRIDGE_HEIGHT = 280; const SCROLL_SPEED = 5; const PLAYER_X = 100; const GRAVITY_DAY = 0.6; const GRAVITY_NIGHT = 0.35; let currentGravity = GRAVITY_DAY; const JUMP_POWER = 12;
    let isGameRunning = false; let animationId; let playerY = BRIDGE_HEIGHT; let playerVy = 0; let isGrounded = true; let isRespawning = false; let isGalaxyMode = false;
    let obstacles = []; let items = []; let crows = []; let stolenScenes = []; let carriageCount = 0;
    
    // ボス戦用変数
    let isBossBattle = false; let bossHP = 10; const MAX_BOSS_HP = 10; let bossY = 300; let bossVy = 2;
    let bossCrows = []; // ボスが撃つカラス
    let playerMissiles = [];
    let isStunned = false; // スタン状態フラグ

    // スワイプ/タップ制御用
    let isDragging = false;
    let dragStartY = 0;
    let trainStartY = 0;

    function createStars() { for (let i = 0; i < 20; i++) { const star = document.createElement('div'); star.classList.add('star', 'drawn'); star.style.left = `${Math.random() * 95}%`; star.style.top = `${Math.random() * 60}%`; const scale = 0.8 + Math.random() * 0.5; star.style.transform = `scale(${scale})`; star.style.animationDelay = `${Math.random() * 3}s`; starsContainer.appendChild(star); } for (let i = 0; i < 50; i++) { const star = document.createElement('div'); star.classList.add('star'); star.style.width = '3px'; star.style.height = '3px'; star.style.left = `${Math.random() * 100}%`; star.style.top = `${Math.random() * 80}%`; star.style.animation = `twinkle ${1 + Math.random()}s infinite alternate`; starsContainer.appendChild(star); } } createStars();
    
    function toggleGalaxyMode(enable) { if (isGalaxyMode === enable) return; isGalaxyMode = enable; if (enable) { gameScreen.classList.add('galaxy-mode'); currentGravity = GRAVITY_NIGHT; root.style.setProperty('--current-sky-top', 'var(--sky-top-night)'); root.style.setProperty('--current-sky-bottom', 'var(--sky-bottom-night)'); root.style.setProperty('--current-water-top', 'var(--water-top-night)'); root.style.setProperty('--current-water-bottom', 'var(--water-bottom-night)'); root.style.setProperty('--current-bridge-base', 'var(--bridge-base-night)'); crows.forEach(crow => crow.element.classList.add('space-mode')); } else { gameScreen.classList.remove('galaxy-mode'); currentGravity = GRAVITY_DAY; root.style.setProperty('--current-sky-top', 'var(--sky-top-day)'); root.style.setProperty('--current-sky-bottom', 'var(--sky-bottom-day)'); root.style.setProperty('--current-water-top', 'var(--water-top-day)'); root.style.setProperty('--current-water-bottom', 'var(--water-bottom-day)'); root.style.setProperty('--current-bridge-base', 'var(--bridge-base-day)'); crows.forEach(crow => crow.element.classList.remove('space-mode')); } }
    function createTrainUnitHTML(isHead) { return `<div class="train-unit ${isHead ? 'head' : 'wagon'}"><div class="smoke"></div><div class="wheels-container"><div class="wheel"></div><div class="wheel"></div></div><div class="train-body"><div class="window"></div><div class="window"></div><div class="window"></div></div></div>`; }
    function renderTrain() { playerTrain.innerHTML = ''; playerTrain.insertAdjacentHTML('beforeend', createTrainUnitHTML(true)); for (let i = 0; i < carriageCount; i++) { playerTrain.insertAdjacentHTML('beforeend', createTrainUnitHTML(false)); } carriageCountDisplay.textContent = `車両: ${carriageCount + 1}`; 
        if (carriageCount + 1 >= 4 && !isBossBattle) toggleGalaxyMode(true); else if (!isBossBattle) toggleGalaxyMode(false);
        if (carriageCount >= 7 && !isBossBattle) startBossBattle();
    }
    
    function initGame() { isGameRunning = true; isRespawning = false; isBossBattle = false; isStunned = false; bossElement.style.display = 'none'; bossAlert.style.display = 'none'; playerTrain.classList.remove('stunned'); playerTrain.classList.add('poyo'); playerY = BRIDGE_HEIGHT; playerVy = 0; isGrounded = true; updatePlayerPosition(); obstacles.forEach(obs => obs.element.remove()); obstacles = []; items.forEach(item => item.element.remove()); items = []; crows.forEach(crow => crow.element.remove()); crows = []; stolenScenes.forEach(s => s.element.remove()); stolenScenes = []; bossCrows.forEach(b => b.element.remove()); bossCrows = []; playerMissiles.forEach(m => m.element.remove()); playerMissiles = []; carriageCount = 0; renderTrain(); createObstacle(0, 2000, 'bridge'); if (animationId) cancelAnimationFrame(animationId); gameLoop(); }
    
    function startBossBattle() {
        isBossBattle = true; toggleGalaxyMode(true); bossAlert.style.display = 'flex';
        setTimeout(() => { bossAlert.style.display = 'none'; bossElement.style.display = 'block'; }, 2000);
        obstacles.forEach(obs => obs.element.remove()); obstacles = []; crows.forEach(c => c.element.remove()); crows = [];
        createObstacle(0, 2000, 'bridge');
        bossHP = MAX_BOSS_HP; bossHpBar.style.width = '100%';
        playerTrain.style.bottom = 'auto'; playerY = 300; updatePlayerPosition();
    }

    // --- シューティング用操作 ---
    function shoot() {
        if (!isBossBattle || carriageCount <= 0 || isStunned) return;
        carriageCount--; renderTrain();
        const missile = document.createElement('div'); missile.classList.add('train-missile');
        missile.innerHTML = createTrainUnitHTML(false); 
        missile.style.left = `${PLAYER_X + 50}px`; missile.style.top = `${600 - playerY - 40}px`;
        skyContainer.appendChild(missile);
        playerMissiles.push({ element: missile, x: PLAYER_X + 50, y: playerY });
    }

    // --- スワイプとタップの制御 ---
    function handleStart(e) {
        if (!isGameRunning || !isBossBattle || isStunned) return;
        isDragging = false;
        const clientY = e.clientY || e.touches[0].clientY;
        dragStartY = clientY;
        trainStartY = playerY;
    }

    function handleMove(e) {
        if (!isGameRunning || !isBossBattle || isStunned) return;
        e.preventDefault(); // スクロール防止
        const clientY = e.clientY || e.touches[0].clientY;
        const deltaY = dragStartY - clientY; // 上にスワイプすると deltaY はプラス
        
        // 5px以上動いたらドラッグとみなす
        if (Math.abs(deltaY) > 5) {
            isDragging = true;
            playerY = trainStartY + deltaY;
            if (playerY < 50) playerY = 50;
            if (playerY > 550) playerY = 550;
            updatePlayerPosition();
        }
    }

    function handleEnd(e) {
        if (!isGameRunning || !isBossBattle || isStunned) return;
        if (!isDragging) {
            // ドラッグせずに離した＝タップ＝発射！
            shoot();
        }
        isDragging = false;
    }

    // --- タップでジャンプ（通常時） ---
    function handleNormalTap(e) {
        if (!isBossBattle && !isRespawning) {
            if (isGrounded) { playerVy = -JUMP_POWER; isGrounded = false; }
        }
    }

    function updatePlayerPosition() { playerTrain.style.bottom = `${playerY}px`; }

    function createCrowHTML() { return `<div class="crow-helmet"></div><div class="crow-head"></div><div class="crow-beak"></div><div class="crow-body"></div><div class="crow-wing"></div><div class="crow-eye"></div>`; }
    function spawnCrow() { const element = document.createElement('div'); element.classList.add('crow'); if (isGalaxyMode) element.classList.add('space-mode'); element.innerHTML = createCrowHTML(); const startX = gameScreen.offsetWidth + 50; const startY = Math.random() * 200 + 350; element.style.left = `${startX}px`; element.style.bottom = `${startY}px`; skyContainer.appendChild(element); const targetX = PLAYER_X + 20; const targetY = BRIDGE_HEIGHT + 20; const speed = 4 + Math.random() * 2; const dx = targetX - startX; const dy = targetY - startY; const distance = Math.sqrt(dx*dx + dy*dy); crows.push({ element, x: startX, y: startY, vx: (dx/distance)*speed, vy: (dy/distance)*speed, state: 'attack' }); }
    function createStolenScene(x, y) { const container = document.createElement('div'); container.classList.add('stolen-scene'); const crowDiv = document.createElement('div'); crowDiv.classList.add('crow'); if (isGalaxyMode) crowDiv.classList.add('space-mode'); crowDiv.innerHTML = createCrowHTML(); const trainDiv = document.createElement('div'); trainDiv.innerHTML = createTrainUnitHTML(true); trainDiv.style.position = 'absolute'; trainDiv.style.top = '20px'; trainDiv.style.left = '5px'; container.appendChild(crowDiv); container.appendChild(trainDiv); container.style.left = `${x}px`; container.style.bottom = `${y}px`; skyContainer.appendChild(container); stolenScenes.push({ element: container, x: x, y: y, vx: 3, vy: 5 }); }
    function createObstacle(left, width, type) { const element = document.createElement('div'); if (type === 'bridge') element.classList.add('bridge-part'); element.style.left = `${left}px`; element.style.width = `${width}px`; obstaclesContainer.appendChild(element); obstacles.push({ element, left, width, type }); if (type === 'bridge' && width > 150 && Math.random() < 0.35) createItem(left + width / 2); }
    function createItem(left) { const element = document.createElement('div'); element.classList.add('item'); element.style.left = `${left}px`; element.style.bottom = `${BRIDGE_HEIGHT + 30}px`; obstaclesContainer.appendChild(element); items.push({ element, left }); }
    function spawnNextObstacle() { const lastObstacle = obstacles[obstacles.length - 1]; const nextLeft = lastObstacle.left + lastObstacle.width; if (nextLeft < gameScreen.offsetWidth + SCROLL_SPEED * 20) { let type, width; if (lastObstacle.type === 'gap') { type = 'bridge'; width = Math.random() * 300 + 200; } else { type = Math.random() > 0.4 ? 'bridge' : 'gap'; width = type === 'bridge' ? Math.random() * 300 + 200 : Math.random() * 120 + 80; } createObstacle(nextLeft, width, type); } }
    function respawn() { if (isRespawning) return; isRespawning = true; carriageCount = 0; renderTrain(); setTimeout(() => { playerY = 600; playerVy = 0; updatePlayerPosition(); isRespawning = false; }, 1000); }
    function showGetEffect() { const effect = document.createElement('div'); effect.classList.add('get-effect'); effect.textContent = 'CONNECT!'; effect.style.left = `${PLAYER_X}px`; effect.style.top = `${gameScreen.offsetHeight - playerY - 80}px`; gameScreen.appendChild(effect); setTimeout(() => effect.remove(), 800); }
    function spawnSpaceObjects() { if (!isGalaxyMode) return; if (Math.random() < 0.003) { const rocket = document.createElement('div'); rocket.classList.add('rocket'); const directions = ['right', 'left', 'up', 'down', 'up-right', 'down-right', 'up-left', 'down-left']; const randomDir = directions[Math.floor(Math.random() * directions.length)]; rocket.classList.add(`rocket-${randomDir}`); rocket.innerHTML = '<div class="rocket-fire"></div><div class="rocket-body"></div><div class="rocket-fin top"></div><div class="rocket-fin bottom"></div><div class="rocket-window"></div>'; skyContainer.appendChild(rocket); setTimeout(() => rocket.remove(), 8000); } if (Math.random() < 0.008) { const shootingStar = document.createElement('div'); shootingStar.classList.add('shooting-star'); shootingStar.style.top = `${Math.random() * 200}px`; shootingStar.style.right = `${Math.random() * 200 - 200}px`; skyContainer.appendChild(shootingStar); setTimeout(() => shootingStar.remove(), 3000); } }
    function createExplosion(x, y) { const exp = document.createElement('div'); exp.classList.add('explosion'); exp.textContent = '💥'; exp.style.left = `${x}px`; exp.style.bottom = `${y}px`; skyContainer.appendChild(exp); setTimeout(() => exp.remove(), 500); }

    function applyStun() {
        isStunned = true;
        playerTrain.classList.add('stunned');
        setTimeout(() => {
            isStunned = false;
            playerTrain.classList.remove('stunned');
        }, 1000);
    }

    function gameLoop() {
        if (!isGameRunning) return;

        if (isBossBattle) {
            if (!isStunned) {
                bossY += bossVy; if (bossY > 500 || bossY < 100) bossVy *= -1; bossElement.style.bottom = `${bossY}px`;
            }

            // ボス攻撃（特攻カラス発射）
            if (Math.random() < 0.02) {
                const bCrow = document.createElement('div'); bCrow.classList.add('crow', 'space-mode'); // 宇宙カラスの見た目
                bCrow.innerHTML = createCrowHTML();
                bCrow.style.left = `${gameScreen.offsetWidth - 100}px`; bCrow.style.bottom = `${bossY + 50}px`;
                skyContainer.appendChild(bCrow);
                bossCrows.push({ element: bCrow, x: gameScreen.offsetWidth - 100, y: bossY + 50 });
            }

            if (Math.random() < 0.03) {
                const item = document.createElement('div'); item.classList.add('item');
                item.style.left = `${gameScreen.offsetWidth}px`; item.style.bottom = `${Math.random() * 500 + 50}px`;
                skyContainer.appendChild(item); items.push({ element: item, left: gameScreen.offsetWidth, y: parseFloat(item.style.bottom) });
            }

            playerMissiles.forEach((m, i) => {
                m.x += 10; m.element.style.left = `${m.x}px`;
                if (m.x > gameScreen.offsetWidth - 140 && Math.abs(m.y - bossY) < 80) {
                    m.element.remove(); playerMissiles.splice(i, 1); createExplosion(m.x, m.y);
                    bossHP--; bossHpBar.style.width = `${(bossHP/MAX_BOSS_HP)*100}%`;
                    if (bossHP <= 0) { alert("YOU WIN! 銀河の平和は守られた！"); initGame(); }
                } else if (m.x > gameScreen.offsetWidth) { m.element.remove(); playerMissiles.splice(i, 1); }
            });

            // ボス・カラスの当たり判定
            bossCrows.forEach((b, i) => {
                b.x -= 7; b.element.style.left = `${b.x}px`; b.element.style.bottom = `${b.y}px`;
                // プレイヤー当たり判定
                if (b.x < PLAYER_X + 50 && b.x > PLAYER_X && Math.abs(b.y - playerY) < 40 && !isStunned) {
                    b.element.remove(); bossCrows.splice(i, 1);
                    if (carriageCount > 0) {
                        carriageCount--; renderTrain();
                        createStolenScene(PLAYER_X, playerY); // 連れ去り演出
                    } else {
                        // ★1両しかない時はスタン！★
                        applyStun();
                    }
                } else if (b.x < -50) { b.element.remove(); bossCrows.splice(i, 1); }
            });

            items.forEach((item, index) => {
                item.left -= 5; item.element.style.left = `${item.left}px`;
                const itemY = parseFloat(item.element.style.bottom); 
                if (item.left < PLAYER_X + 54 && item.left + 30 > PLAYER_X) {
                    if (Math.abs(playerY - itemY) < 50 && !isStunned) {
                        item.element.remove(); items.splice(index, 1); carriageCount++; renderTrain(); showGetEffect();
                    }
                }
                if (item.left < -50) { item.element.remove(); items.splice(index, 1); }
            });

        } else {
            // 通常モード
            if (!isRespawning) { playerVy += currentGravity; playerY -= playerVy; }
            if (carriageCount >= 1 && crows.length === 0 && !isRespawning && Math.random() < 0.005) spawnCrow();
            spawnSpaceObjects();
            crows.forEach((crow, index) => { crow.x += crow.vx; crow.y += crow.vy; crow.element.style.left = `${crow.x}px`; crow.element.style.bottom = `${crow.y}px`; if (crow.state === 'attack') { const dx = (crow.x + 25) - (PLAYER_X + 27); const dy = (crow.y + 15) - (playerY + 20); if (Math.sqrt(dx*dx + dy*dy) < 40 && !isRespawning) { carriageCount--; renderTrain(); createStolenScene(PLAYER_X, playerY); crow.element.remove(); crows.splice(index, 1); return; } } if (crow.x < -100 || crow.y > 800 || crow.y < -50) { crow.element.remove(); crows.splice(index, 1); } });
            stolenScenes.forEach((scene, index) => { scene.x += scene.vx; scene.y += scene.vy; scene.element.style.left = `${scene.x}px`; scene.element.style.bottom = `${scene.y}px`; if (scene.y > 800) { scene.element.remove(); stolenScenes.splice(index, 1); } });
            let currentGround = null; obstacles.forEach((obs, index) => { obs.left -= SCROLL_SPEED; obs.element.style.left = `${obs.left}px`; if (PLAYER_X + 44 > obs.left && PLAYER_X + 10 < obs.left + obs.width) { if (obs.type === 'bridge') currentGround = obs; } if (obs.left + obs.width < -100) { obs.element.remove(); obstacles.splice(index, 1); } });
            items.forEach((item, index) => { item.left -= SCROLL_SPEED; item.element.style.left = `${item.left}px`; if (item.left < PLAYER_X + 54 && item.left + 30 > PLAYER_X) { if (playerY < BRIDGE_HEIGHT + 70 && playerY + 40 > BRIDGE_HEIGHT + 30) { item.element.remove(); items.splice(index, 1); carriageCount++; renderTrain(); showGetEffect(); } } if (item.left < -50) { item.element.remove(); items.splice(index, 1); } });
            spawnNextObstacle();
            if (!isRespawning) { if (currentGround && playerY <= BRIDGE_HEIGHT && playerY > BRIDGE_HEIGHT - 30 && playerVy >= 0) { if (!isGrounded) { playerTrain.classList.remove('poyo'); playerTrain.classList.add('landing'); setTimeout(() => { playerTrain.classList.remove('landing'); playerTrain.classList.add('poyo'); }, 400); } playerY = BRIDGE_HEIGHT; playerVy = 0; isGrounded = true; } else if (!currentGround && playerY <= BRIDGE_HEIGHT && isGrounded) { isGrounded = false; } if (playerY < -100) respawn(); }
        }
        
        updatePlayerPosition(); animationId = requestAnimationFrame(gameLoop);
    }

    // イベントリスナーの切り替え（PC/スマホ両対応）
    gameScreen.addEventListener('mousedown', (e) => { 
        if(isBossBattle) handleStart(e); else handleNormalTap(e); 
    });
    gameScreen.addEventListener('mousemove', (e) => { 
        if(isBossBattle) handleMove(e); 
    });
    gameScreen.addEventListener('mouseup', (e) => { 
        if(isBossBattle) handleEnd(e); 
    });

    gameScreen.addEventListener('touchstart', (e) => { 
        if(isBossBattle) handleStart(e); else handleNormalTap(e); 
    }, { passive: false });
    gameScreen.addEventListener('touchmove', (e) => { 
        if(isBossBattle) handleMove(e); 
    }, { passive: false });
    gameScreen.addEventListener('touchend', (e) => { 
        if(isBossBattle) handleEnd(e); 
    });

    document.addEventListener('keydown', (e) => { if (e.code === 'Space' && !isBossBattle) { e.preventDefault(); handleNormalTap(e); } }); 
    
    initGame();
</script>
</body>
</html>
"""

# HTMLを描画
components.html(html_code, height=650)

st.write("スワイプで回避、タップで発射！新感覚のボス戦を楽しんでね！🍄💥")
