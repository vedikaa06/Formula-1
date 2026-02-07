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
    """Sets the core theme: Black, White, Red with smooth transitions."""
    st.markdown("""
    <style>
    /* Smooth global transitions for background changes */
    .stApp {
        transition: background-color 0.8s ease-in-out, color 0.5s ease;
        background-color: #000000;
        color: white;
    }

    /* Section-specific background tones */
    .section-home { background: #000000; }
    .section-hof { background: #0a0a0a; border-top: 1px solid #333; }
    
    /* Premium Card Design */
    .f1-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    .f1-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.1);
        border-color: #E10600;
    }

    /* Watermark */
    .watermark {
        position: fixed; top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        font-size: 25vw; font-weight: 900;
        color: rgba(255, 255, 255, 0.02);
        z-index: -1; pointer-events: none;
    }
    </style>
    <div class="watermark">F1</div>
    """, unsafe_allow_html=True)

def apply_dynamic_background(color_hex, opacity="22"):
    """Injects a style override for the current page state."""
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(135deg, #000000 60%, {color_hex}{opacity} 100%) !important;
    }}
    </style>
    """, unsafe_allow_html=True)

def get_score_color(score):
    """Dynamic coloring for the ML Predictor."""
    if score >= 85: return "#00FF41" # Elite Green
    if score >= 60: return "#FFD700" # Solid Gold
    return "#E10600" # High Risk Red
