import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Ollama Configuration
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")
    
    # CSV File Paths
    WYCKOFF_QUESTIONS_CSV = os.getenv("WYCKOFF_QUESTIONS_CSV", "data/wyckoff_questions.csv")
    WYCKOFF_QA_CSV = os.getenv("WYCKOFF_QA_CSV", "data/Wyckoff_Trading_Psychology_10000_QA.csv")
    
    # Vector Store Configuration
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1500"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "300"))
    TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "5"))
    
    # Local Embeddings Model
    EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL", "all-MiniLM-L6-v2")
    
    # Streamlit Configuration
    STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", "8501"))
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        # No API key validation needed for local setup
        return True
