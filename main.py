from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Dragy AI")

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <h1>🚀 Dragy AI</h1>
    <p>AI Chat + Image + Video</p>
    """