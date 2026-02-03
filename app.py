import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Bridge Cross Game", layout="wide")

st.title("🚃 ギリギリ橋渡しゲームだっち 🍄")
st.write("マウスを押して橋を伸ばすっち！離すと橋が倒れるよ。長さがピッタリじゃないと…ポトッ😱")

# ゲームの本体（HTML/CSS/JS）
html_code = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style>
    @import url('https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@700&display=swap');

    body {
        margin: 0;
        padding: 0;
        background-color: #f0f8ff; /* 空の色 */
        font-family: 'M PLUS Rounded 1c', sans-serif;
        overflow: hidden;
        user-select: none;
        touch-action: manipulation;
    }
    #game-container {
        position: relative;
        width: 100%;
        height: 400px;
        background: linear-gradient(#87CEEB, #E0F7FA);
        overflow: hidden;
        border-radius: 15px;
        border: 4px solid #333;
        cursor: pointer;
    }
    
    /* 崖（柱）のデザイン - 画像の茶色いレンガ風 */
    .pillar {
        position: absolute;
        bottom: 0;
        background-color: #8B4513;
        background-image: repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(0,0,0,0.1) 10px, rgba(0,0,0,0.1) 20px);
        border-top: 5px solid #5D4037;
        z-index: 2;
    }

    /* プレイヤー（バス/電車） */
    #player {
        position: absolute;
        bottom: 0; /* 柱の上に配置 */
        width: 40px;
        height: 40px;
        font-size: 30px;
        text-align: center;
        line-height: 40px;
        z-index: 3;
        transition: transform 0.5s linear; /* ぬるぬる動く指定 */
    }

    /* 橋（棒） */
    #bridge {
        position: absolute;
        bottom: 0; /* 柱の高さに合わせる JSで調整 */
        width: 4px;
        background-color: #333;
        transform-origin: bottom right; /* 右下を中心に回転 */
        transform: rotate(0deg);
        z-index: 1;
        display: none;
    }

    /* 落ちる時のアニメーション */
    @keyframes fall {
        0% { transform: translateY(0) rotate(0deg); }
        100% { transform: translateY(300px) rotate(45deg); opacity: 0; }
    }
    .falling {
        animation: fall 0.8s forwards;
    }

    /* メッセージ表示 */
    #message {
        position: absolute;
        top: 20%;
        width: 100%;
        text-align: center;
        font-size: 24px;
        color: #333;
        pointer-events: none;
        text-shadow: 2px 2px 0px white;
    }
    
    .score-board {
        position: absolute;
        top: 10px;
        right: 20px;
        font-size: 20px;
        color: #333;
    }

</style>
</head>
<body>

<div id="game-container">
    <div id="score" class="score-board">Score: 0</div>
    <div id="message">画面を長押しして橋を伸ばすっち！</div>
    
    <div id="bridge"></div>
    <div id="player">🚃</div>
</div>

