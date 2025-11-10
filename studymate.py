import streamlit as st
from datetime import datetime
import requests
import time

# ---- StudyMate Function using FREE HF API with fallback ----
def ask_studymate(topic, mode="explain"):
    """
    Uses multiple FREE AI models with automatic fallback
    """
    if not topic.strip():
        return "Please enter a valid topic."
    
    # Shorter, clearer prompts
    prompt_map = {
        "explain": f"Explain {topic}:",
        "simplify": f"Explain {topic} simply:",
        "examples": f"3 examples of {topic}:",
        "quiz": f"Quiz on {topic}:",
    }

    prompt = prompt_map.get(mode, prompt_map["explain"])
    
    # Try multiple FREE models in order
    models = [
        "gpt2",
        "facebook/opt-350m",
        "EleutherAI/gpt-neo-125m"
    ]
    
    for model in models:
        API_URL = f"https://api-inference.huggingface.co/models/{model}"
        
        try:
            response = requests.post(
                API_URL,
                headers={"Content-Type": "application/json"},
                json={
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": 100,
                        "temperature": 0.7,
                        "do_sample": True,
                        "return_full_text": False
                    },
                    "options": {
                        "wait_for_model": True,
                        "use_cache": True
                    }
                },
                timeout=45
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, list) and len(data) > 0:
                    result = data[0].get("generated_text", "")
                    
                    if result.startswith(prompt):
                        result = result[len(prompt):].strip()
                    
                    if result:
                        return result
            
            # Try next model if this one failed
            continue
                
        except Exception:
            continue
    
    # All models failed
    return "AI models are busy. Please try again in a moment."


# ---- Streamlit Configuration ----
st.set_page_config(
    page_title="StudyMate",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---- Better CSS - High Contrast ----
st.markdown("""
    <style>
    .stApp {
        background-color: #F5F5F5;
    }
    
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
    }
    
    /* FIXED: High contrast button */
    .stButton > button {
        background-color: #FF6B35 !important;
        color: white !important;
        font-weight: bold !important;
        border: 3px solid #FF6B35 !important;
        padding: 0.75rem 2rem !important;
        border-radius: 10px !important;
        font-size: 18px !important;
        width: 100% !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
    }
    
    .stButton > button:hover {
        background-color: #E55A2B !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.4) !important;
        transform: scale(1.05);
    }
    
    /* FIXED: Readable selectbox */
    .stSelectbox label {
        font-size: 16px !important;
        font-weight: 600 !important;
        color: #1F618D !important;
    }
    
    /* Selectbox options visibility */
    div[data-baseweb="select"] > div {
        background-color: white !important;
        border: 2px solid #1F618D !important;
    }
    
    h1 { color: #1F618D; }
    h2 { color: #1F618D; }
    h3 { color: #117A65; }
    p { color: #2C3E50; }
    </style>
""", unsafe_allow_html=True)

# ---- Sidebar ----
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("---")
    
    # Topic input
    topic_input = st.text_area(
        "Enter topics:",
        height=100,
        placeholder="Physics\nChemistry\nBiology",
        help="One topic per line or comma-separated"
    )
    
    # FIXED: Shorter dropdown labels
    mode_labels = {
        "explain": "Explain",
        "simplify": "Simplify",
        "examples": "Examples",
        "quiz": "Quiz",
        "all": "All Modes"
    }
    
    mode = st.selectbox(
        "Mode:",
        options=list(mode_labels.keys()),
        format_func=lambda x: mode_labels[x]
    )
    
    st.markdown("---")
    
    # FIXED: Super visible button
    generate_btn = st.button(
        "🚀 GENERATE", 
        type="primary", 
        use_container_width=True
    )
    
    st.markdown("---")
    
    with st.expander("How to Use"):
        st.write("1. Enter topic")
        st.write("2. Choose mode")
        st.write("3. Click GENERATE")

# ---- Main Area ----

# Banner
st.markdown("""
    <div style='background: linear-gradient(135deg, #1F618D 0%, #117A65 100%); 
                padding: 25px; 
                border-radius: 12px; 
                text-align: center;
                margin-bottom: 20px;'>
        <h1 style='color: white; margin: 0; font-size: 2.2em;'>📚 StudyMate</h1>
        <p style='color: white; font-size: 1.1em; margin-top: 8px;'>AI Study Buddy</p>
    </div>
""", unsafe_allow_html=True)

# Intro
st.markdown("""
    <div style='background-color: white; 
                padding: 18px; 
                border-radius: 8px; 
                border-left: 4px solid #1F618D;
                margin-bottom: 20px;'>
        <p style='margin: 0; font-size: 15px;'>
        Enter any topic, choose how to study it, and get AI-generated learning materials instantly! 🎓
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border: 2px solid #CCC; margin: 25px 0;'>", unsafe_allow_html=True)

# ---- Generate Content ----
if generate_btn:
    topics = []
    for line in topic_input.split('\n'):
        topics.extend([t.strip() for t in line.split(',') if t.strip()])
    
    if not topics:
        st.warning("⚠️ Please enter at least one topic!")
    else:
        st.info(f"🔍 Generating for {len(topics)} topic(s)...")
        
        for topic_idx, topic in enumerate(topics, 1):
            # Topic header
            st.markdown(f"""
                <div style='background-color: #E3F2FD; 
                            padding: 12px; 
                            border-radius: 8px; 
                            margin: 15px 0;
                            border-left: 4px solid #1F618D;'>
                    <h2 style='margin: 0; font-size: 1.5em;'>
                        📖 {topic}
                    </h2>
                </div>
            """, unsafe_allow_html=True)
            
            # Modes to run
            modes_to_run = ["explain", "simplify", "examples", "quiz"] if mode == "all" else [mode]
            
            # Generate each mode
            for m in modes_to_run:
                mode_icons = {
                    "explain": "📘",
                    "simplify": "🪄",
                    "examples": "💡",
                    "quiz": "📝"
                }
                
                st.markdown(f"""
                    <h3 style='margin-top: 15px;'>
                        {mode_icons.get(m)} {m.title()}
                    </h3>
                """, unsafe_allow_html=True)
                
                with st.spinner(f"Generating {m}..."):
                    result = ask_studymate(topic, m)
                    time.sleep(0.5)  # Prevent rate limit
                
                # Display result
                st.markdown(f"""
                    <div style='background-color: white; 
                                padding: 15px; 
                                border-radius: 6px; 
                                border-left: 3px solid #117A65;
                                margin: 8px 0;
                                box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                        <p style='font-size: 15px; 
                                   line-height: 1.6; 
                                   margin: 0;'>
                            {result}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            if topic_idx < len(topics):
                st.markdown("<hr style='border: 1px solid #CCC; margin: 30px 0;'>", unsafe_allow_html=True)
        
        st.success("✅ Done!")
        st.info("💡 Copy or screenshot the content above for your notes!")

# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; 
                color: #888; 
                padding: 15px;
                border-top: 1px solid #CCC;'>
        <p style='margin: 0;'>Made with ❤️ using Streamlit & Hugging Face</p>
        <p style='margin: 5px 0 0 0; font-size: 13px;'>100% Free • No Signup Required</p>
    </div>
""", unsafe_allow_html=True)
