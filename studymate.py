import streamlit as st
from datetime import datetime
import requests
import time

# ---- Function with multiple model fallbacks ----
def ask_studymate(topic, mode="explain"):
    if not topic.strip():
        return "Please enter a valid topic."
    
    prompt_map = {
        "explain": f"Explain {topic} in detail with key concepts:\n\n",
        "simplify": f"Explain {topic} simply for beginners:\n\n",
        "examples": f"Give 3 real-world examples of {topic}:\n\n",
        "quiz": f"Create 3 quiz questions about {topic} with answers:\n\n",
    }
    
    prompt = prompt_map.get(mode, prompt_map["explain"])
    
    # Try multiple working models in order
    models = [
        "HuggingFaceH4/zephyr-7b-beta",
        "google/flan-t5-large",
        "tiiuae/falcon-7b-instruct",
        "EleutherAI/gpt-neo-2.7B"
    ]
    
    for model in models:
        try:
            API_URL = f"https://api-inference.huggingface.co/models/{model}"
            
            response = requests.post(
                API_URL,
                json={
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": 250,
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "return_full_text": False
                    },
                    "options": {
                        "wait_for_model": True,
                        "use_cache": True
                    }
                },
                timeout=25
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if isinstance(result, list) and len(result) > 0:
                    text = result[0].get("generated_text", "")
                    if text and len(text) > 50:
                        return text.strip()
            
            elif response.status_code == 503:
                # Model loading, try next one
                continue
                
        except:
            continue
    
    # If all models fail, return helpful guidance
    return f"""**{topic}** - Study Guide

For comprehensive information on {topic}, explore:

📚 **Learning Resources:**
- Khan Academy - Free video lessons
- Coursera/edX - Online courses
- YouTube - Educational channels
- Wikipedia - Overview and basics

🔍 **Study Tips:**
1. Start with basic concepts
2. Watch explanatory videos
3. Practice with examples
4. Test yourself with quizzes

💡 The AI models are currently busy. Please try again in a moment, or use the resources above."""


# ---- Streamlit App ----
st.set_page_config(
    page_title="StudyMate",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded"
)

# CSS
st.markdown("""
    <style>
    .stApp { background-color: #F5F5F5; }
    [data-testid="stSidebar"] { background-color: #FFFFFF; }
    
    .stButton > button {
        background-color: #2E86AB !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 0.75rem 2rem !important;
        border-radius: 8px !important;
        font-size: 18px !important;
        width: 100% !important;
    }
    
    h1, h2 { color: #2E86AB !important; }
    h3 { color: #495057 !important; }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### Settings")
    st.markdown("---")
    
    st.info("⏰ First use: Wait 20-30 sec for AI to load")
    
    topic_input = st.text_area(
        "Enter topics:",
        height=100,
        placeholder="Physics, Biology, Math..."
    )
    
    mode = st.selectbox(
        "Learning mode:",
        options=["explain", "simplify", "examples", "quiz", "all"],
        format_func=lambda x: x.title() if x != "all" else "All Modes"
    )
    
    st.markdown("---")
    generate_btn = st.button("Generate", type="primary", use_container_width=True)

# Header
st.title("StudyMate")
st.subheader("AI-Powered Study Assistant")
st.divider()

# Generate
if generate_btn:
    topics = []
    for line in topic_input.split('\n'):
        topics.extend([t.strip() for t in line.split(',') if t.strip()])
    
    if not topics:
        st.warning("Please enter at least one topic")
    else:
        with st.spinner("🔄 Generating content... (first time may take 30 seconds)"):
            for topic_idx, topic in enumerate(topics, 1):
                st.markdown(f"## {topic}")
                
                modes_to_run = ["explain", "simplify", "examples", "quiz"] if mode == "all" else [mode]
                
                for m in modes_to_run:
                    st.markdown(f"### {m.title()}")
                    
                    result = ask_studymate(topic, m)
                    st.info(result)
                    
                    time.sleep(1)  # Rate limiting
                
                if topic_idx < len(topics):
                    st.divider()
        
        st.success("Generated successfully!")

st.divider()
st.caption("StudyMate • Educational Tool")
