import streamlit as st
from datetime import datetime
import requests
import time

# ---- StudyMate Function - WORKING VERSION ----
def ask_studymate(topic, mode="explain"):
    """
    Uses working Hugging Face models with better prompts
    """
    if not topic.strip():
        return "Please enter a valid topic."
    
    # Better prompts that generate more content
    prompt_map = {
        "explain": f"Explain {topic} in detail:\n\n",
        "simplify": f"Explain {topic} in simple words for beginners:\n\n",
        "examples": f"Give 3 real-world examples of {topic}:\n1.",
        "quiz": f"Create 3 quiz questions about {topic}:\n\nQuestion 1:",
    }

    prompt = prompt_map.get(mode, prompt_map["explain"])
    
    # Use TextSynth API (free, reliable alternative)
    # Or we'll use a working HF model
    API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-1.3B"
    
    try:
        response = requests.post(
            API_URL,
            json={
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 200,
                    "temperature": 0.9,
                    "top_p": 0.95,
                    "do_sample": True,
                    "repetition_penalty": 1.2
                },
                "options": {
                    "wait_for_model": True,
                    "use_cache": True
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            if isinstance(result, list) and len(result) > 0:
                text = result[0].get("generated_text", "")
                
                # Remove prompt
                if text.startswith(prompt):
                    text = text[len(prompt):].strip()
                
                # If we got good content, return it
                if text and len(text) > 30:
                    return text
        
        # If first model fails, try backup
        return try_backup_model(prompt)
            
    except Exception as e:
        return try_backup_model(prompt)


def try_backup_model(prompt):
    """Try a backup model"""
    API_URL = "https://api-inference.huggingface.co/models/gpt2-medium"
    
    try:
        response = requests.post(
            API_URL,
            json={
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 180,
                    "temperature": 0.85,
                    "do_sample": True
                },
                "options": {"wait_for_model": True}
            },
            timeout=25
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                text = result[0].get("generated_text", "")
                if text.startswith(prompt):
                    text = text[len(prompt):].strip()
                if text and len(text) > 30:
                    return text
    except:
        pass
    
    return "⚠️ AI models are currently loading. Please wait 30 seconds and try again!"


# ---- Streamlit Configuration ----
st.set_page_config(
    page_title="StudyMate",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---- FIXED CSS - Dark text on light background ----
st.markdown("""
    <style>
    .stApp {
        background-color: #F5F5F5;
    }
    
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
    }
    
    /* Super visible red button */
    .stButton > button {
        background-color: #FF4136 !important;
        color: white !important;
        font-weight: 900 !important;
        border: 4px solid #FF4136 !important;
        padding: 1rem 2rem !important;
        border-radius: 12px !important;
        font-size: 20px !important;
        width: 100% !important;
        box-shadow: 0 6px 10px rgba(255,65,54,0.4) !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stButton > button:hover {
        background-color: #DC352F !important;
        box-shadow: 0 8px 16px rgba(255,65,54,0.6) !important;
        transform: scale(1.08);
    }
    
    /* FIXED: High contrast text */
    .stSelectbox label {
        font-size: 16px !important;
        font-weight: 700 !important;
        color: #000000 !important;
    }
    
    div[data-baseweb="select"] > div {
        background-color: white !important;
        border: 2px solid #1F618D !important;
        font-size: 16px !important;
        color: #000000 !important;
    }
    
    /* All text dark and readable */
    h1 { color: #1F618D !important; font-weight: 700; }
    h2 { color: #1F618D !important; font-weight: 600; }
    h3 { color: #117A65 !important; font-weight: 600; }
    p { color: #000000 !important; line-height: 1.7; }
    
    /* Make sure content boxes have dark text */
    div[style*="background-color: white"] p {
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---- Sidebar ----
with st.sidebar:
    st.markdown("### ⚙️ Study Settings")
    st.markdown("---")
    
    topic_input = st.text_area(
        "📝 Topics:",
        height=100,
        placeholder="Quantum Computing\nPhotosynthesis\nMachine Learning",
        help="One per line or comma-separated"
    )
    
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
    
    generate_btn = st.button(
        "🚀 GENERATE", 
        type="primary",
        use_container_width=True
    )
    
    st.markdown("---")
    
    st.warning("⏰ First generation takes 20-30 seconds while AI loads!")
    
    with st.expander("📖 Instructions"):
        st.write("1. Enter topic")
        st.write("2. Pick mode")
        st.write("3. Click GENERATE")
        st.write("4. Wait 20-30 sec")
        st.write("5. Try again if it fails")

# ---- Main Content ----

st.markdown("""
    <div style='background: linear-gradient(135deg, #1F618D 0%, #117A65 100%); 
                padding: 30px; 
                border-radius: 15px; 
                text-align: center;
                margin-bottom: 25px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);'>
        <h1 style='color: white; margin: 0; font-size: 2.5em;'>📚 StudyMate</h1>
        <p style='color: white; font-size: 1.2em; margin-top: 10px; font-weight: 500;'>Free AI Study Assistant</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div style='background-color: #FFFACD; 
                padding: 20px; 
                border-radius: 10px; 
                border-left: 5px solid #FF4136;
                margin-bottom: 25px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
        <p style='margin: 0; font-size: 16px; font-weight: 600; color: #000000;'>
        🎓 100% Free • No Signup Required • AI-Powered Learning
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border: 2px solid #CCC; margin: 30px 0;'>", unsafe_allow_html=True)

# ---- Generate ----
if generate_btn:
    topics = []
    for line in topic_input.split('\n'):
        topics.extend([t.strip() for t in line.split(',') if t.strip()])
    
    if not topics:
        st.warning("⚠️ Please enter at least one topic!")
    else:
        st.info(f"🔄 Generating for {len(topics)} topic(s)... First time takes 20-30 seconds!")
        
        progress_bar = st.progress(0)
        total_tasks = len(topics) * (4 if mode == "all" else 1)
        current_task = 0
        
        for topic_idx, topic in enumerate(topics, 1):
            st.markdown(f"""
                <div style='background-color: #E3F2FD; 
                            padding: 15px; 
                            border-radius: 10px; 
                            margin: 20px 0;
                            border-left: 5px solid #1F618D;'>
                    <h2 style='margin: 0; font-size: 1.6em; color: #1F618D;'>
                        📖 {topic}
                    </h2>
                </div>
            """, unsafe_allow_html=True)
            
            modes_to_run = ["explain", "simplify", "examples", "quiz"] if mode == "all" else [mode]
            
            for m in modes_to_run:
                mode_icons = {
                    "explain": "📘",
                    "simplify": "🪄",
                    "examples": "💡",
                    "quiz": "📝"
                }
                
                st.markdown(f"""
                    <h3 style='margin-top: 18px; font-size: 1.3em; color: #117A65;'>
                        {mode_icons.get(m)} {m.title()}
                    </h3>
                """, unsafe_allow_html=True)
                
                with st.spinner(f"⏳ Generating {m}... (20-30 seconds first time)"):
                    result = ask_studymate(topic, m)
                    current_task += 1
                    progress_bar.progress(current_task / total_tasks)
                
                # FIXED: Yellow background with BLACK text
                st.markdown(f"""
                    <div style='background-color: #FFFACD; 
                                padding: 20px; 
                                border-radius: 8px; 
                                border-left: 4px solid #117A65;
                                margin: 12px 0;
                                box-shadow: 0 2px 6px rgba(0,0,0,0.15);'>
                        <p style='font-size: 17px; 
                                   line-height: 1.9; 
                                   margin: 0;
                                   color: #000000;
                                   font-weight: 500;
                                   white-space: pre-wrap;'>
                            {result}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
                time.sleep(2)  # Rate limiting
            
            if topic_idx < len(topics):
                st.markdown("<hr style='border: 1px solid #CCC; margin: 35px 0;'>", unsafe_allow_html=True)
        
        progress_bar.empty()
        st.success("✅ Done! If results are short, try clicking GENERATE again!")
        st.balloons()

# Footer
st.markdown("<br><br>", unsafe_allow_hash=True)
st.markdown("""
    <div style='text-align: center; 
                color: #555; 
                padding: 20px;
                border-top: 2px solid #CCC;'>
        <p style='margin: 0; font-size: 15px; font-weight: 600; color: #000;'>Made with ❤️ using Streamlit & Hugging Face</p>
        <p style='margin: 8px 0 0 0; font-size: 14px; color: #000;'>100% Free • No Payment Required</p>
    </div>
""", unsafe_allow_html=True)
