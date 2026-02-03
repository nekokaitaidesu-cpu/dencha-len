import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="ぽよぽよ電車ジャンプ！", layout="wide")

# タイトル
st.title("🍄 カラス襲来！連結＆略奪サバイバル 🦅🚃")
st.write("連結して長くなると、カラスが先頭車両を盗みに来るよ！ジャンプでかわせ！")

# HTML/CSS/JSコード
html_code = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style>
    /* --- CSS (スタイル設定) --- */
    :root {
        --sky-color-top: #87CEEB;
        --sky-color-bottom: #E0F7FA;
        --water-color-top: #40a4df;
        --water-color-bottom: #0077be;
        --bridge-base-color: #A0522D;
        --bridge-line-color: rgba(0,0,0,0.2);
        --bridge-height: 280px;
    }

    #game-screen {
        width: 100%;
        height: 600px;
        background: linear-gradient(to bottom, var(--sky-color-top) 0%, var(--sky-color-bottom) 70%, var(--water-color-top) 70%, var(--water-color-bottom) 100%);
        position: relative;
        overflow: hidden;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        user-select: none;
        cursor: pointer;
    }

    .cloud {
        position: absolute;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 50px;
        z-index: 1;
    }
    .cloud::after, .cloud::before { content: ''; position: absolute; background: inherit; border-radius: 50%; }
    .cloud.c1 { width: 120px; height: 40px; top: 60px; left: 10%; }
    .cloud.c1::after { width: 50px; height: 50px; top: -20px; left: 15px; }
    .cloud.c1::before { width: 40px; height: 40px; top: -15px; left: 50px; }
    .cloud.c2 { width: 80px; height: 30px; top: 150px; left: 60%; }
    .cloud.c2::after { width: 35px; height: 35px; top: -15px; left: 10px; }

    #obstacles-container {
        position: absolute; bottom: 0; left: 0; width: 100%; height: var(--bridge-height); z-index: 5;
    }
    .bridge-part {
        position: absolute; bottom: 0; height: 100%;
        background-color: var(--bridge-base-color);
        background-image: linear-gradient(to bottom, var(--bridge-line-color) 2px, transparent 2px), linear-gradient(90deg, var(--bridge-line-color) 2px, transparent 2px);
        background-size: 100% 20px, 40px 100%; box-sizing: border-box; border-top: 10px solid #5D4037;
    }

    /* アイテム（増結チケット） */
    .item {
        position: absolute;
        bottom: 50px;
        width: 30px;
        height: 20px;
        background: #FFD700;
        border: 2px solid #FFA000;
        border-radius: 4px;
        z-index: 6;
        display: flex; justify-content: center; align-items: center;
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.6);
        animation: floatItem 1s ease-in-out infinite alternate;
    }
    .item::after { content: '+1'; font-size: 12px; font-weight: bold; color: #8B4500; }
    @keyframes floatItem { from { transform: translateY(0); } to { transform: translateY(-10px); } }

    /* --- カラス (The Crow) --- */
    .crow {
        position: absolute;
        width: 50px; height: 30px;
        z-index: 20;
    }
    .crow-body {
        position: absolute; top: 5px; left: 10px;
        width: 35px; height: 20px;
        background: #333; /* カラス色 */
        border-radius: 50%;
    }
    .crow-head {
        position: absolute; top: 0; left: 0;
        width: 18px; height: 18px;
        background: #333;
        border-radius: 50%;
    }
    .crow-beak {
        position: absolute; top: 5px; left: -8px;
        width: 0; height: 0;
        border-top: 5px solid transparent;
        border-bottom: 5px solid transparent;
        border-right: 10px solid #FFD700; /* 黄色のくちばし */
    }
    .crow-eye {
        position: absolute; top: 5px; left: 5px;
        width: 4px; height: 4px; background: white; border-radius: 50%;
    }
    .crow-wing {
        position: absolute; top: -5px; left: 15px;
        width: 25px; height: 15px;
        background: #222;
        border-radius: 50% 50% 0 0;
        transform-origin: bottom center;
        animation: flap 0.2s infinite alternate;
    }
    @keyframes flap { from { transform: rotate(0deg) scaleY(1); } to { transform: rotate(-20deg) scaleY(0.5); } }

    /* 連れ去り演出用のコンテナ */
    .stolen-scene {
        position: absolute;
        z-index: 30;
        pointer-events: none; /* クリック透過 */
    }
    .stolen-scene .train-unit {
        transform: rotate(10deg); /* ぶら下がってる感 */
    }

    /* プレイヤーコンテナ */
    #player-train {
        position: absolute;
        left: 100px;
        height: 40px;
        z-index: 10;
        transform-origin: bottom center;
        display: flex;
        flex-direction: row-reverse;
        align-items: flex-end;
        gap: 2px;
        transition: transform 0.1s;
    }
    #player-train.poyo { animation: poyoPoyo 0.6s steps(3) infinite alternate; }

    /* 車両ユニット共通 */
    .train-unit { position: relative; width: 54px; height: 40px; flex-shrink: 0; }
    .train-body {
        width: 100%; height: 28px; background-color: #4DB6AC; border-radius: 6px; border: 2px solid #004D40;
        position: absolute; bottom: 4.5px; left: 0; display: flex; justify-content: space-evenly; align-items: center;
        box-shadow: 2px 2px 0px rgba(0,0,0,0.2); box-sizing: border-box; z-index: 2;
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

    .get-effect {
        position: absolute; color: #FFD700; font-weight: bold; font-size: 20px;
        animation: floatUp 0.8s ease-out forwards; pointer-events: none; z-index: 20; text-shadow: 1px 1px 0 #000;
    }
    @keyframes floatUp { 0% { opacity: 1; transform: translateY(0); } 100% { opacity: 0; transform: translateY(-50px); } }

</style>
</head>
<body>

<div id="game-screen">
    <div class="cloud c1"></div>
    <div class="cloud c2"></div>
    <div id="obstacles-container"></div>
    <div id="sky-container"></div>
    
    <div id="player-train" class="poyo">
        </div>
</div>

<script>
    const gameScreen = document.getElementById('game-screen');
    const playerTrain = document.getElementById('player-train');
    const obstaclesContainer = document.getElementById('obstacles-container');
    const skyContainer = document.getElementById('sky-container');

    const BRIDGE_HEIGHT = 280;
    const GRAVITY = 0.6;
    const JUMP_POWER = 12;
    const SCROLL_SPEED = 5;
    const PLAYER_X = 100;
    
    let isGameRunning = false;
    let animationId;
    let playerY = BRIDGE_HEIGHT;
    let playerVy = 0;
    let isGrounded = true;
    let isRespawning = false;

    let obstacles = [];
    let items = [];
    let crows = []; // カラス管理用
    let stolenScenes = []; // 連れ去り演出管理用
    let carriageCount = 0;

    function createTrainUnitHTML(isHead) {
        return `
            <div class="train-unit ${isHead ? 'head' : 'wagon'}">
                <div class="smoke"></div>
                <div class="wheels-container"><div class="wheel"></div><div class="wheel"></div></div>
                <div class="train-body"><div class="window"></div><div class="window"></div><div class="window"></div></div>
            </div>
        `;
    }

    function renderTrain() {
        playerTrain.innerHTML = '';
        playerTrain.insertAdjacentHTML('beforeend', createTrainUnitHTML(true));
        for (let i = 0; i < carriageCount; i++) {
            playerTrain.insertAdjacentHTML('beforeend', createTrainUnitHTML(false));
        }
    }

    function initGame() {
        isGameRunning = true;
        isRespawning = false;
        playerTrain.classList.add('poyo');

        playerY = BRIDGE_HEIGHT;
        playerVy = 0;
        isGrounded = true;
        updatePlayerPosition();
        
        obstacles.forEach(obs => obs.element.remove());
        obstacles = [];
        items.forEach(item => item.element.remove());
        items = [];
        crows.forEach(crow => crow.element.remove());
        crows = [];
        stolenScenes.forEach(s => s.element.remove());
        stolenScenes = [];
        
        carriageCount = 0;
        renderTrain();

        createObstacle(0, gameScreen.offsetWidth + 200, 'bridge');
        
        if (animationId) cancelAnimationFrame(animationId);
        gameLoop();
    }

    // --- カラス関連の関数 ---

    // カラスのHTML生成
    function createCrowHTML() {
        return `
            <div class="crow-head"></div>
            <div class="crow-beak"></div>
            <div class="crow-body"></div>
            <div class="crow-wing"></div>
            <div class="crow-eye"></div>
        `;
    }

    function spawnCrow() {
        const element = document.createElement('div');
        element.classList.add('crow');
        element.innerHTML = createCrowHTML();
        
        // 画面右上のランダムな高さから出現
        const startX = gameScreen.offsetWidth + 50;
        const startY = Math.random() * 200 + 350; // 下(bottom基準)から350~550pxの高さ
        
        element.style.left = `${startX}px`;
        element.style.bottom = `${startY}px`;
        
        skyContainer.appendChild(element);
        
        // 狙う位置：プレイヤーの先頭車両の「地面」位置
        // 少し手前(PLAYER_X + 20)を狙うと当たりやすい
        const targetX = PLAYER_X + 20; 
        const targetY = BRIDGE_HEIGHT + 20; // 車両の中心あたり
        
        // 速度計算
        const speed = 4 + Math.random() * 2; // 少しランダム
        const dx = targetX - startX;
        const dy = targetY - startY;
        const distance = Math.sqrt(dx*dx + dy*dy);
        const vx = (dx / distance) * speed;
        const vy = (dy / distance) * speed;

        crows.push({ element, x: startX, y: startY, vx, vy, state: 'attack' });
    }

    function createStolenScene(x, y) {
        // 連れ去り演出用の要素を作成
        const container = document.createElement('div');
        container.classList.add('stolen-scene');
        
        // カラスを追加
        const crowDiv = document.createElement('div');
        crowDiv.classList.add('crow');
        crowDiv.innerHTML = createCrowHTML();
        crowDiv.style.position = 'absolute';
        crowDiv.style.top = '0';
        crowDiv.style.left = '0';
        
        // 電車を追加（カラスの下にぶら下げる）
        const trainDiv = document.createElement('div');
        trainDiv.innerHTML = createTrainUnitHTML(true); // 先頭車両の見た目
        trainDiv.style.position = 'absolute';
        trainDiv.style.top = '20px'; // カラスの足元
        trainDiv.style.left = '5px';
        
        container.appendChild(crowDiv);
        container.appendChild(trainDiv);
        
        container.style.left = `${x}px`;
        container.style.bottom = `${y}px`;
        
        skyContainer.appendChild(container);
        
        // 右上へ飛び去る速度
        stolenScenes.push({ element: container, x: x, y: y, vx: 3, vy: 5 });
    }

    // ----------------------

    function createObstacle(left, width, type) {
        const element = document.createElement('div');
        if (type === 'bridge') element.classList.add('bridge-part');
        element.style.left = `${left}px`;
        element.style.width = `${width}px`;
        obstaclesContainer.appendChild(element);
        obstacles.push({ element, left, width, type });

        if (type === 'bridge' && width > 150) {
            if (Math.random() < 0.3) createItem(left + width / 2);
        }
    }

    function createItem(left) {
        const element = document.createElement('div');
        element.classList.add('item');
        element.style.left = `${left}px`;
        element.style.bottom = `${BRIDGE_HEIGHT + 30}px`; 
        obstaclesContainer.appendChild(element);
        items.push({ element, left });
    }

    function spawnNextObstacle() {
        const lastObstacle = obstacles[obstacles.length - 1];
        const nextLeft = lastObstacle.left + lastObstacle.width;
        
        if (nextLeft < gameScreen.offsetWidth + SCROLL_SPEED * 10) {
            let type, width;
            if (lastObstacle.type === 'gap') {
                type = 'bridge';
                width = Math.random() * 300 + 200;
            } else {
                type = Math.random() > 0.4 ? 'bridge' : 'gap';
                width = type === 'bridge' ? Math.random() * 300 + 200 : Math.random() * 120 + 80;
            }
            createObstacle(nextLeft, width, type);
        }
    }

    function jump() {
        if (!isGameRunning || isRespawning) return;
        if (isGrounded) {
            playerVy = -JUMP_POWER;
            isGrounded = false;
        }
    }

    function updatePlayerPosition() {
        playerTrain.style.bottom = `${playerY}px`;
    }

    function respawn() {
        if (isRespawning) return;
        isRespawning = true;
        carriageCount = 0;
        renderTrain();
        setTimeout(() => {
            playerY = 600;
            playerVy = 0;
            updatePlayerPosition();
            isRespawning = false;
        }, 1000);
    }

    function showGetEffect() {
        const effect = document.createElement('div');
        effect.classList.add('get-effect');
        effect.textContent = 'CONNECT!';
        effect.style.left = `${PLAYER_X}px`;
        effect.style.top = `${gameScreen.offsetHeight - playerY - 80}px`; 
        gameScreen.appendChild(effect);
        setTimeout(() => effect.remove(), 800);
    }

    function gameLoop() {
        if (!isGameRunning) return;

        if (!isRespawning) {
            playerVy += GRAVITY;
            playerY -= playerVy;
        }

        // カラスのスポーン判定（車両が1両以上あるときだけ）
        // 確率で出現 & 画面内にカラスが多すぎないように
        if (carriageCount >= 1 && crows.length === 0 && !isRespawning) {
            if (Math.random() < 0.005) { // 0.5%の確率で毎フレーム抽選
                spawnCrow();
            }
        }

        // --- カラスの更新 ---
        crows.forEach((crow, index) => {
            crow.x += crow.vx;
            crow.y += crow.vy;
            crow.element.style.left = `${crow.x}px`;
            crow.element.style.bottom = `${crow.y}px`;

            // 攻撃中なら当たり判定
            if (crow.state === 'attack') {
                // プレイヤーの先頭車両との距離判定
                const trainCenterX = PLAYER_X + 27; // 車両幅54の半分
                const trainCenterY = playerY + 20;  // 車両高さ40の半分
                
                const dx = (crow.x + 25) - trainCenterX; // カラス中心
                const dy = (crow.y + 15) - trainCenterY;
                const distance = Math.sqrt(dx*dx + dy*dy);

                // ヒット！
                if (distance < 40 && !isRespawning) {
                    // 1. 車両を減らす
                    carriageCount--;
                    renderTrain(); // 描画更新（これで先頭が消え、次が先頭になる）
                    
                    // 2. 連れ去り演出生成
                    createStolenScene(PLAYER_X, playerY);
                    
                    // 3. この攻撃カラスは消す
                    crow.element.remove();
                    crows.splice(index, 1);
                    return; // ループ抜ける
                }
            }

            // 画面外に出たら消す
            if (crow.x < -100 || crow.y > 800 || crow.y < -50) {
                crow.element.remove();
                crows.splice(index, 1);
            }
        });

        // --- 連れ去り演出の更新 ---
        stolenScenes.forEach((scene, index) => {
            scene.x += scene.vx;
            scene.y += scene.vy;
            scene.element.style.left = `${scene.x}px`;
            scene.element.style.bottom = `${scene.y}px`;
            
            if (scene.y > 800) {
                scene.element.remove();
                stolenScenes.splice(index, 1);
            }
        });

        // --- 障害物 & アイテム ---
        let currentGround = null;
        obstacles.forEach((obs, index) => {
            obs.left -= SCROLL_SPEED;
            obs.element.style.left = `${obs.left}px`;

            const playerRight = PLAYER_X + 54;
            if (playerRight - 10 > obs.left && PLAYER_X + 10 < obs.left + obs.width) {
                if (obs.type === 'bridge') currentGround = obs;
            }

            if (obs.left + obs.width < -100) {
                obs.element.remove();
                obstacles.splice(index, 1);
            }
        });

        items.forEach((item, index) => {
            item.left -= SCROLL_SPEED;
            item.element.style.left = `${item.left}px`;
            const itemWidth = 30;
            const playerWidth = 54;
            if (item.left < PLAYER_X + playerWidth && item.left + itemWidth > PLAYER_X) {
                const itemBottom = BRIDGE_HEIGHT + 30;
                if (playerY < itemBottom + 40 && playerY + 40 > itemBottom) {
                    item.element.remove();
                    items.splice(index, 1);
                    carriageCount++;
                    renderTrain();
                    showGetEffect();
                }
            }
            if (item.left < -50) {
                item.element.remove();
                items.splice(index, 1);
            }
        });

        spawnNextObstacle();

        // 接地・落下
        if (!isRespawning) {
            if (currentGround && playerY <= BRIDGE_HEIGHT && playerY > BRIDGE_HEIGHT - 30 && playerVy >= 0) {
                if (!isGrounded) {
                    playerTrain.classList.remove('poyo');
                    playerTrain.classList.add('landing');
                    setTimeout(() => {
                        playerTrain.classList.remove('landing');
                        playerTrain.classList.add('poyo');
                    }, 400);
                }
                playerY = BRIDGE_HEIGHT;
                playerVy = 0;
                isGrounded = true;
            } else if (!currentGround && playerY <= BRIDGE_HEIGHT && isGrounded) {
                isGrounded = false;
            }
    
            if (playerY < -100) {
                respawn();
            }
        }

        updatePlayerPosition();
        animationId = requestAnimationFrame(gameLoop);
    }

    gameScreen.addEventListener('mousedown', jump);
    document.addEventListener('keydown', (e) => { if (e.code === 'Space') { e.preventDefault(); jump(); } });
    gameScreen.addEventListener('touchstart', (e) => { e.preventDefault(); jump(); }, { passive: false });

    initGame();

</script>
</body>
</html>
"""

# HTMLを描画
components.html(html_code, height=650)

st.write("チケットを集めるとカラスが襲ってくる！ジャンプでかわして、連結を守り抜けだっち！🦅🍄")
