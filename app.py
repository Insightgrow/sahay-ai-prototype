import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
import PyPDF2

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_model():
    return genai.GenerativeModel('gemini-1.5-flash')

def extract_text_from_pdf(uploaded_file):
    if uploaded_file is not None:
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
            return text
        except Exception as e:
            st.error(f"Error reading PDF file: {e}")
            return None
    return None

st.set_page_config(page_title="Sahay AI Prototype", layout="wide")
st.title("Sahay AI: Your Legal Document Companion ⚖️")
st.write("Upload a legal document to get started. This prototype demonstrates key features of the Sahay AI solution.")

if 'document_text' not in st.session_state:
    st.session_state.document_text = ""
if 'summary' not in st.session_state:
    st.session_state.summary = ""
if 'explanation' not in st.session_state:
    st.session_state.explanation = ""
if 'ai_assistant_history' not in st.session_state:
    st.session_state.ai_assistant_history = []
if 'negotiation_history' not in st.session_state:
    st.session_state.negotiation_history = []
if 'risky_clause' not in st.session_state:
    st.session_state.risky_clause = ""

with st.sidebar:
    st.header("Upload Your Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if st.button("Process Document"):
        if uploaded_file is not None:
            with st.spinner("Reading and processing your document..."):
                st.session_state.document_text = ""
                st.session_state.summary = ""
                st.session_state.explanation = ""
                st.session_state.ai_assistant_history = []
                st.session_state.negotiation_history = []
                st.session_state.risky_clause = ""
                extracted_text = extract_text_from_pdf(uploaded_file)
                if extracted_text:
                    st.session_state.document_text = extracted_text
                    st.success("Document processed successfully!")
        else:
            st.warning("Please upload a PDF file first.")
if st.session_state.document_text:
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Document Viewer & Explainer", "🤖 AI Assistant (Chat)", "🤝 Negotiation Simulator", "📝 Summary"])
    with tab1:
        st.subheader("Document Content")
        st.text_area("Full Text", st.session_state.document_text, height=400)
        
        st.subheader("Highlight-to-Explain (Copy-Paste a Clause)")
        st.info("Copy any sentence or clause from the text above and paste it below for a simple explanation.")
        
        text_to_explain = st.text_input("Paste the text you want explained:")
        if st.button("Explain This Clause"):
            if text_to_explain:
                with st.spinner("AI is thinking..."):
                    model = get_gemini_model()
                    prompt = f"In simple, easy-to-understand terms, explain what this legal phrase means: '{text_to_explain}'"
                    response = model.generate_content(prompt)
                    st.session_state.explanation = response.text
            else:
                st.warning("Please paste some text to explain.")
        
        if st.session_state.explanation:
            st.success("Here's the explanation:")
            st.markdown(st.session_state.explanation)
    with tab4:
        st.subheader("Document Summary")
        if st.button("Generate Full Summary"):
            with st.spinner("Generating summary... This may take a moment."):
                model = get_gemini_model()
                prompt = f"Summarize the following legal document and list its key details (like names, dates, amounts) in a clear, structured way:\n\n{st.session_state.document_text}"
                response = model.generate_content(prompt)
                st.session_state.summary = response.text
        
        if st.session_state.summary:
            st.success("Summary Generated:")
            st.markdown(st.session_state.summary)
    with tab2:
        st.subheader("Chat with your AI Assistant")
        st.info("Ask any question about the document you uploaded.")
        for message in st.session_state.ai_assistant_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        if prompt := st.chat_input("What is your question?"):
            st.session_state.ai_assistant_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.spinner("AI is thinking..."):
                model = get_gemini_model()
                contextual_prompt = f"Based on the following document text, answer the user's question.\n\nDOCUMENT:\n{st.session_state.document_text}\n\nQUESTION:\n{prompt}"
                response = model.generate_content(contextual_prompt)
                ai_response = response.text
                st.session_state.ai_assistant_history.append({"role": "assistant", "content": ai_response})
                with st.chat_message("assistant"):
                    st.markdown(ai_response)

    with tab3:
        st.subheader("Practice Your Negotiation Skills")
        
        if not st.session_state.risky_clause:
            if st.button("Find a Risky Clause to Negotiate"):
                with st.spinner("AI is identifying a risky clause..."):
                    model = get_gemini_model()
                    prompt = f"From the following legal text, identify and quote one single clause that could be considered unfair, ambiguous, or risky for one of the parties. Quote the clause exactly as it appears in the text:\n\n{st.session_state.document_text}"
                    response = model.generate_content(prompt)
                    st.session_state.risky_clause = response.text
                    st.session_state.negotiation_history = [
                        {"role": "user", "parts": [f"System instruction: You are a landlord. The clause we are negotiating is: '{st.session_state.risky_clause}'. Be polite but firm. Start by greeting the user."]},
                        {"role": "model", "parts": ["Hello! I understand you wanted to discuss one of the clauses in the agreement. Which part is concerning you?"]}
                    ]
        else:
            st.warning(f"**Clause to Negotiate:** {st.session_state.risky_clause}")

            for message in st.session_state.negotiation_history[1:]:
                role = "assistant" if message["role"] == "model" else "user"
                with st.chat_message(role):
                    st.markdown(message["parts"][0])
            if prompt := st.chat_input("Type your response..."):
                st.session_state.negotiation_history.append({"role": "user", "parts": [prompt]})
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.spinner("Landlord is typing..."):
                    model = get_gemini_model()
                    chat = model.start_chat(history=st.session_state.negotiation_history)
                    response = chat.send_message(prompt)
                    ai_response = response.parts[0].text
                    
                    st.session_state.negotiation_history.append({"role": "model", "parts": [ai_response]})
                    with st.chat_message("assistant"):
                        st.markdown(ai_response)

else:
    st.info("Please upload and process a document in the sidebar to activate the features.")