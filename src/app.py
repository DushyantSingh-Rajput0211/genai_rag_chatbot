import streamlit as st
import logging
from datetime import datetime
from src.rag_chatbot import WyckoffRAGChatbot
from src.config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Wyckoff Trading RAG Chatbot",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #1f77b4;
    }
    .user-message {
        background-color: #edf2f7;
        border-left-color: #ff6b6b;
        color: #2d3748;
        border: 1px solid #e2e8f0;
    }
    .bot-message {
        background-color: #f7fafc;
        border-left-color: #1f77b4;
        color: #2d3748;
        border: 1px solid #e2e8f0;
    }
    .source-box {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 0.25rem;
        padding: 0.75rem;
        margin-top: 0.5rem;
        font-size: 0.875rem;
    }
    .stButton > button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        border: none;
        border-radius: 0.25rem;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #1565c0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_chatbot():
    """Initialize the chatbot (cached for performance)"""
    try:
        with st.spinner("🚀 Initializing Wyckoff RAG Chatbot with local embeddings..."):
            chatbot = WyckoffRAGChatbot()
        st.success("✅ Chatbot initialized successfully with local embeddings!")
        return chatbot
    except Exception as e:
        st.error(f"❌ Failed to initialize chatbot: {str(e)}")
        return None

def display_chat_message(message, is_user=False):
    """Display a chat message with styling"""
    css_class = "user-message" if is_user else "bot-message"
    icon = "🧑" if is_user else "🤖"
    
    st.markdown(f"""
    <div class="chat-message {css_class}">
        <strong>{icon} {'You' if is_user else 'Wyckoff Bot'}:</strong><br>
        {message}
    </div>
    """, unsafe_allow_html=True)

def display_sources(sources):
    """Display source documents"""
    if sources:
        st.markdown("**📚 Sources:**")
        for i, source in enumerate(sources, 1):
            with st.expander(f"Source {i} - {source['metadata'].get('source', 'Unknown')}"):
                st.markdown(f"**Content:** {source['content']}")
                st.markdown(f"**Metadata:** {source['metadata']}")

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<h1 class="main-header">📈 Wyckoff Trading RAG Chatbot 🤖</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # Display configuration info
        st.info(f"""
        **Model:** {Config.OLLAMA_MODEL}
        **Embeddings:** {Config.EMBEDDINGS_MODEL} (Local)
        **CSV Files:**
        - wyckoff_questions.csv
        - Wyckoff_Trading_Psychology_10000_QA.csv
        """)
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        
        # Example questions
        st.header("💡 Example Questions")
        example_questions = [
            "What are the three fundamental laws of Wyckoff?",
            "How do you identify accumulation phases?",
            "Explain volume spread analysis",
            "What is the difference between accumulation and distribution?",
            "How do you spot smart money activity?",
            "What is a spring in Wyckoff analysis?",
            "Explain the concept of effort vs result"
        ]
        
        for question in example_questions:
            if st.button(question, key=f"example_{hash(question)}"):
                st.session_state.messages.append({"role": "user", "content": question})
                st.rerun()
    
    # Initialize chatbot
    chatbot = initialize_chatbot()
    
    if not chatbot:
        st.error("❌ Cannot proceed without a working chatbot. Please check your configuration and ensure Ollama is running.")
        st.info("💡 Make sure to run: `ollama serve` and `ollama pull llama2`")
        return
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        display_chat_message(message["content"], message["role"] == "user")
        
        if message["role"] == "assistant" and "sources" in message:
            display_sources(message["sources"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about Wyckoff trading methodology..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        display_chat_message(prompt, is_user=True)
        
        # Get bot response
        with st.spinner("🤔 Thinking..."):
            try:
                response = chatbot.ask_question(prompt)
                
                # Add assistant response to chat history
                assistant_message = {
                    "role": "assistant", 
                    "content": response["answer"],
                    "sources": response["sources"]
                }
                st.session_state.messages.append(assistant_message)
                
                # Display response
                display_chat_message(response["answer"])
                display_sources(response["sources"])
                
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                display_chat_message(error_msg)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.875rem;">
        🚀 Powered by Local Embeddings & Wyckoff CSV Knowledge Base | Built with Streamlit & LangChain
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
