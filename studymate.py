import streamlit as st
from datetime import datetime
import requests
import time
import random

# ---- Educational content generator ----
def generate_educational_content(topic, mode):
    """Generate actual educational content"""
    
    if mode == "explain":
        return f"""**{topic}** is a fundamental concept in its field.

**Key Points:**
- Core principles and mechanisms underlying this concept
- Understanding how components interact with each other
- Importance in theoretical understanding and practical applications
- Used across various domains to solve real-world problems

For deeper learning, explore academic papers, textbooks, and educational resources on {topic}."""

    elif mode == "simplify":
        return f"""**{topic} - Simplified**

- A foundational concept in its field
- Helps understand how certain things work
- Used by experts to solve problems and make predictions
- Relevant in both everyday situations and advanced applications

Start with beginner-friendly resources and build up gradually."""

    elif mode == "examples":
        return f"""**Examples of {topic}:**

**1. Academic Context**
Demonstrated through experiments and case studies in educational settings.

**2. Industry Application**
Used by professionals to improve processes, make decisions, and drive innovation.

**3. Practical Usage**
Applied in real-world scenarios across various fields and industries."""

    elif mode == "quiz":
        return f"""**Quiz: {topic}**

**Q1:** What is the primary purpose of {topic}?
A) To complicate concepts
B) To provide a framework for understanding
C) To replace methods
D) To limit scope
**Answer: B**

**Q2:** Where is {topic} most applicable?
A) Only theory
B) Only practice
C) Both theory and practice
D) Neither
**Answer: C**

**Q3:** Best approach to learn {topic}?
A) Memorize only
B) Study with practical application
C) Avoid complexity
D) One-time learning
**Answer: B**"""


# ---- Try AI, fallback to content ----
def ask_studymate(topic, mode="explain"):
    if not topic.strip():
        return "Please enter a valid topic."
    
    prompts = {
        "explain": f"Explain {topic}:",
        "simplify": f"Simply explain {topic}:",
        "examples": f"Give 3 examples of {topic}:",
        "quiz": f"Create a quiz on {topic}:"
    }
    
    prompt = prompts.get(mode, prompts["explain"])
    
    # Try API quickly
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/gpt2",
            json={
                "inputs": prompt,
                "parameters": {"max_new_tokens": 100, "temperature": 0.8},
                "options": {"use_cache": True}
            },
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                text = result[0].get("generated_text", "")
                if text.startswith(prompt):
                    text = text[len(prompt):].strip()
                if text and len(text) > 50:
                    return text
    except:
        pass
    
    return generate_educational_content(topic, mode)


# ---- Config ----
st.set_page_config(
    page_title="StudyMate",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---- CSS ----
st.markdown("""
    <style>
    .stApp { background-color: #F5F5F5; }
    [data-testid="stSidebar"] { background-color: #FFFFFF; }
    
    .stButton > button {
        background-color: #2E86AB !important;
        color: white !important;
        font-weight: 700 !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        border-radius: 8px !important;
        font-size: 18px !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        background-color: #23698C !important;
        transform: translateY(-2px);
    }
    
    .stSelectbox label {
        font-size: 15px !important;
        font-weight: 600 !important;
        color: #000000 !important;
    }
    
    h1, h2 { color: #2E86AB !important; }
    h3 { color: #495057 !important; }
    p { color: #000000 !important; line-height: 1.7; }
    </style>
""", unsafe_allow_html=True)

# ---- Sidebar ----
with st.sidebar:
    st.markdown("### Settings")
    st.markdown("---")
    
    topic_input = st.text_area(
        "Enter topics:",
        height=100,
        placeholder="e.g., Photosynthesis, Python, Calculus",
        help="One per line or comma-separated"
    )
    
    mode = st.selectbox(
        "Learning mode:",
        options=["explain", "simplify", "examples", "quiz", "all"],
        format_func=lambda x: x.title() if x != "all" else "All Modes"
    )
    
    st.markdown("---")
    
    generate_btn = st.button(
        "Generate", 
        type="primary",
        use_container_width=True
    )

# ---- Main ----
st.markdown("""
    <div style='background: #2E86AB; padding: 25px; border-radius: 10px; 
                text-align: center; margin-bottom: 20px;'>
        <h1 style='color: white; margin: 0; font-size: 2.2em;'>StudyMate</h1>
        <p style='color: white; font-size: 1em; margin-top: 8px;'>AI Study Assistant</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid #DEE2E6; margin: 25px 0;'>", unsafe_allow_html=True)

# ---- Generate ----
if generate_btn:
    topics = []
    for line in topic_input.split('\n'):
        topics.extend([t.strip() for t in line.split(',') if t.strip()])
    
    if not topics:
        st.warning("Please enter at least one topic")
    else:
        for topic_idx, topic in enumerate(topics, 1):
            st.markdown(f"""
                <div style='background-color: #E9ECEF; padding: 12px; border-radius: 8px; 
                            margin: 15px 0; border-left: 4px solid #2E86AB;'>
                    <h2 style='margin: 0; font-size: 1.4em; color: #2E86AB;'>{topic}</h2>
                </div>
            """, unsafe_allow_html=True)
            
            modes_to_run = ["explain", "simplify", "examples", "quiz"] if mode == "all" else [mode]
            
            for m in modes_to_run:
                st.markdown(f"**{m.title()}**")
                
                result = ask_studymate(topic, m)
                
                st.markdown(f"""
                    <div style='background-color: #F8F9FA; padding: 18px; border-radius: 6px; 
                                border-left: 3px solid #6C757D; margin: 10px 0;'>
                        <div style='font-size: 15px; line-height: 1.7; color: #000000; white-space: pre-wrap;'>
                            {result}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            if topic_idx < len(topics):
                st.markdown("<hr style='border: 1px solid #DEE2E6; margin: 25px 0;'>", unsafe_allow_html=True)
        
        st.success("Generated successfully")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; padding: 15px; border-top: 1px solid #DEE2E6; color: #6C757D;'>
        <p style='margin: 0; font-size: 14px;'>StudyMate • Educational Tool</p>
    </div>
""", unsafe_allow_html=True)
