import streamlit as st
from datetime import datetime
import requests
import time

# ---- StudyMate Function using HF Inference API ----
def ask_studymate(topic, mode="explain"):
    """
    Generates AI responses using Hugging Face's free Inference API
    No local model needed - all processing happens on HF servers
    """
    if not topic.strip():
        return "Please enter a valid topic."
    
    prompt_map = {
        "explain": f"Explain the concept of {topic} in detail with clear explanations.\n\n",
        "simplify": f"Explain {topic} in very simple words that a beginner can understand.\n\n",
        "examples": f"Provide 3 concrete, real-world examples that demonstrate {topic}.\n\n",
        "quiz": f"Create 3 multiple-choice questions about {topic} with answers.\n\n",
    }

    prompt = prompt_map.get(mode, prompt_map["explain"])
    
    # Hugging Face's free Inference API endpoint
    API_URL = "https://api-inference.huggingface.co/models/distilgpt2"
    
    try:
        response = requests.post(
            API_URL,
            headers={"Content-Type": "application/json"},
            json={
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 150,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "do_sample": True,
                    "return_full_text": False
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()[0]["generated_text"]
            
            # Clean up the output
            if result.startswith(prompt):
                result = result[len(prompt):].strip()
            
            return result if result else "Unable to generate response. Please try again."
            
        elif response.status_code == 503:
            return "Model is loading... Please wait 20 seconds and try again."
        else:
            return f"API returned error code {response.status_code}. Please try again."
            
    except requests.exceptions.Timeout:
        return "Request timed out. Please try again."
    except Exception as e:
        return f"Error: {str(e)}"


# ---- Streamlit App Configuration ----
st.set_page_config(
    page_title="StudyMate - AI Study Buddy",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---- Custom CSS for Better Styling ----
st.markdown("""
    <style>
    /* Main app background */
    .stApp {
        background-color: #F8F9FA;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #E8EAF6;
    }
    
    /* Make buttons more visible */
    .stButton > button {
        background-color: #1F618D;
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 8px;
        font-size: 16px;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #174A6B;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Headers */
    h1 {
        color: #1F618D;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    h2 {
        color: #1F618D;
        font-family: 'Georgia', serif;
    }
    
    h3 {
        color: #117A65;
        font-family: 'Tahoma', sans-serif;
    }
    
    /* Text */
    p {
        color: #2C3E50;
        line-height: 1.6;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #1F618D !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---- Sidebar Configuration ----
with st.sidebar:
    st.markdown(
        "<h2 style='color:#1F618D; font-family:Arial; text-align:center;'>⚙️ Study Settings</h2>", 
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    
    # Topic input
    topic_input = st.text_area(
        "📝 Enter topics (one per line or comma-separated):",
        height=120,
        placeholder="Example:\nQuantum Physics\nPhotosynthesis\nMachine Learning",
        help="You can enter multiple topics separated by commas or on separate lines"
    )
    
    # Mode selection
    mode_options = {
        "explain": "📘 Explain - Detailed explanation",
        "simplify": "🪄 Simplify - Beginner-friendly",
        "examples": "💡 Examples - Real-world cases",
        "quiz": "📝 Quiz - Test your knowledge",
        "all": "🌟 All Modes - Complete study guide"
    }
    
    mode = st.selectbox(
        "Choose learning mode:",
        options=list(mode_options.keys()),
        format_func=lambda x: mode_options[x],
        help="Select how you want to learn about your topic"
    )
    
    st.markdown("---")
    
    # Generate button - now very visible!
    generate_btn = st.button("🚀 Generate Study Material", type="primary", use_container_width=True)
    
    st.markdown("---")
    
    # Info section
    with st.expander("ℹ️ How to Use"):
        st.markdown("""
        **Steps:**
        1. Enter one or more topics
        2. Choose a learning mode
        3. Click 'Generate Study Material'
        4. Review your personalized content!
        
        **Tips:**
        - Start with 'Simplify' for new topics
        - Use 'Quiz' to test understanding
        - Try 'All Modes' for comprehensive learning
        """)
    
    with st.expander("🔧 About"):
        st.markdown("""
        **StudyMate** uses AI to help you learn any topic quickly and effectively.
        
        Powered by:
        - Hugging Face Inference API
        - Streamlit
        - DistilGPT-2 Language Model
        """)

# ---- Main Content Area ----

# Banner
st.markdown(
    """
    <div style='background: linear-gradient(135deg, #1F618D 0%, #117A65 100%); 
                padding: 30px; 
                border-radius: 15px; 
                text-align: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                margin-bottom: 20px;'>
        <h1 style='color: white; margin: 0; font-size: 2.5em;'>📚 StudyMate</h1>
        <p style='color: #E8F4F8; font-size: 1.2em; margin-top: 10px;'>Your Personal AI Study Buddy</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# Introduction
st.markdown(
    """
    <div style='background-color: white; 
                padding: 20px; 
                border-radius: 10px; 
                border-left: 5px solid #1F618D;
                margin-bottom: 20px;'>
        <p style='color:#2C3E50; font-size:16px; margin: 0;'>
        Welcome! Enter any topic you want to learn about, choose how you'd like to study it, 
        and let AI create personalized learning materials for you. Perfect for students, 
        professionals, and curious minds! 🎓
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<hr style='border: 2px solid #BDC3C7; margin: 30px 0;'>", unsafe_allow_html=True)

# ---- Generate Content ----
if generate_btn:
    # Parse topics
    topics = []
    for line in topic_input.split('\n'):
        topics.extend([t.strip() for t in line.split(',') if t.strip()])
    
    if not topics:
        st.warning("⚠️ Please enter at least one topic to study!")
    else:
        # Show what we're generating
        st.info(f"🔍 Generating study materials for {len(topics)} topic(s)...")
        
        # Process each topic
        for topic_idx, topic in enumerate(topics, 1):
            # Topic header
            st.markdown(
                f"""
                <div style='background-color: #E8F4F8; 
                            padding: 15px; 
                            border-radius: 10px; 
                            margin: 20px 0;
                            border-left: 5px solid #1F618D;'>
                    <h2 style='margin: 0; color: #1F618D;'>
                        📖 Topic {topic_idx}: {topic}
                    </h2>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Determine which modes to run
            modes_to_run = ["explain", "simplify", "examples", "quiz"] if mode == "all" else [mode]
            
            # Generate content for each mode
            for mode_idx, m in enumerate(modes_to_run, 1):
                # Mode header with icon
                mode_icons = {
                    "explain": "📘",
                    "simplify": "🪄",
                    "examples": "💡",
                    "quiz": "📝"
                }
                
                st.markdown(
                    f"""
                    <h3 style='color: #117A65; margin-top: 20px;'>
                        {mode_icons.get(m, "📌")} {m.capitalize()}
                    </h3>
                    """,
                    unsafe_allow_html=True
                )
                
                # Generate with spinner
                with st.spinner(f"✨ Generating {m} for '{topic}'..."):
                    result = ask_studymate(topic, m)
                    
                    # Small delay to prevent rate limiting
                    if mode_idx < len(modes_to_run):
                        time.sleep(1)
                
                # Display result in a nice box
                st.markdown(
                    f"""
                    <div style='background-color: white; 
                                padding: 20px; 
                                border-radius: 8px; 
                                border-left: 3px solid #117A65;
                                margin: 10px 0;
                                box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                        <p style='font-family: Verdana; 
                                   font-size: 16px; 
                                   line-height: 1.8; 
                                   color: #2C3E50;
                                   margin: 0;'>
                            {result}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            # Separator between topics
            if topic_idx < len(topics):
                st.markdown("<hr style='border: 1px solid #BDC3C7; margin: 40px 0;'>", unsafe_allow_html=True)
        
        # Success message
        st.success("✅ All study materials generated successfully!")
        
        # Download option (optional feature)
        st.markdown("---")
        st.info("💡 **Tip:** Take screenshots or copy the content above for your notes!")

# ---- Footer ----
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align: center; 
                color: #7F8C8D; 
                padding: 20px;
                border-top: 1px solid #BDC3C7;'>
        <p style='margin: 0;'>Made with ❤️ using Streamlit & Hugging Face</p>
        <p style='margin: 5px 0 0 0; font-size: 14px;'>
            StudyMate - Learn Smarter, Not Harder
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
