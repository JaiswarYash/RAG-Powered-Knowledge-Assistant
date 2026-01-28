# 🤖 RAG Knowledge Assistant

An AI-powered document Q&A system that lets you upload documents and ask questions about them using Retrieval Augmented Generation (RAG).

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](YOUR_STREAMLIT_URL_HERE)

![Demo](https://img.shields.io/badge/Status-Live-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🌟 Features

- 📁 **Multi-format Support**: Upload PDF, DOCX, DOC, and TXT files
- 💬 **Intelligent Q&A**: Ask questions and get accurate answers from your documents
- 🔍 **Source Citations**: See exactly where answers come from with page numbers and excerpts
- ⚡ **Fast Processing**: Powered by Groq's high-speed LLM inference
- 💾 **Persistent Storage**: Your documents stay indexed between sessions
- 🎨 **Clean Interface**: Beautiful, easy-to-use Streamlit interface

---

## 🚀 Live Demo

Try it out: **[[Live Application Demo:](https://jaiswaryash-rag-powered-knowledge-assistant-app-dwnd1z.streamlit.app/)]**

---

## 📸 Screenshots

### Main Interface
![Main Interface](docs/images/user_interface.png)

### Q&A with Sources
![Q&A Example](docs/images/QnA_image.png)
![Q&A Example](docs/images/sourcce_image.png)

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **LLM**: [Groq](https://groq.com/) (Llama 3.1 8B)
- **Embeddings**: [Sentence Transformers](https://www.sbert.net/) (all-MiniLM-L6-v2)
- **Vector DB**: [ChromaDB](https://www.trychroma.com/)
- **Document Processing**: [Unstructured](https://unstructured.io/)
- **Framework**: [LangChain](https://www.langchain.com/)

---

## 📋 How It Works

1. **Upload Documents** 📄
   - User uploads PDF, DOCX, or TXT files
   - Documents are processed and split into chunks

2. **Create Embeddings** 🧮
   - Each chunk is converted to a vector embedding
   - Embeddings are stored in ChromaDB

3. **Ask Questions** ❓
   - User asks a question
   - System finds relevant chunks using semantic search

4. **Generate Answer** 💡
   - Relevant chunks are sent to Groq LLM
   - AI generates an answer based on the context
   - Sources are provided with page numbers

---

## 🏃 Running Locally

### Prerequisites

- Python 3.11+
- Groq API Key ([Get one free](https://console.groq.com))

### Installation

1. **Clone the repository**
```bash
   git clone https://github.com/YOUR_USERNAME/rag-knowledge-assistant.git
   cd rag-knowledge-assistant
```

2. **Create virtual environment**
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
   # Create .env file
   echo "GROQ_API_KEY=your_api_key_here" > .env
```

5. **Run the app**
```bash
   streamlit run app.py
```

6. **Open browser**
   - Go to `http://localhost:8501`

---

## 📁 Project Structure
```
rag-knowledge-assistant/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore rules
├── .env.example                # Example environment variables
└── core/                       # Core modules
    ├── __init__.py
    ├── main.py                 # RAG system orchestrator
    ├── rag_logic.py            # Document processing & chunking
    ├── vector_db.py            # Vector database operations
    ├── document_loader.py      # Document loading utilities
    └── config.py               # Configuration settings
```

---

## 🔧 Configuration

Edit `core/config.py` to customize:
```python
# Embedding Model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Groq Model
GROQ_MODEL = "llama-3.1-8b-instant"

# LLM Temperature (0 = deterministic, 1 = creative)
LLM_TEMPERATURE = 0.7

# Chunking Parameters
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
```

---

## 🎯 Usage Guide

### Uploading Documents

1. Click **"Browse files"** in the sidebar
2. Select one or more documents (PDF, DOCX, TXT)
3. Click **"Process Uploaded Files"**
4. Wait for processing to complete

### Asking Questions

1. Ensure documents are uploaded and processed
2. Type your question in the chat input
3. Press Enter or click Send
4. View the AI-generated answer with sources

### Viewing Sources

- Click the **"Sources"** dropdown below each answer
- See which document, page, and text excerpt was used
- Verify accuracy of the AI's response

---

## 📊 System Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| RAM      | 4 GB    | 8 GB        |
| CPU      | 2 cores | 4 cores     |
| Storage  | 1 GB    | 5 GB        |
| Internet | Required | Required   |

---

## 🚀 Deployment

### Streamlit Cloud (Current)

Already deployed! The app uses:
- **Free tier**: Unlimited usage
- **Resources**: 1 GB RAM, 1 CPU core
- **Persistence**: Limited (use Streamlit Cloud secrets)

### Deploy Your Own

1. Fork this repository
2. Sign up at [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Add `GROQ_API_KEY` to Streamlit secrets
5. Deploy!

---

## 🔐 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | API key from Groq | ✅ Yes |
| `PERSIST_DIRECTORY` | Vector DB storage path | ❌ No (default: `./chroma_db`) |

---

## 🐛 Known Issues

- **Large PDFs**: Files over 50 pages may take longer to process
- **Scanned PDFs**: OCR not currently supported
- **Image-heavy docs**: May result in lower quality chunks

---

## 🗺️ Roadmap

- [ ] Add support for more file formats (CSV, Excel, PowerPoint)
- [ ] Implement conversation memory
- [ ] Add multi-language support
- [ ] Enable document comparison
- [ ] Add OCR for scanned documents
- [ ] Implement re-ranking for better accuracy
- [ ] Add export functionality (chat history, answers)

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Groq](https://groq.com/) for blazing-fast LLM inference
- [Streamlit](https://streamlit.io/) for the amazing web framework
- [LangChain](https://www.langchain.com/) for RAG orchestration
- [ChromaDB](https://www.trychroma.com/) for vector storage
- [Sentence Transformers](https://www.sbert.net/) for embeddings

---

## 📞 Contact

**Yash Jaiswar** -- yash.jaiswar0709@gmail.com

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/yash-jaiswar-266849301/)

**Project Link**: [rag-knowledge-assistant]( https://github.com/JaiswarYash/RAG-Powered-Knowledge-Assistant.git)

**Live Demo**: [STREAMLIT_URL](https://jaiswaryash-rag-powered-knowledge-assistant-app-dwnd1z.streamlit.app/)

---

## ⭐ Star History

If you find this project helpful, please give it a star!

[![Star History Chart](https://api.star-history.com/svg?repos=YOUR_USERNAME/rag-knowledge-assistant&type=Date)](https://star-history.com/#YOUR_USERNAME/rag-knowledge-assistant&Date)

---

**Found this helpful? Give it a star!**