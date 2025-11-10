import streamlit as st
import requests
import time

def ask_studymate(topic, mode="explain"):
    if not topic.strip():
        return "Please enter a valid topic."
    
    # Correct secret access
    try:
        API_KEY = st.secrets["GROQ"]["GROQ_API_KEY"]
    except KeyError:
        return "⚙️ API key not configured. Add GROQ_API_KEY to Streamlit secrets under [GROQ]."
    
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
                "model": "groq/compound-mini",  # <- Corrected here
                "messages": [{"role": "user", "content": prompts.get(mode, prompts["explain"])}],
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
            return f"API Error {response.status_code}: {response.text}"
            
    except requests.exceptions.Timeout:
        return "⏱️ Request timed out. Please try again."
    except Exception as e:
        return f"Error: {str(e)}"


# --- Streamlit App ---
st.set_page_config(
    page_title="StudyMate",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded"
)

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
                
                time.sleep(0.3)
            
            if topic_idx < len(topics):
                st.divider()
        
        st.success("✅ Generated successfully!")

st.divider()
st.caption("StudyMate • Educational Tool")
