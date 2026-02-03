import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="ぽよぽよ電車だっち", layout="wide")

# タイトル
st.title("🚂 レンガの橋をゆく、豆粒電車だっち 🍄")
st.write("手描きイラストみたいに、レンガ造りのアーチ橋の上を走るようにしたよ！橋の下には川も流れてるだっち！")

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
        /* 空と水面のグラデーション：下30%を水の色にしたよ */
        background: linear-gradient(to bottom, #87CEEB 0%, #E0F7FA 70%, #40a4df 70%, #0077be 100%);
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

    /* --- 橋（デザイン変更） --- */
    .bridge {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 200%;
        height: 280px; /* 接地基準 */
        z-index: 5;
        
        /* 背景を3層重ねてレンガ橋を表現！
           1. アーチの穴（透明にして背景の水を見せる）
           2. レンガの横線（薄い黒線）
           3. 橋のベース色（赤茶色）
        */
        background-color: #A0522D; /* ベースの茶色（Sienna） */
        background-image: 
            /* 層1: アーチ（下中央に円形の透明部分を作る） */
            radial-gradient(circle at bottom center, transparent 60%, #A0522D 60.5%),
            /* 層2: レンガ風の横縞模様 */
            linear-gradient(to bottom, rgba(0,0,0,0.1) 2px, transparent 2px);
            
        /* サイズ設定 */
        background-size: 
            200px 280px, /* アーチの間隔 */
            100% 20px;   /* レンガの線の間隔 */
            
        background-repeat: repeat-x, repeat;
        background-position: bottom left;
        
        animation: scrollBridge 3s linear infinite;
    }

    /* 橋の上部（路盤・手すり部分） */
    .bridge::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 15px;
        background: #5D4037; /* 濃い茶色 */
        border-bottom: 4px solid #3E2723;
    }
    
    /* 橋のレンガの縦線（アクセント）- 擬似要素で簡易的に追加 */
    .bridge::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        /* 破線でレンガの縦目地を表現 */
        background-image: linear-gradient(90deg, rgba(0,0,0,0.05) 2px, transparent 2px);
        background-size: 40px 100%;
        pointer-events: none;
    }

    /* --- 電車コンテナ（変更なし） --- */
    .train-container {
        position: absolute;
        bottom: 280px; /* 橋の高さに合わせる */
        width: 54px;
        height: 40px;
        z-index: 10;
        transform-origin: bottom center;
        animation: poyoPoyo 0.5s steps(3) infinite alternate;
    }

    /* 電車のボディ（変更なし） */
    .train-body {
        width: 100%;
        height: 28px;
        background-color: #4DB6AC;
        border-radius: 6px;
        border: 2px solid #004D40;
        position: absolute;
        bottom: 4.5px; 
        left: 0;
        display: flex;
        justify-content: space-evenly;
        align-items: center;
        box-shadow: 2px 2px 0px rgba(0,0,0,0.2);
        box-sizing: border-box;
        z-index: 2;
    }

    /* 屋根 */
    .train-body::before {
        content: '';
        position: absolute;
        top: -5px;
        left: 2px;
        width: 46px;
        height: 5px;
        background-color: #004D40;
        border-radius: 3px 3px 0 0;
    }

    /* 窓（3つ） */
    .window {
        width: 8px;
        height: 8px;
        background-color: #FFF9C4;
        border: 1px solid #004D40;
        border-radius: 2px;
    }

    /* タイヤコンテナ */
    .wheels-container {
        position: absolute;
        bottom: 0;
        width: 100%;
        height: 9px;
        display: flex;
        justify-content: space-between;
        padding: 0 8px;
        box-sizing: border-box;
        z-index: 1;
    }

    /* タイヤ */
    .wheel {
        width: 9px;
        height: 9px;
        background-color: #FFC107;
        border: 1.5px solid #FF6F00;
        border-radius: 50%;
    }
    
    /* 煙 */
    .smoke {
        position: absolute;
        top: -15px;
        right: 5px;
        width: 10px;
        height: 10px;
        background: white;
        border-radius: 50%;
        opacity: 0;
        animation: smoke 1s ease-out infinite;
        z-index: 0;
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
        50% { transform: translateY(0.5px) scale(1.03, 0.97); }
        100% { transform: translateY(-0.5px) scale(0.98, 1.02); }
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
            <div class="wheels-container">
                <div class="wheel"></div>
                <div class="wheel"></div>
            </div>
            <div class="train-body">
                <div class="window"></div>
                <div class="window"></div>
                <div class="window"></div>
            </div>
        </div>
    </div>

</body>
</html>
"""

# HTMLを描画
components.html(html_code, height=600)

st.write("橋の下から水面が見えて、いい景色になっただっち🍄")
