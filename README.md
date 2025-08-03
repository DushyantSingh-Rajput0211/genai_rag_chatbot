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

### Prerequisites
- Python 3.8+ installed
- Git installed
- 4GB+ RAM recommended

### Step-by-Step Setup

```bash
# 1. Clone repository
git clone https://github.com/DushyantSingh-Rajput0211/genai_rag_chatbot.git
cd genai_rag_chatbot

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Windows Command Prompt:
venv\Scripts\activate.bat

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment variables
cp .env.example .env
# Edit .env file with your settings (optional - works with defaults)

# 6. Create data directory and add CSV files
mkdir -p data
# Place your CSV files:
# - wyckoff_questions.csv
# - Wyckoff_Trading_Psychology_10000_QA.csv

# 7. Install and start Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama2

# 8. Run the application
PYTHONPATH=. streamlit run src/app.py
```

## 📊 **CSV Data Files**

**Important:** You need to provide your own CSV files in the `data/` directory:
- `wyckoff_questions.csv` - Categorized questions with difficulty levels
- `Wyckoff_Trading_Psychology_10000_QA.csv` - 10,000 Q&A pairs

**CSV Format Expected:**
```csv
question,answer,category,difficulty
"What are Wyckoff's laws?","The three laws are...","fundamentals","beginner"
```

## 🔧 **Troubleshooting**

### Common Issues:
1. **ModuleNotFoundError: No module named 'src'**
   ```bash
   # Run with PYTHONPATH
   PYTHONPATH=. streamlit run src/app.py
   ```

2. **Ollama not found**
   ```bash
   # Start Ollama service
   ollama serve
   # In another terminal, pull model
   ollama pull llama2
   ```

3. **CSV files not found**
   - Ensure CSV files are in `data/` directory
   - Check file names match exactly

## 🎯 **Quick Start (Alternative)**
```bash
# Use the setup script
chmod +x scripts/setup.sh
./scripts/setup.sh

# Use the run script
chmod +x scripts/run.sh
./scripts/run.sh
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
