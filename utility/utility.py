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
    """Applies elite F1 styling with a faded background image."""
    bin_str = get_base64_image("image/background.jpg")
    bg_img_css = f"background-image: url('data:image/jpg;base64,{bin_str}');" if bin_str else ""

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&display=swap');

    /* Global Font and Base Theme */
    * {{ 
        font-family: 'Syncopate', sans-serif !important; 
        color: #FFFFFF; /* Ensures all writing is white for visibility */
    }}

    .stApp {{
        background-color: #000000;
        {bg_img_css}
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        transition: background-color 1.0s ease-in-out;
    }}

    /* Very Faded Watermark Layer */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.92); /* High opacity black to fade the image */
        z-index: -1;
    }}

    /* Content Cards: Glassmorphism ensures readability */
    .f1-card, .nav-card {{
        background: rgba(20, 20, 20, 0.85); /* Dark solid-ish background for text */
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 30px;
        backdrop-filter: blur(10px); /* Blurs background behind text for clarity */
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }}

    .nav-card:hover {{
        border-color: #E10600;
        background: rgba(40, 40, 40, 0.9);
        transform: translateY(-5px);
    }}
    
    /* Metrics and Tables styling for visibility */
    [data-testid="stMetricValue"] {{ color: #E10600 !important; }}
    .stTable {{ background-color: rgba(255,255,255,0.05); border-radius: 10px; }}

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
