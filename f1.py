import streamlit as st
import pandas as pd
import os
from utility.utility import inject_base_css, apply_dynamic_background, TEAM_COLORS
from streamlit_option_menu import option_menu

st.set_page_config(page_title="F1 Velocity Hub", layout="wide")
inject_base_css()

if 'page' not in st.session_state:
    st.session_state.page = "Home"

@st.cache_data
def load_data():
    path = os.path.join('dataset', 'f1_master_dataset.csv')
    data = pd.read_csv(path)
    data.columns = data.columns.str.strip()
    return data

df = load_data()

with st.sidebar:
    selected = option_menu(
        "Velocity Hub", ["Home", "Hall of Fame", "Search Hub", "ML Predictor"],
        icons=['house', 'trophy', 'search', 'cpu'],
        menu_icon="speedometer2", 
        default_index=["Home", "Hall of Fame", "Search Hub", "ML Predictor"].index(st.session_state.page)
    )
    st.session_state.page = selected

# --- DYNAMIC NAVIGATION LOGIC ---

if st.session_state.page == "Home":
    st.markdown("<h1 style='text-align: center; color: #E10600; font-size: 50px;'>VELOCITY HUB</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; letter-spacing: 4px; color: #FFFFFF;'>70+ YEARS OF RACING DNA</p>", unsafe_allow_html=True)
    
    st.write("##")
    
    # Perfectly Aligned Navigation Grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="nav-card"><h2 style="color:#E10600">🏆</h2><h3>HALL OF FAME</h3><p style="font-size:12px">TOP 10 LEGENDS</p></div>', unsafe_allow_html=True)
        if st.button("GO TO HOF", use_container_width=True):
            st.session_state.page = "Hall of Fame"
            st.rerun()

    with col2:
        st.markdown('<div class="nav-card"><h2 style="color:#E10600">🔍</h2><h3>SEARCH HUB</h3><p style="font-size:12px">DRIVER ANALYSIS</p></div>', unsafe_allow_html=True)
        if st.button("GO TO SEARCH", use_container_width=True):
            st.session_state.page = "Search Hub"
            st.rerun()

    with col3:
        st.markdown('<div class="nav-card"><h2 style="color:#E10600">🤖</h2><h3>ML PREDICTOR</h3><p style="font-size:12px">AI SIMULATION</p></div>', unsafe_allow_html=True)
        if st.button("GO TO AI", use_container_width=True):
            st.session_state.page = "ML Predictor"
            st.rerun()

elif st.session_state.page == "Hall of Fame":
    apply_dynamic_background("#FFD700", "10") # Gold tint for HOF
    st.markdown("<h1 style='color: #E10600;'>🏆 THE PANTHEON</h1>", unsafe_allow_html=True)
    
    top_10 = df.groupby('driver_full_name').agg({'is_win': 'sum', 'points': 'sum'}).sort_values('is_win', ascending=False).head(10)
    st.dataframe(top_10, use_container_width=True)

elif st.session_state.page == "Search Hub":
    search_driver = st.selectbox("CHOOSE DRIVER", df['driver_full_name'].unique())
    d_data = df[df['driver_full_name'] == search_driver]
    team = d_data['team_name'].iloc[0]
    
    # Background color changes with selection
    team_color = TEAM_COLORS.get(team, "#E10600")
    apply_dynamic_background(team_color, "25")
    
    st.markdown(f"""
        <div class="f1-card" style="border-left: 10px solid {team_color};">
            <h1 style="margin:0;">{search_driver}</h1>
            <p style="color:{team_color}; font-weight:bold;">{team.upper()}</p>
        </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == "ML Predictor":
    st.markdown("<h1 style='color: #E10600;'>🤖 AI PREDICTOR</h1>", unsafe_allow_html=True)
    # Your prediction inputs...
