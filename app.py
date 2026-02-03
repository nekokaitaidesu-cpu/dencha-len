import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="ぽよぽよ電車だっち", layout="wide")

# タイトル
st.title("🚂 地面にピタッ！豆粒電車だっち 🍄")
st.write("タイヤが小さくなって、地面をしっかり走ってるよ！")

# HTML/CSSコード
html_code = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style>
    /* 全体のコンテナ */
    .scene {
        width: 100%;
        height: 600px;
        background: linear-gradient(to bottom, #87CEEB 0%, #E0F7FA 70%, #f0e68c 100%);
        position: relative;
        overflow: hidden;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* 雲（背景装飾） */
    .cloud {
        position: absolute;
        top: 80px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 50px;
        animation: moveClouds 35s linear infinite;
    }
    .cloud::after, .cloud::before {
        content: '';
        position: absolute;
        background: inherit;
        border-radius: 50%;
    }
    .cloud.c1 { width: 150px; height: 60px; top: 80px; left: -180px; animation-duration: 40s; }
    .cloud.c1::after { width: 70px; height: 70px; top: -35px; left: 25px; }
    .cloud.c1::before { width: 60px; height: 60px; top: -25px; left: 70px; }
    .cloud.c2 { width: 100px; height: 40px; top: 180px; left: -120px; animation-duration: 25s; animation-delay: 10s; }
    .cloud.c2::after { width: 50px; height: 50px; top: -25px; left: 15px; }

    /* 橋（巨大） */
    .bridge {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 200%;
        height: 280px;
        background-color: #8B4513;
        background-image: radial-gradient(circle at bottom center, transparent 65%, #A0522D 66%);
        background-size: 200px 200px;
        background-repeat: repeat-x;
        background-position: bottom;
        animation: scrollBridge 3s linear infinite;
    }
    /* 橋の上の線路部分（高さ30px） */
    .bridge::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 30px;
        background: #654321;
        border-bottom: 8px solid #4e342e;
    }

    /* --- 電車 --- */
    .train-container {
        position: absolute;
        /* 橋の高さ(280px) + 線路の高さ(30px) - タイヤの高さ(約10px) で調整 */
        bottom: 300px; /* 地面に接地するように位置を調整したよ！ */
        width: 50px;
        height: 40px;
        z-index: 10;
        animation: poyoPoyo 0.5s steps(3) infinite alternate;
    }

    /* 電車のボディ */
    .train-body {
        width: 100%;
        height: 70%;
        background-color: #4DB6AC;
        border-radius: 8px;
        border: 2px solid #004D40;
        position: relative;
        display: flex;
        justify-content: space-evenly;
        align-items: center;
        box-shadow: 2px 2px 0px rgba(0,0,0,0.2);
    }

    /* 屋根 */
    .train-body::before {
        content: '';
        position: absolute;
        top: -6px;
        left: 3px;
        width: 44px;
        height: 6px;
        background-color: #004D40;
        border-radius: 3px 3px 0 0;
    }

    /* 窓 */
    .window {
        width: 10px;
        height: 10px;
        background-color: #FFF9C4;
        border: 1px solid #004D40;
        border-radius: 2px;
    }

    /* タイヤコンテナ */
    .wheels-container {
        position: absolute;
        bottom: 0px;
        width: 100%;
        height: 10px; /* タイヤに合わせて少し低く */
        display: flex;
        justify-content: space-between;
        padding: 0 4px; /* 左右の余白を調整して配置を整えた */
        box-sizing: border-box;
    }

    /* 左右のタイヤグループ（きゅっとくっつける） */
    .wheel-group {
        display: flex;
        gap: 1px; /* タイヤ間の隙間を狭くしたよ！ */
    }

    /* 黄色い小さいタイヤ（さらに小さく） */
    .wheel {
        width: 8px;  /* サイズダウン */
        height: 8px; /* サイズダウン */
        background-color: #FFC107;
        border: 1px solid #FF6F00;
        border-radius: 50%;
        animation: spinWheels 0.5s linear infinite;
        position: relative;
    }
    
    /* タイヤの回転マーク */
    .wheel::after {
        content: '';
        position: absolute;
        top: 1px; /* 位置調整 */
        left: 3px; /* 位置調整 */
        width: 2px;
        height: 2px;
        background-color: #FF6F00;
        border-radius: 50%;
    }

    /* 煙 */
    .smoke {
        position: absolute;
        top: -10px;
        right: 2px;
        width: 10px;
        height: 10px;
        background: white;
        border-radius: 50%;
        opacity: 0;
        animation: smoke 1s ease-out infinite;
    }

    /* --- アニメーション --- */
    @keyframes scrollBridge {
        0% { transform: translateX(0); }
        100% { transform: translateX(-200px); }
    }
    @keyframes moveClouds {
        0% { transform: translateX(130%); }
        100% { transform: translateX(-200%); }
    }
    @keyframes poyoPoyo {
        0% { transform: translateY(0) scale(1, 1); }
        50% { transform: translateY(-1px) scale(1.05, 0.95); } /* 上下の動きを控えめに */
        100% { transform: translateY(1px) scale(0.95, 1.05); } /* 上下の動きを控えめに */
    }
    @keyframes spinWheels {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    @keyframes smoke {
        0% { opacity: 0.8; transform: scale(0.5) translate(0, 0); }
        100% { opacity: 0; transform: scale(1.5) translate(-10px, -20px); }
    }

</style>
</head>
<body>

    <div class="scene">
        <div class="cloud c1"></div>
        <div class="cloud c2"></div>
        
        <div class="bridge"></div>

        <div class="train-container">
            <div class="smoke"></div>
            <div class="train-body">
                <div class="window"></div>
                <div class="window"></div>
            </div>
            <div class="wheels-container">
                <div class="wheel-group left">
                    <div class="wheel"></div>
                    <div class="wheel"></div>
                </div>
                <div class="wheel-group right">
                    <div class="wheel"></div>
                    <div class="wheel"></div>
                </div>
            </div>
        </div>
    </div>

</body>
</html>
"""

# HTMLを描画
components.html(html_code, height=600)

st.write("タイヤがきゅっとなって、地面をしっかり捉えてる感じが出たかな？🍄")
