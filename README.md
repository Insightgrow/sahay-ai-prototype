# Sahay AI - AI-Powered Legal Companion

**Sahay AI** is a Gen AI-powered companion that translates complex contracts into simple language, proactively highlights hidden risks, and even provides an AI simulator to practice negotiations to make legal processes safe and accessible for everyone. It tackles the widespread problem of intimidating legal documents that expose millions to hidden risks. 

What sets Sahay AI apart is its proactive approach: it automatically flags unfair clauses and empowers users with a first-of-its-kind "AI Negotiation Simulator" to practice handling these issues with confidence. It has been built with Python, React, and Google's Vertex AI (Gemini).

---

## Live Demo 

* **Live Prototype Link:** https://sahay-ai-prototype-zd3yxhgj2qhz8bt4sg5w7j.streamlit.app/
---

## Key Features

The proposed solution is designed to provide end-to-end support for navigating legal documents.

* **Guided Legal Journeys:** Provides pre-built "Journey Templates" for specific legal goals (e.g., Rent Agreements).
* **Multi-format Document Upload:** Users can upload PDFs to be processed. `(Implemented in Prototype)`
* **Instant Explanation:** Copy-paste a clause to get a simple, real-time explanation. `(Implemented in Prototype)`
* **Full Document Summarization:** Generate a concise summary and list of key details with one click. `(Implemented in Prototype)`
* **Context-Aware AI Assistant:** Chat with an AI that understands the context of your document to answer any question. `(Implemented in Prototype)`
* **AI Negotiation Simulator:** Practice handling difficult conversations in a safe, simulated environment with an AI persona. `(Implemented in Prototype)`
---

## Technology Stack

* **Frontend:** React, Next.js
* **Backend:** Python, FastAPI
* **AI/ML:** Google Vertex AI (Gemini), LangChain
* **Databases:** PostgreSQL, Firestore, Vertex AI Vector Search
* **Cloud Services:** Firebase Authentication, Google Cloud Storage, Cloud Functions
* **Prototype:** The prototype is built with **Streamlit** for rapid development.

---

## How to Use the Prototype

1.  **Upload a Document:** Use the sidebar to upload a legal document in PDF format.
2.  **Process:** Click the "Process Document" button.
3.  **Interact:** Once processed, use the tabs on the main screen to:
    * **View & Explain:** Copy-paste a clause to get a simple explanation.
    * **Get a Summary:** Generate a full summary of the document.
    * **Chat with AI Assistant:** Ask any question about the document.
    * **Simulate Negotiation:** Find a risky clause and practice your negotiation skills with an AI persona.
