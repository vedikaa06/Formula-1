import streamlit as st

# Expanded Team Palette
TEAM_COLORS = {
    'Ferrari': '#FF2800', 'Mercedes': '#00D2BE', 'Red Bull': '#0600EF',
    'McLaren': '#FF8700', 'Aston Martin': '#006F62', 'Alpine': '#0090FF',
    'Williams': '#005AFF', 'Haas': '#FFFFFF', 'RB': '#6692FF', 
    'Kick Sauber': '#52E252', 'Lotus': '#FFB800', 'Renault': '#FFF500',
    'Benetton': '#008855', 'Brawn': '#B3FD01', 'Tyrrell': '#0000FF'
}

def inject_base_css():
    """Injects Orbitron font, background watermark, and smooth transitions."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

    * { font-family: 'Orbitron', sans-serif; }

    .stApp {
        transition: background-color 0.8s ease-in-out;
        background-color: #000000;
        color: white;
    }

    /* Background Image Watermark */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: url('https://www.transparenttextures.com/patterns/carbon-fibre.png'); /* Fallback pattern */
        background-image: url('file/background.jpg'); 
        background-size: cover;
        background-position: center;
        opacity: 0.08;
        z-index: -1;
    }

    .f1-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 25px;
        border-left: 5px solid #E10600;
        transition: transform 0.3s ease;
    }
    .f1-card:hover { transform: translateY(-5px); background: rgba(255, 255, 255, 0.1); }
    </style>
    """, unsafe_allow_html=True)

def apply_dynamic_background(color_hex, opacity="22"):
    """Smoothly transitions the background color based on selection."""
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(135deg, #000000 65%, {color_hex}{opacity} 100%) !important;
    }}
    </style>
    """, unsafe_allow_html=True)

def get_score_color(score):
    """Returns color based on prediction probability."""
    if score >= 85: return "#00FF41" # Green
    if score >= 60: return "#FFD700" # Gold
    return "#E10600" # Red
