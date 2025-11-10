import streamlit as st
from datetime import datetime
import requests

# ---- Function to ask StudyMate using HF Inference API ----
def ask_studymate(topic, mode="explain"):
    if not topic.strip():
        return "Please enter a valid topic."
    
    prompt_map = {
        "explain": f"Provide a detailed explanation of {topic}, including key concepts and applications.",
        "simplify": f"Explain {topic} in simple, easy-to-understand terms for beginners.",
        "examples": f"Give 3 specific, real-world examples of {topic} with brief descriptions.",
        "quiz": f"Create 3 multiple-choice questions about {topic}. Include the question, 4 options (A-D), and mark the correct answer.",
    }
    
    prompt = prompt_map.get(mode, prompt_map["explain"])
    
    # Use Hugging Face Inference API (completely free, no signup needed)
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    
    try:
        response = requests.post(
            API_URL,
            headers={"Content-Type": "application/json"},
            json={
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 300,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "return_full_text": False
                },
                "options": {
                    "wait_for_model": True,
                    "use_cache": False
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                text = result[0].get("generated_text", "")
                return text.strip() if text else "Unable to generate response."
        
        elif response.status_code == 503:
            return "⏳ Model is loading (first time takes 20-30 seconds). Please try again."
        
        else:
            return f"API Error {response.status_code}. Please try again."
            
    except requests.exceptions.Timeout:
        return "⏱️ Request timed out. Please try again."
    except Exception as e:
        return f"Error: {str(e)}"


# ---- Streamlit App ----
st.set_page_config(
    page_title="StudyMate",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Sidebar inputs
st.sidebar.markdown("<h2 style='color:#1F618D;'>StudyMate Settings</h2>", unsafe_allow_html=True)
st.sidebar.info("💡 First generation may take 20-30 seconds while the AI model loads.")

topic_input = st.sidebar.text_area(
    "Enter topics:",
    height=120,
    placeholder="e.g., Quantum Physics, Photosynthesis, Python"
)

mode_options = {
    "explain": "Explain",
    "simplify": "Simplify",
    "examples": "Examples",
    "quiz": "Quiz",
    "all": "All Modes"
}

mode = st.sidebar.selectbox(
    "Learning mode:",
    options=list(mode_options.keys()),
    format_func=lambda x: mode_options[x]
)

generate_btn = st.sidebar.button("Generate", type="primary", use_container_width=True)

# Main content
st.markdown(
    "<div style='background-color:#1F618D; padding:25px; border-radius:10px; text-align:center;'>"
    "<h1 style='color:white; margin:0;'>📚 StudyMate</h1>"
    "<p style='color:white; margin-top:8px;'>AI-Powered Study Assistant</p>"
    "</div>",
    unsafe_allow_html=True
)

st.markdown("<hr style='border:1px solid #BDC3C7;'>", unsafe_allow_html=True)

# Styling
st.markdown(
    """
    <style>
    .stApp { background-color: #F5F5F5; }
    h2 { color: #1F618D !important; }
    h3 { color: #117A65 !important; }
    p { color: #2C3E50; }
    </style>
    """,
    unsafe_allow_html=True
)

# Generate content
if generate_btn:
    topics = []
    for line in topic_input.split('\n'):
        topics.extend([t.strip() for t in line.split(',') if t.strip()])
    
    if not topics:
        st.warning("⚠️ Please enter at least one topic")
    else:
        progress_bar = st.progress(0)
        modes_to_run = ["explain", "simplify", "examples", "quiz"] if mode == "all" else [mode]
        total_tasks = len(topics) * len(modes_to_run)
        current_task = 0
        
        for topic_idx, topic in enumerate(topics, 1):
            st.markdown(f"## {topic}")
            
            for m in modes_to_run:
                st.markdown(f"### {m.title()}")
                
                with st.spinner(f"Generating {m}... (may take 20-30 seconds first time)"):
                    result = ask_studymate(topic, m)
                    current_task += 1
                    progress_bar.progress(current_task / total_tasks)
                
                st.info(result)
            
            if topic_idx < len(topics):
                st.divider()
        
        progress_bar.empty()
        st.success("✅ Content generated successfully!")
        st.balloons()

st.divider()
st.caption("StudyMate • Educational Tool")
