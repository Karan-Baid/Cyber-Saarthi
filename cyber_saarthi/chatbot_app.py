import streamlit as st
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

try:
    from cyber_saarthi.inference import CyberSaarthiModel
    INFERENCE_AVAILABLE = True
except ImportError as e:
    INFERENCE_AVAILABLE = False
    IMPORT_ERROR = str(e)


st.set_page_config(
    page_title="Cyber Saarthi - Indian Cyber Laws Chatbot",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .example-query {
        background-color: #f0f2f6;
        padding: 0.75rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .example-query:hover {
        background-color: #e0e2e6;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #1f77b4;
    }
    .bot-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
    }
    .disclaimer {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


EXAMPLE_QUERIES = [
    "What is Section 66C of the IT Act?",
    "What are the penalties for hacking in India?",
    "How do I report a cybercrime?",
    "Explain Section 43A about data protection",
    "What is identity theft under Indian cyber law?",
    "What is cyber terrorism according to Indian law?",
    "What are the privacy laws in India?",
    "What is CERT-In and what does it do?",
    "What are cybersecurity best practices for individuals?",
    "Can the government intercept online communications?",
]


@st.cache_resource
def load_model(model_path):
    if not INFERENCE_AVAILABLE:
        error_msg = f"""
        **Missing Dependencies**
        
        The required ML libraries are not installed. Error: `{IMPORT_ERROR}`
        
        **To fix this, you have two options:**
        
        **Option 1: Install Full Requirements (needs ~10GB disk space)**
        ```bash
        source saarthi_env/bin/activate
        pip install torch transformers peft bitsandbytes accelerate datasets
        ```
        
        **Option 2: Use this as a Demo**
        - The UI is working perfectly to demonstrate your project structure
        - The dataset (422 Q&A pairs) is fully generated in `data/`
        - For actual model training, use Google Colab with free GPU
        
        **For now, the chatbot interface is live to showcase the project!**
        """
        return None, error_msg
    
    try:
        model = CyberSaarthiModel(model_path)
        return model, None
    except Exception as e:
        return None, f"Error loading model: {str(e)}"


def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "model_loaded" not in st.session_state:
        st.session_state.model_loaded = False


def display_chat_history():
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 You:</strong><br/>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot-message">
                <strong>🛡️ Cyber Saarthi:</strong><br/>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)


def main():
    """Main application"""
    initialize_session_state()
    
    st.markdown('<div class="main-header">🛡️ Cyber Saarthi</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Your AI Guide to Indian Cyber Laws (IT Act 2000)</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="disclaimer">
        <strong>⚠️ Disclaimer:</strong> This chatbot is for educational purposes only. 
        While it provides information based on the IT Act 2000, it should not be considered 
        as legal advice. For actual legal matters, please consult qualified legal professionals.
    </div>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Use default model path
        model_path = "./models/cyber-saarthi/final"
        
        st.subheader("Generation Parameters")
        max_new_tokens = st.slider("Max Tokens", 128, 1024, 512, 64)
        temperature = st.slider("Temperature", 0.1, 2.0, 0.7, 0.1)
        top_p = st.slider("Top P", 0.1, 1.0, 0.9, 0.05)
        
        st.markdown("---")
        
        st.subheader("📖 About")
        st.markdown("""
        **Cyber Saarthi** is a fine-tuned LLM chatbot specialized in Indian cyber laws.
        
        **Coverage:**
        - IT Act 2000
        - Cybercrimes & Penalties
        - Data Protection
        - Privacy Laws
        - CERT-In Guidelines
        - Best Practices
        """)
        
        st.markdown("---")
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.repost()
        
        st.markdown("---")
        st.caption("Built with ❤️ using Hugging Face & Streamlit")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 Chat")
        
        if not st.session_state.model_loaded:
            with st.spinner("Loading Cyber Saarthi model..."):
                if os.path.exists(model_path):
                    model, error = load_model(model_path)
                    if model:
                        st.session_state.model = model
                        st.session_state.model_loaded = True
                        st.success("✅ Model loaded successfully!")
                    else:
                        st.error(f"❌ Error loading model: {error}")
                        st.stop()
                else:
                    st.error(f"❌ Model not found at: {model_path}")
                    st.info("""
                    **To use this chatbot:**
                    1. First generate the dataset: `python -m cyber_saarthi.dataset_generator`
                    2. Train the model: `python -m cyber_saarthi.fine_tune`
                    3. Then run this chatbot: `streamlit run cyber_saarthi/chatbot_app.py`
                    
                    **Alternative:** For demo purposes, you can use the base model without fine-tuning 
                    by setting the model path to a Hugging Face model ID.
                    """)
                    st.stop()
        
        display_chat_history()
        
        user_input = st.chat_input("Ask me about Indian cyber laws...")
        
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.model.generate(
                        instruction=user_input,
                        max_new_tokens=max_new_tokens,
                        temperature=temperature,
                        top_p=top_p,
                    )
                    
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    st.error(f"Error generating response: {e}")
            
            st.rerun()
    
    with col2:
        st.subheader("💡 Example Queries")
        st.markdown("Click on any example to try:")
        
        for i, query in enumerate(EXAMPLE_QUERIES):
            if st.button(query, key=f"example_{i}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": query})
                
                with st.spinner("Thinking..."):
                    try:
                        response = st.session_state.model.generate(
                            instruction=query,
                            max_new_tokens=max_new_tokens,
                            temperature=temperature,
                            top_p=top_p,
                        )
                        
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        
                    except Exception as e:
                        st.error(f"Error: {e}")
                
                st.rerun()
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>Dataset: 422 Q&A pairs covering IT Act 2000 | Model: Fine-tuned with QLoRA</p>
        <p>For questions or feedback, please open an issue on GitHub</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
