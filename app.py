import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ぽよぽよ電車ジャンプ！", layout="wide")
st.title("🍄 激闘！特攻カラスと回転列車 🚂🌀🆚🦅")
st.write("ボス撃破後は駅に到着！タップで即リスタートだっち！")

html_code = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style>
* {
    -webkit-tap-highlight-color: transparent;
    user-select: none;
}

body { margin:0; }

#game-screen {
    width:100%;
    height:600px;
    position:relative;
    overflow:hidden;
    background:linear-gradient(#87CEEB 70%, #40a4df 70%);
    border-radius:15px;
    touch-action:none;
}

/* ===== 駅ホーム ===== */
#station {
    position:absolute;
    bottom:0;
    left:0;
    width:100%;
    height:180px;
    background:#ccc;
    display:none;
    z-index:8;
}
#station::before {
    content:"";
    position:absolute;
    bottom:0;
    width:100%;
    height:40px;
    background:#999;
}
#station-roof {
    position:absolute;
    top:-40px;
    width:100%;
    height:40px;
    background:#555;
}
#station-sign {
    position:absolute;
    top:-80px;
    left:50%;
    transform:translateX(-50%);
    background:#2E7D32;
    color:white;
    padding:10px 30px;
    font-size:24px;
    border-radius:8px;
    font-weight:bold;
}

/* ===== ゴール表示 ===== */
#goal-message {
    position:absolute;
    inset:0;
    display:none;
    justify-content:center;
    align-items:center;
    flex-direction:column;
    font-size:48px;
    font-weight:bold;
    color:white;
    background:rgba(0,0,0,0.5);
    z-index:50;
    cursor:pointer;
    text-shadow:3px 3px 0 #000;
}

/* ===== 花吹雪 ===== */
.confetti {
    position:absolute;
    width:10px;
    height:10px;
    opacity:0.9;
    animation:fall 3s linear forwards;
}
@keyframes fall {
    from { transform:translateY(-20px) rotate(0deg); }
    to { transform:translateY(700px) rotate(360deg); }
}

/* ===== プレイヤー（簡易） ===== */
#player {
    position:absolute;
    left:100px;
    bottom:180px;
    width:60px;
    height:40px;
    background:#4DB6AC;
    border:3px solid #004D40;
    border-radius:8px;
    z-index:10;
}
</style>
</head>
<body>

<div id="game-screen">

    <div id="station">
        <div id="station-roof"></div>
        <div id="station-sign">🚉 ぽよぽよ駅</div>
    </div>

    <div id="player"></div>

    <div id="goal-message">
        🚉 無事到着！！<br>
        <span style="font-size:24px;margin-top:10px;">（タップで最初から）</span>
    </div>

</div>

<script>
const game = document.getElementById("game-screen");
const station = document.getElementById("station");
const goalMessage = document.getElementById("goal-message");
const player = document.getElementById("player");

let isGoal = false;

/* ===== 花吹雪生成 ===== */
function spawnConfetti() {
    for (let i = 0; i < 80; i++) {
        const c = document.createElement("div");
        c.className = "confetti";
        c.style.left = Math.random() * 100 + "%";
        c.style.background =
            ["#ff5252","#ffeb3b","#69f0ae","#40c4ff","#e040fb"]
            [Math.floor(Math.random()*5)];
        c.style.animationDelay = Math.random() * 1 + "s";
        game.appendChild(c);
        setTimeout(()=>c.remove(),3000);
    }
}

/* ===== ゴール演出 ===== */
function showGoal() {
    isGoal = true;
    station.style.display = "block";
    goalMessage.style.display = "flex";
    player.style.bottom = "180px";
    spawnConfetti();
}

/* ===== タップでリスタート ===== */
goalMessage.addEventListener("click", ()=>{
    if (!isGoal) return;
    isGoal = false;
    goalMessage.style.display = "none";
    station.style.display = "none";
});

/* ===== デモ用：3秒後にゴール ===== */
setTimeout(showGoal, 3000);
</script>

</body>
</html>
"""

components.html(html_code, height=650)
