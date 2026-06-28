import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API Key dari file .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Konfigurasi Parameter & UI Sidebars
st.set_page_config(page_title="EduGuide AI", page_icon="🎓", layout="wide")
st.title("🎓 EduGuide AI: Asisten Belajar & Karier")

st.sidebar.header("⚙️ Konfigurasi Bot")
gaya_bahasa = st.sidebar.selectbox("Gaya Bahasa:", ["Santai/Gen-Z", "Formal", "Semi-Formal"])
topik_fokus = st.sidebar.selectbox("Fokus Edukasi:", ["Programming", "Bisnis/Finance", "Desain Grafis", "Umum"])

# Menentukan System Instruction berdasarkan input user
instruction = f"Kamu adalah EduGuide AI, mentor edukasi yang ahli di bidang {topik_fokus}. " \
              f"Jawablah dengan gaya bahasa yang {gaya_bahasa}. Berikan jawaban yang solutif, terstruktur, " \
              f"dan berikan rekomendasi langkah konkret untuk belajar."

# Inisialisasi Memory (Chat History) di Streamlit Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=instruction
    )
    st.session_state.chat_session = model.start_chat(history=[])

# Menampilkan Riwayat Pesan
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input Pengguna & Respon Model
if user_input := st.chat_input("Tanyakan roadmap belajar atau topik yang ingin kamu kuasai..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("EduGuide sedang berpikir..."):
            response = st.session_state.chat_session.send_message(user_input)
            bot_response = response.text
            st.markdown(bot_response)
            
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
