# 🌿 RAG Document Intelligence Assistant

An interactive Retrieval-Augmented Generation (RAG) web application designed for automated document analysis and Q&A. Powered by **Google Gemini 3.6 Flash**, **ChromaDB** vector storage, **FastEmbed** ONNX embeddings, and **Streamlit**.

---

## ✨ Key Features
- **📄 Interactive PDF Viewer**: Read and inspect pre-loaded PDF documents in an embedded, high-resolution scrollable reader.
- **💬 Grounded AI Q&A**: Ask natural language questions with answers strictly grounded in document context.
- **🔍 Verified Citations**: Inspect exact page excerpts and similarity scores for full transparency.
- **⚡ High Performance**: FastEmbed ONNX local embeddings paired with Google Gemini 3.6 Flash API.
- **🎨 Modern Mint UI**: Styled with Streamlit in a clean, light emerald theme.

---

## 🛠️ Tech Stack
- **Frontend**: Streamlit
- **LLM Provider**: Google Gemini API (`gemini-3.6-flash`)
- **Framework**: LangChain
- **Embeddings**: FastEmbed (`nomic-ai/nomic-embed-text-v1.5`)
- **Vector Database**: ChromaDB
- **PDF Renderer**: PyPDFium2

---

## 🚀 Quickstart Guide (Local Setup)

Follow these steps to clone and run the application locally on your machine.

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2. Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add your Google Gemini API Key (get a free key at [aistudio.google.com](https://aistudio.google.com/)):

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Add PDFs & Index Database
Place your PDF files inside the `data/` folder, then build the vector index:

```bash
python3 populate_database.py --reset
```

### 6. Run the Streamlit Web Application
```bash
streamlit run app.py
```

Open your browser and navigate to **`http://localhost:8501`**.

---

## 📜 License
This project is open source and available under the [MIT License](LICENSE).
