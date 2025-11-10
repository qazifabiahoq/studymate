import streamlit as st
from datetime import datetime
from transformers import pipeline

# ---- Model Setup ----
st.sidebar.title("Model Setup")
st.sidebar.write("Using distilgpt2 for text generation (CPU-friendly)")
study_bot = pipeline(
    "text-generation",
    model="distilgpt2",  # smaller CPU-friendly GPT-2 variant
    device=-1  # force CPU
)

# ---- StudyMate Function ----
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
            truncation=True
        )
        result = output[0]["generated_text"]
        if result.startswith(prompt):
            result = result[len(prompt):].strip()
        return result
    except Exception as e:
        return f"Error: {str(e)}"
# ---- Streamlit App ----

# Sidebar for inputs
st.sidebar.markdown("<h2 style='color:#1E90FF; font-family:Arial;'>StudyMate Inputs</h2>", unsafe_allow_html=True)
topic_input = st.sidebar.text_area(
    "Enter topics (comma-separated):", 
    height=120,
    placeholder="e.g., Quantum Physics, Photosynthesis"
)
mode_options = ["explain", "simplify", "examples", "quiz", "all"]
mode = st.sidebar.selectbox("Choose a mode:", mode_options)
generate_btn = st.sidebar.button("Generate")

# Main area
st.markdown("<h1 style='color:#0B3D91; text-align:center; font-family:Helvetica;'>StudyMate</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='color:#228B22; font-size:18px; text-align:center; font-family:Verdana;'>Learn any topic interactively: explain, simplify, examples, or quiz.</p>",
    unsafe_allow_html=True
)
st.markdown("<hr style='border:2px solid #A9A9A9;'>", unsafe_allow_html=True)

if generate_btn:
    topics = [t.strip() for t in topic_input.split(",") if t.strip()]
    if not topics:
        st.warning("Please enter at least one topic.")
    else:
        for topic in topics:
            st.markdown(
                f"<h2 style='color:#6A0DAD; font-family:Georgia; margin-top:20px;'>Topic: {topic}</h2>",
                unsafe_allow_html=True
            )
            modes_to_run = ["explain", "simplify", "examples", "quiz"] if mode == "all" else [mode]
            
            for m in modes_to_run:
                st.markdown(
                    f"<h3 style='color:#FF8C00; font-family:Tahoma; margin-bottom:5px;'>{m.capitalize()} for '{topic}':</h3>",
                    unsafe_allow_html=True
                )
                result = ask_studymate(topic, m)
                lines = [line.strip() for line in result.split("\n") if line.strip()]
                for idx, line in enumerate(lines, 1):
                    st.markdown(
                        f"<p style='color:#333333; margin-left:25px; font-family:Verdana; font-size:16px; line-height:1.5;'>{idx}. {line}</p>",
                        unsafe_allow_html=True
                    )
            
            st.markdown("<hr style='border:1px solid #C0C0C0;'>", unsafe_allow_html=True)

        st.success("Session saved successfully!")

