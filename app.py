import streamlit as st

def main():
    # ページ設定（ブラウザのタブ名やアイコンなど）
    st.set_page_config(
        page_title="Relax Breath App",
        page_icon="🍄",
        layout="centered"
    )

    # カスタムCSSとHTMLを埋め込む
    # ぬるぬる動くアニメーション（グラデーション背景と呼吸する円）を定義
    st.markdown("""
        <style>
        /* 全体の背景設定：動くグラデーション */
        .stApp {
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
        }

        /* 背景グラデーションのアニメーション定義 */
        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* メインコンテナのデザイン */
        .main-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 50px;
            background: rgba(255, 255, 255, 0.2); /* ガラスのような半透明効果 */
            border-radius: 20px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            margin-top: 50px;
            text-align: center;
            color: white;
        }

        /* 呼吸する円のデザイン */
        .breathing-circle {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.8);
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
            margin: 30px auto;
            /* ここでぬるぬる動くアニメーションを適用 */
            animation: breathe 6s ease-in-out infinite; 
        }

        /* 円の拡大縮小アニメーション定義 */
        @keyframes breathe {
            0% { transform: scale(1); opacity: 0.8; }
            50% { transform: scale(1.5); opacity: 0.4; } /* 大きく吸う */
            100% { transform: scale(1); opacity: 0.8; } /* 吐く */
        }

        h1 {
            color: white;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            font-family: 'Helvetica Neue', sans-serif;
        }
        
        p {
            font-size: 1.2rem;
            font-weight: bold;
        }
        </style>

        <div class="main-container">
            <h1>Relax & Breathe</h1>
            <div class="breathing-circle"></div>
            <p>円に合わせて深呼吸してみてね</p>
        </div>
    """, unsafe_allow_html=True)

    # Streamlitの標準機能も下に追加可能
    st.write("") # スペース調整
    with st.expander("使い方を見る"):
        st.write("この円のアニメーションはCSSの @keyframes を使って作られています。")
        st.write("吸って... 吐いて... リラックスしましょう！")

if __name__ == "__main__":
    main()
