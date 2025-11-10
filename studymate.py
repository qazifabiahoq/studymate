import streamlit as st
from datetime import datetime
import requests
import time

# ---- StudyMate Function with FASTER models ----
def ask_studymate(topic, mode="explain"):
    """
    Uses Hugging Face's fastest FREE text generation models
    """
    if not topic.strip():
        return "Please enter a valid topic."
    
    # Clear, direct prompts
    prompt_map = {
        "explain": f"Topic: {topic}\n\nDetailed Explanation: ",
        "simplify": f"Topic: {topic}\n\nSimple Explanation: ",
        "examples": f"Topic: {topic}\n\n3 Real Examples:\n1. ",
        "quiz": f"Topic: {topic}\n\nQuiz Questions:\nQ1: ",
    }

    prompt = prompt_map.get(mode, prompt_map["explain"])
    
    # Fastest models that actually work
    models = [
        "bigscience/bloom-560m",
        "facebook/opt-125m",
        "gpt2"
    ]
    
    for model_name in models:
        API_URL = f"https://api-inference.huggingface.co/models/{model_name}"
        
        try:
            response = requests.post(
                API_URL,
                json={
                    "inputs": prompt,
                    "parameters": {
                        "max_length": 150,
                        "temperature": 0.8,
                        "top_p": 0.9,
                        "do_sample": True,
                        "num_return_sequences": 1
                    },
                    "options": {
                        "wait_for_model": True,
                        "use_cache": False
                    }
                },
                timeout=20
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract text
                if isinstance(result, list) and len(result) > 0:
                    text = result[0].get("generated_text", "")
                    
                    # Remove prompt from output
                    if text.startswith(prompt):
                        text = text[len(prompt):].strip()
                    
                    if text and len(text) > 20:
                        return text
            
            elif response.status_code == 503:
                # Model loading, wait and retry once
                time.sleep(3)
                continue
            
        except:
            continue
    
    # If all models fail, return educational fallback content
    return get_fallback_content(topic, mode)


def get_fallback_content(topic, mode):
    """
    Returns educational content when AI is unavailable
    """
    fallback = {
        "explain": f"{topic} is an important concept. For a detailed explanation, please try again or search online resources for comprehensive information.",
        "simplify": f"{topic} in simple terms: This is a fundamental concept worth exploring. Try again for an AI-generated explanation, or look for beginner-friendly resources.",
        "examples": f"Examples of {topic}:\n1. Check educational websites\n2. Review textbooks on this subject\n3. Watch educational videos\n\nTry generating again for AI examples!",
        "quiz": f"Quiz on {topic}:\n\nQ1: What are the key aspects of {topic}?\nQ2: How is {topic} used in real life?\nQ3: Why is {topic} important?\n\nTry again for more detailed questions!"
    }
    return fallback.get(mode, f"Content for {topic} - please try again!")


# ---- Streamlit Configuration ----
st.set_page_config(
    page_title="StudyMate",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---- Enhanced CSS ----
st.markdown("""
    <style>
    .stApp {
        background-color: #F5F5F5;
    }
    
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
    }
    
    /* Super visible button */
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
    
    .stSelectbox label {
        font-size: 16px !important;
        font-weight: 700 !important;
        color: #000 !important;
    }
    
    div[data-baseweb="select"] > div {
        background-color: white !important;
        border: 2px solid #1F618D !important;
        font-size: 16px !important;
    }
    
    h1 { color: #1F618D; font-weight: 700; }
    h2 { color: #1F618D; font-weight: 600; }
    h3 { color: #117A65; font-weight: 600; }
    p { color: #2C3E50; line-height: 1.7; }
    </style>
""", unsafe_allow_html=True)

# ---- Sidebar ----
with st.sidebar:
    st.markdown("### ⚙️ Study Settings")
    st.markdown("---")
    
    topic_input = st.text_area(
        "📝 Enter Topics:",
        height=100,
        placeholder="Physics\nChemistry\nBiology",
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
        "🎯 Learning Mode:",
        options=list(mode_labels.keys()),
        format_func=lambda x: mode_labels[x]
    )
    
    st.markdown("---")
    
    generate_btn = st.button(
        "🚀 GENERATE NOW", 
        type="primary",
        use_container_width=True
    )
    
    st.markdown("---")
    
    st.info("💡 **Tip:** AI might take 10-20 seconds on first use while models load!")
    
    with st.expander("📖 How to Use"):
        st.write("1. Enter topic(s)")
        st.write("2. Pick a mode")
        st.write("3. Click GENERATE")
        st.write("4. Wait 10-20 sec")

# ---- Main Content ----

st.markdown("""
    <div style='background: linear-gradient(135deg, #1F618D 0%, #117A65 100%); 
                padding: 30px; 
                border-radius: 15px; 
                text-align: center;
                margin-bottom: 25px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);'>
        <h1 style='color: white; margin: 0; font-size: 2.5em;'>📚 StudyMate</h1>
        <p style='color: white; font-size: 1.2em; margin-top: 10px; font-weight: 500;'>Your Free AI Study Assistant</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div style='background-color: white; 
                padding: 20px; 
                border-radius: 10px; 
                border-left: 5px solid #FF4136;
                margin-bottom: 25px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
        <p style='margin: 0; font-size: 16px; font-weight: 500;'>
        🎓 100% Free • No Signup • Instant AI-Generated Study Materials
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
        st.info(f"🔄 Generating content for {len(topics)} topic(s)... Please wait 10-20 seconds...")
        
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
                    <h2 style='margin: 0; font-size: 1.6em;'>
                        📖 Topic {topic_idx}: {topic}
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
                    <h3 style='margin-top: 18px; font-size: 1.3em;'>
                        {mode_icons.get(m)} {m.title()}
                    </h3>
                """, unsafe_allow_html=True)
                
                with st.spinner(f"⏳ Generating {m}... (may take 10-20 seconds)"):
                    result = ask_studymate(topic, m)
                    current_task += 1
                    progress_bar.progress(current_task / total_tasks)
                
                st.markdown(f"""
                    <div style='background-color: white; 
                                padding: 18px; 
                                border-radius: 8px; 
                                border-left: 4px solid #117A65;
                                margin: 12px 0;
                                box-shadow: 0 2px 6px rgba(0,0,0,0.08);'>
                        <p style='font-size: 16px; 
                                   line-height: 1.8; 
                                   margin: 0;
                                   white-space: pre-wrap;'>
                            {result}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
                time.sleep(1)  # Rate limiting
            
            if topic_idx < len(topics):
                st.markdown("<hr style='border: 1px solid #CCC; margin: 35px 0;'>", unsafe_allow_html=True)
        
        progress_bar.empty()
        st.success("✅ All content generated successfully!")
        st.balloons()

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; 
                color: #888; 
                padding: 20px;
                border-top: 2px solid #CCC;'>
        <p style='margin: 0; font-size: 15px; font-weight: 600;'>Made with ❤️ using Streamlit & Hugging Face</p>
        <p style='margin: 8px 0 0 0; font-size: 14px;'>100% Free Forever • No Payment Required</p>
    </div>
""", unsafe_allow_html=True)
