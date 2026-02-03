import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="ぽよぽよ電車だっち", layout="wide")

# タイトル
st.title("🚂 果てしない世界と、豆粒電車だっち 🍄")
st.write("電車がさらに小さくなって、タイヤも消えたよ！広大な景色を楽しんでね！")

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
        height: 550px; /* 高さをさらに広げた */
        background: linear-gradient(to bottom, #87CEEB 0%, #E0F7FA 70%, #f0e68c 100%);
        position: relative;
        overflow: hidden;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* 雲（背景装飾）- もっとゆっくり広大に */
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

    /* 橋（さらに巨大化） */
    .bridge {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 200%;
        height: 280px; /* 橋をすごく高く */
        background-color: #8B4513;
        /* アーチも巨大化 */
        background-image: radial-gradient(circle at bottom center, transparent 65%, #A0522D 66%);
        background-size: 200px 200px; /* アーチのサイズ特大 */
        background-repeat: repeat-x;
        background-position: bottom;
        animation: scrollBridge 3s linear infinite; /* ゆっくり雄大に */
    }
    
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

    /* --- 電車（さらに極小サイズに変更） --- */
    .train-container {
        position: absolute;
        bottom: 290px; /* 巨大な橋の上に配置 */
        width: 60px;  /* 幅をさらに小さく */
        height: 40px; /* 高さをさらに小さく */
        z-index: 10;
        /* ぽよぽよアニメーションは継続 */
        animation: poyoPoyo 0.6s steps(3) infinite alternate;
    }

    /* 電車のボディ（極小用調整） */
    .train-body {
        width: 100%;
        height: 75%; /* タイヤがない分、少し高さを確保 */
        background-color: #4DB6AC;
        border-radius: 8px;
        border: 2px solid #004D40; /* 線をさらに細く */
        position: relative;
        display: flex;
        justify-content: space-around;
        align-items: center;
        box-shadow: 2px 2px 0px rgba(0,0,0,0.2);
    }

    /* 屋根（極小用調整） */
    .train-body::before {
        content: '';
        position: absolute;
        top: -6px;
        left: 4px;
        width: 52px;
        height: 6px;
        background-color: #004D40;
        border-radius: 3px 3px 0 0;
    }

    /* 窓（極小用調整） */
    .window {
        width: 12px;
        height: 12px;
        background-color: #FFF9C4;
        border: 1px solid #004D40; /* 極細 */
        border-radius: 3px;
    }

    /* タイヤと連結棒のコンテナを削除しました */

    /* 煙（極小用調整） */
    .smoke {
        position: absolute;
        top: -10px;
        right: 5px;
        width: 10px;
        height: 10px;
        background: white;
        border-radius: 50%;
        opacity: 0;
        animation: smoke 1s ease-out infinite;
    }

    /* --- アニメーション定義 --- */

    @keyframes scrollBridge {
        0% { transform: translateX(0); }
        100% { transform: translateX(-200px); } /* 巨大アーチに合わせて調整 */
    }

    @keyframes moveClouds {
        0% { transform: translateX(130%); }
        100% { transform: translateX(-200%); }
    }

    @keyframes poyoPoyo {
        0% { transform: translateY(0) scale(1, 1); }
        50% { transform: translateY(-2px) scale(1.03, 0.97); }
        100% { transform: translateY(2px) scale(0.97, 1.03); }
    }
    
    /* タイヤのアニメーションは未使用 */

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
                <div class="window"></div>
            </div>
            </div>
    </div>

</body>
</html>
"""

# HTMLを描画（高さをさらに大きく確保）
components.html(html_code, height=600)

st.write("ちっちゃすぎて見失わないように気をつけてね！🍄")
