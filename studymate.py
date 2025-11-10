import streamlit as st
from datetime import datetime
from transformers import pipeline

# ---- Model Setup ----
@st.cache_resource
def load_model():
    # Load distilgpt2 on CPU
    return pipeline(
        "text-generation",
        model="distilgpt2",
        device=-1  # CPU
    )

study_bot = load_model()

# ---- Function to ask StudyMate ----
def ask_studymate(topic, mode="explain"):
    if not topic.strip():
        return "Please enter a valid topic."

    prompt_map = {
        "explain": f"Explain the concept of {topic} clearly:\n",
        "simplify": f"Explain {topic} in simple words:\n",
        "examples": f"Give 3 real-world examples of {topic}:\n",
        "quiz": f"Create 3 quiz questions with answers about {topic}:\n",
    }

    prompt = prompt_map.get(mode, prompt_map["explain"])
    max_tokens = {"explain": 150, "simplify": 100, "examples": 120, "quiz": 100}[mode]

    try:
        output = study_bot(
            prompt,
            max_new_tokens=max_tokens,
            do_sample=True,
            temperature=0.7,
            truncation=True,
            pad_token_id=50256  # GPT-2 EOS token
        )
        result = output[0]["generated_text"]
        if result.startswith(prompt):
            result = result[len(prompt):].strip()
        return result if result else "Unable to generate response."
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
st.sidebar.markdown("<h2 style='color:#1F618D;'>StudyMate Inputs</h2>", unsafe_allow_html=True)
topic_input = st.sidebar.text_area(
    "Enter topics (comma-separated):",
    height=120,
    placeholder="e.g., Quantum Physics, Photosynthesis"
)
mode_options = ["explain", "simplify", "examples", "quiz", "all"]
mode = st.sidebar.selectbox("Choose a mode:", mode_options)
generate_btn = st.sidebar.button("Generate")

# Banner
st.markdown(
    "<div style='background-color:#1F618D; padding:20px; border-radius:10px; text-align:center;'>"
    "<h1 style='color:white; margin:0;'>📚 StudyMate</h1>"
    "</div>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='color:#2C3E50; font-size:18px; text-align:center;'>Learn any topic interactively: explain, simplify, examples, or quiz.</p>",
    unsafe_allow_html=True
)
st.markdown("<hr style='border:1px solid #BDC3C7;'>", unsafe_allow_html=True)

# Styling
st.markdown(
    """
    <style>
    .stApp { background-color: #FFFFFF; }
    h2 { color: #1F618D; }
    h3 { color: #117A65; }
    p { color: #2C3E50; }
    </style>
    """,
    unsafe_allow_html=True
)

# Generate answers
if generate_btn:
    topics = [t.strip() for t in topic_input.split(",") if t.strip()]
    if not topics:
        st.warning("Please enter at least one topic.")
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for topic in topics:
            st.markdown(f"<h2>{topic}</h2>", unsafe_allow_html=True)
            modes_to_run = ["explain", "simplify", "examples", "quiz"] if mode=="all" else [mode]
            for m in modes_to_run:
                st.markdown(f"<h3>{m.capitalize()}:</h3>", unsafe_allow_html=True)
                with st.spinner(f"Generating {m}..."):
                    result = ask_studymate(topic, m)
                # Display each line separately for readability
                lines = [line.strip() for line in result.split("\n") if line.strip()]
                for idx, line in enumerate(lines, 1):
                    st.markdown(f"{idx}. {line}")
            st.markdown("<hr style='border:1px solid #BDC3C7;'>", unsafe_allow_html=True)
        st.success(f"Session generated at {timestamp}")
