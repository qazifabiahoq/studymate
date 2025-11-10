import streamlit as st
from datetime import datetime
import requests
import time

# ---- Smart Educational Content Generator ----
def generate_smart_content(topic, mode):
    """Generate topic-specific educational content"""
    
    topic_lower = topic.lower()
    
    # Topic-specific knowledge base
    topic_database = {
        "machine learning": {
            "explain": """Machine learning is a branch of artificial intelligence that enables computers to learn from data without being explicitly programmed. It uses algorithms that iteratively learn from data to find patterns and make predictions or decisions.

**Core Concepts:**
- Algorithms improve automatically through experience
- Systems learn from examples rather than rules
- Models identify patterns in data to make predictions
- Training data is used to teach the algorithm

**Types:** Supervised, unsupervised, and reinforcement learning.""",
            
            "simplify": """Machine learning teaches computers to learn like humans do - from experience. Instead of programming every rule, you show the computer examples and it figures out the patterns on its own. Like teaching a child to recognize cats by showing them pictures.""",
            
            "examples": """**Real-World Examples:**

1. **Email Spam Filters** - Learns which emails are spam by analyzing patterns
2. **Netflix Recommendations** - Suggests shows based on what you've watched
3. **Voice Assistants** - Siri and Alexa learn to understand your speech patterns""",
            
            "quiz": """**Q1:** What is machine learning?
A) Programming computers with rules
B) Teaching computers to learn from data
C) Building physical robots
D) Creating databases
**Answer: B - Teaching computers to learn from data**

**Q2:** Which is NOT a type of machine learning?
A) Supervised learning
B) Unsupervised learning  
C) Manual learning
D) Reinforcement learning
**Answer: C - Manual learning**

**Q3:** Real-world ML example?
A) Calculator
B) Netflix recommendations
C) Text editor
D) File explorer
**Answer: B - Netflix recommendations**"""
        },
        
        "unsupervised": {
            "explain": """Unsupervised machine learning finds hidden patterns in data without labeled examples. Unlike supervised learning, there's no "correct answer" - the algorithm explores the data structure on its own.

**Key Techniques:**
- Clustering - Groups similar data points together
- Dimensionality reduction - Simplifies complex data
- Anomaly detection - Finds unusual patterns
- Association rules - Discovers relationships

**Use Cases:** Customer segmentation, data exploration, pattern discovery.""",
            
            "simplify": """Unsupervised learning is like giving a computer a puzzle without showing the final picture. It has to figure out how the pieces fit together by looking at their shapes and colors. No teacher, no labels - just pure exploration.""",
            
            "examples": """**Practical Examples:**

1. **Customer Segmentation** - Grouping shoppers by buying habits without predefined categories
2. **Anomaly Detection** - Credit card companies finding unusual transactions that might be fraud
3. **Topic Modeling** - News apps automatically organizing articles by similar themes""",
            
            "quiz": """**Q1:** What makes unsupervised learning different?
A) It's faster
B) No labeled training data
C) It's more accurate
D) Uses more data
**Answer: B - No labeled training data**

**Q2:** Common unsupervised technique?
A) Classification
B) Regression
C) Clustering
D) Prediction
**Answer: C - Clustering**

**Q3:** Unsupervised learning use case?
A) Email classification
B) Customer grouping
C) House price prediction
D) Image labeling
**Answer: B - Customer grouping**"""
        },
        
        "photosynthesis": {
            "explain": """Photosynthesis is the process plants use to convert light energy into chemical energy (glucose). It occurs in chloroplasts using chlorophyll pigment.

**The Process:**
- Light absorption by chlorophyll (in chloroplasts)
- Water splits into hydrogen and oxygen
- Carbon dioxide combines with hydrogen
- Glucose is produced as food
- Oxygen released as byproduct

**Formula:** 6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ + 6O₂""",
            
            "simplify": """Plants make their own food using sunlight, water, and air. The green stuff in leaves (chlorophyll) catches sunlight and uses that energy to turn water and carbon dioxide into sugar (plant food) and oxygen that we breathe.""",
            
            "examples": """**Examples:**

1. **Trees in forests** - Producing oxygen while making food from sunlight
2. **Crops in farms** - Growing wheat, corn using photosynthesis to create grain
3. **Algae in oceans** - Producing most of Earth's oxygen through photosynthesis""",
            
            "quiz": """**Q1:** Where does photosynthesis occur?
A) Roots
B) Chloroplasts
C) Stems
D) Flowers
**Answer: B - Chloroplasts**

**Q2:** What do plants produce?
A) Only oxygen
B) Only glucose
C) Glucose and oxygen
D) Carbon dioxide
**Answer: C - Glucose and oxygen**

**Q3:** What do plants need?
A) Light, water, CO₂
B) Only water
C) Only sunlight
D) Soil minerals only
**Answer: A - Light, water, CO₂**"""
        },
        
        "python": {
            "explain": """Python is a high-level, interpreted programming language known for readability and versatility. Created by Guido van Rossum in 1991.

**Key Features:**
- Simple, readable syntax (almost like English)
- Dynamically typed (no need to declare variable types)
- Extensive standard library
- Large ecosystem of packages (pip)
- Used for web, data science, AI, automation

**Why Popular:** Easy to learn, powerful, and versatile.""",
            
            "simplify": """Python is a beginner-friendly programming language that reads almost like English. It's like giving instructions to a computer in a way that's easy for humans to understand. Great for beginners but powerful enough for experts.""",
            
            "examples": """**What Python Does:**

1. **Web Development** - Instagram and Pinterest are built with Python (Django)
2. **Data Science** - Analyzing data with pandas, creating visualizations
3. **Automation** - Writing scripts to automate boring tasks like file organization""",
            
            "quiz": """**Q1:** Python is known for?
A) Being difficult
B) Readable syntax
C) Only for web
D) Requiring compilation
**Answer: B - Readable syntax**

**Q2:** Python file extension?
A) .java
B) .cpp
C) .py
D) .js
**Answer: C - .py**

**Q3:** Python use case?
A) Only games
B) Only websites
C) Web, data, AI, automation
D) Only mobile apps
**Answer: C - Web, data, AI, automation**"""
        }
    }
    
    # Check if we have specific content for this topic
    for key in topic_database:
        if key in topic_lower:
            return topic_database[key].get(mode, generate_generic_content(topic, mode))
    
    # If topic not in database, generate generic but better content
    return generate_generic_content(topic, mode)


