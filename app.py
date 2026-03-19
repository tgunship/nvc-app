# Copyright © 2026 Takeshi Uchida

import streamlit as st
import random

# --- アプリ全体の背景色と基本デザインの設定 ---
st.markdown("""
    <style>
    /* 画面全体の背景色を柔らかなアイボリーに */
    .stApp {
        background-color: #FDFBF7;
    }
    /* st.infoボックスのデザイン調整（背景をさらに薄い青に） */
    .stAlert {
        background-color: #F8FBFF;
        border: 1px solid #E6F0FA;
        color: #333333;
    }
    /* Streamlitデフォルトの不要な上下余白を削って1画面に収める */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. ニーズリスト ---
DEFAULT_NEEDS = [
    "共感", "受容", "理解", "尊重", "思いやり", 
    "信頼", "所属", "愛", "感謝", "親密さ", 
    "つながり", "支え・協力", "相互性", "循環", "豊かさ",
    "自由・選択", "自律", "空間・間", "自発性", "自分に本物であること", 
    "言行一致・誠実さ", "自己表現", "意味・目的", "貢献", "成長", 
    "探求・発見", "創造性", "内なる力", "効力感・達成", "明確さ",
    "嘆き・悼み", "インスピレーション・直感", "平和・調和", "ただ在ること", "流れ・フロー", 
    "秩序", "平等・公平", "美", "身体の安全", "安心", 
    "休息", "心身の滋養", "ふれあい", "活力・いのちの躍動", "希望", 
    "安らげる居場所", "遊び・気軽さ", "喜び", "祝福", "挑戦・刺激"
]

st.title("🎯 ニーズ アハ！")
# タイトルの直下に小さくバージョン情報を表示
st.markdown("<div style='font-size: 14px; color: #888888; margin-top: -15px; margin-bottom: 10px;'>1枚ずつ版 Ver1.00</div>", unsafe_allow_html=True)

# --- 2. 初期設定（リセット時もここを通る） ---
if 'candidates' not in st.session_state:
    st.session_state.candidates = DEFAULT_NEEDS.copy()
    random.shuffle(st.session_state.candidates) # 最初だけランダム
    st.session_state.kept = []
    st.session_state.current_index = 0
    st.session_state.round_count = 1
    st.session_state.finished = False
    st.session_state.final_need = ""

# --- 3. 判定ロジック（表示の前に計算を行う） ---

# もし「今のラウンド」が終了していたら（インデックスがリスト数を超えたら）
if st.session_state.current_index >= len(st.session_state.candidates) and not st.session_state.finished:
    
    # Keepが1つに絞られたら終了
    if len(st.session_state.kept) == 1:
        st.session_state.final_need = st.session_state.kept[0]
        st.session_state.finished = True
        st.rerun() # 画面を更新して結果表示へ
        
    # Keepが0個になってしまったら救済措置
    elif len(st.session_state.kept) == 0:
        st.warning("すべて「これじゃない」になってしまいました。リストを戻してやり直します。")
        st.session_state.current_index = 0
        st.rerun()
        
    # まだ複数あるなら次のラウンドへ
    else:
        st.session_state.candidates = st.session_state.kept.copy() # Keepしたものを次の候補に
        st.session_state.kept = [] # Keep箱を空にする
        st.session_state.current_index = 0 # 0番目に戻す
        st.session_state.round_count += 1
        st.rerun() # 画面を更新して次のラウンドへ

# --- 4. 画面表示（結果発表 または 選択画面） ---

if st.session_state.finished:
    # === 結果画面 ===
    st.balloons() # お祝いのエフェクト
    
    # メッセージ
    st.markdown("<h2 style='text-align: center; color: #D35400;'>アハ！ 見つかりましたね！</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; color: #666666;'>今のあなたの心のど真ん中にある、一番大切にしたいニーズは...</p>", unsafe_allow_html=True)
    
    # 結果を強調する特別なカードデザイン
    st.markdown(
        f"""
        <div style="
            padding: 50px 20px; 
            background: linear-gradient(135deg, #FFF0D1 0%, #FFDCA8 100%); 
            border: 2px solid #FFC266;
            border-radius: 20px; 
            text-align: center; 
            box-shadow: 0 8px 15px rgba(211, 84, 0, 0.15);
            margin: 30px 0;">
            <h1 style="color: #C0392B; margin:0; font-size: 48px; text-shadow: 1px 1px 2px rgba(255,255,255,0.8);">
                {st.session_state.final_need}
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if st.button("もう一度、心に問いかける", use_container_width=True):
        # セッション状態をクリアしてリセット
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

else:
    # === 選択画面 ===
    # 現在のニーズを取得
    current_need = st.session_state.candidates[st.session_state.current_index]
    
    # 進捗情報
    total = len(st.session_state.candidates)
    
    st.info("""
    💡 **最終的に「これだ！」という1つのニーズに絞り込んでいきます。**
    
    表示されるカードを見て、直感でピンときたら「**キープ！**」、違うなと思ったら「**これじゃない**」を選んで進めてください。
    """)
    st.write(f"ラウンド{st.session_state.round_count}: 現在 **{total} 個**の候補があります。")
    
    # 進捗バー
    st.progress(st.session_state.current_index / total)

    # カード表示（不要なコメント文字列を削除）
    st.markdown(
        f"""
        <div style="
            padding: 25px; 
            background-color: #FFFFFF; 
            border: 2px solid #E2DCD0;
            border-radius: 15px; 
            text-align: center; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            margin: 15px 0;"> 
            <h2 style="color: #4A4A4A; margin:0; font-size: 32px;">{current_need}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ボタンエリア
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("これじゃない", key="drop", use_container_width=True):
            st.session_state.current_index += 1
            st.rerun()

    with col2:
        if st.button("キープ！", key="keep", type="primary", use_container_width=True):
            st.session_state.kept.append(current_need)
            st.session_state.current_index += 1
            st.rerun()

# --- 5. コピーライト表示（フッター） ---
st.markdown(
    """
    <style>
    /* インスタリンク用の控えめなスタイル */
    .insta-link {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        color: #999999;
        text-decoration: none;
        font-size: 14px;
        transition: color 0.3s ease;
        margin-bottom: 4px;
    }
    .insta-link:hover {
        color: #666666;
    }
    </style>
    
    <div style="text-align: center; padding-top: 25px; padding-bottom: 0px;"> 
        <div>
            <a href="https://www.instagram.com/kokochi1205/" target="_blank" rel="noopener noreferrer" class="insta-link">
                <svg style="width: 18px; height: 18px; fill: currentColor;" viewBox="0 0 24 24" aria-hidden="true">
                    <path fill-rule="evenodd" d="M12.315 2c2.43 0 2.784.013 3.808.06 1.064.049 1.791.218 2.427.465a4.902 4.902 0 011.772 1.153 4.902 4.902 0 011.153 1.772c.247.636.416 1.363.465 2.427.048 1.067.06 1.407.06 4.123v.08c0 2.643-.012 2.987-.06 4.043-.049 1.064-.218 1.791-.465 2.427a4.902 4.902 0 01-1.153 1.772 4.902 4.902 0 01-1.772 1.153c-.636.247-1.363.416-2.427.465-1.067.048-1.407.06-4.123.06h-.08c-2.643 0-2.987-.012-4.043-.06-1.064-.049-1.791-.218-2.427-.465a4.902 4.902 0 01-1.772-1.153 4.902 4.902 0 01-1.153-1.772c-.247-.636-.416 1.363-.465-2.427-.047-1.024-.06-1.379-.06-3.808v-.63c0-2.43.013-2.784.06-3.808.049-1.064.218-1.791.465-2.427a4.902 4.902 0 011.153-1.772A4.902 4.902 0 015.45 2.525c.636-.247 1.363-.416 2.427-.465C8.901 2.013 9.256 2 11.685 2h.63zm-.081 1.802h-.468c-2.456 0-2.784.011-3.807.058-.975.045-1.504.207-1.857.344-.467.182-.8.398-1.15.748-.35.35-.566.683-.748 1.15-.137.353-.3.882-.344 1.857-.047 1.023-.058 1.351-.058 3.807v.468c0 2.456.011 2.784.058 3.807.045.975.207 1.504.344 1.857.182.466.399.8.748 1.15.35.35.683.566 1.15.748.353.137.882.3 1.857.344 1.054.048 1.37.058 4.041.058h.08c2.597 0 2.917-.01 3.96-.058.976-.045 1.505-.207 1.858-.344.466-.182.8-.398 1.15-.748.35-.35.566-.683.748-1.15.137-.353.3-.882.344-1.857.048-1.055.058-1.37.058-4.041v-.08c0-2.597-.01-2.917-.058-3.96-.045-.976-.207-1.505-.344-1.858a3.097 3.097 0 00-.748-1.15 3.098 3.098 0 00-1.15-.748c-.353-.137-.882-.3-1.857-.344-1.023-.047-1.351-.058-3.807-.058zM12 6.865a5.135 5.135 0 110 10.27 5.135 5.135 0 010-10.27zm0 1.802a3.333 3.333 0 100 6.666 3.333 3.333 0 000-6.666zm5.338-3.205a1.2 1.2 0 110 2.4 1.2 1.2 0 010-2.4z" clip-rule="evenodd" />
                </svg>
                自分をみつめる空間『ここち』インスタ
            </a>
        </div>
        <div style="color: #999999; font-size: 14px;">
            Copyright © 2026 Takeshi Uchida
        </div>
    </div>
    """, 
    unsafe_allow_html=True
)
