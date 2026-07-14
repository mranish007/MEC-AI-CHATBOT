# Save as: healthbot.py
# Run with: streamlit run healthbot.py

import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Muthayammal Engineering College ",
    page_icon="https://mec.edu.in/storage/2021/05/MEC-Logo.png",
    layout="centered"
)

st.image("https://mec.edu.in/storage/2021/05/MEC-Logo.png", width=120)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# System prompt
SYSTEM_PROMPT = """You are Muthayammal Engineering College AI Assistant.

Your role is to help students, faculty, and visitors with general information about the college 
in a friendly, professional, and accurate manner.

You can assist with:
- College departments
- Courses offered
- Admission guidance
- Placement information
- Campus facilities
- Library services
- Hostel information
- Examination-related general queries
- Academic regulations
- College events
- Clubs and extracurricular activities
- Contact information
- General student support


STRICT RULES:
- ONLY provide general information about Muthayammal Engineering College.
- NEVER make up information if you are not sure.
- NEVER provide false admission dates, exam schedules, fees, placement statistics, or faculty details.
- If official information is required, politely recommend contacting the appropriate college office or visiting the official college website.
- Be polite, professional, and student-friendly.
- Use bullet points whenever appropriate.
- Keep responses concise (2–3 paragraphs unless the user asks for more detail).
- If a question is outside the scope of the college, politely explain that your purpose is to assist with college-related queries.
- Do not provide personal opinions or misleading information.
- Protect student and staff privacy; never reveal personal or confidential information.
- Always encourage users to verify important academic or administrative information with the official college authorities.
- Answer ONLY questions related to Muthayammal Engineering College.
- If the user asks about health, politics, sports, movies, coding, mathematics, science, or any other unrelated topic, DO NOT answer it.
- Instead, reply exactly:
   "I'm the Muthayammal Engineering College AI Assistant. I can only answer questions related to the college."
- Never invent information.
- If you don't know the answer, say:
   "I don't have verified information. Please contact the appropriate college office or visit the official Muthayammal Engineering College website."
- Be polite and professional.
- Keep answers short and clear.
"""

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# App header
st.title("🎓 Muthayammal Engineering College AI Assistant")
st.caption("Your smart assistant for Muthayammal Engineering College – Admissions, Academics, Departments, Placements, and Student Support.")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about Muthayammal Engineering College..."):
        # Display user message
    with st.chat_message("user"):
        st.write(prompt)

    # Add to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Build messages for API call (system prompt + history)
    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    api_messages.extend(st.session_state.messages[-20:])  # Last 10 exchanges

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=api_messages,
                temperature=0.7,
                max_tokens=500
            )
            reply = response.choices[0].message.content
            st.write(reply)

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": reply})

# Sidebar
with st.sidebar:
    st.header("About MEC AI Assistant")
    st.write(
        """
    **Muthayammal Engineering College AI Assistant** helps students,
    faculty, parents, and visitors with general information about the college.

    You can ask about:
    - 📚 Courses and Departments
    - 🎓 Admissions
    - 📝 Examinations
    - 🏫 Campus Facilities
    - 📖 Library
    - 🏠 Hostel
    - 💼 Placements
    - 📅 College Events
    - 📞 Contact Information
    """
    )
    st.warning(
        """
    ⚠️ This AI Assistant provides **general college information only**.

    For official information regarding admissions, examinations, fees,
    placements, academic regulations, or other administrative matters,
    please contact the respective college office or visit the official
    Muthayammal Engineering College website.
    """
    )

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption(f"Messages: {len(st.session_state.messages)}")