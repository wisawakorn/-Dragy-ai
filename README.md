# 🎬 Darky Hatthevas Studio

AI-powered creative platform for generating images, videos, and content. Built with FastAPI, Streamlit, MongoDB, and PyTorch/TensorFlow.

## 🏗️ Architecture

```
Frontend (Streamlit)
        ↓ HTTP API
Backend (FastAPI) ←→ MongoDB Atlas
        ↓
    AI Models (GPU Render)
```

## 🚀 Quick Start

### Local Development

#### Prerequisites
- Python 3.11+
- Git
- MongoDB (local or MongoDB Atlas)

#### Installation

1. **Clone the repository**
```bash
git clone https://github.com/wisawakorn/-Dragy-ai.git
cd dragy-ai
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

4. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run MongoDB** (if using local)
```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

6. **Start backend**
```bash
uvicorn main:app --reload --port 8000
```

7. **Start frontend** (in another terminal)
```bash
streamlit run streamlit_app.py
```

Visit: 
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:8501

---

## 🌐 Cloud Deployment

### Deploy on Render

1. **Create a new Web Service on Render**
   - Connect your GitHub repository
   - Select this repo: `wisawakorn/-Dragy-ai`

2. **Configure Build & Start Commands**
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Add Environment Variables** (Render Dashboard → Environment)
   ```
   MONGO_URI = mongodb+srv://user:pass@cluster.mongodb.net/...
   DATABASE_URL = postgresql://...
   OPENAI_API_KEY = sk-...
   ```

4. **Deploy**
   - Push to `main` branch
   - Render auto-deploys

**Backend URL:** `https://darky-hatthevas-backend.onrender.com`

---

## 📁 Project Structure

```
dragy-ai/
├── main.py                      # FastAPI backend
├── database/
│   ├── connection.py            # DB connection
│   └── models.py                # SQLAlchemy models
├── streamlit_app.py             # Frontend (if exists)
├── templates/                   # HTML templates
├── static/                       # CSS, JS
├── requirements.txt             # Python dependencies
├── render.yaml                  # Render deployment config
├── .env.example                 # Example environment variables
└── README.md                    # This file
```

---

## 🔧 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/generate` | Create a new generation job |
| GET | `/assets` | List all generated assets |
| GET | `/job/{job_id}` | Check job status |
| GET | `/asset/{asset_id}/file` | Download asset file |
| POST | `/chat` | Chat with AI assistant |

---

## 🎨 Features

✅ **AI Content Generation**
- Image generation (via Stable Diffusion)
- Video generation (via Video Diffusion models)
- Real-time progress tracking

✅ **Asset Management**
- Organize by category
- Thumbnail generation
- Reusable asset library

✅ **AI Chat Assistant**
- Thai language support
- Context-aware responses
- Integration with OpenAI or Ollama

✅ **Security**
- Rate limiting
- Request validation
- Input sanitization

---

## 🔐 Environment Variables

```env
# Database
DATABASE_URL=postgresql://localhost/hatthevas_db
MONGO_URI=mongodb://localhost:27017/studio_db

# AI Services
OPENAI_API_KEY=sk-your-key
OPENAI_MODEL=gpt-4o-mini
OLLAMA_MODEL=llama3.2
OLLAMA_BASE_URL=http://127.0.0.1:11434/api/generate

# Server
PORT=8000
DEBUG=false
```

---

## 📚 Technology Stack

- **Backend:** FastAPI, Uvicorn
- **Frontend:** Streamlit
- **Database:** MongoDB Atlas, PostgreSQL
- **AI Models:** PyTorch, TensorFlow, Stable Diffusion
- **Deployment:** Render.com
- **Authentication:** OAuth 2.0 (Google)

---

## 🛠️ Development

### Run Tests
```bash
pytest tests/
```

### Format Code
```bash
black . && isort .
```

### Lint
```bash
pylint main.py database/
```

---

## 📝 License

MIT License - see LICENSE file for details

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📧 Contact

For issues and questions, please open an issue on GitHub.

---

**Made with ❤️ by Darky Hatthevas Team**
