import streamlit as st
import requests
import time

def ask_studymate(topic, mode="explain"):
    if not topic.strip():
        return "Please enter a valid topic."
    
    # Get API key from secrets
    API_KEY = st.secrets.get("GROQ_API_KEY", "")
    
    if not API_KEY:
        return "⚙️ API key not configured. Add GROQ_API_KEY to Streamlit secrets."
    
    prompts = {
        "explain": f"Explain {topic} in detail with key concepts and applications. Be clear and educational.",
        "simplify": f"Explain {topic} in simple, beginner-friendly terms that anyone can understand.",
        "examples": f"Give 3 specific, real-world examples of {topic} with brief explanations for each.",
        "quiz": f"Create 3 multiple-choice questions about {topic}. For each question, provide 4 options (A-D) and clearly mark the correct answer."
    }
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mixtral-8x7b-32768",
                "messages": [
                    {"role": "user", "content": prompts.get(mode, prompts["explain"])}
                ],
                "temperature": 0.7,
                "max_tokens": 600
            },
            timeout=20
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        elif response.status_code == 401:
            return "❌ Invalid API key. Check your Groq API key in secrets."
        else:
            return f"API Error {response.status_code}. Please try again."
            
    except requests.exceptions.Timeout:
        return "⏱️ Request timed out. Please try again."
    except Exception as e:
        return f"Error: {str(e)}"


# Streamlit Config
st.set_page_config(
    page_title="StudyMate",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded"
)

# CSS Styling
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
    
    .stButton > button:hover {
        background-color: #23698C !important;
        transform: translateY(-2px);
    }
    
    h1, h2 { color: #2E86AB !important; }
    h3 { color: #495057 !important; }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### Settings")
    st.markdown("---")
    
    topic_input = st.text_area(
        "Enter topics:",
        height=100,
        placeholder="Physics, Python, Biology, History..."
    )
    
    mode = st.selectbox(
        "Learning mode:",
        ["explain", "simplify", "examples", "quiz", "all"],
        format_func=lambda x: x.title() if x != "all" else "All Modes"
    )
    
    st.markdown("---")
    generate_btn = st.button("Generate", type="primary", use_container_width=True)

# Main Content
st.title("StudyMate")
st.subheader("AI-Powered Study Assistant")
st.divider()

# Generate Content
if generate_btn:
    topics = []
    for line in topic_input.split('\n'):
        topics.extend([t.strip() for t in line.split(',') if t.strip()])
    
    if not topics:
        st.warning("Please enter at least one topic")
    else:
        for topic_idx, topic in enumerate(topics, 1):
            st.markdown(f"## {topic}")
            
            modes = ["explain", "simplify", "examples", "quiz"] if mode == "all" else [mode]
            
            for m in modes:
                st.markdown(f"### {m.title()}")
                
                with st.spinner(f"Generating {m}..."):
                    result = ask_studymate(topic, m)
                
                st.info(result)
                
                time.sleep(0.3)  # Small delay between requests
            
            if topic_idx < len(topics):
                st.divider()
        
        st.success("✅ Generated successfully!")

st.divider()
st.caption("StudyMate • Educational Tool")
