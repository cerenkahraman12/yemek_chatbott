import streamlit as st
from qa_local import MealChatbotLocal as MealChatbot

st.set_page_config(page_title="Yemek Chatbot 🍽️", layout="centered")
st.title("🍽️ Yemek Öneri Chatbot (Gemini + RAG)")

bot = MealChatbot()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Ne yemek istersin? (örn: vegan, akşam yemeği, düşük kalorili...)")

if user_input:
    st.session_state.chat_history.append(("Kullanıcı", user_input))
    with st.spinner("Düşünüyorum..."):
        answer = bot.ask(user_input)
    st.session_state.chat_history.append(("Bot", answer))

for sender, msg in st.session_state.chat_history:
    if sender == "Kullanıcı":
        st.chat_message("user").write(msg)
    else:
        st.chat_message("assistant").write(msg)
