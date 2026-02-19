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
    /* st.infoボックスのデザイン調整 */
    .stAlert {
        background-color: #E8F4FD;
        border: 1px solid #D0E6FC;
        color: #333;
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
st.markdown("<div style='font-size: 14px; color: #888888; margin-top: -15px; margin-bottom: 20px;'>1枚ずつ版 Ver1.00</div>", unsafe_allow_html=True)

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
    
    # 画像を参考に、ラウンド情報とインストラクションを追加
    st.write(f"ラウンド{st.session_state.round_count}: 残り {total} 個の候補")
    
    st.info("""
    💡 **最終的に「これだ！」という1つのニーズに絞り込んでいきます。**
    
    表示されるカードを見て、直感でピンときたら「**キープ！**」、違うなと思ったら「**これじゃない**」を選んで進めてください。
    """)
    
    # 進捗バー
    st.progress(st.session_state.current_index / total)

    # カード表示
    st.markdown(
        f"""
        <div style="
            padding: 40px; 
            background-color: #FFFFFF; 
            border: 2px solid #E2DCD0;
            border-radius: 15px; 
            text-align: center; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            margin: 20px 0;">
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
    <div style="text-align: center; padding-top: 50px; color: #999999; font-size: 14px;">
        Copyright &copy; 2026 Takeshi Uchida
    </div>
    """, 
    unsafe_allow_html=True
)

