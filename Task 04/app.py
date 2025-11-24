import streamlit as st
from pypdf import PdfReader
import io
import requests
import json

# --- Configuration ---
# Assuming the Context7 MCP server will run locally and expose these endpoints
BACKEND_URL = "http://localhost:8000" # Adjust if your backend runs on a different port/host

# --- Helper Functions ---

def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from an uploaded PDF file.
    """
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_summary_from_gemini(text: str) -> str:
    """
    Sends text to the backend for summarization using Gemini.
    """
    st.info("Generating summary with Gemini...")
    try:
        response = requests.post(f"{BACKEND_URL}/summarize", json={"text": text})
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json().get("summary", "Could not retrieve summary.")
    except requests.exceptions.ConnectionError:
        st.error(f"Could not connect to the backend server at {BACKEND_URL}. Please ensure it is running.")
        return "Error: Backend server not reachable."
    except requests.exceptions.RequestException as e:
        st.error(f"Error during summarization request: {e}")
        return f"Error: {e}"

def generate_quiz_from_gemini(text: str) -> str:
    """
    Sends text to the backend for quiz generation using Gemini.
    """
    st.info("Generating quiz with Gemini...")
    try:
        response = requests.post(f"{BACKEND_URL}/generate_quiz", json={"text": text})
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json().get("quiz", "Could not generate quiz.")
    except requests.exceptions.ConnectionError:
        st.error(f"Could not connect to the backend server at {BACKEND_URL}. Please ensure it is running.")
        return "Error: Backend server not reachable."
    except requests.exceptions.RequestException as e:
        st.error(f"Error during quiz generation request: {e}")
        return f"Error: {e}"

# --- Streamlit UI ---
st.set_page_config(page_title="Study Notes Summarizer & Quiz Generator", layout="wide")

st.title("📚 Study Notes Summarizer & Quiz Generator")
st.markdown("Upload your PDF notes to get a concise summary and a practice quiz!")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.success("PDF uploaded successfully! Processing...")

    # Store the extracted text in session state to avoid re-extraction
    if "extracted_text" not in st.session_state:
        st.session_state.extracted_text = extract_text_from_pdf(uploaded_file)
        st.session_state.original_pdf_name = uploaded_file.name

    text = st.session_state.extracted_text

    if text:
        st.subheader(f"Summary for: {st.session_state.original_pdf_name}")
        
        # Only summarize if not already summarized or if user requests re-summary
        if "summary" not in st.session_state:
            st.session_state.summary = get_summary_from_gemini(text)
        
        if st.session_state.summary:
            st.write(st.session_state.summary)

        st.markdown("---")

        st.subheader("Quiz Time!")
        if st.button("Create Quiz"):
            # Only generate quiz if not already generated or if user requests re-generation
            if "quiz" not in st.session_state:
                st.session_state.quiz = generate_quiz_from_gemini(text)
            
            if st.session_state.quiz:
                st.write(st.session_state.quiz)
            else:
                st.warning("Quiz generation did not return any content.")
        elif "quiz" in st.session_state and st.session_state.quiz:
            # Display quiz if already generated
            st.write(st.session_state.quiz)
        else:
            st.info("Click 'Create Quiz' to generate a quiz from your notes.")
    else:
        st.error("Could not extract text from the PDF. Please ensure it's a readable PDF.")
else:
    st.info("Please upload a PDF file to get started.")
