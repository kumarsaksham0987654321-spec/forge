import streamlit as st
import time
from bias_analyzer import analyze_news_bias

st.set_page_config(
    page_title="Forge AI - Bias Analyzer",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Shared Editorial Wireframe & Dual Political Spectrum Background (Matches Home Page)
st.markdown("""
    <style>
    /* Editorial Wireframe & Dual Political Spectrum Ambient Background */
    [data-testid="stAppViewContainer"] {
        background: 
            radial-gradient(ellipse at 10% 25%, rgba(239, 68, 68, 0.12) 0%, transparent 45%),
            radial-gradient(ellipse at 90% 75%, rgba(59, 130, 246, 0.12) 0%, transparent 45%),
            radial-gradient(circle at 50% 50%, rgba(16, 185, 129, 0.08) 0%, transparent 50%),
            linear-gradient(180deg, #0f172a 0%, #020617 100%);
        background-attachment: fixed;
    }

    /* Column Grid Layer Evoking Newspaper Layout & Press Wires */
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

    /* Keyframe Animations */
    @keyframes antiGravityFloat {
        0% { transform: translateY(0px) rotateX(0deg); }
        50% { transform: translateY(-8px) rotateX(1deg); }
        100% { transform: translateY(0px) rotateX(0deg); }
    }

    @keyframes pulseGlow {
        0% { box-shadow: 0 10px 30px -10px rgba(79, 70, 229, 0.4); }
        50% { box-shadow: 0 20px 45px rgba(6, 182, 212, 0.6); }
        100% { box-shadow: 0 10px 30px -10px rgba(79, 70, 229, 0.4); }
    }

    /* Typography & Headers */
    .app-title {
        font-size: 3.8rem;
        font-weight: 900;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 40%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
        line-height: 1.1;
    }

    .app-subtitle {
        font-size: 1.25rem;
        color: #94a3b8;
        margin-bottom: 28px;
    }

    /* 3D Glassmorphic Input Slab */
    .input-container-3d {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 24px;
        padding: 28px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), inset 0 1px 1px rgba(255, 255, 255, 0.2);
        margin-bottom: 32px;
        animation: antiGravityFloat 8s ease-in-out infinite;
    }

    /* Custom Text Area Styling */
    .stTextArea textarea {
        background: rgba(15, 23, 42, 0.7) !important;
        color: #f8fafc !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        padding: 18px !important;
        font-size: 1.05rem !important;
        transition: all 0.3s ease !important;
    }
    .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.4) !important;
    }

    /* Primary Analyze Button with 3D Glow */
    div.stButton > button[kind="primary"] {
        font-size: 1.2rem !important;
        font-weight: 800 !important;
        padding: 16px 32px !important;
        border-radius: 16px !important;
        background: linear-gradient(135deg, #6366f1 0%, #06b6d4 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        color: #ffffff !important;
        animation: pulseGlow 4s infinite ease-in-out;
        transition: all 0.3s ease !important;
    }

    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-4px) scale(1.03) !important;
    }

    /* Back Navigation Button */
    div.stButton > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #cbd5e1 !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background: rgba(255, 255, 255, 0.12) !important;
        color: #ffffff !important;
    }

    /* Glass Metric Cards */
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%) !important;
        backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        padding: 20px !important;
        border-radius: 20px !important;
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.4) !important;
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        color: #f8fafc !important;
    }

    /* Custom Result Box Styles */
    .result-card-3d {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 20px;
        padding: 24px;
        margin-top: 12px;
        color: #e2e8f0;
        font-size: 1.05rem;
        line-height: 1.6;
    }

    .loaded-badge {
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid rgba(239, 68, 68, 0.4);
        color: #fca5a5;
        padding: 8px 16px;
        border-radius: 12px;
        margin-bottom: 10px;
        display: inline-block;
        font-weight: 600;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Top Bar Navigation
col_nav, _ = st.columns([1, 4])
with col_nav:
    if st.button("← Back to Home", type="secondary"):
        st.switch_page("Home.py")

# Title & Subtitle Header
st.markdown('<h1 class="app-title">📰 News Bias Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="app-subtitle">Paste any article text or headline below to generate an instant 3D political spectrum evaluation.</p>', unsafe_allow_html=True)

# Main Input Slab Container
st.markdown('<div class="input-container-3d">', unsafe_allow_html=True)
article_text = st.text_area(
    "Article Text or Headline",
    placeholder="Paste news text or raw transcript here...",
    height=200
)

col_btn, _ = st.columns([1.3, 2.7])
with col_btn:
    analyze_btn = st.button("🚀 Analyze Bias", type="primary", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Analysis Execution Logic
if analyze_btn:
    if not article_text.strip():
        st.warning("Please paste an article text or headline first.")
    else:
        with st.spinner("Analyzing news framing, political leanings, and speech patterns..."):
            progress_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.005)
                progress_bar.progress(percent_complete + 1)

            try:
                # Call core logic from bias_analyzer.py
                results = analyze_news_bias(article_text)
                progress_bar.empty()

                st.success("Analysis Complete!")
                st.write("##")

                # Metrics Dashboard Grid
                st.markdown('<h3 style="color: #f8fafc; font-weight: 800; margin-bottom: 16px;">Analytical Summary</h3>', unsafe_allow_html=True)
                m1, m2, m3 = st.columns(3)

                m1.metric(
                    label="Political Lean",
                    value=results.get("lean", "Neutral"),
                    delta=results.get("bias_score", "0%")
                )
                m2.metric(
                    label="Objectivity Rating",
                    value=results.get("objectivity", "85%")
                )
                m3.metric(
                    label="Sensationalism Level",
                    value=results.get("sensationalism", "Low")
                )

                st.write("##")

                # Detailed Findings Tabs
                tab1, tab2, tab3 = st.tabs([
                    "📌 Summary Breakdown", 
                    "🚩 Loaded Language", 
                    "🔄 Objective Reframe"
                ])

                with tab1:
                    st.markdown(f'''
                        <div class="result-card-3d">
                            {results.get("summary", "No summary available.")}
                        </div>
                    ''', unsafe_allow_html=True)

                with tab2:
                    phrases = results.get("loaded_words", ["None detected."])
                    for phrase in phrases:
                        st.markdown(f'<div class="loaded-badge">⚠️ {phrase}</div>', unsafe_allow_html=True)

                with tab3:
                    st.markdown(f'''
                        <div class="result-card-3d" style="border-color: rgba(16, 185, 129, 0.4);">
                            <span style="color: #34d399; font-weight: 700;">Neutral Restatement:</span><br><br>
                            {results.get("reframe", "Original text maintains an objective stance.")}
                        </div>
                    ''', unsafe_allow_html=True)

            except Exception as e:
                progress_bar.empty()
                st.error(f"Error running analysis: {str(e)}")
import streamlit as st
import sys
import os

# Ensure root folder is in python path to import bias_analyzer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from bias_analyzer import analyze_news_bias

st.set_page_config(page_title="News Bias Detector - Forge AI", layout="wide")

st.title("Forge AI — News Bias Detector")
st.write("Analyze political bias, sensationalism, and framing from news image clippings, URLs, or raw text using Gemini OCR.")

# Input Mode Selector
input_option = st.radio("Select Input Source:", ["Image Upload (Free OCR)", "URL Link", "Raw Text"], horizontal=True)

image_file = None
url_input = ""
text_input = ""

if input_option == "Image Upload (Free OCR)":
    image_file = st.file_uploader("Upload news clipping or article screenshot", type=["png", "jpg", "jpeg", "webp"])
    if image_file:
        st.image(image_file, caption="Uploaded Screenshot", use_container_width=True)

elif input_option == "URL Link":
    url_input = st.text_input("Enter News Article URL:", placeholder="https://www.example.com/article")

else:
    text_input = st.text_area("Paste News Text:", height=200)

if st.button("Analyze Bias", type="primary"):
    if not image_file and not url_input and not text_input:
        st.warning("Please provide an image, URL, or text before running analysis.")
    else:
        with st.spinner("Processing OCR & evaluating bias with Gemini..."):
            try:
                if image_file:
                    bytes_data = image_file.getvalue()
                    mime_type = image_file.type
                    result = analyze_news_bias(image_bytes=bytes_data, image_mime=mime_type)
                elif url_input:
                    result = analyze_news_bias(url=url_input)
                else:
                    result = analyze_news_bias(text_content=text_input)

                st.success("Analysis Completed!")
                st.divider()

                # Results Dashboard
                col1, col2, col3 = st.columns(3)
                col1.metric("Bias Rating", f"{result.bias_score} / 100", result.bias_label)
                col2.metric("Sensationalism Level", f"{result.sensationalism_score}%")
                col3.metric("Input Source", result.input_type.upper())

                st.subheader("Objective Summary")
                st.write(result.objective_summary)

                st.subheader("Framing & Logical Fallacies")
                for item in result.key_fallacies_or_framing:
                    st.markdown(f"- {item}")

                with st.expander("View Extracted / Analyzed Text"):
                    st.write(result.extracted_text)

            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")