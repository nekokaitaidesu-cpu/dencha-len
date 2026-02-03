import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="ぽよぽよ電車ジャンプ！", layout="wide")

# タイトル
st.title("🍄 危機一髪！ぽよぽよ電車ジャンプ！ 🚂")
st.write("画面をクリック、またはスペースキーでジャンプ！穴に落ちたら終わりだっち！")

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

    /* ゲーム画面 */
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

    /* 背景装飾（雲） */
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

    /* 橋と穴のコンテナ */
    #obstacles-container {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: var(--bridge-height);
        z-index: 5;
    }

    /* 橋のパーツ */
    .bridge-part {
        position: absolute;
        bottom: 0;
        height: 100%;
        background-color: var(--bridge-base-color);
        background-image: 
            linear-gradient(to bottom, var(--bridge-line-color) 2px, transparent 2px),
            linear-gradient(90deg, var(--bridge-line-color) 2px, transparent 2px);
        background-size: 100% 20px, 40px 100%;
        box-sizing: border-box;
        border-top: 10px solid #5D4037;
    }

    /* 穴のパーツ（視覚的には何もないが、デバッグや将来の拡張用にクラス定義） */
    .gap-part {
        position: absolute;
        bottom: 0;
        height: 100%;
        /* background: rgba(255,0,0,0.2); デバッグ用 */
    }

    /* プレイヤー（電車） */
    #player-train {
        position: absolute;
        left: 100px;
        width: 54px;
        height: 40px;
        z-index: 10;
        transform-origin: bottom center;
    }
    #player-train.poyo { animation: poyoPoyo 0.6s steps(3) infinite alternate; }

    /* 電車のデザイン（変更なし） */
    .train-body {
        width: 100%; height: 28px; background-color: #4DB6AC; border-radius: 6px; border: 2px solid #004D40;
        position: absolute; bottom: 4.5px; left: 0; display: flex; justify-content: space-evenly; align-items: center;
        box-shadow: 2px 2px 0px rgba(0,0,0,0.2); box-sizing: border-box; z-index: 2;
    }
    .train-body::before { content: ''; position: absolute; top: -5px; left: 2px; width: 46px; height: 5px; background-color: #004D40; border-radius: 3px 3px 0 0; }
    .window { width: 8px; height: 8px; background-color: #FFF9C4; border: 1px solid #004D40; border-radius: 2px; }
    .wheels-container { position: absolute; bottom: 0; width: 100%; height: 9px; display: flex; justify-content: space-between; padding: 0 8px; box-sizing: border-box; z-index: 1; }
    .wheel { width: 9px; height: 9px; background-color: #FFC107; border: 1.5px solid #FF6F00; border-radius: 50%; }
    .smoke { position: absolute; top: -15px; right: 5px; width: 10px; height: 10px; background: white; border-radius: 50%; opacity: 0; z-index: 0; }
    #player-train.poyo .smoke { animation: smokeAnim 1s ease-out infinite; }

    /* ゲームオーバー画面 */
    #game-over-screen {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.7); color: white; display: none;
        flex-direction: column; justify-content: center; align-items: center; z-index: 30;
    }
    #game-over-screen h2 { font-size: 48px; margin-bottom: 20px; color: #FF5722; }
    #restart-button {
        padding: 15px 30px; font-size: 24px; background: #4CAF50; color: white; border: none; border-radius: 10px; cursor: pointer;
        box-shadow: 0 4px #2E7D32; transition: all 0.1s;
    }
    #restart-button:active { box-shadow: 0 2px #2E7D32; transform: translateY(2px); }

    /* アニメーション */
    @keyframes poyoPoyo { 0% { transform: scale(1, 1); } 100% { transform: scale(0.95, 1.05); } }
    @keyframes smokeAnim { 0% { opacity: 0.8; transform: scale(0.5) translate(0, 0); } 100% { opacity: 0; transform: scale(1.5) translate(-10px, -20px); } }
</style>
</head>
<body>

<div id="game-screen">
    <div class="cloud c1"></div>
    <div class="cloud c2"></div>
    
    <div id="obstacles-container"></div>

    <div id="player-train" class="poyo">
        <div class="smoke"></div>
        <div class="wheels-container"><div class="wheel"></div><div class="wheel"></div></div>
        <div class="train-body"><div class="window"></div><div class="window"></div><div class="window"></div></div>
    </div>

    <div id="game-over-screen">
        <h2>GAME OVER</h2>
        <button id="restart-button">もう一度！</button>
    </div>
</div>

<script>
    const gameScreen = document.getElementById('game-screen');
    const playerTrain = document.getElementById('player-train');
    const obstaclesContainer = document.getElementById('obstacles-container');
    const gameOverScreen = document.getElementById('game-over-screen');
    const restartButton = document.getElementById('restart-button');

    // 定数
    const BRIDGE_HEIGHT = 280;
    const GRAVITY = 0.6;
    const JUMP_POWER = 12;
    const SCROLL_SPEED = 5;
    const PLAYER_X = 100;
    
    // 変数
    let isGameRunning = false;
    let animationId;
    let playerY = BRIDGE_HEIGHT;
    let playerVy = 0;
    let isGrounded = true;
    let obstacles = [];

    function initGame() {
        isGameRunning = true;
        gameOverScreen.style.display = 'none';
        playerTrain.classList.add('poyo');

        // リセット
        playerY = BRIDGE_HEIGHT;
        playerVy = 0;
        isGrounded = true;
        updatePlayerPosition();

        obstacles.forEach(obs => obs.element.remove());
        obstacles = [];
        // 最初の足場
        createObstacle(0, gameScreen.offsetWidth + 200, 'bridge');
        
        if (animationId) cancelAnimationFrame(animationId);
        gameLoop();
    }

    function createObstacle(left, width, type) {
        const element = document.createElement('div');
        element.classList.add(type === 'bridge' ? 'bridge-part' : 'gap-part');
        element.style.left = `${left}px`;
        element.style.width = `${width}px`;
        obstaclesContainer.appendChild(element);
        obstacles.push({ element, left, width, type });
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
                type = Math.random() > 0.4 ? 'bridge' : 'gap'; // 穴の確率少しアップ
                width = type === 'bridge' ? Math.random() * 300 + 200 : Math.random() * 120 + 80;
            }
            createObstacle(nextLeft, width, type);
        }
    }

    function jump() {
        if (!isGameRunning) return;
        if (isGrounded) {
            playerVy = -JUMP_POWER;
            isGrounded = false;
        }
    }

    function updatePlayerPosition() {
        playerTrain.style.bottom = `${playerY}px`;
    }

    function gameOver() {
        isGameRunning = false;
        cancelAnimationFrame(animationId);
        playerTrain.classList.remove('poyo');
        gameOverScreen.style.display = 'flex';
    }

    function gameLoop() {
        if (!isGameRunning) return;

        // 1. 物理演算
        playerVy += GRAVITY;
        playerY -= playerVy;

        // 2. 障害物スクロールと接地判定用データの取得
        let currentGround = null;

        obstacles.forEach((obs, index) => {
            obs.left -= SCROLL_SPEED;
            obs.element.style.left = `${obs.left}px`;

            // プレイヤーの足元にある障害物を探す
            const playerRight = PLAYER_X + 54;
            // 判定を少し厳しくして、タイヤが完全に乗らないと落ちるように調整
            if (playerRight - 10 > obs.left && PLAYER_X + 10 < obs.left + obs.width) {
                if (obs.type === 'bridge') {
                    currentGround = obs;
                }
            }

            if (obs.left + obs.width < -100) {
                obs.element.remove();
                obstacles.splice(index, 1);
            }
        });
        spawnNextObstacle();

        // 3. 接地・落下判定（ここを修正！）
        // 「地面があって」かつ「足の高さが地面以下」かつ「落下中(vy>=0)」
        // ★重要：さらに「地面より深すぎない(地面から30px以内)」場合のみ着地成功とする
        // これにより、穴に落ちて体が地面より下にある状態で、横から次の橋が来ても着地せずに落ち続ける
        if (currentGround && playerY <= BRIDGE_HEIGHT && playerY > BRIDGE_HEIGHT - 30 && playerVy >= 0) {
            playerY = BRIDGE_HEIGHT;
            playerVy = 0;
            isGrounded = true;
        } else if (!currentGround && playerY <= BRIDGE_HEIGHT && isGrounded) {
            // 足元に地面がないなら落下開始
            isGrounded = false;
        }

        // 4. ゲームオーバー（画面下へ落下）
        if (playerY < -100) {
            gameOver();
            return;
        }

        updatePlayerPosition();
        animationId = requestAnimationFrame(gameLoop);
    }

    gameScreen.addEventListener('mousedown', jump);
    document.addEventListener('keydown', (e) => {
        if (e.code === 'Space') { e.preventDefault(); jump(); }
    });
    gameScreen.addEventListener('touchstart', (e) => { e.preventDefault(); jump(); }, { passive: false });
    restartButton.addEventListener('click', initGame);

    initGame();

</script>
</body>
</html>
"""

# HTMLを描画
components.html(html_code, height=650)

st.write("これで、穴に落ちたらちゃんとさよならバイバイだっち！👋🍄 気をつけてジャンプしてね！")
