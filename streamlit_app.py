import streamlit as st 
from sidebar import display_sidebar
from chat_interface import display_chat_interface

st.set_page_config(
    page_title="AngelOne RAG Chatbot",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("AngelOne RAG Chatbot")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = [] 

if "session_id" not in st.session_state:
    st.session_state.session_id = None 

if "scraping_done" not in st.session_state:
    st.session_state.scraping_done = False

# Display the sidebar
display_sidebar() 

# Display the chat interface 
display_chat_interface()