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
    """Encodes the image to base64 so CSS can display it."""
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def inject_base_css():
    """Applies elite F1 styling and encodes the background image."""
    # Ensure this path matches your folder structure: 'image/background.jpg'
    bin_str = get_base64_image("image/background.jpg")
    bg_img_css = f"background-image: url('data:image/jpg;base64,{bin_str}');" if bin_str else ""

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&display=swap');

    * {{ font-family: 'Syncopate', sans-serif !important; }}

    .stApp {{
        {bg_img_css}
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        transition: background-color 0.8s ease-in-out;
    }}

    /* The 'Watermark' Effect Overlay */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.88); /* Adjust for image visibility */
        z-index: -1;
    }}

    /* Home Page Navigation Cards */
    .nav-card {{
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 30px;
        text-align: center;
        transition: all 0.4s ease;
        cursor: pointer;
        height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }}
    .nav-card:hover {{
        background: rgba(255, 255, 255, 0.1);
        border-color: #E10600;
        transform: translateY(-10px);
        box-shadow: 0 10px 30px rgba(225, 6, 0, 0.2);
    }}
    </style>
    """, unsafe_allow_html=True)

def apply_dynamic_background(color_hex, opacity="22"):
    st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(135deg, #000000 70%, {color_hex}{opacity} 100%) !important; }}
    </style>
    """, unsafe_allow_html=True)

def get_score_color(score):
    if score >= 85: return "#00FF41"
    if score >= 60: return "#FFD700"
    return "#E10600"
