
import streamlit as st
import json
import time

# --- ページ設定 ---
st.set_page_config(
    page_title="Kawaii Fashion Recommender (100 Items)",
    page_icon="🎀",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- カスタムCSS ---
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #FFF0F5 0%, #FFE4E1 100%); font-family: 'Helvetica Neue', sans-serif; }
    h1, h2, h3 { color: #FF69B4 !important; text-shadow: 1px 1px 2px rgba(255,105,180,0.1); }
    [data-testid="stSidebar"] { background-color: #FFF5F7; border-right: 2px dashed #FFB6C1; }
    div.stButton > button:first-child { background: linear-gradient(45deg, #FF69B4, #FFB6C1); color: white; border-radius: 30px; border: none; padding: 10px 24px; font-size: 18px; font-weight: bold; width: 100%; transition: all 0.3s ease;}
    div.stButton > button:first-child:hover { transform: translateY(-2px); box-shadow: 0 6px 12px rgba(255, 105, 180, 0.4); }
    .rec-card { background-color: rgba(255, 255, 255, 0.95); padding: 25px; border-radius: 20px; box-shadow: 0 8px 16px rgba(255, 105, 180, 0.15); border: 2px solid #FFE4E1; margin-bottom: 25px; text-align: center; }
    .reason-box { background-color: #FFF0F5; padding: 15px; border-radius: 15px; margin-top: 15px; font-size: 0.95em; color: #555; border-left: 5px solid #FF69B4; text-align: left; line-height: 1.6; }
    .item-image { width: 100%; max-width: 280px; border-radius: 15px; margin-bottom: 15px; object-fit: cover; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    .tag { padding: 2px 8px; border-radius: 10px; font-size: 0.85em; font-weight: bold; }
    .kokkaku-tag { background-color: #FF69B4; color: white; }
    .color-tag { background-color: #FFB6C1; color: #A0522D; }
</style>
""", unsafe_allow_html=True)

# データベースの読み込み
@st.cache_data
def load_data():
    with open("clothes_db.json", "r", encoding="utf-8") as f:
        return json.load(f)

clothes_db = load_data()

st.markdown("<h1 style='text-align: center;'>🎀Style Recommender 🎀</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #D87093;'>運命の一着をご提案します✨</p>", unsafe_allow_html=True)

st.sidebar.header("🔍 あなたのプロフィール")
kokkaku = st.sidebar.selectbox("👗 骨格タイプ", ["ストレート", "ウェーブ", "ナチュラル"])
face_type = st.sidebar.selectbox("💄 顔タイプ", ["キュート", "フレッシュ", "フェミニン", "クール"])
personal_color = st.sidebar.selectbox("🎨 パーソナルカラー", ["イエベ春", "ブルベ夏", "イエベ秋", "ブルベ冬"])
scene = st.sidebar.selectbox("👜 どんなシーンで着る？", ["通学", "デート", "おでかけ"])

def recommend(k, f, p, s):
    scored = []
    for item in clothes_db:
        # 骨格フィルター（合わないものは弾く）
        if k not in item["kokkaku"]:
            continue
            
        # スコアリング
        is_color_match = p in item["color"]
        score = (10 if is_color_match else 0) + (2 if f in item["face"] else 0) + (1 if s in item["scene"] else 0)
        
        kokkaku_reason = item["reasons"][k]
        
        if is_color_match:
            color_reason = item["color_reasons"][p]
        else:
            color_reason = f"あえてパーソナルカラー({p})を外すことで、こなれ感を演出できるカラーです✨"
            
        general_reason = item["general_reason"].format(face=f, color=p, scene=s)
        
        full_reason = f"""
        <strong style="color:#FF69B4;">👗 シルエットの秘密:</strong><br><span class='tag kokkaku-tag'>{k}</span> {kokkaku_reason}<br><br>
        <strong style="color:#FF69B4;">🎨 カラーの秘密:</strong><br><span class='tag color-tag'>{p}</span> {color_reason}<br><br>
        <strong style="color:#FF69B4;">✨ さらなる魅力:</strong><br>{general_reason}
        """
        
        scored.append({"item": item, "score": score, "reason": full_reason})
        
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:3] 

if st.button("♡ 私に似合う服を診断する ♡"):
    with st.spinner("探しています...✨"):
        time.sleep(1.5)
    recs = recommend(kokkaku, face_type, personal_color, scene)
    
    st.markdown("<h2 style='text-align: center; margin-top: 20px;'>✨ あなたへのおすすめアイテム ✨</h2>", unsafe_allow_html=True)
    
    if len(recs) == 0:
        st.warning("ごめんなさい💦 現在の条件にぴったり合うアイテムが見つかりませんでした。")
    else:
        for rec in recs:
            item = rec["item"]
            st.markdown(f"""
            <div class="rec-card">
                <h3 style="color: #FF69B4; margin-bottom: 5px;">{item['name']}</h3>
                <p style="color: gray; font-size: 0.9em; margin-bottom: 15px;">カテゴリ: {item['type']} ｜ シーン: {scene}</p>
                <div class="reason-box">{rec['reason']}</div>
            </div>
            """, unsafe_allow_html=True)
            st.select_slider(f"この推薦はどうでしたか？ ({item['name']})", options=["イマイチ💦", "普通", "可愛い！💖", "絶対に買う！😍"], key=item['name'])
        st.balloons()
