import streamlit as st
import pandas as pd
import os
from utility.utility import inject_base_css, apply_dynamic_background, TEAM_COLORS, get_score_color
from utility.ml_model import get_ml_prediction 
from streamlit_option_menu import option_menu

st.set_page_config(page_title="F1 Velocity Hub", layout="wide")

# Force CSS injection based on the current page
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# Logic: is_home is True only when page is "Home"
inject_base_css(is_home=(st.session_state.page == "Home"))

@st.cache_data
def load_data():
    path = os.path.join('dataset', 'f1_master_dataset.csv')
    if os.path.exists(path):
        data = pd.read_csv(path)
        data.columns = data.columns.str.strip()
        return data
    return pd.DataFrame()

df = load_data()

# --- SIDEBAR SYNC ---
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
    st.markdown("<p style='text-align: center; letter-spacing: 4px;'>70+ YEARS OF RACING DNA</p>", unsafe_allow_html=True)
    
    st.write("##")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="nav-card"><h2 style="color:#E10600">🏆</h2><h3>HALL OF FAME</h3></div>', unsafe_allow_html=True)
        if st.button("GO TO HOF", use_container_width=True):
            st.session_state.page = "Hall of Fame"
            st.rerun()

    with col2:
        st.markdown('<div class="nav-card"><h2 style="color:#E10600">🔍</h2><h3>SEARCH HUB</h3></div>', unsafe_allow_html=True)
        if st.button("GO TO SEARCH", use_container_width=True):
            st.session_state.page = "Search Hub"
            st.rerun()

    with col3:
        st.markdown('<div class="nav-card"><h2 style="color:#E10600">🤖</h2><h3>ML PREDICTOR</h3></div>', unsafe_allow_html=True)
        if st.button("GO TO AI", use_container_width=True):
            st.session_state.page = "ML Predictor"
            st.rerun()

elif st.session_state.page == "Hall of Fame":
    apply_dynamic_background("#FFD700", "15") 
    st.markdown("<h1 style='color: #E10600;'>🏆 THE PANTHEON</h1>", unsafe_allow_html=True)
    
    top_10 = df.groupby('driver_full_name').agg({'is_win': 'sum', 'points': 'sum'}).sort_values('is_win', ascending=False).head(10)
    st.dataframe(top_10, use_container_width=True)

elif st.session_state.page == "Search Hub":
    search_driver = st.selectbox("CHOOSE DRIVER", df['driver_full_name'].unique())
    d_data = df[df['driver_full_name'] == search_driver]
    
    team = d_data['team_name'].iloc[0]
    team_color = TEAM_COLORS.get(team, "#E10600")
    apply_dynamic_background(team_color, "25")
    
    st.markdown(f"""
        <div class="f1-card" style="border-left: 10px solid {team_color};">
            <h1 style="margin:0; color: white;">{search_driver}</h1>
            <p style="color:{team_color}; font-weight:bold;">{team.upper()}</p>
        </div>
    """, unsafe_allow_html=True)
    # Add your stats metrics here (Nationality, DOB, etc.)

elif st.session_state.page == "ML Predictor":
    st.header("🤖 AI WIN PREDICTOR")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        p_driver = st.selectbox("SELECT DRIVER", df['driver_full_name'].unique())
    with col_b:
        p_team = st.selectbox("SELECT TEAM", df['team_name'].unique())
    with col_c:
        p_circuit = st.selectbox("SELECT CIRCUIT", df['circuit_name'].unique())

    if st.button("CALCULATE WIN PERCENTAGE"):
        with st.spinner('Training AI...'):
            win_percentage, model_accuracy = get_ml_prediction(df, p_team, p_driver, p_circuit)
            
            res_color = get_score_color(win_percentage)
            apply_dynamic_background(res_color, "25")
            
            st.markdown(f"""
                <div class="f1-card" style="text-align: center; border-bottom: 5px solid {res_color};">
                    <h2 style="color: white;">WIN PROBABILITY</h2>
                    <h1 style="color: {res_color}; font-size: 80px;">{win_percentage}%</h1>
                    <p style="color: #00FF41; font-weight: bold; font-size: 20px;">MODEL ACCURACY: {model_accuracy}%</p>
                </div>
            """, unsafe_allow_html=True)
