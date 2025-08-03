# Wyckoff Trading RAG Chatbot 📈🤖

An intelligent RAG (Retrieval-Augmented Generation) chatbot specialized in Wyckoff trading methodology, powered by your CSV knowledge bases.

## 🚀 Features

- **CSV Knowledge Base Integration**: Uses your `wyckoff_questions.csv` and `Wyckoff_Trading_Psychology_10000_QA.csv`
- **Semantic Search**: Vector-based retrieval for accurate responses
- **Local LLM Support**: Runs with Ollama (llama2, mistral, etc.)
- **Streamlit UI**: Clean, interactive web interface
- **Real-time Chat**: Conversational interface with chat history

## 📊 Knowledge Base

- **wyckoff_questions.csv**: Categorized questions with difficulty levels
- **Wyckoff_Trading_Psychology_10000_QA.csv**: 10,000 Q&A pairs on Wyckoff methodology

## 🛠️ Installation

```bash
# Clone repository
git clone <your-repo-url>
cd GenAI-RAG-chatbot

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your API keys and file paths

# Place CSV files in data/ directory
mkdir -p data
cp "path/to/wyckoff_questions.csv" data/
cp "path/to/Wyckoff_Trading_Psychology_10000_QA.csv" data/

# Install and start Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama2

# Run the application
streamlit run src/app.py
```

## 🔧 Configuration

Update `.env` file with your settings:
- OpenAI API key for embeddings
- CSV file paths
- Ollama model preferences

## 📖 Usage

1. Start the Streamlit app
2. Ask questions about Wyckoff trading methodology
3. Get AI-powered responses based on your CSV knowledge base
4. View source references for transparency

## 🎯 Example Questions

- "What are the three fundamental laws of Wyckoff?"
- "How do you identify accumulation phases?"
- "Explain volume spread analysis in Wyckoff method"