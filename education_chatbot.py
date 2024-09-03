import os
import streamlit as st
import google.generativeai as genai

# Streamlit page configuration
st.set_page_config(page_title="Education Chatbot", page_icon=":robot:")


api_key = st.secrets["GEMINI_API_KEY"]

# Configure the Gemini API using the API key
genai.configure(api_key=api_key)

# Model configuration
generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 50,
    "max_output_tokens": 1000,
    "response_mime_type": "text/plain",
}

# Initialize the Generative Model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Function to ask a question and get the model response
def ask_education_question(question):
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(question)
    return response.text

# Streamlit UI
st.title("AI Education Chatbot")
st.write("Ask me any educational question!")

# Input form
user_question = st.text_input("Your Question", placeholder="Enter your question about any educational topic here...")
if st.button("Ask"):
    if user_question:
        with st.spinner('Thinking...'):
            answer = ask_education_question(user_question)
        st.write(f"**Bot:** {answer}")
    else:
        st.warning("Please enter a question before asking.")

# Sidebar for model settings (optional)
st.sidebar.title("Settings")
temperature = st.sidebar.slider("Temperature (randomness)", 0.1, 1.0, 0.7)
top_p = st.sidebar.slider("Top P (nucleus sampling)", 0.1, 1.0, 0.9)
top_k = st.sidebar.slider("Top K (token consideration)", 10, 100, 50)

# Update model configuration dynamically
generation_config.update({
    "temperature": temperature,
    "top_p": top_p,
    "top_k": top_k,
})
