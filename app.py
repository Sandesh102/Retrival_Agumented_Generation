import os
import base64
import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from get_embedding_function import get_embedding_function
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables from .env
load_dotenv()

CHROMA_PATH = "chroma"
DATA_PATH = "data"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

# Streamlit Page Config
st.set_page_config(
    page_title="Sandesh AI Document Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Light Green & Mint Emerald Design System
st.markdown(
    """
<style>
    /* Main Gradient Header */
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #10B981 0%, #059669 50%, #047857 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.1rem;
        letter-spacing: -0.5px;
    }
    
    .sub-header {
        color: #047857;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 1.8rem;
    }
    
    /* Green Tech Badge */
    .tech-badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        font-size: 0.82rem;
        font-weight: 600;
        border-radius: 9999px;
        color: #047857;
        background-color: #D1FAE5;
        border: 1px solid #A7F3D0;
        margin-right: 0.4rem;
        margin-bottom: 0.5rem;
    }

    /* Light Green Answer Container */
    .answer-box {
        background-color: #ECFDF5;
        border-left: 5px solid #10B981;
        border-radius: 10px;
        padding: 1.4rem;
        color: #064E3B;
        font-size: 1.05rem;
        line-height: 1.6;
        box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.1);
        margin-top: 1rem;
        margin-bottom: 1.5rem;
    }

    /* Card styling */
    .doc-card {
        background: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.8rem;
    }
</style>
""",
    unsafe_allow_html=True,
)


def get_llm():
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    if gemini_key:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(
                model="gemini-3.6-flash",
                google_api_key=gemini_key,
                temperature=0.2,
            )
        except Exception:
            pass

    # Fallback to local Ollama if available
    try:
        from langchain_community.llms.ollama import Ollama
        return Ollama(model="mistral")
    except Exception as e:
        st.error(f"Failed to initialize LLM: {str(e)}")
        st.stop()


# Sidebar Configuration
with st.sidebar:
    st.markdown("### 🌿 Knowledge Base")
    st.caption("Pre-loaded Documents & System Status")

    # List Available Documents
    if os.path.exists(DATA_PATH):
        pdf_files = [f for f in os.listdir(DATA_PATH) if f.endswith(".pdf")]
    else:
        pdf_files = []

    if pdf_files:
        st.markdown(f"**Loaded Documents ({len(pdf_files)}):**")
        selected_pdf = st.selectbox("Select PDF to Preview:", pdf_files)
        
        # Display selected PDF file info
        pdf_path = os.path.join(DATA_PATH, selected_pdf)
        file_size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
        st.caption(f"📁 Size: `{file_size_mb:.2f} MB`")
    else:
        selected_pdf = None
        st.warning("No PDF documents found in data/ folder.")

    st.markdown("---")
    st.markdown("### 🛠 Architecture Details")
    st.markdown(
        """
    <span class="tech-badge">Embedding: FastEmbed (ONNX)</span>
    <span class="tech-badge">Vector DB: ChromaDB</span>
    <span class="tech-badge">LLM: Gemini 1.5 Flash</span>
    <span class="tech-badge">RAG Framework: LangChain</span>
    """,
        unsafe_allow_html=True,
    )
    
    st.markdown("---")
    st.caption("🔒 *Environment: Pre-indexed Knowledge Base (Read Only)*")


# Main Page Layout
st.markdown('<div class="main-header">Sandesh AI Bot</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Interactive Document Intelligence & Q&A Assistant grounded in verified text context.</div>',
    unsafe_allow_html=True,
)

# Tabs: [1] Document Viewer, [2] Ask Questions
tab1, tab2 = st.tabs(["📄 View PDF Document", "💬 Ask Questions (RAG)"])

# TAB 1: PDF DOCUMENT VIEWER
with tab1:
    st.subheader(f"📖 Document Reader: {selected_pdf if selected_pdf else 'No PDF Selected'}")
    if selected_pdf:
        pdf_path = os.path.join(DATA_PATH, selected_pdf)
        
        try:
            import pypdfium2 as pdfium
            pdf = pdfium.PdfDocument(pdf_path)
            total_pages = len(pdf)
            
            col_info, col_dl = st.columns([3, 1])
            with col_info:
                st.write(f"**Document**: `{selected_pdf}` ({total_pages} pages)")
            with col_dl:
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label=f"⬇️ Download PDF",
                        data=f.read(),
                        file_name=selected_pdf,
                        mime="application/pdf",
                        use_container_width=True,
                    )

            st.markdown("---")

            # Simple scrollable frame for all pages
            with st.container(height=750):
                for p_idx in range(total_pages):
                    st.caption(f"Page {p_idx + 1} of {total_pages}")
                    page = pdf[p_idx]
                    pil_img = page.render(scale=2.0).to_pil()
                    st.image(pil_img, use_container_width=True)
                    st.divider()
                
        except Exception as e:
            st.error(f"Error rendering PDF document: {str(e)}")
    else:
        st.info("Please place a PDF in the data/ folder to preview.")

# TAB 2: ASK QUESTIONS (RAG INTERFACE)
with tab2:
    st.subheader("💡 Ask Anything About the Document")
    
    # Suggested Sample Questions
    st.markdown("**Suggested Quick Questions:**")
    col1, col2 = st.columns(2)
    sample_query = ""
    with col1:
        if st.button("🤖 What is Artificial Intelligence?"):
            sample_query = "What is Artificial Intelligence?"
    with col2:
        if st.button("📊 Explain the key concepts of AI discussed in the document"):
            sample_query = "What are the main topics and key concepts discussed in this document?"

    user_query = st.text_input(
        "Enter your question:",
        value=sample_query,
        placeholder="e.g. What is machine learning or neural networks according to the document?",
    )

    if user_query:
        with st.spinner("Searching document vector store & generating response..."):
            try:
                embedding_function = get_embedding_function()
                db = Chroma(
                    persist_directory=CHROMA_PATH,
                    embedding_function=embedding_function,
                )

                # Search top 5 similarity results
                results = db.similarity_search_with_score(user_query, k=5)

                if not results:
                    st.warning("No relevant information found in the knowledge base.")
                else:
                    context_text = "\n\n---\n\n".join(
                        [doc.page_content for doc, _score in results]
                    )
                    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
                    prompt = prompt_template.format(
                        context=context_text, question=user_query
                    )

                    model = get_llm()
                    response = model.invoke(prompt)
                    
                    # Extract clean text string from LangChain response
                    if hasattr(response, "content"):
                        content = response.content
                        if isinstance(content, str):
                            response_text = content
                        elif isinstance(content, list):
                            text_parts = [item.get("text", str(item)) if isinstance(item, dict) else str(item) for item in content]
                            response_text = "\n".join(text_parts)
                        else:
                            response_text = str(content)
                    else:
                        response_text = str(response)

                    # Render AI Answer in Light Green Container
                    st.markdown("### 🌿 Answer:")
                    st.markdown(
                        f'<div class="answer-box">{response_text}</div>',
                        unsafe_allow_html=True,
                    )

                    # Source Citations
                    with st.expander("🔍 View Verified Source Citations & PDF Page Excerpts"):
                        for idx, (doc, score) in enumerate(results, 1):
                            source_id = doc.metadata.get("id", "Unknown Source")
                            page_num = doc.metadata.get("page", "N/A")
                            st.markdown(
                                f"**Source #{idx}** (`File/Page: {source_id}` | Similarity Score: `{score:.4f}`):"
                            )
                            st.info(doc.page_content)

            except Exception as e:
                st.error(f"Error processing query: {str(e)}")
