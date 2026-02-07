import streamlit as st
import pandas as pd
import os
from utility.unility import inject_base_css, apply_dynamic_background, TEAM_COLORS, get_score_color
from streamlit_option_menu import option_menu

st.set_page_config(page_title="F1 Velocity Hub", layout="wide")
inject_base_css()

# 1. Load and Clean Data
@st.cache_data
def load_data():
    path = os.path.join('dataset', 'f1_master_dataset.csv')
    if os.path.exists(path):
        data = pd.read_csv(path)
        # Fix for KeyError: Strips hidden spaces from headers
        data.columns = data.columns.str.strip() 
        return data
    return pd.DataFrame()

df = load_data()

# Check for data presence
if df.empty:
    st.error("Dataset not found or empty. Please check the 'datase' folder.")
    st.stop()

# 2. Navigation
with st.sidebar:
    selected = option_menu(
        "Velocity Hub", ["Home", "Hall of Fame", "Search Hub", "ML Predictor"],
        icons=['house', 'trophy', 'search', 'cpu'],
        menu_icon="speedometer2", default_index=0,
        styles={"nav-link-selected": {"background-color": "#E10600"}}
    )

# 3. Page Logic
if selected == "Home":
    st.markdown("<h1 style='color: #E10600; font-size: 60px;'>VELOCITY HUB</h1>", unsafe_allow_html=True)
    st.write("### DECODING 70+ YEARS OF RACING DNA")
    
    st.markdown("#### Navigation")
    c1, c2, c3 = st.columns(3)
    with c1: st.info("🏆 **Hall of Fame**: View top 10 legends.")
    with c2: st.info("🔍 **Search Hub**: Explore driver history.")
    with c3: st.info("🤖 **ML Predictor**: Build your dream team.")

elif selected == "Hall of Fame":
    apply_dynamic_background("#FFD700", "15") 
    st.header("🏆 The All-Time Top 10")
    
    # Aggregating top 10 drivers
    top_10 = df.groupby('driver_full_name').agg({
        'is_win': 'sum',
        'points': 'sum'
    }).sort_values('is_win', ascending=False).head(10)
    
    st.table(top_10)

elif selected == "Search Hub":
    driver = st.selectbox("Select Driver", df['driver_full_name'].unique())
    d_data = df[df['driver_full_name'] == driver]
    
    team = d_data['team_name'].iloc[0] if 'team_name' in d_data.columns else "N/A"
    apply_dynamic_background(TEAM_COLORS.get(team, "#E10600"), "44")
    
    st.title(driver)
    st.write(f"**Career History:** {', '.join(d_data['team_name'].unique())}")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Race Wins", int(d_data['is_win'].sum()))
    col2.metric("Podiums", int(d_data['is_podium'].sum()) if 'is_podium' in df.columns else "N/A")
    col3.metric("Career Points", int(d_data['points'].sum()))

elif selected == "ML Predictor":
    st.header("🤖 AI Strategy Engine")
    
    cola, colb, colc = st.columns(3)
    with cola: p_driver = st.selectbox("Select Driver", df['driver_full_name'].unique())
    with colb: p_team = st.selectbox("Select Team", list(TEAM_COLORS.keys()))
    with colc: p_circuit = st.selectbox("Select Circuit", df['circuit_name'].unique() if 'circuit_name' in df.columns else ["Monaco"])

    if st.button("PREDICT SCORE"):
        score = 85.0 # Simulated probability
        apply_dynamic_background(get_score_color(score), "33")
        st.success(f"Calculated Performance Index: {score}%")
