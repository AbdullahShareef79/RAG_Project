from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from retriever import retrieve_documents, load_vector_store
from generator import ResponseGenerator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Load retriever and generator
try:
    retriever = load_vector_store("embeddings/")  # Load FAISS vector store
    generator = ResponseGenerator(model_name="facebook/opt-1.3b")
except Exception as e:
    logger.error(f"Failed to initialize retriever or generator: {e}")
    raise HTTPException(status_code=500, detail="Failed to initialize chatbot components.")

# Define request format
class QueryRequest(BaseModel):
    query: str

# Define response format
class Response(BaseModel):
    query: str
    retrieved_context: List[str]
    answer: str

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the GDPR RAG Chatbot! Use the /ask endpoint to query the chatbot."}

# Query endpoint
@app.post("/ask", response_model=Response)
async def ask_gdpr_bot(request: QueryRequest):
    try:
        # Retrieve relevant documents
        context = retrieve_documents(request.query, retriever)

        # Generate response
        answer = generator.generate_response(request.query, context)
        logger.info(f"Generated Answer: {answer}")

        return Response(query=request.query, retrieved_context=context, answer=answer)
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)