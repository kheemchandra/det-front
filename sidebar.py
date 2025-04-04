import streamlit as st 
from api_utils import upload_document, list_documents, delete_document
import requests
from dotenv import load_dotenv
import os

load_dotenv()

BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")


def display_sidebar():
    # Model selection 
    model_options = ['gemini-2.0-flash', 'gemini-2.5-pro-exp-03-25']
    st.sidebar.selectbox('Select Model', options=model_options, key='model')

    # Document upload 
    uploaded_file = st.sidebar.file_uploader('Choose a file', type=['pdf', 'docx', 'html'])
    if uploaded_file and st.sidebar.button('Upload'):
        with st.spinner('Uploading...'):
            upload_response = upload_document(uploaded_file)
            if upload_response:
                st.sidebar.success(f"File uploaded successfully with ID {upload_response['file_id']}.")
                st.session_state.documents = list_documents()

    # List and delete documents 
    st.sidebar.header('Uploaded Documents')
    if st.sidebar.button('Refresh Document List'):
        st.session_state.documents = list_documents()

    # Display document list and delete functionality 
    if "documents" in st.session_state and st.session_state.documents:
        for doc in st.session_state.documents:
            st.sidebar.text(f"{doc['filename']} (ID: {doc['id']})")
        
        selected_file_id = st.sidebar.selectbox("Select a document to delete",  
                                                options=[doc['id'] for doc in st.session_state.documents])
        if st.sidebar.button("Delete Selected Document"):
            delete_response = delete_document(selected_file_id)
            if delete_response:
                st.sidebar.success(f"Document deleted successfully.")
                st.session_state.documents = list_documents()

    # Add Web Scraping Section
    st.sidebar.markdown("---")
    st.sidebar.subheader("Knowledge Base Management")
    
    # Initialize session state for scraping status
    if "scraping_done" not in st.session_state:
        st.session_state.scraping_done = False
    if "scraping_in_progress" not in st.session_state:
        st.session_state.scraping_in_progress = False
    
    # Function to call the scraping API
    def start_scraping():
        st.session_state.scraping_in_progress = True
        try:
            with st.sidebar.status("Scraping FAQs from Angel One support..."):
                response = requests.post(
                    f"{BACKEND_API_URL}/scrape-faqs",
                    json={"base_url": "https://www.angelone.in/support/"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.scraping_done = True
                    st.sidebar.success(f"✅ {result['message']}")
                    # Store the file IDs of scraped documents
                    st.session_state.scraped_file_ids = result.get('file_ids', [])
                else:
                    st.sidebar.error(f"❌ Error: {response.text}")
        except Exception as e:
            st.sidebar.error(f"❌ Error: {str(e)}")
        finally:
            st.session_state.scraping_in_progress = False
    
    # Show different UI based on scraping status
    if st.session_state.scraping_done:
        st.sidebar.success("✅ FAQ data has been scraped and indexed")
        if st.sidebar.button("Scrape Again"):
            start_scraping()
    else:
        scrape_button = st.sidebar.button(
            "Scrape Angel One FAQs",
            disabled=st.session_state.scraping_in_progress
        )
        if scrape_button:
            start_scraping()