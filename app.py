import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="ぽよぽよ電車ジャンプ！", layout="wide")

# タイトル
st.title("🍄 連結！無限ゆるゆる電車ジャンプ 🚃🚃")
st.write("「増結チケット」を拾って車両を増やそう！落ちると1両に戻っちゃうから気をつけて！")

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
        bottom: 50px; /* 橋の上に浮く */
        width: 30px;
        height: 20px;
        background: #FFD700; /* 金色 */
        border: 2px solid #FFA000;
        border-radius: 4px;
        z-index: 6;
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.6);
        animation: floatItem 1s ease-in-out infinite alternate;
    }
    .item::after {
        content: '+1';
        font-size: 12px;
        font-weight: bold;
        color: #8B4500;
    }
    @keyframes floatItem { from { transform: translateY(0); } to { transform: translateY(-10px); } }

    /* プレイヤーコンテナ（全体） */
    #player-train {
        position: absolute;
        left: 100px;
        /* 高さは車両の高さ、幅は可変（flex） */
        height: 40px;
        z-index: 10;
        transform-origin: bottom center;
        display: flex;
        flex-direction: row-reverse; /* 先頭車両を右（進行方向）にするため反転 */
        align-items: flex-end; /* 下揃え */
        gap: 2px; /* 連結間隔 */
        transition: transform 0.1s;
    }
    #player-train.poyo { animation: poyoPoyo 0.6s steps(3) infinite alternate; }

    /* 車両ユニット（先頭も客車も共通） */
    .train-unit {
        position: relative;
        width: 54px;
        height: 40px;
        flex-shrink: 0; /* 縮まないように */
    }

    /* 車両ボディ */
    .train-body {
        width: 100%; height: 28px; background-color: #4DB6AC; border-radius: 6px; border: 2px solid #004D40;
        position: absolute; bottom: 4.5px; left: 0; display: flex; justify-content: space-evenly; align-items: center;
        box-shadow: 2px 2px 0px rgba(0,0,0,0.2); box-sizing: border-box; z-index: 2;
    }
    /* 客車（後ろの車両）は少し色を変える？いや、統一感重視で同じにする */
    /* .wagon .train-body { background-color: #81C784; } */

    .train-body::before { content: ''; position: absolute; top: -5px; left: 2px; width: 46px; height: 5px; background-color: #004D40; border-radius: 3px 3px 0 0; }
    .window { width: 8px; height: 8px; background-color: #FFF9C4; border: 1px solid #004D40; border-radius: 2px; }
    .wheels-container { position: absolute; bottom: 0; width: 100%; height: 9px; display: flex; justify-content: space-between; padding: 0 8px; box-sizing: border-box; z-index: 1; }
    .wheel { width: 9px; height: 9px; background-color: #FFC107; border: 1.5px solid #FF6F00; border-radius: 50%; }
    
    /* 煙は先頭車両（head）だけ */
    .smoke { position: absolute; top: -15px; right: 5px; width: 10px; height: 10px; background: white; border-radius: 50%; opacity: 0; z-index: 0; display: none; }
    .train-unit.head .smoke { display: block; }
    #player-train.poyo .head .smoke { animation: smokeAnim 1s ease-out infinite; }

    /* アニメーション */
    @keyframes poyoPoyo { 0% { transform: scale(1, 1); } 100% { transform: scale(0.95, 1.05); } }
    @keyframes smokeAnim { 0% { opacity: 0.8; transform: scale(0.5) translate(0, 0); } 100% { opacity: 0; transform: scale(1.5) translate(-10px, -20px); } }
    @keyframes landBounce { 0% { transform: scale(1, 1); } 30% { transform: scale(1.1, 0.9); } 60% { transform: scale(0.95, 1.05); } 100% { transform: scale(1, 1); } }
    .landing { animation: landBounce 0.4s ease-out !important; }

    /* アイテムゲット時のポップアップ */
    .get-effect {
        position: absolute;
        color: #FFD700;
        font-weight: bold;
        font-size: 20px;
        animation: floatUp 0.8s ease-out forwards;
        pointer-events: none;
        z-index: 20;
        text-shadow: 1px 1px 0 #000;
    }
    @keyframes floatUp { 0% { opacity: 1; transform: translateY(0); } 100% { opacity: 0; transform: translateY(-50px); } }

</style>
</head>
<body>

<div id="game-screen">
    <div class="cloud c1"></div>
    <div class="cloud c2"></div>
    <div id="obstacles-container"></div>
    
    <div id="player-train" class="poyo">
        </div>
</div>

<script>
    const gameScreen = document.getElementById('game-screen');
    const playerTrain = document.getElementById('player-train');
    const obstaclesContainer = document.getElementById('obstacles-container');

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

    let obstacles = []; // 橋と穴
    let items = [];     // アイテム
    let carriageCount = 0; // 追加された客車の数

    // 車両のHTML生成関数
    function createTrainUnitHTML(isHead) {
        return `
            <div class="train-unit ${isHead ? 'head' : 'wagon'}">
                <div class="smoke"></div>
                <div class="wheels-container"><div class="wheel"></div><div class="wheel"></div></div>
                <div class="train-body"><div class="window"></div><div class="window"></div><div class="window"></div></div>
            </div>
        `;
    }

    // 車両を描画する関数
    function renderTrain() {
        // 一旦空にする
        playerTrain.innerHTML = '';
        // 先頭車両を追加
        playerTrain.insertAdjacentHTML('beforeend', createTrainUnitHTML(true));
        // 客車を追加
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
        
        // 障害物リセット
        obstacles.forEach(obs => obs.element.remove());
        obstacles = [];
        items.forEach(item => item.element.remove());
        items = [];
        
        // 車両リセット（1両に戻す）
        carriageCount = 0;
        renderTrain();

        createObstacle(0, gameScreen.offsetWidth + 200, 'bridge');
        
        if (animationId) cancelAnimationFrame(animationId);
        gameLoop();
    }

    function createObstacle(left, width, type) {
        const element = document.createElement('div');
        if (type === 'bridge') element.classList.add('bridge-part');
        element.style.left = `${left}px`;
        element.style.width = `${width}px`;
        obstaclesContainer.appendChild(element);
        obstacles.push({ element, left, width, type });

        // 橋の場合、確率でアイテムを生成
        if (type === 'bridge' && width > 150) {
            // 30%の確率でアイテム出現
            if (Math.random() < 0.3) {
                createItem(left + width / 2); // 橋の真ん中あたりに
            }
        }
    }

    function createItem(left) {
        const element = document.createElement('div');
        element.classList.add('item');
        element.style.left = `${left}px`;
        // 橋の上(BRIDGE_HEIGHT)より少し上(bottomからの距離)
        // 障害物コンテナ内なので bottom 指定でOK
        element.style.bottom = `${BRIDGE_HEIGHT + 30}px`; 
        obstaclesContainer.appendChild(element); // 障害物と同じコンテナでスクロール管理
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
        
        // 落下したら車両リセット！
        carriageCount = 0;
        renderTrain();
        
        setTimeout(() => {
            playerY = 600;
            playerVy = 0;
            updatePlayerPosition();
            isRespawning = false;
        }, 1000);
    }

    // アイテムゲットのエフェクト
    function showGetEffect() {
        const effect = document.createElement('div');
        effect.classList.add('get-effect');
        effect.textContent = 'CONNECT!';
        effect.style.left = `${PLAYER_X}px`;
        effect.style.top = `${gameScreen.offsetHeight - playerY - 80}px`; // プレイヤーの上に表示
        gameScreen.appendChild(effect);
        setTimeout(() => effect.remove(), 800);
    }

    function gameLoop() {
        if (!isGameRunning) return;

        // 1. 物理演算
        if (!isRespawning) {
            playerVy += GRAVITY;
            playerY -= playerVy;
        }

        // 2. 障害物スクロール & アイテム処理
        let currentGround = null;

        // --- 障害物 ---
        obstacles.forEach((obs, index) => {
            obs.left -= SCROLL_SPEED;
            obs.element.style.left = `${obs.left}px`;

            const playerRight = PLAYER_X + 54;
            // 接地判定（先頭車両のみ判定する）
            if (playerRight - 10 > obs.left && PLAYER_X + 10 < obs.left + obs.width) {
                if (obs.type === 'bridge') currentGround = obs;
            }

            if (obs.left + obs.width < -100) {
                obs.element.remove();
                obstacles.splice(index, 1);
            }
        });

        // --- アイテム ---
        items.forEach((item, index) => {
            item.left -= SCROLL_SPEED;
            item.element.style.left = `${item.left}px`;
            
            // アイテム当たり判定（先頭車両と）
            // 簡易的な距離判定 or 矩形判定
            const itemWidth = 30;
            const playerWidth = 54;
            // プレイヤーXは固定(100)。アイテムがプレイヤーの範囲に入ったか
            if (item.left < PLAYER_X + playerWidth && item.left + itemWidth > PLAYER_X) {
                // 高さ判定（ジャンプで取れるように）
                // プレイヤーの底辺(playerY)から高さ40pxの間にあるか
                const itemBottom = BRIDGE_HEIGHT + 30; // アイテムの高さ
                // プレイヤーがアイテムの高さ付近にいるか
                if (playerY < itemBottom + 40 && playerY + 40 > itemBottom) {
                    // ゲット！
                    item.element.remove();
                    items.splice(index, 1);
                    
                    // 車両追加処理
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

        // 3. 接地・落下判定
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

st.write("増結チケットをゲットして、なが〜い電車を作ってみてね！落ちると一瞬で解散だっち！🍄👋")
