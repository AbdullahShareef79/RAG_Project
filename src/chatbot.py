import os
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from src.retriever import retrieve_documents, load_vector_store
from src.generator import ResponseGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory structure
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Serve static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Load Jinja2 templates
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Load retriever and generator
try:
    retriever = load_vector_store(os.path.join(BASE_DIR, "../embeddings"))  # Load FAISS vector store
    generator = ResponseGenerator(model_name="facebook/opt-1.3b")
except Exception as e:
    logger.error(f"Failed to initialize components: {e}")
    raise HTTPException(status_code=500, detail="Failed to initialize chatbot components.")

# Define request format
class QueryRequest(BaseModel):
    query: str

# Define response format
class Response(BaseModel):
    query: str
    retrieved_context: List[str]
    answer: str

# Home route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Chatbot query endpoint
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
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
