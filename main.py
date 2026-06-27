import os
import random
from datetime import datetime
from typing import List

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(title="Dragy Hattewar Quantum Server")


class QuantumCore:
    def __init__(self) -> None:
        self.state = "SUPERPOSITION"

    def collapse_state(self, user_location: str) -> dict:
        q_bit = random.choice([0, 1])

        if "Sakon" in user_location or "Sakon Nakhon" in user_location:
            news_feed = [
                {"type": "Royal", "title": "ทรงพระกรุณาโปรดเกล้าฯ โครงการอีสานเขียว"},
                {"type": "Religion", "title": "โอวาทหลวงปู่มั่น: ความเพียรคือกุญแจ"},
                {"type": "Local", "title": "สภาพอากาศสกลนคร: เมฆมาก มีฝนฟ้าคะนอง"},
            ]
        else:
            news_feed = [
                {"type": "Global", "title": "Quantum Computing ก้าวหน้าไปอีกขั้น"},
                {"type": "Philosophy", "title": "Stoicism: ศิลปะแห่งการนิ่งสงบ"},
            ]

        return {
            "status": "COLLAPSED",
            "q_bit": q_bit,
            "location_resonance": user_location,
            "news_feed": news_feed,
            "timestamp": datetime.now().isoformat(),
        }


q_core = QuantumCore()


class ChatMessage(BaseModel):
    role: str
    parts: str


class ChatPayload(BaseModel):
    message: str
    history: List[ChatMessage] = Field(default_factory=list)


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>Dragy Hattewar | Quantum Private Server</title>
    <style>
        body {{ background: #050505; color: #FFD700; font-family: 'Sarabun', sans-serif; text-align: center; padding: 50px; }}
        .container {{ border: 2px solid #FFD700; padding: 20px; max-width: 800px; margin: auto; box-shadow: 0 0 20px #b8860b; }}
        h1 {{ text-shadow: 0 0 10px #FF4500; }}
        .terminal {{ background: #000; color: #0f0; padding: 15px; text-align: left; font-family: monospace; margin-top: 20px; border-left: 5px solid #FFD700; }}
        .news-item {{ border-bottom: 1px solid #333; padding: 10px; text-align: left; }}
        .tag {{ background: #333; color: #fff; padding: 2px 5px; font-size: 0.8em; border-radius: 3px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>👑 DRAGY HATTEWAR 👑</h1>
        <p>Private Quantum Server | Domain: .Dragy</p>
        <hr style="border-color: #FFD700;">

        <div id="dashboard">
            <h3>📡 Quantum Status: {status}</h3>
            <p>Location Resonance: {location}</p>

            <div class="terminal">
                > Initializing Dragy Core... OK<br>
                > Quantum Entanglement... STABLE<br>
                > Loading Sacred Art Assets... DONE<br>
                > User Detected: {location}<br>
                > System Time: {timestamp}
            </div>

            <h3 style="margin-top: 30px; color: #fff;">📰 ข่าวสารตามภูมิประเทศ (Real-time)</h3>
            {news_html}
        </div>
    </div>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def home() -> HTMLResponse:
    data = q_core.collapse_state("Sakon Nakhon, TH")
    news_html = "".join(
        f'<div class="news-item"><span class="tag">{item["type"]}</span> {item["title"]}</div>'
        for item in data["news_feed"]
    )
    html = HTML_TEMPLATE.format(
        status=data["status"],
        location=data["location_resonance"],
        timestamp=data["timestamp"],
        news_html=news_html,
    )
    return HTMLResponse(content=html)


@app.post("/api/chat")
async def chat(payload: ChatPayload) -> JSONResponse:
    if not payload.message.strip():
        return JSONResponse(status_code=400, content={"reply": "กรุณาพิมพ์ข้อความก่อนส่งครับ"})

    reply = f"คำสั่งของคุณถูกรับแล้ว: {payload.message}"
    return JSONResponse(content={"reply": reply})


@app.get("/api/quantum-status")
async def api_status() -> JSONResponse:
    return JSONResponse(
        content={
            "server": "Dragy Private Node",
            "domain": ".Dragy",
            "security": "Quantum Encrypted",
        }
    )


@app.get("/health")
async def health() -> JSONResponse:
    return JSONResponse(content={"status": "ok"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")), reload=False)
