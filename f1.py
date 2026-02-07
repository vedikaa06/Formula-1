import streamlit as st
import pandas as pd
import os
from utility.utility import inject_base_css, apply_dynamic_background, TEAM_COLORS, get_score_color
from streamlit_option_menu import option_menu

st.set_page_config(page_title="F1 Velocity Hub", layout="wide")
inject_base_css()

@st.cache_data
def load_data():
    path = os.path.join('datase', 'f1_master_dataset.csv')
    if os.path.exists(path):
        data = pd.read_csv(path)
        # SAFETY FIX: Remove any hidden spaces from column names
        data.columns = data.columns.str.strip() 
        return data
    return pd.DataFrame()

df = load_data()

# Check if required column exists to avoid crash
if 'driver_full_name' not in df.columns:
    st.error(f"Column 'driver_full_name' not found. Available columns: {list(df.columns)}")
    st.stop()

with st.sidebar:
    selected = option_menu(
        "Velocity Hub", ["Home", "Hall of Fame", "Search Hub", "ML Predictor"],
        icons=['house', 'trophy', 'search', 'cpu'],
        menu_icon="speedometer2", default_index=0,
        styles={"nav-link-selected": {"background-color": "#E10600"}}
    )

if selected == "Home":
    st.markdown("<h1 style='color: #E10600; font-size: 60px;'>VELOCITY HUB</h1>", unsafe_allow_html=True)
    st.write("### DECODING 70+ YEARS OF RACING DNA")

elif selected == "Hall of Fame":
    apply_dynamic_background("#FFD700", "15") 
    st.header("🏆 The All-Time Top 10")
    top_10 = df.groupby('driver_full_name').agg({
        'is_win': 'sum',
        'points': 'sum'
    }).sort_values('is_win', ascending=False).head(10)
    st.table(top_10)

elif selected == "Search Hub":
    driver = st.selectbox("Select Driver", df['driver_full_name'].unique())
    d_data = df[df['driver_full_name'] == driver]
    team = d_data['team_name'].iloc[0] if 'team_name' in d_data.columns else "Unknown"
    apply_dynamic_background(TEAM_COLORS.get(team, "#E10600"), "44")
    st.title(driver)

elif selected == "ML Predictor":
    st.header("🤖 AI Strategy Engine")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        p_driver = st.selectbox("Select Driver", df['driver_full_name'].unique())
    with col_b:
        p_team = st.selectbox("Select Team", list(TEAM_COLORS.keys()))
    with col_c:
        p_circuit = st.selectbox("Select Circuit", df['circuit_name'].unique() if 'circuit_name' in df.columns else ["Monaco"])
    
    if st.button("PREDICT SCORE"):
        score = 85.0
        apply_dynamic_background(get_score_color(score), "33")
        st.success(f"Win Probability: {score}%")
