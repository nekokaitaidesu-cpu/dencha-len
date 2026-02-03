import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="ぽよぽよ電車ジャンプ！", layout="wide")

# タイトル
st.title("🍄 カラスも宇宙仕様！シャボン玉ヘルメットだっち 🦅🫧🌌")
st.write("カラスの宇宙ヘルメットを、顔だけを包むシャボン玉みたいにしたよ！銀河の旅を楽しんでね！")

# HTML/CSS/JSコード
html_code = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style>
    /* --- CSS (スタイル設定) --- */
    :root {
        /* 昼モードの色 */
        --sky-top-day: #87CEEB; --sky-bottom-day: #E0F7FA;
        --water-top-day: #40a4df; --water-bottom-day: #0077be;
        --bridge-base-day: #A0522D;
        --bridge-top-day: #5D4037;
        
        /* 夜（銀河）モードの色 */
        --sky-top-night: #0a0a2a; --sky-bottom-night: #2a0a5a;
        --water-top-night: #050520; --water-bottom-night: #1a0a3a;
        --bridge-base-night: #4a5b6c;
        --bridge-top-night: #2a3b4c;

        /* 現在適用される色 */
        --current-sky-top: var(--sky-top-day);
        --current-sky-bottom: var(--sky-bottom-day);
        --current-water-top: var(--water-top-day);
        --current-water-bottom: var(--water-bottom-day);
        --current-bridge-base: var(--bridge-base-day);
        --current-bridge-top: var(--bridge-top-day);

        --bridge-height: 280px;
    }

    #game-screen {
        width: 100%; height: 600px;
        background: linear-gradient(to bottom, var(--current-sky-top) 0%, var(--current-sky-bottom) 70%, var(--current-water-top) 70%, var(--current-water-bottom) 100%);
        position: relative; overflow: hidden; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        user-select: none; cursor: pointer; transition: background 1s ease;
    }

    /* 雲（昼のみ） */
    .cloud {
        position: absolute; background: rgba(255, 255, 255, 0.9); border-radius: 50px; z-index: 1;
        transition: opacity 1s ease; opacity: 1;
    }
    .cloud::after, .cloud::before { content: ''; position: absolute; background: inherit; border-radius: 50%; }
    .cloud.c1 { width: 120px; height: 40px; top: 60px; left: 10%; }
    .cloud.c1::after { width: 50px; height: 50px; top: -20px; left: 15px; }
    .cloud.c1::before { width: 40px; height: 40px; top: -15px; left: 50px; }
    .cloud.c2 { width: 80px; height: 30px; top: 150px; left: 60%; }
    .cloud.c2::after { width: 35px; height: 35px; top: -15px; left: 10px; }

    /* 星と月（夜のみ） */
    .star { position: absolute; background: #FFF; border-radius: 50%; z-index: 0; opacity: 0; display: none; box-shadow: 0 0 4px #FFF; }
    .star.drawn { width: 10px; height: 10px; background: #FFD700; clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%); animation: twinkle 2s infinite alternate; }
    .moon { position: absolute; top: 40px; right: 60px; width: 60px; height: 60px; background: transparent; border-radius: 50%; box-shadow: -15px 15px 0 0 #FFD700; opacity: 0; display: none; z-index: 0; transform: rotate(-10deg); animation: floatMoon 3s ease-in-out infinite alternate; }
    @keyframes floatMoon { from { transform: rotate(-10deg) translateY(0); } to { transform: rotate(-10deg) translateY(-10px); } }
    @keyframes twinkle { from { transform: scale(0.8); opacity: 0.7; } to { transform: scale(1.1); opacity: 1; } }

    #game-screen.galaxy-mode .cloud { opacity: 0; display: none; }
    #game-screen.galaxy-mode .star, #game-screen.galaxy-mode .moon { display: block; opacity: 1; }
    #game-screen.galaxy-mode .train-body { box-shadow: 0 0 15px #00BFFF, inset 0 0 5px #E0FFFF; border-color: #00BFFF; }

    #obstacles-container { position: absolute; bottom: 0; left: 0; width: 100%; height: var(--bridge-height); z-index: 5; }
    .bridge-part {
        position: absolute; bottom: 0; height: 100%;
        background-color: var(--current-bridge-base);
        background-image: radial-gradient(circle at bottom center, transparent 60%, var(--current-bridge-base) 61%), linear-gradient(rgba(0,0,0,0.1) 2px, transparent 2px);
        background-size: 200px 280px, 100% 20px; background-repeat: repeat-x, repeat; background-position: bottom left; box-sizing: border-box; transition: background-color 1s ease;
    }
    .bridge-part::after { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 15px; background: var(--current-bridge-top); transition: background 1s ease; z-index: 2; }
    
    /* 虹色のレール（銀河モード時のみ） */
    .bridge-part::before {
        content: ''; position: absolute; top: -5px; left: 0; width: 100%; height: 15px;
        background: repeating-linear-gradient(45deg, #ff0000, #ff0000 10px, #ff7f00 10px, #ff7f00 20px, #ffff00 20px, #ffff00 30px, #00ff00 30px, #00ff00 40px, #0000ff 40px, #0000ff 50px, #4b0082 50px, #4b0082 60px, #9400d3 60px, #9400d3 70px);
        z-index: 3; opacity: 0; transition: opacity 1s ease; background-size: 200% 100%; animation: rainbowMove 2s linear infinite;
    }
    @keyframes rainbowMove { 0% { background-position: 0 0; } 100% { background-position: 100px 0; } }
    #game-screen.galaxy-mode .bridge-part::before { opacity: 1; }
    #game-screen.galaxy-mode .bridge-part::after { opacity: 0; }

    /* アイテム */
    .item {
        position: absolute; bottom: 50px; width: 30px; height: 20px; background: #FFD700; border: 2px solid #FFA000; border-radius: 4px; z-index: 6;
        display: flex; justify-content: center; align-items: center; box-shadow: 0 0 10px rgba(255, 215, 0, 0.6); animation: floatItem 1s ease-in-out infinite alternate;
    }
    .item::after { content: '+1'; font-size: 12px; font-weight: bold; color: #8B4500; }
    @keyframes floatItem { from { transform: translateY(0); } to { transform: translateY(-10px); } }

    /* カラス */
    .crow { position: absolute; width: 50px; height: 30px; z-index: 20; }
    .crow-body { position: absolute; top: 5px; left: 10px; width: 35px; height: 20px; background: #333; border-radius: 50%; }
    .crow-head { position: absolute; top: 0; left: 0; width: 18px; height: 18px; background: #333; border-radius: 50%; }
    .crow-beak { position: absolute; top: 5px; left: -8px; width: 0; height: 0; border-top: 5px solid transparent; border-bottom: 5px solid transparent; border-right: 10px solid #FFD700; }
    .crow-eye { position: absolute; top: 5px; left: 5px; width: 4px; height: 4px; background: white; border-radius: 50%; }
    .crow-wing { position: absolute; top: -5px; left: 15px; width: 25px; height: 15px; background: #222; border-radius: 50% 50% 0 0; transform-origin: bottom center; animation: flap 0.2s infinite alternate; }
    @keyframes flap { from { transform: rotate(0deg) scaleY(1); } to { transform: rotate(-20deg) scaleY(0.5); } }

    /* ★カラス用宇宙ヘルメット（修正：顔だけシャボン玉）★ */
    .crow-helmet {
        position: absolute;
        top: -7px; left: -12px; /* 顔とくちばしを覆う位置に調整 */
        width: 34px; height: 34px; /* 顔より少し大きめ */
        border-radius: 50%;
        z-index: 25; display: none;
        /* シャボン玉のような透明感と光沢 */
        background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.9), rgba(200,240,255,0.3) 60%, transparent 90%);
        border: 1px solid rgba(255, 255, 255, 0.4);
        box-shadow: inset -3px -3px 8px rgba(200,240,255,0.2), 0 0 5px rgba(255,255,255,0.3);
    }
    .crow.space-mode .crow-helmet { display: block; }

    .stolen-scene { position: absolute; z-index: 30; pointer-events: none; }
    .stolen-scene .train-unit { transform: rotate(10deg); }

    /* プレイヤー */
    #player-train {
        position: absolute; left: 100px; height: 40px; z-index: 10; transform-origin: bottom center;
        display: flex; flex-direction: row-reverse; align-items: flex-end; gap: 2px; transition: transform 0.1s;
    }
    #player-train.poyo { animation: poyoPoyo 0.6s steps(3) infinite alternate; }
    .train-unit { position: relative; width: 54px; height: 40px; flex-shrink: 0; }
    .train-body {
        width: 100%; height: 28px; background-color: #4DB6AC; border-radius: 6px; border: 2px solid #004D40;
        position: absolute; bottom: 4.5px; left: 0; display: flex; justify-content: space-evenly; align-items: center;
        box-shadow: 2px 2px 0px rgba(0,0,0,0.2); box-sizing: border-box; z-index: 2; transition: box-shadow 1s ease, border-color 1s ease;
    }
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

    #carriage-count-display {
        position: absolute; top: 20px; left: 20px; font-size: 20px; font-weight: bold; color: #333; z-index: 20;
        background: rgba(255,255,255,0.8); padding: 5px 15px; border-radius: 10px;
    }
</style>
</head>
<body>
<div id="game-screen">
    <div class="cloud c1"></div><div class="cloud c2"></div>
    <div id="stars-container"></div><div class="moon"></div>
    <div id="carriage-count-display">車両: 1</div>
    <div id="obstacles-container"></div><div id="sky-container"></div><div id="player-train" class="poyo"></div>
</div>
<script>
    const gameScreen = document.getElementById('game-screen');
    const playerTrain = document.getElementById('player-train');
    const obstaclesContainer = document.getElementById('obstacles-container');
    const skyContainer = document.getElementById('sky-container');
    const starsContainer = document.getElementById('stars-container');
    const carriageCountDisplay = document.getElementById('carriage-count-display');
    const root = document.documentElement;
    const BRIDGE_HEIGHT = 280; const SCROLL_SPEED = 5; const PLAYER_X = 100;
    const GRAVITY_DAY = 0.6; const GRAVITY_NIGHT = 0.35; let currentGravity = GRAVITY_DAY; const JUMP_POWER = 12;
    let isGameRunning = false; let animationId; let playerY = BRIDGE_HEIGHT; let playerVy = 0; let isGrounded = true; let isRespawning = false; let isGalaxyMode = false;
    let obstacles = []; let items = []; let crows = []; let stolenScenes = []; let carriageCount = 0;

    function createStars() {
        for (let i = 0; i < 20; i++) {
            const star = document.createElement('div'); star.classList.add('star', 'drawn');
            star.style.left = `${Math.random() * 95}%`; star.style.top = `${Math.random() * 60}%`;
            const scale = 0.8 + Math.random() * 0.5; star.style.transform = `scale(${scale})`;
            star.style.animationDelay = `${Math.random() * 3}s`; starsContainer.appendChild(star);
        }
        for (let i = 0; i < 50; i++) {
            const star = document.createElement('div'); star.classList.add('star');
            star.style.width = '3px'; star.style.height = '3px'; star.style.left = `${Math.random() * 100}%`; star.style.top = `${Math.random() * 80}%`;
            star.style.animation = `twinkle ${1 + Math.random()}s infinite alternate`; starsContainer.appendChild(star);
        }
    }
    createStars();

    function toggleGalaxyMode(enable) {
        if (isGalaxyMode === enable) return;
        isGalaxyMode = enable;
        if (enable) {
            gameScreen.classList.add('galaxy-mode'); currentGravity = GRAVITY_NIGHT;
            root.style.setProperty('--current-sky-top', 'var(--sky-top-night)'); root.style.setProperty('--current-sky-bottom', 'var(--sky-bottom-night)');
            root.style.setProperty('--current-water-top', 'var(--water-top-night)'); root.style.setProperty('--current-water-bottom', 'var(--water-bottom-night)');
            root.style.setProperty('--current-bridge-base', 'var(--bridge-base-night)');
            crows.forEach(crow => crow.element.classList.add('space-mode'));
        } else {
            gameScreen.classList.remove('galaxy-mode'); currentGravity = GRAVITY_DAY;
            root.style.setProperty('--current-sky-top', 'var(--sky-top-day)'); root.style.setProperty('--current-sky-bottom', 'var(--sky-bottom-day)');
            root.style.setProperty('--current-water-top', 'var(--water-top-day)'); root.style.setProperty('--current-water-bottom', 'var(--water-bottom-day)');
            root.style.setProperty('--current-bridge-base', 'var(--bridge-base-day)');
            crows.forEach(crow => crow.element.classList.remove('space-mode'));
        }
    }

    function createTrainUnitHTML(isHead) {
        return `<div class="train-unit ${isHead ? 'head' : 'wagon'}"><div class="smoke"></div><div class="wheels-container"><div class="wheel"></div><div class="wheel"></div></div><div class="train-body"><div class="window"></div><div class="window"></div><div class="window"></div></div></div>`;
    }
    function renderTrain() {
        playerTrain.innerHTML = ''; playerTrain.insertAdjacentHTML('beforeend', createTrainUnitHTML(true));
        for (let i = 0; i < carriageCount; i++) { playerTrain.insertAdjacentHTML('beforeend', createTrainUnitHTML(false)); }
        carriageCountDisplay.textContent = `車両: ${carriageCount + 1}`;
        if (carriageCount + 1 >= 4) { toggleGalaxyMode(true); } else { toggleGalaxyMode(false); }
    }

    function initGame() {
        isGameRunning = true; isRespawning = false; playerTrain.classList.add('poyo');
        playerY = BRIDGE_HEIGHT; playerVy = 0; isGrounded = true; updatePlayerPosition();
        obstacles.forEach(obs => obs.element.remove()); obstacles = []; items.forEach(item => item.element.remove()); items = [];
        crows.forEach(crow => crow.element.remove()); crows = []; stolenScenes.forEach(s => s.element.remove()); stolenScenes = [];
        carriageCount = 0; renderTrain();
        createObstacle(0, 2000, 'bridge');
        if (animationId) cancelAnimationFrame(animationId); gameLoop();
    }

    function createCrowHTML() { return `<div class="crow-helmet"></div><div class="crow-head"></div><div class="crow-beak"></div><div class="crow-body"></div><div class="crow-wing"></div><div class="crow-eye"></div>`; }
    function spawnCrow() {
        const element = document.createElement('div'); element.classList.add('crow');
        if (isGalaxyMode) element.classList.add('space-mode');
        element.innerHTML = createCrowHTML();
        const startX = gameScreen.offsetWidth + 50; const startY = Math.random() * 200 + 350;
        element.style.left = `${startX}px`; element.style.bottom = `${startY}px`; skyContainer.appendChild(element);
        const targetX = PLAYER_X + 20; const targetY = BRIDGE_HEIGHT + 20;
        const speed = 4 + Math.random() * 2; const dx = targetX - startX; const dy = targetY - startY; const distance = Math.sqrt(dx*dx + dy*dy);
        crows.push({ element, x: startX, y: startY, vx: (dx/distance)*speed, vy: (dy/distance)*speed, state: 'attack' });
    }
    function createStolenScene(x, y) {
        const container = document.createElement('div'); container.classList.add('stolen-scene');
        const crowDiv = document.createElement('div'); crowDiv.classList.add('crow');
        if (isGalaxyMode) crowDiv.classList.add('space-mode');
        crowDiv.innerHTML = createCrowHTML();
        const trainDiv = document.createElement('div'); trainDiv.innerHTML = createTrainUnitHTML(true);
        trainDiv.style.position = 'absolute'; trainDiv.style.top = '20px'; trainDiv.style.left = '5px';
        container.appendChild(crowDiv); container.appendChild(trainDiv);
        container.style.left = `${x}px`; container.style.bottom = `${y}px`; skyContainer.appendChild(container);
        stolenScenes.push({ element: container, x: x, y: y, vx: 3, vy: 5 });
    }

    function createObstacle(left, width, type) {
        const element = document.createElement('div'); if (type === 'bridge') element.classList.add('bridge-part');
        element.style.left = `${left}px`; element.style.width = `${width}px`; obstaclesContainer.appendChild(element); obstacles.push({ element, left, width, type });
        if (type === 'bridge' && width > 150 && Math.random() < 0.35) createItem(left + width / 2);
    }
    function createItem(left) {
        const element = document.createElement('div'); element.classList.add('item');
        element.style.left = `${left}px`; element.style.bottom = `${BRIDGE_HEIGHT + 30}px`; obstaclesContainer.appendChild(element); items.push({ element, left });
    }
    function spawnNextObstacle() {
        const lastObstacle = obstacles[obstacles.length - 1]; const nextLeft = lastObstacle.left + lastObstacle.width;
        if (nextLeft < gameScreen.offsetWidth + SCROLL_SPEED * 20) {
            let type, width;
            if (lastObstacle.type === 'gap') { type = 'bridge'; width = Math.random() * 300 + 200; }
            else { type = Math.random() > 0.4 ? 'bridge' : 'gap'; width = type === 'bridge' ? Math.random() * 300 + 200 : Math.random() * 120 + 80; }
            createObstacle(nextLeft, width, type);
        }
    }

    function jump() { if (!isGameRunning || isRespawning) return; if (isGrounded) { playerVy = -JUMP_POWER; isGrounded = false; } }
    function updatePlayerPosition() { playerTrain.style.bottom = `${playerY}px`; }
    function respawn() { if (isRespawning) return; isRespawning = true; carriageCount = 0; renderTrain(); setTimeout(() => { playerY = 600; playerVy = 0; updatePlayerPosition(); isRespawning = false; }, 1000); }
    function showGetEffect() { const effect = document.createElement('div'); effect.classList.add('get-effect'); effect.textContent = 'CONNECT!'; effect.style.left = `${PLAYER_X}px`; effect.style.top = `${gameScreen.offsetHeight - playerY - 80}px`; gameScreen.appendChild(effect); setTimeout(() => effect.remove(), 800); }

    function gameLoop() {
        if (!isGameRunning) return;
        if (!isRespawning) { playerVy += currentGravity; playerY -= playerVy; }
        if (carriageCount >= 1 && crows.length === 0 && !isRespawning && Math.random() < 0.005) spawnCrow();
        crows.forEach((crow, index) => {
            crow.x += crow.vx; crow.y += crow.vy; crow.element.style.left = `${crow.x}px`; crow.element.style.bottom = `${crow.y}px`;
            if (crow.state === 'attack') {
                const dx = (crow.x + 25) - (PLAYER_X + 27); const dy = (crow.y + 15) - (playerY + 20);
                if (Math.sqrt(dx*dx + dy*dy) < 40 && !isRespawning) { carriageCount--; renderTrain(); createStolenScene(PLAYER_X, playerY); crow.element.remove(); crows.splice(index, 1); return; }
            }
            if (crow.x < -100 || crow.y > 800 || crow.y < -50) { crow.element.remove(); crows.splice(index, 1); }
        });
        stolenScenes.forEach((scene, index) => { scene.x += scene.vx; scene.y += scene.vy; scene.element.style.left = `${scene.x}px`; scene.element.style.bottom = `${scene.y}px`; if (scene.y > 800) { scene.element.remove(); stolenScenes.splice(index, 1); } });
        let currentGround = null;
        obstacles.forEach((obs, index) => {
            obs.left -= SCROLL_SPEED; obs.element.style.left = `${obs.left}px`;
            if (PLAYER_X + 44 > obs.left && PLAYER_X + 10 < obs.left + obs.width) { if (obs.type === 'bridge') currentGround = obs; }
            if (obs.left + obs.width < -100) { obs.element.remove(); obstacles.splice(index, 1); }
        });
        items.forEach((item, index) => {
            item.left -= SCROLL_SPEED; item.element.style.left = `${item.left}px`;
            if (item.left < PLAYER_X + 54 && item.left + 30 > PLAYER_X) {
                if (playerY < BRIDGE_HEIGHT + 70 && playerY + 40 > BRIDGE_HEIGHT + 30) { item.element.remove(); items.splice(index, 1); carriageCount++; renderTrain(); showGetEffect(); }
            }
            if (item.left < -50) { item.element.remove(); items.splice(index, 1); }
        });
        spawnNextObstacle();
        if (!isRespawning) {
            if (currentGround && playerY <= BRIDGE_HEIGHT && playerY > BRIDGE_HEIGHT - 30 && playerVy >= 0) {
                if (!isGrounded) { playerTrain.classList.remove('poyo'); playerTrain.classList.add('landing'); setTimeout(() => { playerTrain.classList.remove('landing'); playerTrain.classList.add('poyo'); }, 400); }
                playerY = BRIDGE_HEIGHT; playerVy = 0; isGrounded = true;
            } else if (!currentGround && playerY <= BRIDGE_HEIGHT && isGrounded) { isGrounded = false; }
            if (playerY < -100) respawn();
        }
        updatePlayerPosition(); animationId = requestAnimationFrame(gameLoop);
    }
    gameScreen.addEventListener('mousedown', jump); document.addEventListener('keydown', (e) => { if (e.code === 'Space') { e.preventDefault(); jump(); } }); gameScreen.addEventListener('touchstart', (e) => { e.preventDefault(); jump(); }, { passive: false }); initGame();
</script>
</body>
</html>
"""

# HTMLを描画
components.html(html_code, height=650)

st.write("カラスの顔だけシャボン玉、いい感じでしょ？🫧 これで宇宙でも安心だっち！🦅🍄")
