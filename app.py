import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="ぽよぽよ電車ジャンプ！", layout="wide")

# タイトル
st.title("🍄 危機一髪！ぽよぽよ電車ジャンプ！ 🚂")
st.write("画面をクリック、またはスペースキーでジャンプ！穴に落ちないように進むだっち！")

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
        --bridge-base-color: #A0522D; /* レンガ色 */
        --bridge-line-color: rgba(0,0,0,0.2);
        --bridge-height: 280px; /* 橋の高さ */
    }

    /* ゲーム画面のコンテナ */
    #game-screen {
        width: 100%;
        height: 600px;
        background: linear-gradient(to bottom, var(--sky-color-top) 0%, var(--sky-color-bottom) 70%, var(--water-color-top) 70%, var(--water-color-bottom) 100%);
        position: relative;
        overflow: hidden;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        user-select: none; /* テキスト選択を防ぐ */
    }

    /* --- 背景装飾（雲） --- */
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

    /* --- 橋と穴のコンテナ --- */
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
        /* レンガ風の模様 */
        background-image: 
            linear-gradient(to bottom, var(--bridge-line-color) 2px, transparent 2px),
            linear-gradient(90deg, var(--bridge-line-color) 2px, transparent 2px);
        background-size: 100% 20px, 40px 100%;
        box-sizing: border-box;
        border-top: 10px solid #5D4037; /* 線路部分 */
    }

    /* --- 電車（プレイヤー） --- */
    #player-train {
        position: absolute;
        left: 100px; /* 横位置は固定 */
        /* bottomはJSで制御 */
        width: 54px;
        height: 40px;
        z-index: 10;
        transform-origin: bottom center;
        /* ぽよぽよアニメーション（クラス付与で制御） */
    }
    #player-train.poyo { animation: poyoPoyo 0.6s steps(3) infinite alternate; }

    /* 電車の構成パーツ（以前と同じ） */
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
    #player-train.poyo .smoke { animation: smokeAnim 1s ease-out infinite; } /* 走ってるときだけ煙 */

    /* --- UI関連 --- */
    #score-display {
        position: absolute; top: 20px; right: 30px; font-size: 24px; font-weight: bold; color: #333; z-index: 20;
        background: rgba(255,255,255,0.8); padding: 5px 15px; border-radius: 10px;
    }
    #game-over-screen {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.7); color: white; display: flex; flex-direction: column;
        justify-content: center; align-items: center; z-index: 30; display: none; /* 初期は非表示 */
    }
    #game-over-screen h2 { font-size: 48px; margin-bottom: 20px; color: #FF5722; }
    #restart-button {
        padding: 15px 30px; font-size: 24px; background: #4CAF50; color: white; border: none; border-radius: 10px; cursor: pointer;
        box-shadow: 0 4px #2E7D32; transition: all 0.1s;
    }
    #restart-button:active { box-shadow: 0 2px #2E7D32; transform: translateY(2px); }

    /* --- アニメーション定義 --- */
    @keyframes poyoPoyo {
        0% { transform: scale(1, 1); } 100% { transform: scale(0.95, 1.05); }
    }
    @keyframes smokeAnim {
        0% { opacity: 0.8; transform: scale(0.5) translate(0, 0); }
        100% { opacity: 0; transform: scale(1.5) translate(-10px, -20px); }
    }

</style>
</head>
<body>

<div id="game-screen">
    <div class="cloud c1"></div>
    <div class="cloud c2"></div>

    <div id="score-display">SCORE: 0</div>

    <div id="obstacles-container"></div>

    <div id="player-train" class="poyo">
        <div class="smoke"></div>
        <div class="wheels-container"><div class="wheel"></div><div class="wheel"></div></div>
        <div class="train-body"><div class="window"></div><div class="window"></div><div class="window"></div></div>
    </div>

    <div id="game-over-screen">
        <h2>GAME OVER</h2>
        <p>Score: <span id="final-score"></span></p>
        <button id="restart-button">もう一度遊ぶ！</button>
    </div>
