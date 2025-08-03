#!/bin/bash

echo "🚀 Setting up Wyckoff Trading RAG Chatbot (Local Setup)..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create data directory
echo "📁 Creating data directory..."
mkdir -p data

# Copy environment file
echo "⚙️ Setting up environment..."
cp .env.example .env

# Install Ollama (macOS specific)
echo "🦙 Checking Ollama installation..."
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama for macOS..."
    echo "Please download and install Ollama from: https://ollama.ai/download"
    echo "Or install via Homebrew: brew install ollama"
    echo ""
    echo "After installing Ollama, run these commands manually:"
    echo "1. ollama serve"
    echo "2. ollama pull llama2"
    echo ""
    read -p "Press Enter after installing Ollama to continue..."
else
    echo "✅ Ollama is already installed"
    # Pull Ollama model
    echo "📥 Pulling Ollama model..."
    ollama pull llama2
fi

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Place your CSV files in the data/ directory:"
echo "   - wyckoff_questions.csv"
echo "   - Wyckoff_Trading_Psychology_10000_QA.csv"
echo "2. Start Ollama: ollama serve"
echo "3. Run: streamlit run src/app.py"
echo ""
echo "🎯 No OpenAI API key needed - using local embeddings!"
