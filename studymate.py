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
st.title("StudyMate")
st.write("Learn any topic interactively: explain, simplify, examples, or quiz.")

topic_input = st.text_area("Enter one or more topics (separate by commas):")
mode_options = ["explain", "simplify", "examples", "quiz", "all"]
mode = st.selectbox("Choose a mode:", mode_options)

if st.button("Generate"):
    topics = [t.strip() for t in topic_input.split(",") if t.strip()]
    if not topics:
        st.warning("Please enter at least one topic.")
    else:
        for topic in topics:
            st.header(f"Topic: {topic}")
            modes_to_run = ["explain", "simplify", "examples", "quiz"] if mode == "all" else [mode]
            
            for m in modes_to_run:
                st.subheader(f"{m.capitalize()} for '{topic}':")
                result = ask_studymate(topic, m)
                lines = [line.strip() for line in result.split("\n") if line.strip()]
                for idx, line in enumerate(lines, 1):
                    st.write(f"{idx}. {line}")
            
            # Save session log
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            with open(f"studymate_session_{timestamp}.txt", "a", encoding="utf-8") as f:
                for m in modes_to_run:
                    f.write(f"{m.capitalize()} for '{topic}':\n{result}\n\n")
        st.success("Session saved successfully.")
