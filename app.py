import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="ぽよぽよ電車だっち", layout="wide")

# タイトル
st.title("🚂 広野をゆく、ぽよぽよ電車だっち 🍄")
st.write("電車が小さくなって、背景が広くなったよ！タイヤもかっこよくなっただっち！")

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
        height: 450px; /* 高さを少し広げた */
        background: linear-gradient(to bottom, #87CEEB 0%, #E0F7FA 80%, #f0e68c 100%); /* 空の下の方を少し黄色っぽくして地平線感を出す */
        position: relative;
        overflow: hidden;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* 雲（背景装飾）- 少しゆっくりに */
    .cloud {
        position: absolute;
        top: 50px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 50px;
        animation: moveClouds 25s linear infinite; /* ゆっくり */
    }
    .cloud::after, .cloud::before {
        content: '';
        position: absolute;
        background: inherit;
        border-radius: 50%;
    }
    .cloud.c1 { width: 120px; height: 45px; top: 60px; left: -150px; animation-duration: 30s; }
    .cloud.c1::after { width: 60px; height: 60px; top: -30px; left: 20px; }
    .cloud.c1::before { width: 50px; height: 50px; top: -20px; left: 60px; }

    .cloud.c2 { width: 90px; height: 35px; top: 120px; left: -100px; animation-duration: 20s; animation-delay: 8s; }
    .cloud.c2::after { width: 45px; height: 45px; top: -22px; left: 12px; }

    /* 橋（動く背景） */
    .bridge {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 200%;
        height: 180px; /* 橋を大きく見せる */
        background-color: #8B4513;
        /* アーチを大きく */
        background-image: radial-gradient(circle at bottom center, transparent 65%, #A0522D 66%);
        background-size: 150px 150px; /* アーチのサイズアップ */
        background-repeat: repeat-x;
        background-position: bottom;
        animation: scrollBridge 2.5s linear infinite; /* 電車が小さいので少しゆっくりに見せる */
    }
    
    .bridge::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 25px;
        background: #654321;
        border-bottom: 6px solid #4e342e;
    }

    /* --- 電車（小さく変更） --- */
    .train-container {
        position: absolute;
        bottom: 190px; /* 橋の上に配置（位置調整） */
        width: 90px;  /* 幅を小さく */
        height: 60px; /* 高さを小さく */
        z-index: 10;
        animation: poyoPoyo 0.6s steps(3) infinite alternate;
    }

    /* 電車のボディ */
    .train-body {
        width: 100%;
        height: 70%;
        background-color: #4DB6AC;
        border-radius: 10px; /* 角丸を小さく */
        border: 3px solid #004D40; /* 線を細く */
        position: relative;
        display: flex;
        justify-content: space-around;
        align-items: center;
        box-shadow: 3px 3px 0px rgba(0,0,0,0.2);
    }

    /* 屋根 */
    .train-body::before {
        content: '';
        position: absolute;
        top: -8px;
        left: 5px;
        width: 80px;
        height: 8px;
        background-color: #004D40;
        border-radius: 4px 4px 0 0;
    }

    /* 窓 */
    .window {
        width: 18px; /* 小さく */
        height: 18px; /* 小さく */
        background-color: #FFF9C4;
        border: 2px solid #004D40; /* 細く */
        border-radius: 4px;
    }

    /* タイヤ周りのコンテナ */
    .wheels-container {
        position: absolute;
        bottom: 2px;
        width: 100%;
        height: 30px;
        display: flex;
        justify-content: space-between;
        padding: 0 8px;
        box-sizing: border-box;
        pointer-events: none; /* 連結棒が邪魔しないように */
    }

    /* --- 新しいタイヤのデザイン --- */
    .wheel {
        width: 24px;
        height: 24px;
        background-color: #222; /* 黒 */
        border-radius: 50%;
        border: 3px dashed #555; /* ギザギザ感を出す */
        animation: spinWheels 0.6s linear infinite;
        position: relative;
        z-index: 1; /* 連結棒より後ろ */
    }
    
    /* タイヤの中央（黄色い装飾） */
    .wheel::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 10px;
        height: 10px;
        background-color: #FFD700; /* 黄色 */
        border: 2px solid #B8860B;
        border-radius: 50%;
    }

    /* --- 黄色い連結棒（ロッド） --- */
    .connecting-rod {
        position: absolute;
        bottom: 10px; /* タイヤの中心付近 */
        left: 14px;   /* 位置調整 */
        width: 46px;  /* タイヤ間をつなぐ長さ */
        height: 7px;
        background-color: #FFD700; /* 黄色 */
        border: 2px solid #B8860B;
        border-radius: 4px;
        z-index: 2; /* タイヤより手前 */
        /* 電車のぽよぽよに合わせて動く */
        animation: rodMove 0.6s steps(3) infinite alternate;
    }

    /* 煙（小さく調整） */
    .smoke {
        position: absolute;
        top: -15px;
        right: 10px;
        width: 15px;
        height: 15px;
        background: white;
        border-radius: 50%;
        opacity: 0;
        animation: smoke 1s ease-out infinite;
    }

    /* --- アニメーション定義 --- */

    @keyframes scrollBridge {
        0% { transform: translateX(0); }
        100% { transform: translateX(-150px); } /* アーチのサイズに合わせて調整 */
    }

    @keyframes moveClouds {
        0% { transform: translateX(120%); }
        100% { transform: translateX(-180%); }
    }

    @keyframes poyoPoyo {
        0% { transform: translateY(0) scale(1, 1); }
        50% { transform: translateY(-2px) scale(1.03, 0.97); } /* 動きを少し控えめに */
        100% { transform: translateY(2px) scale(0.97, 1.03); }
    }

    @keyframes spinWheels {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* 連結棒のアニメーション（電車の動きに合わせる） */
    @keyframes rodMove {
        0% { transform: translateY(0); }
        50% { transform: translateY(-1px); }
        100% { transform: translateY(1px); }
    }
    
    @keyframes smoke {
        0% { opacity: 0.8; transform: scale(0.5) translate(0, 0); }
        100% { opacity: 0; transform: scale(1.8) translate(-15px, -25px); }
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
                <div class="window"></div>
            </div>
            <div class="wheels-container">
                <div class="wheel left"></div>
                <div class="wheel right"></div>
                <div class="connecting-rod"></div>
            </div>
        </div>
    </div>

</body>
</html>
"""

# HTMLを描画（高さを少し大きく確保）
components.html(html_code, height=500)

st.write("ちっちゃい電車が一生懸命走ってる感じ、出てるかな？🍄")
