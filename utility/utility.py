import streamlit as st
import base64
import os

TEAM_COLORS = {
    'Ferrari': '#FF2800', 'Mercedes': '#00D2BE', 'Red Bull': '#0600EF',
    'McLaren': '#FF8700', 'Aston Martin': '#006F62', 'Alpine': '#0090FF',
    'Williams': '#005AFF', 'Haas': '#FFFFFF', 'RB': '#6692FF', 
    'Kick Sauber': '#52E252', 'Lotus': '#FFB800', 'Renault': '#FFF500'
}

def get_base64_image(image_path):
    """Encodes the image to base64 for CSS injection."""
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def inject_base_css(is_home=False):
    """Applies F1 styling with adaptive text colors for visibility."""
    bin_str = get_base64_image("image/background.jpg")
    bg_img_css = f"background-image: url('data:image/jpg;base64,{bin_str}');" if bin_str and is_home else ""

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&display=swap');

    /* Global Font and Base Theme */
    * {{ 
        font-family: 'Syncopate', sans-serif !important; 
    }}

    .stApp {{
        background-color: #000000 !important;
        {bg_img_css}
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #FFFFFF; /* Default global text color */
    }}

    /* Specific fix for Input Widgets (Selectbox, Text Input, etc) */
    /* When background is white/light, text MUST be black */
    input, select, textarea, [data-testid="stSelectbox"] div {{
        color: #000000 !important; 
    }}
    
    label {{
        color: #FFFFFF !important; /* Keep labels white for dark background */
    }}

    /* Very Faded Watermark Layer */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.92);
        z-index: -1;
    }}

    /* Content Cards */
    .f1-card, .nav-card {{
        background: rgba(20, 20, 20, 0.85); 
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 30px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        color: #FFFFFF !important; /* Ensure card content stays white */
    }}

    /* Metrics and Tables */
    [data-testid="stMetricValue"] {{ color: #E10600 !important; }}
    
    /* Make Dataframe/Table text visible */
    .stTable, [data-testid="stTable"] {{ 
        color: #FFFFFF !important; 
        background-color: rgba(255,255,255,0.05); 
    }}

    </style>
    """, unsafe_allow_html=True)

def apply_dynamic_background(color_hex, opacity="15"):
    """Smoothly transitions the background glow based on team selection."""
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(135deg, #000000 60%, {color_hex}{opacity} 100%) !important;
        background-attachment: fixed !important;
    }}
    </style>
    """, unsafe_allow_html=True)
