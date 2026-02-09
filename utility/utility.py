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

def inject_base_css():
    """Applies elite F1 styling with strict black text for light backgrounds."""
    bin_str = get_base64_image("image/background.jpg")
    bg_img_css = f"background-image: url('data:image/jpg;base64,{bin_str}');" if bin_str else ""

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&display=swap');

    /* Global Font and Base Theme */
    * {{ 
        font-family: 'Syncopate', sans-serif !important; 
    }}

    /* Force all text elements to Black for visibility on white/light backgrounds */
    .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp span, .stApp label, .stApp div {{
        color: #000000 !important;
    }}

    .stApp {{
        background-color: #FFFFFF; /* Base is white */
        {bg_img_css}
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Adjusted Watermark Layer: White overlay to keep it light */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(255, 255, 255, 0.85); /* Light overlay for white theme */
        z-index: -1;
    }}

    /* Content Cards: Light background with black text */
    .f1-card, .nav-card {{
        background: rgba(245, 245, 245, 0.9); 
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 12px;
        padding: 30px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        color: #000000 !important;
    }}

    .nav-card:hover {{
        border-color: #E10600;
        background: rgba(230, 230, 230, 1.0);
        transform: translateY(-5px);
    }}
    
    /* Metrics and Tables */
    [data-testid="stMetricValue"] {{ color: #E10600 !important; }}
    .stTable {{ background-color: rgba(0,0,0,0.05); border-radius: 10px; color: #000000 !important; }}

    /* Fix for Sidebar visibility */
    [data-testid="stSidebar"] {{
        background-color: #F0F2F6 !important;
    }}
    [data-testid="stSidebar"] * {{
        color: #000000 !important;
    }}

    </style>
    """, unsafe_allow_html=True)

def apply_dynamic_background(color_hex, opacity="15"):
    """Smoothly transitions the background glow while maintaining black text."""
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(135deg, #FFFFFF 60%, {color_hex}{opacity} 100%) !important;
        background-attachment: fixed !important;
    }}
    /* Re-enforce black text after dynamic change */
    .stApp * {{
        color: #000000 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

def get_score_color(percentage):
    """Returns a color hex based on the win probability percentage."""
    if percentage > 75:
        return "#00FF41"  # F1 Green
    elif percentage > 50:
        return "#FFD700"  # Gold
    elif percentage > 25:
        return "#FF8700"  # McLaren Orange
    else:
        return "#E10600"  # F1 Red
