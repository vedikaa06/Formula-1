import streamlit as st
import base64

# Team Palette
TEAM_COLORS = {
    'Ferrari': '#FF2800', 'Mercedes': '#00D2BE', 'Red Bull': '#0600EF',
    'McLaren': '#FF8700', 'Aston Martin': '#006F62', 'Alpine': '#0090FF',
    'Williams': '#005AFF', 'Haas': '#FFFFFF', 'RB': '#6692FF', 
    'Kick Sauber': '#52E252', 'Lotus': '#FFB800', 'Renault': '#FFF500'
}

def get_base64(bin_file):
    """Encodes a local file to base64 for CSS injection."""
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

def inject_base_css():
    """Injects Orbitron font and base64 background image watermark."""
    img_b64 = get_base64("background.jpg")
    bg_style = f"background-image: url('data:image/jpg;base64,{img_b64}');" if img_b64 else ""

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    * {{ font-family: 'Orbitron', sans-serif !important; }}

    .stApp {{
        transition: background-color 0.8s ease-in-out;
        background-color: #000000;
        {bg_style}
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }}
    
    /* Watermark Effect Overlay */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.85); 
        z-index: -1;
    }}

    .f1-card {{
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 20px;
        border-left: 5px solid #E10600;
        margin-bottom: 15px;
    }}
    </style>
    """, unsafe_allow_html=True)

def apply_dynamic_background(color_hex, opacity="22"):
    st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(135deg, #000000 65%, {color_hex}{opacity} 100%) !important; }}
    </style>
    """, unsafe_allow_html=True)

def get_score_color(score):
    if score >= 85: return "#00FF41"
    if score >= 60: return "#FFD700"
    return "#E10600"
