#!/bin/bash

echo "🚀 Starting Wyckoff Trading RAG Chatbot..."

# Activate virtual environment
source venv/bin/activate

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "🦙 Starting Ollama..."
    ollama serve &
    sleep 5
fi

# Start Streamlit app
echo "🌐 Starting Streamlit app..."
streamlit run src/app.py --server.port 8501