<script>
    const container = document.getElementById('game-container');
    const player = document.getElementById('player');
    const bridge = document.getElementById('bridge');
    const msg = document.getElementById('message');
    const scoreEl = document.getElementById('score');

    let pillarHeight = 150; // 崖の高さ
    let startPillarWidth = 60;
    let gameStatus = 'ready'; // ready, growing, rotating, moving, falling, reset
    let bridgeHeight = 0;
    let growSpeed = 4;
    let animationId;
    let score = 0;
    
    // 最初の柱とターゲットの柱
    let currentPillar = createPillar(0, startPillarWidth);
    let targetPillar = createTargetPillar();

    // プレイヤーの初期位置
    let playerX = startPillarWidth - 40; // 右端に寄せる
    updatePlayerPos();

    function createPillar(left, width) {
        const p = document.createElement('div');
        p.className = 'pillar';
        p.style.width = width + 'px';
        p.style.height = pillarHeight + 'px';
        p.style.left = left + 'px';
        container.appendChild(p);
        return { el: p, left: left, width: width };
    }

    function createTargetPillar() {
        // ランダムな距離と幅
        const dist = 50 + Math.random() * 150; 
        const width = 40 + Math.random() * 60;
        const left = currentPillar.left + currentPillar.width + dist;
        return createPillar(left, width);
    }

    function updatePlayerPos() {
        player.style.left = playerX + 'px';
        player.style.bottom = pillarHeight + 'px';
    }

    // マウス/タッチイベント
    container.addEventListener('mousedown', startGrow);
    container.addEventListener('touchstart', startGrow);
    container.addEventListener('mouseup', stopGrow);
    container.addEventListener('touchend', stopGrow);

    function startGrow(e) {
        if (e.type === 'touchstart') e.preventDefault();
        if (gameStatus !== 'ready') return;
        
        gameStatus = 'growing';
        msg.innerText = "伸ばすっち…！";
        
        // 橋の初期設定
        bridge.style.display = 'block';
        bridge.style.height = '0px';
        bridge.style.left = (currentPillar.left + currentPillar.width - 4) + 'px'; // 柱の右端
        bridge.style.bottom = pillarHeight + 'px';
        bridge.style.transform = 'rotate(0deg)';
        bridgeHeight = 0;

        growLoop();
    }

    function growLoop() {
        if (gameStatus !== 'growing') return;
        bridgeHeight += growSpeed;
        bridge.style.height = bridgeHeight + 'px';
        animationId = requestAnimationFrame(growLoop);
    }

    function stopGrow() {
        if (gameStatus !== 'growing') return;
        gameStatus = 'rotating';
        cancelAnimationFrame(animationId);
        
        msg.innerText = "倒れるっち！";
        // CSS transitionで回転
        bridge.style.transition = 'transform 0.5s ease-in';
        bridge.style.transform = 'rotate(90deg)';

        setTimeout(() => {
            checkResult();
        }, 500); // 回転アニメーションの時間待つ
    }

    function checkResult() {
        bridge.style.transition = ''; // transitionリセット
        
        // 橋の長さ（倒れたら幅になる）
        const bridgeLen = bridgeHeight;
        
        // ギャップの距離
        const gapStart = targetPillar.left - (currentPillar.left + currentPillar.width);
        const gapEnd = gapStart + targetPillar.width;

        // 判定
        if (bridgeLen >= gapStart && bridgeLen <= gapEnd) {
            // 成功！
            movePlayerSuccess(bridgeLen);
        } else {
            // 失敗…
            movePlayerFail(bridgeLen);
        }
    }

    function movePlayerSuccess(distance) {
        gameStatus = 'moving';
        msg.innerText = "ぴゅー💨";
        
        // 次の柱の上まで移動
        const nextX = targetPillar.left + targetPillar.width - 40;
        const moveDist = nextX - playerX;
        
        // CSSでぬるぬる移動
        player.style.transition = `left 1.0s linear`;
        playerX = nextX;
        player.style.left = playerX + 'px';

        setTimeout(() => {
            score++;
            scoreEl.innerText = 'Score: ' + score;
            msg.innerText = "やったっち！🍄";
            nextLevel();
        }, 1000);
    }

    function movePlayerFail(distance) {
        gameStatus = 'moving';
        
        // 橋の先端、または次の柱の手前まで移動
        let targetX = currentPillar.left + currentPillar.width + distance;
        
        // 橋が短すぎる場合は橋の先端へ。長すぎる場合も橋の先端へ（そして落ちる）
        // プレイヤーの動き
        player.style.transition = `left 0.8s linear`;
        playerX = targetX; 
        player.style.left = playerX + 'px';

        setTimeout(() => {
            msg.innerText = "ポトッ…😢";
            player.classList.add('falling'); // 落ちるアニメーション
            bridge.style.transform = 'rotate(180deg)'; // 橋もブラ〜ンとなる
            bridge.style.transition = 'transform 0.5s ease-in';
            
            setTimeout(() => {
                alert('ゲームオーバーだっち！ Score: ' + score);
                location.reload(); // リロードしてリセット
            }, 1000);
        }, 800);
    }

    function nextLevel() {
        // 画面全体を左にスクロール（柱を移動）
        gameStatus = 'reset';
        
        // 現在の柱を削除対象に
        const oldPillar = currentPillar.el;
        
        // 新しい基準位置計算
        const shiftX = targetPillar.left; 

        // アニメーションで全体を左に寄せるのは少し複雑なので
        // 簡易的にDOMを再生成してリセットする
        
        container.removeChild(oldPillar);
        bridge.style.display = 'none';
        bridge.style.height = '0px';
        bridge.style.transform = 'rotate(0deg)';

        // ターゲットだった柱を現在の柱にする
        currentPillar = targetPillar;
        
        // 位置調整（左端に寄せるアニメーションっぽく見せる）
        // ここでは簡易的に座標を更新して、新しいターゲットを作る
        
        // すべての柱を左にシフト
        const shiftAmount = currentPillar.left;
        
        const pillars = document.querySelectorAll('.pillar');
        pillars.forEach(p => {
            let currentL = parseInt(p.style.left);
            p.style.transition = 'left 0.5s ease';
            p.style.left = (currentL - shiftAmount) + 'px';
        });
        
        // プレイヤーもシフト
        player.style.transition = 'left 0.5s ease';
        playerX -= shiftAmount;
        player.style.left = playerX + 'px';
        
        // データ上の位置も更新
        currentPillar.left = 0;

        // 新しいターゲット作成（画面外右側に作って入ってくるようにする）
        setTimeout(() => {
             player.style.transition = ''; // transition解除
             const pillars = document.querySelectorAll('.pillar');
             pillars.forEach(p => p.style.transition = '');
             
             targetPillar = createTargetPillar();
             gameStatus = 'ready';
             msg.innerText = "次へGOだっち！";
        }, 500);
    }
</script>

</body>
</html>
"""

# Streamlitに埋め込む
components.html(html_code, height=450)

st.write("※ 画面を長押しすると橋が伸びるよ。離すと倒れるっち！")
