import streamlit as st
import pandas as pd
import os
from utility.utility import inject_base_css, apply_dynamic_background, TEAM_COLORS, get_score_color
from streamlit_option_menu import option_menu

st.set_page_config(page_title="F1 Velocity Hub", layout="wide")
inject_base_css()

# 1. Load Data
@st.cache_data
def load_data():
    path = os.path.join('datase', 'f1_master_dataset.csv')
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

df = load_data()

# 2. Navigation
with st.sidebar:
    selected = option_menu(
        "Velocity Hub", ["Home", "Hall of Fame", "Search Hub", "ML Predictor"],
        icons=['house', 'trophy', 'search', 'cpu'],
        menu_icon="speedometer2", default_index=0,
        styles={"nav-link-selected": {"background-color": "#E10600"}}
    )

# 3. Pages
if selected == "Home":
    st.markdown("<h1 style='color: #E10600; font-size: 60px;'>VELOCITY HUB</h1>", unsafe_allow_html=True)
    st.write("### DECODING 70+ YEARS OF RACING DNA")
    
    st.markdown("---")
    st.subheader("Explore the Paddock")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="f1-card">🏆 <b>Hall of Fame</b><br>Analyze the top 10 drivers in history.</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="f1-card">🔍 <b>Search Hub</b><br>Deep dive into career stats and wins.</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="f1-card">🤖 <b>ML Predictor</b><br>Build your own team & predict results.</div>', unsafe_allow_html=True)

elif selected == "Hall of Fame":
    apply_dynamic_background("#FFD700", "15") 
    st.header("🏆 The All-Time Top 10")
    
    # Calculate Top 10 based on Wins
    top_10 = df.groupby('driver_full_name').agg({
        'is_win': 'sum',
        'team_name': lambda x: x.iloc[-1], # Last known team
        'points': 'sum'
    }).sort_values('is_win', ascending=False).head(10)
    
    st.table(top_10)

elif selected == "Search Hub":
    driver = st.selectbox("Select Driver", df['driver_full_name'].unique())
    d_data = df[df['driver_full_name'] == driver]
    
    # Dynamic transition to team color
    team = d_data['team_name'].iloc[0]
    apply_dynamic_background(TEAM_COLORS.get(team, "#E10600"), "44")
    
    st.markdown(f'<div class="f1-card"><h1>{driver}</h1><h3>Driven for: {", ".join(d_data["team_name"].unique())}</h3></div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Race Wins", int(d_data['is_win'].sum()))
    c2.metric("Sprint Wins", "Data N/A") # Place holder if sprint column exists
    c3.metric("Career Points", int(d_data['points'].sum()))

elif selected == "ML Predictor":
    st.header("🤖 AI Strategy Engine")
    st.write("Build a custom combination to predict Win Probability.")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        p_driver = st.selectbox("Select Driver", df['driver_full_name'].unique())
    with col_b:
        p_team = st.selectbox("Select Team", TEAM_COLORS.keys())
    with col_c:
        p_circuit = st.selectbox("Select Circuit", df['circuit_name'].unique() if 'circuit_name' in df.columns else ["Monaco", "Silverstone", "Monza"])

    if st.button("PREDICT PERFORMANCE SCORE"):
        # Simulated prediction logic
        score = 82.5 
        res_color = get_score_color(score)
        apply_dynamic_background(res_color, "44") # Background morphs to result color
        
        st.markdown(f"""
            <div style="text-align: center; padding: 50px;">
                <h2 style="color: {res_color}; font-size: 80px;">{score}%</h2>
                <p>PROBABILITY OF DOMINANCE</p>
            </div>
        """, unsafe_allow_html=True)
