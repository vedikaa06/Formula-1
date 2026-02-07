import streamlit as st
import pandas as pd
import os
from utility.design import inject_base_css, apply_dynamic_background, TEAM_COLORS, get_score_color
from streamlit_option_menu import option_menu

st.set_page_config(page_title="F1 Velocity Hub", layout="wide")

# 1. Load Data
@st.cache_data
def load_data():
    path = os.path.join('datase', 'f1_master_dataset.csv')
    return pd.read_csv(path)

df = load_data()
inject_base_css() # Inject the core black/white/red theme

# 2. Sidebar Navigation
with st.sidebar:
    selected = option_menu(
        "Velocity Hub", ["Home", "Hall of Fame", "Search Hub", "ML Predictor"],
        icons=['house', 'trophy', 'search', 'cpu'],
        menu_icon="speedometer2", default_index=0,
        styles={"nav-link-selected": {"background-color": "#E10600"}}
    )

# 3. Dynamic Section Logic
if selected == "Home":
    st.markdown("<h1 style='color: #E10600; font-size: 60px;'>VELOCITY HUB</h1>", unsafe_allow_html=True)
    st.write("### Decoding 70+ Years of Racing DNA")
    # Home background remains pure black

elif selected == "Hall of Fame":
    apply_dynamic_background("#333333", "11") # Subtle charcoal differentiation
    st.header("🏆 The Pantheon of Speed")
    # Add your charts here...

elif selected == "Search Hub":
    driver = st.selectbox("Select Driver", df['driver_full_name'].unique())
    team = df[df['driver_full_name'] == driver]['team_name'].iloc[0]
    
    # DYNAMIC BACKGROUND CHANGE
    team_color = TEAM_COLORS.get(team, "#E10600")
    apply_dynamic_background(team_color, "44") # The whole app morphs to team color
    
    st.markdown(f"""
        <div class="f1-card" style="border-left: 10px solid {team_color};">
            <h1>{driver}</h1>
            <h3 style="color: {team_color};">{team}</h3>
        </div>
    """, unsafe_allow_html=True)

elif selected == "ML Predictor":
    st.header("🤖 AI Performance Predictor")
    if st.button("Calculate Probability"):
        score = 88.5 # Example result from your model
        result_color = get_score_color(score)
        
        # DYNAMIC BACKGROUND CHANGE BASED ON SCORE
        apply_dynamic_background(result_color, "33")
        
        st.markdown(f"""
            <div style="text-align: center;">
                <h2 style="color: {result_color}; font-size: 80px;">{score}%</h2>
                <p>WIN PROBABILITY INDEX</p>
            </div>
        """, unsafe_allow_html=True)