import streamlit as st
import os
from core.main import RagSystem
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="RAG Knowledge Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stat-box {
        background-color: #1f77b4;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .source-box {
        background-color:  #1f77b4;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    .answer-box {
        background-color:  #1f77b4;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'rag_system' not in st.session_state:
    with st.spinner("🔄 Initializing RAG system..."):
        try:
            st.session_state.rag_system = RagSystem()
            st.session_state.initialized = True
        except Exception as e:
            st.error(f"❌ Error initializing system: {e}")
            st.session_state.initialized = False

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Header
st.markdown('<h1 class="main-header">🤖 RAG Knowledge Assistant</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📁 Document Management")
    
    # Upload documents
    uploaded_files = st.file_uploader(
        "Upload Documents",
        type=['pdf', 'docx', 'doc', 'txt'],
        accept_multiple_files=True,
        help="Upload PDF, DOCX, DOC, or TXT files"
    )
    
    if uploaded_files:
        if st.button("📤 Process Uploaded Files", type="primary"):
            with st.spinner("Processing documents..."):
                for uploaded_file in uploaded_files:
                    # Save to temp directory
                    temp_path = f"temp_{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Add to RAG system
                    success = st.session_state.rag_system.add_document(temp_path)
                    
                    if success:
                        st.success(f"✅ {uploaded_file.name}")
                    else:
                        st.error(f"❌ Failed: {uploaded_file.name}")
                    
                    # Clean up
                    os.remove(temp_path)
    
    st.divider()
    
    # System statistics
    st.header("📊 System Stats")
    
    if st.session_state.initialized:
        stats = st.session_state.rag_system.get_stats()
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="stat-box">
                <h3>{stats.get('total_files', 0)}</h3>
                <p>Documents</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-box">
                <h3>{stats.get('total_chunks', 0)}</h3>
                <p>Chunks</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Show indexed files
        if stats.get('indexed_files'):
            with st.expander("📋 Indexed Files"):
                for i, file in enumerate(stats['indexed_files'], 1):
                    st.text(f"{i}. {Path(file).name}")
    
    st.divider()
    
    # Settings
    st.header("⚙️ Settings")
    top_k = st.slider("Number of sources", 1, 10, 4)
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# Main area - Q&A
st.header("💬 Ask Questions")

# Display chat history
for chat in st.session_state.chat_history:
    # User question
    with st.chat_message("user"):
        st.write(chat['question'])
    
    # Assistant answer
    with st.chat_message("assistant"):
        st.markdown(f'<div class="answer-box">{chat["answer"]}</div>', unsafe_allow_html=True)
        
        # Show sources
        if chat.get('sources'):
            with st.expander(f"📚 Sources ({len(chat['sources'])})"):
                for i, source in enumerate(chat['sources'], 1):
                    st.markdown(f"""
                    <div class="source-box">
                        <strong>Source {i}: {source['filename']}</strong><br>
                        Page: {source['page']} | Chunk: {source['chunk_id']}<br>
                        <em>{source['content'][:150]}...</em>
                    </div>
                    """, unsafe_allow_html=True)

# Question input
if st.session_state.initialized:
    question = st.chat_input("Ask a question about your documents...")
    
    if question:
        # Add user message
        with st.chat_message("user"):
            st.write(question)
        
        # Get answer
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                result = st.session_state.rag_system.ask_with_sources(question, top_k=top_k)
                
                # Display answer
                st.markdown(f'<div class="answer-box">{result["answer"]}</div>', unsafe_allow_html=True)
                
                # Display sources
                if result.get('sources'):
                    with st.expander(f"📚 Sources ({len(result['sources'])})"):
                        for i, source in enumerate(result['sources'], 1):
                            st.markdown(f"""
                            <div class="source-box">
                                <strong>Source {i}: {source['filename']}</strong><br>
                                Page: {source['page']} | Chunk: {source['chunk_id']}<br>
                                <em>{source['content'][:150]}...</em>
                            </div>
                            """, unsafe_allow_html=True)
        
        # Save to history
        st.session_state.chat_history.append({
            'question': question,
            'answer': result['answer'],
            'sources': result.get('sources', [])
        })
else:
    st.warning("⚠️ System not initialized. Check the error messages above.")

# Footer
st.divider()
st.caption("🤖 Powered by Groq AI | Built with Streamlit")