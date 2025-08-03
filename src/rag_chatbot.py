import os
import logging
import pandas as pd
from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from src.config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WyckoffRAGChatbot:
    def __init__(self):
        """Initialize the Wyckoff RAG Chatbot with local embeddings"""
        logger.info("🚀 Initializing Wyckoff RAG Chatbot with local embeddings...")
        
        # Validate configuration
        Config.validate()
        
        # Initialize local embeddings
        logger.info(f"📥 Loading local embeddings model: {Config.EMBEDDINGS_MODEL}")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=Config.EMBEDDINGS_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Initialize Ollama LLM
        self.llm = Ollama(
            base_url=Config.OLLAMA_BASE_URL,
            model=Config.OLLAMA_MODEL,
            temperature=0.1
        )
        
        self.vector_store = None
        self.qa_chain = None
        
        # Load data and setup RAG
        self.setup_rag_system()
        
    def load_csv_data(self) -> List[Document]:
        """Load data from CSV files and convert to documents"""
        logger.info("📊 Loading CSV data...")
        all_docs = []
        
        try:
            # Load wyckoff_questions.csv
            if os.path.exists(Config.WYCKOFF_QUESTIONS_CSV):
                logger.info(f"📄 Loading {Config.WYCKOFF_QUESTIONS_CSV}")
                questions_df = pd.read_csv(Config.WYCKOFF_QUESTIONS_CSV)
                
                for _, row in questions_df.iterrows():
                    question = str(row.get('question', ''))
                    answer = str(row.get('answer', ''))
                    category = str(row.get('category', 'General'))
                    difficulty = str(row.get('difficulty', 'Intermediate'))
                    
                    if question and answer and question != 'nan' and answer != 'nan':
                        content = f"Category: {category}\nDifficulty: {difficulty}\nQuestion: {question}\nAnswer: {answer}"
                        doc = Document(
                            page_content=content,
                            metadata={
                                "source": "wyckoff_questions",
                                "category": category,
                                "difficulty": difficulty,
                                "type": "structured_qa"
                            }
                        )
                        all_docs.append(doc)
                
                logger.info(f"✅ Loaded {len(questions_df)} questions from wyckoff_questions.csv")
            else:
                logger.warning(f"⚠️ File not found: {Config.WYCKOFF_QUESTIONS_CSV}")
            
            # Load Wyckoff_Trading_Psychology_10000_QA.csv
            if os.path.exists(Config.WYCKOFF_QA_CSV):
                logger.info(f"📄 Loading {Config.WYCKOFF_QA_CSV}")
                qa_df = pd.read_csv(Config.WYCKOFF_QA_CSV)
                
                for _, row in qa_df.iterrows():
                    # Handle different possible column names
                    question = str(row.get('question', row.get('Question', '')))
                    answer = str(row.get('answer', row.get('Answer', '')))
                    
                    if question and answer and question != 'nan' and answer != 'nan':
                        content = f"Question: {question}\nAnswer: {answer}"
                        doc = Document(
                            page_content=content,
                            metadata={
                                "source": "wyckoff_qa_10000",
                                "type": "qa_pair"
                            }
                        )
                        all_docs.append(doc)
                
                logger.info(f"✅ Loaded {len(qa_df)} Q&A pairs from Wyckoff_Trading_Psychology_10000_QA.csv")
            else:
                logger.warning(f"⚠️ File not found: {Config.WYCKOFF_QA_CSV}")
            
            # If no CSV files found, create sample data
            if not all_docs:
                logger.warning("⚠️ No CSV files found. Creating sample data...")
                all_docs = self._create_sample_data()
            
            logger.info(f"📚 Total documents loaded: {len(all_docs)}")
            return all_docs
            
        except Exception as e:
            logger.error(f"❌ Error loading CSV data: {e}")
            # Return sample data as fallback
            return self._create_sample_data()
    
    def _create_sample_data(self) -> List[Document]:
        """Create sample Wyckoff data if CSV files are not available"""
        sample_data = [
            {
                "content": "Question: What are the three fundamental laws of Wyckoff?\nAnswer: The three fundamental laws are: 1) Law of Supply and Demand - price moves based on the relationship between supply and demand, 2) Law of Cause and Effect - accumulation/distribution phases create price movements, 3) Law of Effort vs Result - volume should confirm price movements.",
                "metadata": {"source": "sample", "category": "Basic Principles", "difficulty": "Beginner"}
            },
            {
                "content": "Question: How do you identify accumulation phases?\nAnswer: Accumulation phases are identified by: sideways price movement after a downtrend, decreasing volume on price declines, spring action (false breakdown), Sign of Strength (SOS), and Last Point of Support (LPS).",
                "metadata": {"source": "sample", "category": "Market Phases", "difficulty": "Intermediate"}
            },
            {
                "content": "Question: What is Volume Spread Analysis (VSA)?\nAnswer: VSA analyzes the relationship between volume, price spread (high-low range), and closing price position to determine market sentiment and identify smart money activity.",
                "metadata": {"source": "sample", "category": "Technical Analysis", "difficulty": "Advanced"}
            },
            {
                "content": "Question: What is the Wyckoff Method?\nAnswer: The Wyckoff Method is a technical analysis approach developed by Richard Wyckoff that focuses on understanding market structure through the analysis of price and volume to identify the activities of large institutional investors.",
                "metadata": {"source": "sample", "category": "Overview", "difficulty": "Beginner"}
            }
        ]
        
        docs = []
        for item in sample_data:
            doc = Document(page_content=item["content"], metadata=item["metadata"])
            docs.append(doc)
        
        logger.info(f"📝 Created {len(docs)} sample documents")
        return docs
    
    def setup_rag_system(self):
        """Setup the RAG system with vector store and QA chain"""
        try:
            # Load documents
            documents = self.load_csv_data()
            
            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=Config.CHUNK_SIZE,
                chunk_overlap=Config.CHUNK_OVERLAP,
                length_function=len,
            )
            
            splits = text_splitter.split_documents(documents)
            logger.info(f"📝 Created {len(splits)} text chunks")
            
            # Create vector store with local embeddings
            logger.info("🔄 Creating vector store with local embeddings...")
            self.vector_store = FAISS.from_documents(splits, self.embeddings)
            logger.info("✅ Vector store created successfully")
            
            # Setup QA chain with custom prompt
            prompt_template = """You are a Wyckoff trading methodology expert. Use the following context to answer the question about Wyckoff trading principles, market analysis, and trading psychology.

Context: {context}

Question: {question}

Instructions:
- Provide accurate, detailed answers based on Wyckoff methodology
- If the context doesn't contain enough information, say so clearly
- Include practical examples when relevant
- Focus on actionable trading insights
- Maintain a professional, educational tone

Answer:"""

            PROMPT = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )
            
            # Create QA chain
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vector_store.as_retriever(
                    search_kwargs={"k": Config.TOP_K_RESULTS}
                ),
                chain_type_kwargs={"prompt": PROMPT},
                return_source_documents=True
            )
            
            logger.info("✅ RAG system setup complete")
            
        except Exception as e:
            logger.error(f"❌ Error setting up RAG system: {e}")
            raise e
    
    def ask_question(self, question: str) -> Dict[str, Any]:
        """Ask a question and get an answer with sources"""
        try:
            logger.info(f"❓ Processing question: {question}")
            
            if not self.qa_chain:
                raise ValueError("QA chain not initialized")
            
            # Get answer from QA chain
            result = self.qa_chain({"query": question})
            
            # Extract source information
            sources = []
            for doc in result.get("source_documents", []):
                source_info = {
                    "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                    "metadata": doc.metadata
                }
                sources.append(source_info)
            
            response = {
                "answer": result["result"],
                "sources": sources,
                "question": question
            }
            
            logger.info("✅ Question processed successfully")
            return response
            
        except Exception as e:
            logger.error(f"❌ Error processing question: {e}")
            return {
                "answer": f"Sorry, I encountered an error: {str(e)}",
                "sources": [],
                "question": question
            }
    
    def get_similar_documents(self, query: str, k: int = 5) -> List[Document]:
        """Get similar documents for a query"""
        if not self.vector_store:
            return []
        
        try:
            docs = self.vector_store.similarity_search(query, k=k)
            return docs
        except Exception as e:
            logger.error(f"❌ Error retrieving similar documents: {e}")
            return []
