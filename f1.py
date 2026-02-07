import streamlit as st
import pandas as pd
import os
from utility.utility import inject_base_css, apply_dynamic_background, TEAM_COLORS, get_score_color
from streamlit_option_menu import option_menu

st.set_page_config(page_title="F1 Velocity Hub", layout="wide")
inject_base_css()

# Initialize session state for navigation if not exists
if 'page' not in st.session_state:
    st.session_state.page = "Home"

@st.cache_data
def load_data():
    # Cleaning column names during load to prevent KeyErrors
    path = os.path.join('dataset', 'f1_master_dataset.csv')
    data = pd.read_csv(path)
    data.columns = data.columns.str.strip()
    return data

df = load_data()

# Sidebar Sync
with st.sidebar:
    selected = option_menu(
        "Velocity Hub", ["Home", "Hall of Fame", "Search Hub", "ML Predictor"],
        icons=['house', 'trophy', 'search', 'cpu'],
        menu_icon="speedometer2", 
        # Set default index based on the session state page
        default_index=["Home", "Hall of Fame", "Search Hub", "ML Predictor"].index(st.session_state.page)
    )
    st.session_state.page = selected

# --- PAGES ---

if st.session_state.page == "Home":
    st.markdown("<h1 style='text-align: center; color: #E10600; margin-top: 50px;'>VELOCITY HUB</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; letter-spacing: 5px;'>DECODING 70+ YEARS OF RACING DNA</p>", unsafe_allow_html=True)
    
    st.write("##")
    
    # Perfectly Aligned Navigation Grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="nav-card"><h3>🏆</h3><p>HALL OF FAME</p></div>', unsafe_allow_html=True)
        if st.button("ENTER HOF", use_container_width=True):
            st.session_state.page = "Hall of Fame"
            st.rerun()

    with col2:
        st.markdown('<div class="nav-card"><h3>🔍</h3><p>SEARCH HUB</p></div>', unsafe_allow_html=True)
        if st.button("ENTER SEARCH", use_container_width=True):
            st.session_state.page = "Search Hub"
            st.rerun()

    with col3:
        st.markdown('<div class="nav-card"><h3>🤖</h3><p>ML PREDICTOR</p></div>', unsafe_allow_html=True)
        if st.button("ENTER PREDICTOR", use_container_width=True):
            st.session_state.page = "ML Predictor"
            st.rerun()

elif st.session_state.page == "Hall of Fame":
    apply_dynamic_background("#FFD700", "15")
    st.title("🏆 Hall of Fame")
    # Top 10 Logic
    top_10 = df.groupby('driver_full_name').agg({'is_win': 'sum', 'points': 'sum'}).sort_values('is_win', ascending=False).head(10)
    st.table(top_10)

elif st.session_state.page == "Search Hub":
    driver = st.selectbox("Select Driver", df['driver_full_name'].unique())
    d_data = df[df['driver_full_name'] == driver]
    team = d_data['team_name'].iloc[0]
    apply_dynamic_background(TEAM_COLORS.get(team, "#E10600"), "44")
    st.title(driver)
    # Add your stats cards here...

elif st.session_state.page == "ML Predictor":
    st.header("🤖 AI Strategy Engine")
    # Custom Team Building UI
    c_d = st.selectbox("Select Driver", df['driver_full_name'].unique())
    c_t = st.selectbox("Select Team", list(TEAM_COLORS.keys()))
    c_c = st.selectbox("Select Circuit", df['circuit_name'].unique())
    
    if st.button("PREDICT WIN PROBABILITY"):
        score = 87.2
        apply_dynamic_background(get_score_color(score), "33")
        st.success(f"Chance of Dominance: {score}%")
