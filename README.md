

# StudyMate

**StudyMate** is an AI-powered study assistant built with Streamlit and Groq’s AI models. It helps you learn any topic by generating explanations, simplified summaries, real-world examples, and quizzes.

**Live App:** [https://studymateapplication.streamlit.app/](https://studymateapplication.streamlit.app/)

---

## Features

* **Explain**: Get a detailed explanation of a topic.
* **Simplify**: Learn complex topics in beginner-friendly terms.
* **Examples**: See real-world examples of the topic.
* **Quiz**: Test yourself with multiple-choice questions.
* **Safe Free Quota**: Keeps track of your daily usage to stay within Groq free tier limits.

---

## How to Use

1. Open the [live app](https://studymateapplication.streamlit.app/) in your browser.
2. Enter the topic(s) you want to learn in the text area.
3. Choose a learning mode: **Explain, Simplify, Examples, Quiz, or All Modes**.
4. Click **Generate**.
5. View the AI-generated content below.

> If you reach the daily safe quota (200 calls/day), the app will stop generating new content for the day.

---

## Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/studymate.git
cd studymate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add your **Groq API key** to Streamlit secrets:

Create a `secrets.toml` file in `.streamlit/` with:

```toml
[GROQ]
GROQ_API_KEY = "your_groq_api_key_here"
```

4. Run the app locally:

```bash
streamlit run app.py
```

---

## Customization

* **UI Colors**: Primary color is `#1f618d` (matches banner).
* **Banner**: Add your banner image as `studymate_banner.png` in the root folder.
* **Quota**: Adjust `MAX_DAILY_CALLS` in `app.py` to control safe free usage.

---

## Requirements

* Python 3.8+
* Streamlit
* Requests

---

## License

MIT License

---


Do you want me to do that next?
