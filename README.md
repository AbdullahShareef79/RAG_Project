# GDPR RAG Chatbot

A **Retrieval-Augmented Generation (RAG) chatbot** designed for answering GDPR-related queries using **FastAPI**, **FAISS**, and **Facebook OPT**.

## 🚀 Features
- **FastAPI** for a high-performance backend.
- **FAISS** for efficient document retrieval.
- **Facebook OPT-1.3B** as the language model for response generation.
- **Jinja2 & HTML** for a simple web-based chatbot interface.
- **GDPR-focused Q&A** with retrieval-augmented responses.
- **CORS-enabled** for flexibility in frontend integration.

---

## 📦 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-repo/gdpr-rag-chatbot.git
cd gdpr-rag-chatbot
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Download Model & Data
Ensure that the **FAISS vector store** and **GDPR-related documents** are stored in the `embeddings` folder.
If not, you may need to preprocess documents and generate embeddings manually.

### 5️⃣ Run the Chatbot
```bash
uvicorn src.chatbot:app --host 127.0.0.1 --port 8000 --reload
```

---

## 🔧 Project Structure
```
📂 gdpr-rag-chatbot
│── 📂 src
│   │── chatbot.py       # FastAPI chatbot backend
│   │── retriever.py     # FAISS-based document retriever
│   │── generator.py     # Response generator using Facebook OPT
│   │── templates/       # HTML templates for UI
│── 📂 static            # Static assets (CSS, JS)
│── 📂 embeddings        # FAISS vector store
│── requirements.txt     # Python dependencies
│── README.md            # This file
```

---

## 🎯 How It Works
1. **User asks a question** via the web interface.
2. **Retriever** searches for relevant GDPR documents using FAISS.
3. **Generator** (Facebook OPT-1.3B) formulates a response using retrieved documents.
4. **Response** is displayed on the chatbot UI.

---

## 📌 API Endpoints

### 🔹 **Home Page**
- **`GET /`** → Returns the chatbot UI (HTML page).

### 🔹 **Chatbot Query**
- **`POST /ask`**
  - **Request Body:** `{ "query": "What is GDPR compliance?" }`
  - **Response:** `{ "query": "...", "retrieved_context": [...], "answer": "..." }`

---

## 🛠 Troubleshooting
- **ModuleNotFoundError:** Ensure you are running in the correct virtual environment.
- **Missing FAISS Index:** Re-run document preprocessing to generate embeddings.
- **CORS Issues:** Modify `allow_origins` in `chatbot.py`.

---

## 🤝 Contributing
Feel free to **fork**, **contribute**, or **open issues** to enhance the chatbot.

---

## 📜 License
This project is open-source and licensed under the **MIT License**.

---

🚀 **Happy Coding!**

