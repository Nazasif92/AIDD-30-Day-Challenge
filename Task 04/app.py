import streamlit as st
from pypdf import PdfReader
import google.generativeai as genai

# -------------------------
# CONFIGURE GEMINI
# -------------------------
# Add your Gemini API key
GENAI_API_KEY = st.secrets["MY_API_KEY"]

genai.configure(api_key=GENAI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# -------------------------
# PDF TEXT EXTRACTOR
# -------------------------
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PdfReader(uploaded_file)
    return "".join(page.extract_text() or "" for page in pdf_reader.pages)

# -------------------------
# SUMMARY DIRECT FROM GEMINI
# -------------------------
def get_summary_from_gemini(text):
    st.info("Generating summary using Gemini model...")
    prompt = f"Summarize the following study notes in simple language:\n\n{text}"
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# -------------------------
# QUIZ DIRECT FROM GEMINI
# -------------------------
def generate_quiz_from_gemini(text):
    st.info("Generating quiz using Gemini model...")
    prompt = (
        "Create a 5-question MCQ quiz from the following text. "
        "Include 4 options for each and mark the correct answer.\n\n"
        f"{text}"
    )
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# -------------------------
# STREAMLIT UI
# -------------------------
st.set_page_config(page_title="Study Notes Summarizer & Quiz Generator", layout="wide")

st.title("📚 Study Notes Summarizer & Quiz Generator")
st.markdown("Upload your PDF notes to get a summary + quiz directly from **Gemini** (no backend needed).")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    st.success("PDF uploaded successfully!")

    if "extracted_text" not in st.session_state:
        st.session_state.extracted_text = extract_text_from_pdf(uploaded_file)
        st.session_state.original_pdf_name = uploaded_file.name

    text = st.session_state.extracted_text

    if text.strip():
        st.subheader(f"Summary ({st.session_state.original_pdf_name})")

        if "summary" not in st.session_state:
            st.session_state.summary = get_summary_from_gemini(text)

        st.write(st.session_state.summary)

        st.markdown("---")

        st.subheader("Quiz Generator")

        if st.button("Generate Quiz"):
            st.session_state.quiz = generate_quiz_from_gemini(text)

        if "quiz" in st.session_state:
            st.write(st.session_state.quiz)

    else:
        st.error("Could not extract text. Make sure the PDF is not scanned or image-only.")
else:
    st.info("Please upload a PDF to begin.")
