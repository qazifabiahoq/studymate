
import streamlit as st
from datetime import datetime
from transformers import pipeline
import torch

# ---- Model Setup ----
@st.cache_resource
def load_model():
    return pipeline(
        "text-generation",
        model="distilgpt2",
        device=0 if torch.cuda.is_available() else -1,  # GPU if available, else CPU
        torch_dtype=torch.float32  # Explicit dtype
    )

study_bot = load_model()

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
            truncation=True,
            pad_token_id=study_bot.tokenizer.eos_token_id  # Fix padding issue
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
    layout="centered",
    initial_sidebar_state="expanded"
)

st.sidebar.markdown(
    "<h2 style='color:#1F618D; font-family:Arial;'>StudyMate Inputs</h2>", 
    unsafe_allow_html=True
)
topic_input = st.sidebar.text_area(
    "Enter topics (comma-separated):", 
    height=120,
    placeholder="e.g., Quantum Physics, Photosynthesis"
)
mode_options = ["explain", "simplify", "examples", "quiz", "all"]
mode = st.sidebar.selectbox("Choose a mode:", mode_options)
generate_btn = st.sidebar.button("Generate")

# Text banner instead of image
st.markdown(
    "<div style='background-color:#1F618D; padding:20px; border-radius:10px; text-align:center;'>"
    "<h1 style='color:white; margin:0;'>📚 StudyMate</h1>"
    "</div>", 
    unsafe_allow_html=True
)

st.markdown(
    "<p style='color:#2C3E50; font-size:18px; text-align:center; font-family:Verdana; margin-top:10px;'>"
    "Learn any topic interactively: explain, simplify, examples, or quiz.</p>",
    unsafe_allow_html=True
)
st.markdown("<hr style='border:1px solid #BDC3C7;'>", unsafe_allow_html=True)

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

if generate_btn:
    topics = [t.strip() for t in topic_input.split(",") if t.strip()]
    if not topics:
        st.warning("Please enter at least one topic.")
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("studymate_output.txt", "a") as f:
            f.write(f"--- Session at {timestamp} ---\n")
            
            for topic in topics:
                st.markdown(
                    f"<h2 style='font-family:Georgia; margin-top:20px;'>Topic: {topic}</h2>",
                    unsafe_allow_html=True
                )
                f.write(f"Topic: {topic}\n")
                
                modes_to_run = ["explain", "simplify", "examples", "quiz"] if mode=="all" else [mode]
                
                for m in modes_to_run:
                    st.markdown(
                        f"<h3 style='font-family:Tahoma; margin-bottom:5px;'>{m.capitalize()}:</h3>",
                        unsafe_allow_html=True
                    )
                    result = ask_studymate(topic, m)
                    f.write(f"{m.capitalize()}:\n{result}\n\n")
                    
                    lines = [line.strip() for line in result.split("\n") if line.strip()]
                    for idx, line in enumerate(lines, 1):
                        st.markdown(
                            f"<p style='margin-left:25px; font-family:Verdana; font-size:16px; line-height:1.5;'>"
                            f"{idx}. {line}</p>",
                            unsafe_allow_html=True
                        )
                
                st.markdown("<hr style='border:1px solid #BDC3C7;'>", unsafe_allow_html=True)
            
            f.write("\n\n")
        
        st.success("Session saved successfully! Output written to studymate_output.txt")
