import pdfplumber
import re
import json
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Extract text from GDPR PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
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
    # Define paths
    pdf_path = os.path.join(os.path.dirname(__file__), "../data/CELEX_32016R0679_EN_TXT.pdf")
    output_path = os.path.join(os.path.dirname(__file__), "../data/processed_text.json")
    
    # Extract and process text
    raw_text = extract_text_from_pdf(pdf_path)
    cleaned_text = clean_text(raw_text)
    text_chunks = chunk_text(cleaned_text)
    
    # Save processed text chunks to JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(text_chunks, f, ensure_ascii=False, indent=4)
    
    print(f"✅ Extracted {len(text_chunks)} chunks from the GDPR document.")
    print(f"✅ Saved processed text to {output_path}")
