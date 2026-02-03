import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="ぽよぽよ電車だっち", layout="wide")

# タイトル
st.title("🚂 ぽよぽよ走る電車だっち 🍄")
st.write("CSSだけで描いた電車が、橋の上をガタンゴトン走るよ！")

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
        height: 400px;
        background: linear-gradient(to bottom, #87CEEB 0%, #E0F7FA 100%); /* 空のグラデーション */
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
        top: 50px;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 50px;
        animation: moveClouds 15s linear infinite;
    }
    .cloud::after, .cloud::before {
        content: '';
        position: absolute;
        background: inherit;
        border-radius: 50%;
    }
    .cloud.c1 { width: 100px; height: 40px; top: 40px; left: -120px; animation-duration: 20s; }
    .cloud.c1::after { width: 50px; height: 50px; top: -25px; left: 15px; }
    .cloud.c1::before { width: 40px; height: 40px; top: -15px; left: 50px; }

    .cloud.c2 { width: 80px; height: 30px; top: 80px; left: -100px; animation-duration: 12s; animation-delay: 5s; }
    .cloud.c2::after { width: 40px; height: 40px; top: -20px; left: 10px; }

    /* 橋（動く背景） */
    .bridge {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 200%; /* ループさせるために広く */
        height: 150px;
        background-color: #8B4513; /* 茶色 */
        /* アーチを描くためのグラデーション */
        background-image: radial-gradient(circle at bottom center, transparent 65%, #A0522D 66%);
        background-size: 100px 100px; /* アーチのサイズ */
        background-repeat: repeat-x;
        background-position: bottom;
        animation: scrollBridge 1.5s linear infinite;
    }
    
    /* 橋の上部（線路部分） */
    .bridge::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 20px;
        background: #654321;
        border-bottom: 5px solid #4e342e;
    }

    /* 電車本体のコンテナ */
    .train-container {
        position: absolute;
        bottom: 155px; /* 橋の上に配置 */
        width: 160px;
        height: 100px;
        z-index: 10;
        /* ぽよぽよさせるアニメーション（3パターンのコマ送り風） */
        animation: poyoPoyo 0.6s steps(3) infinite alternate;
    }

    /* 電車のボディ */
    .train-body {
        width: 100%;
        height: 70%;
        background-color: #4DB6AC; /* 緑っぽい色 */
        border-radius: 15px;
        border: 4px solid #004D40;
        position: relative;
        display: flex;
        justify-content: space-around;
        align-items: center;
        box-shadow: 4px 4px 0px rgba(0,0,0,0.2);
    }

    /* 屋根 */
    .train-body::before {
        content: '';
        position: absolute;
        top: -10px;
        left: 10px;
        width: 140px;
        height: 10px;
        background-color: #004D40;
        border-radius: 5px 5px 0 0;
    }

    /* 窓 */
    .window {
        width: 30px;
        height: 30px;
        background-color: #FFF9C4; /* 薄い黄色 */
        border: 3px solid #004D40;
        border-radius: 5px;
    }

    /* タイヤ */
    .wheels-container {
        position: absolute;
        bottom: 5px;
        width: 100%;
        display: flex;
        justify-content: space-between;
        padding: 0 15px;
        box-sizing: border-box;
    }

    .wheel {
        width: 35px;
        height: 35px;
        background-color: #333;
        border-radius: 50%;
        border: 3px dashed #999; /* 回転がわかるように破線 */
        animation: spinWheels 0.5s linear infinite;
        position: relative;
    }
    
    /* タイヤの中央 */
    .wheel::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 10px;
        height: 10px;
        background-color: #999;
        border-radius: 50%;
    }

    /* 煙（おまけ） */
    .smoke {
        position: absolute;
        top: -20px;
        right: 20px;
        width: 20px;
        height: 20px;
        background: white;
        border-radius: 50%;
        opacity: 0;
        animation: smoke 1s ease-out infinite;
    }

    /* --- アニメーション定義 --- */

    /* 橋が左に流れる（電車が走ってるように見える） */
    @keyframes scrollBridge {
        0% { transform: translateX(0); }
        100% { transform: translateX(-100px); } /* アーチ1個分移動 */
    }

    /* 雲が流れる */
    @keyframes moveClouds {
        0% { transform: translateX(110%); }
        100% { transform: translateX(-150%); }
    }

    /* 電車がぽよぽよする（コマ送り風） */
    @keyframes poyoPoyo {
        0% { transform: translateY(0) scale(1, 1); }
        50% { transform: translateY(-3px) scale(1.02, 0.98); }
        100% { transform: translateY(3px) scale(0.98, 1.02); }
    }

    /* タイヤの回転 */
    @keyframes spinWheels {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* 煙のアニメーション */
    @keyframes smoke {
        0% { opacity: 0.8; transform: scale(0.5) translate(0, 0); }
        100% { opacity: 0; transform: scale(2) translate(-20px, -30px); }
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
                <div class="wheel"></div>
                <div class="wheel"></div>
            </div>
        </div>
    </div>

</body>
</html>
"""

# HTMLを描画
components.html(html_code, height=450)

st.write("電車はCSSで作ってるから、画像ファイルはいらないよ！")
st.write("コードの中の `poyoPoyo` アニメーションの `steps(3)` が、カクカクしたコマ送りの可愛さを出してるポイントだっち🍄")
