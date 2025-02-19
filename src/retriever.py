from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the processed text chunks
def load_text_chunks(file_path):
    """
    Load processed text chunks from a JSON file.
    :param file_path: Path to the JSON file.
    :return: List of text chunks.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load text chunks: {e}")
        raise

# Create and save the FAISS vector store
def create_vector_database(chunks, persist_directory="embeddings/"):
    """
    Create a FAISS vector store from text chunks and save it to disk.
    :param chunks: List of text chunks.
    :param persist_directory: Directory to save the FAISS database.
    """
    try:
        embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_db = FAISS.from_texts(chunks, embeddings_model)
        vector_db.save_local(persist_directory)
        logger.info("✅ Embeddings saved successfully!")
    except Exception as e:
        logger.error(f"Failed to create vector database: {e}")
        raise

# Load FAISS vector store
def load_vector_store(persist_directory="embeddings/"):
    """
    Load the FAISS vector store from the given directory.
    :param persist_directory: Path to the FAISS database.
    :return: Loaded FAISS retriever.
    """
    try:
        embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        retriever = FAISS.load_local(persist_directory, embeddings=embeddings_model, allow_dangerous_deserialization=True)
        return retriever
    except Exception as e:
        logger.error(f"Failed to load vector store: {e}")
        raise

# Retrieve top-k relevant documents
def retrieve_documents(query, retriever, top_k=5):
    """
    Retrieve relevant documents using FAISS similarity search.
    :param query: User query string.
    :param retriever: Loaded FAISS retriever.
    :param top_k: Number of top results to return.
    :return: List of retrieved text chunks.
    """
    try:
        docs = retriever.similarity_search(query, k=top_k)
        return [doc.page_content for doc in docs]
    except Exception as e:
        logger.error(f"Failed to retrieve documents: {e}")
        raise