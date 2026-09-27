import streamlit as st
import time

st.set_page_config(
    page_title="Forge AI - Bias Detector",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Editorial Spectrum Background
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: 
            radial-gradient(ellipse at 10% 25%, rgba(239, 68, 68, 0.12) 0%, transparent 45%),
            radial-gradient(ellipse at 90% 75%, rgba(59, 130, 246, 0.12) 0%, transparent 45%),
            radial-gradient(circle at 50% 50%, rgba(16, 185, 129, 0.08) 0%, transparent 50%),
            linear-gradient(180deg, #0f172a 0%, #020617 100%);
        background-attachment: fixed;
    }

    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
        background-size: 80px 80px;
        pointer-events: none;
        z-index: 0;
    }

    [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0);
    }

    @keyframes antiGravityFloat {
        0% { transform: translateY(0px) rotateX(0deg); }
        50% { transform: translateY(-12px) rotateX(2deg); }
        100% { transform: translateY(0px) rotateX(0deg); }
    }

    @keyframes pulseGlow {
        0% { box-shadow: 0 10px 30px -10px rgba(79, 70, 229, 0.4); }
        50% { box-shadow: 0 20px 45px rgba(6, 182, 212, 0.6); }
        100% { box-shadow: 0 10px 30px -10px rgba(79, 70, 229, 0.4); }
    }

    .quote-box-3d {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.02) 100%);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-left: 6px solid #6366f1;
        border-radius: 20px;
        padding: 24px 28px;
        margin-bottom: 32px;
        font-size: 1.3rem;
        font-weight: 500;
        color: #f1f5f9;
        line-height: 1.6;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
        animation: antiGravityFloat 7s ease-in-out infinite;
    }

    .hero-title-3d {
        font-size: 4.4rem;
        font-weight: 900;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 40%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 12px;
        line-height: 1.1;
    }

    .hero-sub-3d {
        font-size: 1.45rem;
        color: #94a3b8;
        margin-bottom: 36px;
        line-height: 1.6;
    }

    .badge-3d {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(6, 182, 212, 0.2) 100%);
        border: 1px solid rgba(165, 180, 252, 0.4);
        color: #38bdf8;
        padding: 8px 22px;
        border-radius: 30px;
        font-size: 1rem;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 20px;
    }

    div.stButton > button[kind="primary"] {
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        padding: 18px 36px !important;
        border-radius: 20px !important;
        background: linear-gradient(135deg, #6366f1 0%, #06b6d4 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        color: #ffffff !important;
        animation: pulseGlow 4s infinite ease-in-out;
        transition: all 0.3s ease !important;
    }

    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-6px) scale(1.04) !important;
    }

    .section-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #f8fafc;
        margin-top: 24px;
        margin-bottom: 8px;
    }

    .section-subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        margin-bottom: 28px;
    }

    .carousel-stage {
        perspective: 1200px;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 380px;
        position: relative;
        margin: 20px 0 40px 0;
    }

    .carousel-card {
        position: absolute;
        width: 360px;
        padding: 32px;
        border-radius: 24px;
        backdrop-filter: blur(20px);
        transition: all 0.8s cubic-bezier(0.25, 1, 0.5, 1);
    }

    .card-pos-0 {
        transform: translateX(0px) translateZ(100px) scale(1.05);
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(99, 102, 241, 0.6);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.8), 0 0 30px rgba(99, 102, 241, 0.3);
        opacity: 1;
        z-index: 3;
    }

    .card-pos-1 {
        transform: translateX(-240px) translateZ(-120px) rotateY(18deg) scale(0.85);
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        opacity: 0.45;
        z-index: 1;
        filter: blur(4px);
    }

    .card-pos-2 {
        transform: translateX(240px) translateZ(-120px) rotateY(-18deg) scale(0.85);
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        opacity: 0.45;
        z-index: 1;
        filter: blur(4px);
    }

    .card-icon-3d { font-size: 3rem; margin-bottom: 16px; }
    .card-title-3d { font-size: 1.5rem; font-weight: 800; color: #f8fafc; margin-bottom: 10px; }
    .card-text-3d { color: #cbd5e1; font-size: 1.05rem; line-height: 1.6; }

    .dot-container { display: flex; justify-content: center; gap: 10px; margin-bottom: 20px; }
    .dot { width: 12px; height: 12px; border-radius: 50%; background-color: rgba(255, 255, 255, 0.2); }
    .dot-active { background-color: #6366f1; width: 28px; border-radius: 12px; }
    </style>
""", unsafe_allow_html=True)

# Quote Box
st.markdown("""
    <div class="quote-box-3d">
        <i>"In the world where information is weaponized and stories are sold rather than told, 
        uncovering objective reality is no longer just a luxury—it is the ultimate shield for a free mind."</i>
    </div>
""", unsafe_allow_html=True)

st.markdown('<span class="badge-3d">✨ Intelligent Media Intelligence</span>', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title-3d">AI Media Bias Detector</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub-3d">Analyze news articles, uncover subtle political leanings, spot loaded language, and generate objective reframes in real-time.</p>', unsafe_allow_html=True)

col_btn, _ = st.columns([1.3, 2.7])
with col_btn:
    if st.button("🚀 Analyze News", type="primary", use_container_width=True):
        st.switch_page("pages/1_Main_App.py")

st.write("##")
st.divider()

# Core Intelligence Modules
st.markdown('<h2 class="section-title">Core Intelligence Modules</h2>', unsafe_allow_html=True)
st.markdown('<p class="section-subtitle">3D real-time analytical pipeline running on Gemini AI.</p>', unsafe_allow_html=True)

if "carousel_step" not in st.session_state:
    st.session_state.carousel_step = 0

cards_data = [
    {"icon": "📊", "title": "Spectrum Analysis", "text": "Evaluates left, right, or neutral leanings along with clear objectivity percentage metrics."},
    {"icon": "🔍", "title": "Framing & Tone", "text": "Detects emotionally charged phrases, sensationalized headlines, and opinionated rhetoric."},
    {"icon": "🔄", "title": "Neutral Reframe", "text": "Converts biased coverage into balanced, matter-of-fact journalistic text automatically."}
]

step = st.session_state.carousel_step
pos_0 = (0 - step) % 3
pos_1 = (1 - step) % 3
pos_2 = (2 - step) % 3

st.markdown(f"""
    <div class="carousel-stage">
        <div class="carousel-card card-pos-{pos_0}">
            <div class="card-icon-3d">{cards_data[0]['icon']}</div>
            <div class="card-title-3d">{cards_data[0]['title']}</div>
            <div class="card-text-3d">{cards_data[0]['text']}</div>
        </div>
        <div class="carousel-card card-pos-{pos_1}">
            <div class="card-icon-3d">{cards_data[1]['icon']}</div>
            <div class="card-title-3d">{cards_data[1]['title']}</div>
            <div class="card-text-3d">{cards_data[1]['text']}</div>
        </div>
        <div class="carousel-card card-pos-{pos_2}">
            <div class="card-icon-3d">{cards_data[2]['icon']}</div>
            <div class="card-title-3d">{cards_data[2]['title']}</div>
            <div class="card-text-3d">{cards_data[2]['text']}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

dots_html = '<div class="dot-container">'
for i in range(3):
    dots_html += f'<div class="dot {"dot-active" if i == (step % 3) else ""}"></div>'
dots_html += '</div>'
st.markdown(dots_html, unsafe_allow_html=True)

st.divider()

# Interactive Spectrum Gauge
st.markdown('<h2 class="section-title">Live Interactive Spectrum Visualizer</h2>', unsafe_allow_html=True)
st.markdown('<p class="section-subtitle">Select a headline framing or test your own text to see the pointer shift in real time.</p>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "🔴 Left-Leaning Framing", 
    "🟢 Neutral Framing", 
    "🔵 Right-Leaning Framing",
    "🧪 Test Custom Text"
])

def render_gauge(percentage, lean_text, color_code):
    st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 24px; text-align: center; margin-bottom: 20px;">
            <div style="font-size: 1rem; color: #94a3b8; margin-bottom: 8px;">CALCULATED BIAS POINTER</div>
            <div style="height: 18px; width: 100%; background: linear-gradient(90deg, #ef4444 0%, #10b981 50%, #3b82f6 100%); border-radius: 10px; position: relative; margin: 20px 0;">
                <div style="position: absolute; top: -6px; left: calc({percentage}% - 10px); width: 20px; height: 30px; background: #ffffff; border: 3px solid {color_code}; border-radius: 6px; box-shadow: 0 0 15px {color_code}; transition: all 0.5s ease;"></div>
            </div>
            <div style="font-size: 1.4rem; font-weight: 800; color: {color_code};">{lean_text} ({percentage}%)</div>
        </div>
    """, unsafe_allow_html=True)

with tab1:
    render_gauge(18, "Left-Leaning Framing Detected", "#ef4444")
    st.info('**Sample Headline:** "Radical Policy Shifts Proposed to Dismantle Corporate Privileges"')

with tab2:
    render_gauge(50, "Balanced & Objective Stance", "#10b981")
    st.success('**Sample Headline:** "Legislators Introduce Bill Modifying Existing Corporate Tax Structures"')

with tab3:
    render_gauge(84, "Right-Leaning Framing Detected", "#3b82f6")
    st.info('**Sample Headline:** "Heavy-Handed Government Regulations Threaten Business Innovation"')

with tab4:
    custom_text = st.text_input("Enter a news phrase or headline to simulate:", placeholder="e.g. Unprecedented economic growth sweeping the region...")
    if custom_text:
        text_len = len(custom_text)
        calc_perc = (text_len * 7) % 100
        if calc_perc < 35:
            render_gauge(calc_perc, "Left Spectrum Score", "#ef4444")
        elif calc_perc <= 65:
            render_gauge(calc_perc, "Neutral Spectrum Score", "#10b981")
        else:
            render_gauge(calc_perc, "Right Spectrum Score", "#3b82f6")
    else:
        render_gauge(50, "Awaiting Input...", "#94a3b8")

# Timer to rotate cards
time.sleep(3.5)
st.session_state.carousel_step = (st.session_state.carousel_step + 1) % 3
st.rerun()