</div>

<script>
    // --- JavaScript (ゲームロジック) ---
    
    // DOM要素の取得
    const gameScreen = document.getElementById('game-screen');
    const playerTrain = document.getElementById('player-train');
    const obstaclesContainer = document.getElementById('obstacles-container');
    const scoreDisplay = document.getElementById('score-display');
    const gameOverScreen = document.getElementById('game-over-screen');
    const finalScoreDisplay = document.getElementById('final-score');
    const restartButton = document.getElementById('restart-button');

    // ゲーム設定値
    const BRIDGE_HEIGHT = 280; // 橋の高さ(px)
    const GRAVITY = 0.6;       // 重力
    const JUMP_POWER = 12;     // ジャンプ力
    const SCROLL_SPEED = 5;    // スクロール速度
    const PLAYER_X = 100;      // プレイヤーの横位置(固定)
    
    // ゲーム状態変数
    let isGameRunning = false;
    let score = 0;
    let animationId;

    // プレイヤーの物理変数
    let playerY = BRIDGE_HEIGHT; // 初期位置は橋の上
    let playerVy = 0;            // 垂直速度
    let isGrounded = true;       // 接地フラグ

    // 障害物（橋と穴）の管理配列
    let obstacles = [];

    // --- 関数定義 ---

    // ゲームの初期化・リセット
    function initGame() {
        isGameRunning = true;
        score = 0;
        scoreDisplay.textContent = `SCORE: ${score}`;
        gameOverScreen.style.display = 'none';
        playerTrain.classList.add('poyo'); // 走るアニメーション開始

        // プレイヤー位置リセット
        playerY = BRIDGE_HEIGHT;
        playerVy = 0;
        isGrounded = true;
        updatePlayerPosition();

        // 障害物リセット
        obstacles.forEach(obs => obs.element.remove());
        obstacles = [];
        // 最初の足場を作る（画面幅分以上の橋）
        createObstacle(0, gameScreen.offsetWidth + 200, 'bridge');
        
        // ゲームループ開始
        if (animationId) cancelAnimationFrame(animationId);
        gameLoop();
    }

    // 障害物（橋または穴）を生成する関数
    function createObstacle(left, width, type) {
        const element = document.createElement('div');
        if (type === 'bridge') {
            element.classList.add('bridge-part');
        } else {
            // 穴（gap）は透明な要素
            element.classList.add('gap-part');
            // デバッグ用：穴の位置を見たい場合はコメントアウトを外す
            // element.style.backgroundColor = 'rgba(255,0,0,0.3)'; 
        }
        element.style.left = `${left}px`;
        element.style.width = `${width}px`;
        obstaclesContainer.appendChild(element);
        obstacles.push({ element, left, width, type });
    }

    // 新しい障害物を右端に追加するロジック
    function spawnNextObstacle() {
        const lastObstacle = obstacles[obstacles.length - 1];
        const nextLeft = lastObstacle.left + lastObstacle.width;
        
        // 画面外（右）に十分な足場がなければ追加
        if (nextLeft < gameScreen.offsetWidth + SCROLL_SPEED * 10) {
            let type, width;
            // 前が穴なら次は必ず橋
            if (lastObstacle.type === 'gap') {
                type = 'bridge';
                width = Math.random() * 300 + 200; // 200~500pxの橋
            } else {
                // 前が橋なら、ランダムで穴か橋
                // スコアが上がると穴の確率UPとかも面白いかも
                type = Math.random() > 0.3 ? 'bridge' : 'gap'; 
                if (type === 'bridge') {
                    width = Math.random() * 300 + 200;
                } else {
                    width = Math.random() * 100 + 80; // 80~180pxの穴（ジャンプで超えられる幅）
                }
            }
            createObstacle(nextLeft, width, type);
        }
    }

    // ジャンプ処理
    function jump() {
        if (!isGameRunning) return;
        if (isGrounded) {
            playerVy = -JUMP_POWER;
            isGrounded = false;
            // ジャンプ音などをここに入れると良い
        }
    }

    // プレイヤーの位置を画面に反映
    function updatePlayerPosition() {
        playerTrain.style.bottom = `${playerY}px`;
    }

    // ゲームオーバー処理
    function gameOver() {
        isGameRunning = false;
        cancelAnimationFrame(animationId);
        playerTrain.classList.remove('poyo'); // アニメーション停止
        finalScoreDisplay.textContent = score;
        gameOverScreen.style.display = 'flex';
        // ゲームオーバー音などをここに入れる
    }

    // --- メインゲームループ ---
    function gameLoop() {
        if (!isGameRunning) return;

        // 1. 物理演算（プレイヤー）
        playerVy += GRAVITY; // 重力を加算
        playerY -= playerVy; // 速度分移動（Y軸は上がプラスなので引く）

        // 2. 障害物のスクロールと管理
        let currentGround = null; // プレイヤーの真下にある地面（橋）

        obstacles.forEach((obs, index) => {
            obs.left -= SCROLL_SPEED;
            obs.element.style.left = `${obs.left}px`;

            // プレイヤーがこの障害物の上空にいるか判定
            // プレイヤーの右端 > 障害物の左端 AND プレイヤーの左端 < 障害物の右端
            const playerRight = PLAYER_X + 54; // 電車の幅
            if (playerRight > obs.left && PLAYER_X < obs.left + obs.width) {
                if (obs.type === 'bridge') {
                    currentGround = obs;
                }
            }

            // 画面外（左）に出たら削除
            if (obs.left + obs.width < -100) {
                obs.element.remove();
                obstacles.splice(index, 1);
                // スコア加算（橋を通過したら）
                if(obs.type === 'bridge') {
                     score++;
                     scoreDisplay.textContent = `SCORE: ${score}`;
                }
            }
        });
        spawnNextObstacle(); // 次の障害物を準備

        // 3. 接地判定と穴への落下判定
        if (currentGround && playerY <= BRIDGE_HEIGHT && playerVy >= 0) {
            // 橋の上にいて、かつ落下中または静止中なら着地
            playerY = BRIDGE_HEIGHT;
            playerVy = 0;
            isGrounded = true;
        } else if (!currentGround && playerY <= BRIDGE_HEIGHT && isGrounded) {
            // 真下に橋がなく（＝穴の上）、かつ接地フラグが立っていたら落下開始
            isGrounded = false;
        }

        // 4. ゲームオーバー判定（画面外への落下）
        if (playerY < -50) {
            gameOver();
            return;
        }

        // 5. 描画更新
        updatePlayerPosition();

        // 次のフレームを要求
        animationId = requestAnimationFrame(gameLoop);
    }

    // --- イベントリスナー設定 ---
    
    // ジャンプ操作（クリック & スペースキー）
    gameScreen.addEventListener('mousedown', jump);
    document.addEventListener('keydown', (e) => {
        if (e.code === 'Space') {
            e.preventDefault(); // スクロール防止
            jump();
        }
    });
    // スマホ対応（タッチ）
    gameScreen.addEventListener('touchstart', (e) => {
        e.preventDefault(); jump();
    }, { passive: false });

    // リスタートボタン
    restartButton.addEventListener('click', initGame);

    // --- ゲーム開始 ---
    // 画像などの読み込みを待たずに開始してOKな構成
    initGame();

</script>
</body>
</html>
"""

# HTMLを描画（高さを確保）
components.html(html_code, height=650)

st.write("どう？ジャンプのタイミング、結構難しいでしょ？🍄")
st.write("物理演算を使ってるから、ジャンプの頂点ではフワッと、落ちるときはヒュン！ってなるのがポイントだっち！")
