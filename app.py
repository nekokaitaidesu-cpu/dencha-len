import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="ぽよぽよ電車だっち", layout="wide")

# タイトル
st.title("🚂 手描き風レンガ橋と、きらめく水面だっち 🍄")
st.write("手描きイラストの雰囲気に合わせて、レンガの質感と水面のきらめきをCSSで作り込んだよ！")

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
        position: relative;
        overflow: hidden;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        display: flex;
        justify-content: center;
        align-items: center;
        /* 背景は空と水面をレイヤーで表現 */
        background-color: #87CEEB; /* 空のベース色 */
    }

    /* --- 背景レイヤー（空と水面） --- */
    /* 空のグラデーション（少し温かい色味に） */
    .scene::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 70%; /* 空の高さ */
        background: linear-gradient(to bottom, #87CEEB 0%, #E0F7FA 80%, #FFFACD 100%);
        z-index: 1;
    }

    /* 水面（きらめく波模様） */
    .scene::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 30%; /* 水面の高さ */
        background: 
            /* キラキラ反射 */
            radial-gradient(circle at 50% 50%, rgba(255,255,255,0.6) 0%, transparent 10%),
            radial-gradient(circle at 20% 30%, rgba(255,255,255,0.5) 0%, transparent 8%),
            radial-gradient(circle at 80% 70%, rgba(255,255,255,0.5) 0%, transparent 8%),
            /* 波模様 */
            repeating-linear-gradient(45deg, rgba(255,255,255,0.2) 0px, rgba(255,255,255,0.2) 2px, transparent 2px, transparent 10px),
            /* 水のベースグラデーション */
            linear-gradient(to bottom, #40a4df 0%, #0077be 100%);
        background-size: 
            100px 100px, /* キラキラのサイズ */
            80px 80px,
            120px 120px,
            20px 20px,   /* 波のサイズ */
            100% 100%;
        background-repeat: repeat;
        animation: wave 5s linear infinite; /* 波を動かす */
        z-index: 1;
    }

    /* 雲（背景装飾） */
    .cloud {
        position: absolute;
        top: 80px;
        background: rgba(255, 255, 255, 0.95); /* 少し濃く */
        border-radius: 50px;
        animation: moveClouds 35s linear infinite;
        z-index: 2; /* 空より前 */
        box-shadow: 4px 4px 0px rgba(0,0,0,0.05); /* 手描き風の影 */
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

    /* --- 橋（手描き風レンガ） --- */
    .bridge {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 200%;
        height: 280px; /* 接地基準 */
        z-index: 5;
        
        /* 手描きレンガの表現
           複数のグラデーションを重ねて、不規則なレンガ模様を作る
        */
        background-color: #A0522D; /* ベースの茶色 */
        background-image: 
            /* アーチの穴（透明） */
            radial-gradient(circle at bottom center, transparent 60%, rgba(160, 82, 45, 0) 60.5%),
            /* レンガ模様レイヤー1（濃い茶色の不規則な矩形） */
            linear-gradient(to right, rgba(93, 64, 55, 0.6) 0%, rgba(93, 64, 55, 0.6) 40%, transparent 40%, transparent 100%),
            /* レンガ模様レイヤー2（少しずらして配置） */
            linear-gradient(to right, transparent 0%, transparent 50%, rgba(93, 64, 55, 0.5) 50%, rgba(93, 64, 55, 0.5) 90%, transparent 90%),
            /* レンガの目地（横線） */
            linear-gradient(to bottom, rgba(62, 39, 35, 0.4) 2px, transparent 2px);
            
        /* サイズと位置をランダムに設定 */
        background-size: 
            200px 280px, /* アーチ */
            60px 25px,   /* レンガ1 */
            70px 30px,   /* レンガ2 */
            100% 25px;   /* 目地 */
            
        background-position: 
            bottom left,
            0 0,
            30px 12px,
            0 0;
            
        background-repeat: repeat-x, repeat, repeat, repeat;
        
        animation: scrollBridge 3s linear infinite;
        box-shadow: inset 0 -10px 20px rgba(0,0,0,0.2); /* 橋の下に影を落とす */
    }

    /* 橋の上部（路盤・手すり部分） */
    .bridge::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 18px;
        background: #5D4037; /* 濃い茶色 */
        border-bottom: 5px solid #3E2723;
        border-radius: 2px;
    }
    
    /* 橋の縁取り（手描き風） */
    .bridge::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        /* アーチの縁取り */
        background-image: radial-gradient(circle at bottom center, transparent 59%, #3E2723 60%, transparent 62%);
        background-size: 200px 280px;
        background-repeat: repeat-x;
        background-position: bottom left;
        opacity: 0.7;
    }

    /* --- 電車コンテナ（変更なし） --- */
    .train-container {
        position: absolute;
        bottom: 280px;
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
        box-shadow: 1px 1px 0px rgba(0,0,0,0.2); /* タイヤにも影 */
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
    @keyframes wave {
        0% { background-position: 0 0, 0 0, 0 0, 0 0, 0 0; }
        100% { background-position: -50px 20px, -40px 30px, -60px 10px, 100px 0, 0 0; }
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

st.write("レンガの積み重なりや、水面のキラキラ感が伝わるかな？🍄")
