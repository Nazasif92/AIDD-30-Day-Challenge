# 📘 Task — Build the Study Notes Summarizer & Quiz Generator Agent

Build an AI agent using the following technologies:

- **OpenAgents SDK**
- **Streamlit** (recommended for UI)
- **PyPDF** (for extracting PDF text)
- **Gemini CLI**
- **Context7 MCP Server** (as the tool provider)

---

## 🎯 Agent Requirements

### A. PDF Summarizer

The agent must:

- Allow the user to upload a PDF file
- Extract text using **PyPDF**
- Send the text to the agent through **Gemini CLI + Context7 MCP**
- Generate a clean, meaningful, structured summary
- Display the summary in any UI style (card, block, container, etc.)

---

### B. Quiz Generator

After showing the summary:

- Display a button **Create Quiz**
- When clicked:
  - The agent will use the **original extracted PDF text**
  - Generate:
    - **Multiple Choice Questions (MCQs)**, or
    - **Mixed-style quiz questions**

---

## 🛠 Expected Output

The agent must:

- Process PDFs with PyPDF
- Summarize the PDF content
- Generate quizzes from the original text
- Use **Gemini CLI** integrated with **Context7 MCP**
- Provide a user-friendly Streamlit interface

---

## ✔️ Your Task

Create a complete working agent that performs:

1. **PDF Summarization**
2. **Quiz Generation**

Use best coding practices, clean UI, and follow the above requirements.