def generate_generic_content(topic, mode):
    """Generic fallback for unknown topics"""
    if mode == "explain":
        return f"""**{topic}** - Educational Overview

This concept involves understanding the fundamental principles and applications related to {topic}. 

To learn more about {topic}, explore:
- Academic textbooks and research papers
- Online courses (Coursera, edX, Khan Academy)
- Educational videos (YouTube, MIT OpenCourseWare)
- Practice problems and hands-on projects

**Note:** For detailed, accurate information on {topic}, please consult authoritative educational resources."""
    
    elif mode == "simplify":
        return f"""**{topic} - Simple Explanation**

{topic} is an important concept worth learning about. Start with:
- Beginner-friendly introductions
- Visual explanations and diagrams
- Simple examples before complex theory
- Practice with real applications

Build your understanding step by step."""
    
    elif mode == "examples":
        return f"""**Learning {topic}:**

To understand {topic} better:
1. Search for "{topic} examples" online
2. Watch educational videos demonstrating {topic}
3. Try hands-on practice or experiments
4. Join study groups or forums discussing {topic}"""
    
    elif mode == "quiz":
        return f"""**Study {topic}:**

To test your knowledge of {topic}:
1. Create flashcards with key concepts
2. Practice with online quizzes
3. Explain the concept to someone else
4. Apply it to real-world problems

The best way to learn is through active practice!"""


# ---- Try AI, then smart fallback ----
def ask_studymate(topic, mode="explain"):
    if not topic.strip():
        return "Please enter a valid topic."
    
    prompts = {
        "explain": f"Explain {topic} in detail:",
        "simplify": f"Explain {topic} simply:",
        "examples": f"Give 3 concrete examples of {topic}:",
        "quiz": f"Create 3 multiple choice questions about {topic}:"
    }
    
    prompt = prompts.get(mode, prompts["explain"])
    
    # Try API (quick timeout)
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/gpt2",
            json={
                "inputs": prompt,
                "parameters": {"max_new_tokens": 150, "temperature": 0.7},
                "options": {"use_cache": True}
            },
            timeout=3
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                text = result[0].get("generated_text", "")
                if text.startswith(prompt):
                    text = text[len(prompt):].strip()
                if text and len(text) > 60:
                    return text
    except:
        pass
    
    # Use smart fallback
    return generate_smart_content(topic, mode)


# ---- Rest of your code stays the same ----
st.set_page_config(
    page_title="StudyMate",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded"
)

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
    }
    
    h1, h2 { color: #2E86AB !important; }
    h3 { color: #495057 !important; }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Settings")
    st.markdown("---")
    
    topic_input = st.text_area(
        "Enter topics:",
        height=100,
        placeholder="e.g., Machine Learning, Photosynthesis, Python"
    )
    
    mode = st.selectbox(
        "Learning mode:",
        options=["explain", "simplify", "examples", "quiz", "all"],
        format_func=lambda x: x.title() if x != "all" else "All Modes"
    )
    
    st.markdown("---")
    generate_btn = st.button("Generate", type="primary", use_container_width=True)

st.title("StudyMate")
st.subheader("AI-Powered Study Assistant")
st.divider()

if generate_btn:
    topics = []
    for line in topic_input.split('\n'):
        topics.extend([t.strip() for t in line.split(',') if t.strip()])
    
    if not topics:
        st.warning("Please enter at least one topic")
    else:
        for topic in topics:
            st.markdown(f"## {topic}")
            
            modes_to_run = ["explain", "simplify", "examples", "quiz"] if mode == "all" else [mode]
            
            for m in modes_to_run:
                st.markdown(f"### {m.title()}")
                result = ask_studymate(topic, m)
                st.info(result)
            
            st.divider()
        
        st.success("Generated successfully")

st.divider()
st.caption("StudyMate • Educational Tool")
