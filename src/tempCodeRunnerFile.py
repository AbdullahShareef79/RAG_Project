import pdfplumber
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load the GDPR PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# Clean text (remove extra spaces, line breaks, etc.)
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    text = text.strip()
    return text

# Chunk text into smaller sections for retrieval
def chunk_text(text, chunk_size=1000, chunk_overlap=100):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, separators=["\n", ". ", "? ", "! "]
    )
    chunks = text_splitter.split_text(text)
    return chunks

if __name__ == "__main__":
    pdf_path = "E:/RAG_Project/data/CELEX_32016R0679_EN_TXT.pdf"  
    raw_text = extract_text_from_pdf(pdf_path)
    cleaned_text = clean_text(raw_text)
    text_chunks = chunk_text(cleaned_text)
    
    print(f"Extracted {len(text_chunks)} chunks from the GDPR document.")
