import hashlib
import json
import logging
import os
import random
import re
import time
import urllib.request
from collections import deque
from datetime import datetime
from typing import Any, Deque, List, Optional

import numpy as np
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("DragyHattewar")

app = FastAPI(title="Dragy Hattewar Quantum Server")


class SecurityShield:
    def __init__(self, max_requests_per_minute: int = 60) -> None:
        self.request_history: Deque[dict[str, Any]] = deque()
        self.max_requests = max_requests_per_minute
        self.blocked_ips: set[str] = set()
        logger.info("[Security] Dragy Defense Shield Initialized.")

    def is_rate_limited(self, client_id: str) -> bool:
        current_time = time.time()
        while self.request_history and self.request_history[0]["time"] < current_time - 60:
            self.request_history.popleft()

        recent_requests = sum(1 for req in self.request_history if req["id"] == client_id)
        if recent_requests >= self.max_requests:
            logger.warning(f"[Security] Rate limit exceeded for {client_id}")
            return True

        self.request_history.append({"id": client_id, "time": current_time})
        return False

    def sanitize_input(self, data: str) -> str:
        if not isinstance(data, str):
            return str(data)
        return re.sub(r"[;<>'\"\\]", "", data)

    def verify_integrity(self, payload: str, signature: str, secret_key: str) -> bool:
        if not signature or not isinstance(signature, str):
            return False
        expected_sig = hashlib.sha256((payload + secret_key).encode()).hexdigest()
        return hashlib.compare_digest(expected_sig, signature)


class DragyMLEngine:
    def __init__(self, learning_rate: float = 0.01, epochs: int = 1000, regularization_lambda: float = 0.01) -> None:
        self.weights: Optional[float] = None
        self.bias = 0.0
        self.lr = learning_rate
        self.epochs = epochs
        self.reg_lambda = regularization_lambda
        self.is_trained = False
        logger.info("[AI Core] Dragy ML Engine Ready.")

    def train(self, X: List[float], y: List[float]) -> None:
        logger.info("[AI Core] Starting Training Process...")
        X_np = np.array(X, dtype=float)
        y_np = np.array(y, dtype=float)
        self.weights = float(np.random.randn())
        n_samples = len(X_np)

        for epoch in range(self.epochs):
            predictions = X_np * self.weights + self.bias
            errors = predictions - y_np
            dw = (2 / n_samples) * np.dot(X_np, errors) + (self.reg_lambda * self.weights)
            db = (2 / n_samples) * np.sum(errors)
            self.weights -= self.lr * dw
            self.bias -= self.lr * db

            if epoch % 100 == 0:
                loss = np.mean(errors**2)
                logger.debug(f"[AI Core] Epoch {epoch}, Loss: {loss:.4f}")

        self.is_trained = True
        logger.info(f"[AI Core] Training Complete. Final Weight: {self.weights:.4f}, Bias: {self.bias:.4f}")

    def predict(self, x: float) -> float:
        if not self.is_trained:
            raise RuntimeError("[AI Error] Model not trained yet!")
        return float(x * self.weights + self.bias)


class VideoPipelineManager:
    def __init__(self) -> None:
        self.queue: List[dict[str, Any]] = []
        logger.info("[Pipeline] Video Pipeline Manager Initialized.")

    def add_job(self, job_id: str, prompt: str) -> None:
        job = {"id": job_id, "prompt": prompt, "status": "queued", "timestamp": time.time()}
        self.queue.append(job)
        logger.info(f"[Pipeline] Job {job_id} added to queue.")

    def process_queue(self) -> Optional[dict[str, Any]]:
        if not self.queue:
            return None

        job = self.queue.pop(0)
        logger.info(f"[Pipeline] Processing Job {job['id']}...")
        time.sleep(0.2)
        job["status"] = "completed"
        job["output_url"] = f"https://storage.dragy.ai/{job['id']}_h265_optimized.mp4"
        logger.info(f"[Pipeline] Job {job['id']} Completed. Saved to: {job['output_url']}")
        return job


class DragyHattewarSystem:
    def __init__(self) -> None:
        self.security = SecurityShield(max_requests_per_minute=10)
        self.ai_engine = DragyMLEngine()
        self.video_manager = VideoPipelineManager()
        self.secret_key = "DRAGY_SECRET_KEY_2026"
        self._train_default_model()
        logger.info("=================================================")
        logger.info(" DRAGY HATTEWAR SYSTEM (AI Core Engine a1) STARTED")
        logger.info(" Creator: Dragy Hattewar")
        logger.info("=================================================")

    def _train_default_model(self) -> None:
        X_train = [1, 2, 3, 4, 5]
        y_train = [2, 4, 6, 8, 10]
        self.ai_engine.train(X_train, y_train)

    def login_google_mock(self, token: str) -> bool:
        if token.startswith("valid_"):
            logger.info("[Auth] Google Login Successful.")
            return True
        logger.warning("[Auth] Invalid Google Token.")
        return False

    def request_video_generation(self, client_id: str, prompt: str, signature: str) -> dict[str, Any]:
        if self.security.is_rate_limited(client_id):
            return {"error": "Too many requests. Slow down."}

        safe_prompt = self.security.sanitize_input(prompt)
        if not self.security.verify_integrity(safe_prompt, signature, self.secret_key):
            return {"error": "Security Alert: Data tampering detected."}

        complexity_score = self.ai_engine.predict(len(safe_prompt))
        job_id = hashlib.md5(f"{client_id}{time.time()}".encode()).hexdigest()
        self.video_manager.add_job(job_id, safe_prompt)

        return {
            "status": "success",
            "job_id": job_id,
            "message": "Video generation queued.",
            "estimated_complexity": round(float(complexity_score), 2),
        }

    def run_demonstration(self) -> dict[str, Any]:
        self.ai_engine.train([1, 2, 3, 4, 5], [2, 4, 6, 8, 10])
        user_id = "user_kutums"
        test_prompt = "Create a cyberpunk city video"
        sig = hashlib.sha256((test_prompt + self.secret_key).encode()).hexdigest()
        response = self.request_video_generation(user_id, test_prompt, sig)
        job = self.video_manager.process_queue()
        pred = self.ai_engine.predict(10)
        return {
            "training_complete": True,
            "prediction": round(float(pred), 2),
            "queue_response": response,
            "completed_job": job,
        }


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
dragy_system = DragyHattewarSystem()


def _build_ai_prompt(prompt: str, history: Optional[List["ChatMessage"]] = None) -> str:
    recent_history = []
    for msg in (history or [])[-4:]:
        if msg.role and msg.parts:
            recent_history.append(f"{msg.role}: {msg.parts}")
    history_text = "\n".join(recent_history)
    return (
        "You are Dragy AI, a polished Thai assistant for an AI studio. "
        "Answer warmly, concisely, and creatively in Thai unless the user clearly asks in another language. "
        f"User request: {prompt}\nConversation history:\n{history_text}"
    )


def generate_ai_reply(prompt: str, history: Optional[List["ChatMessage"]] = None) -> tuple[str, str]:
    cleaned_prompt = prompt.strip()
    if not cleaned_prompt:
        return "กรุณาพิมพ์ข้อความก่อนส่งครับ", "fallback"

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=api_key)
            response = client.responses.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                instructions="You are Dragy AI, a helpful Thai assistant. Be concise, practical, and polished.",
                input=_build_ai_prompt(cleaned_prompt, history),
            )
            reply = getattr(response, "output_text", None) or ""
            if reply.strip():
                return reply.strip(), "openai"
        except Exception as exc:
            logger.warning(f"[AI] OpenAI unavailable: {exc}")

    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434/api/generate")
    ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2")
    try:
        payload = json.dumps(
            {
                "model": ollama_model,
                "prompt": _build_ai_prompt(cleaned_prompt, history),
                "stream": False,
            }
        ).encode("utf-8")
        req = urllib.request.Request(
            ollama_url,
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        reply = (data.get("response") or "").strip()
        if reply:
            return reply, "ollama"
    except Exception as exc:
        logger.warning(f"[AI] Ollama unavailable: {exc}")

    if "code" in cleaned_prompt.lower() or "สคริปต์" in cleaned_prompt.lower():
        reply = (
            f"ผมช่วยออกแบบแนวทางที่ใช้งานได้ทันทีให้คุณได้ครับ สำหรับคำขอ: {cleaned_prompt}. "
            "ลองเริ่มจากเป้าหมายของคุณ ข้อมูลที่มี และผลลัพธ์ที่ต้องการ แล้วผมจะช่วยสรุปเป็นโค้ดหรือแผนงานให้"
        )
    else:
        reply = (
            f"คำขอของคุณคือ: {cleaned_prompt}\n"
            "ผมกำลังเตรียมคำตอบแบบมืออาชีพให้คุณโดยอัตโนมัติในโหมดตัวอย่าง. "
            "ถ้าต้องการให้ตอบแบบสมจริงมากขึ้น ให้เพิ่ม OpenAI API key หรือรัน Ollama ในเครื่อง"
        )
    return reply, "fallback"


class ChatMessage(BaseModel):
    role: str
    parts: str


class ChatPayload(BaseModel):
    message: str
    history: List[ChatMessage] = Field(default_factory=list)


class DragyRequest(BaseModel):
    client_id: str = "demo-client"
    prompt: str
    signature: Optional[str] = None


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Dragy Hattewar | AI Studio</title>
    <style>
        :root {{
            --bg: #060816;
            --panel: rgba(14, 20, 40, 0.9);
            --border: rgba(255, 255, 255, 0.12);
            --text: #f5f7ff;
            --muted: #96a0c2;
            --accent: #8b5cf6;
            --accent-2: #22d3ee;
            --gold: #fbbf24;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            margin: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: radial-gradient(circle at top left, #14213d 0%, var(--bg) 45%, #02040b 100%);
            color: var(--text);
            min-height: 100vh;
            padding: 24px;
        }}
        .shell {{
            max-width: 1180px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1.1fr 0.9fr;
            gap: 20px;
        }}
        .card {{
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 24px;
            box-shadow: 0 16px 60px rgba(0, 0, 0, 0.35);
            overflow: hidden;
            backdrop-filter: blur(18px);
        }}
        .hero {{ padding: 28px 28px 22px; }}
        .badge {{
            display: inline-block;
            padding: 7px 12px;
            border-radius: 999px;
            background: rgba(139, 92, 246, 0.18);
            color: #d7c7ff;
            font-size: 12px;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            margin-bottom: 14px;
        }}
        h1 {{ font-size: 34px; margin: 0 0 8px; }}
        .subtitle {{ color: var(--muted); font-size: 15px; line-height: 1.6; margin: 0 0 16px; }}
        .stats {{ display: flex; gap: 12px; flex-wrap: wrap; margin-top: 16px; }}
        .stat {{ background: rgba(255,255,255,0.05); padding: 10px 12px; border-radius: 14px; border: 1px solid rgba(255,255,255,0.06); }}
        .chip-row {{ display: flex; gap: 8px; flex-wrap: wrap; margin-top: 14px; }}
        .chip {{ border: 1px solid rgba(255,255,255,0.12); background: rgba(255,255,255,0.06); color: var(--text); padding: 8px 10px; border-radius: 999px; font-size: 12px; cursor: pointer; }}
        .chip:hover {{ transform: translateY(-1px); filter: brightness(1.1); }}
        .stat strong {{ display: block; font-size: 16px; }}
        .stat span {{ color: var(--muted); font-size: 12px; }}
        .composer {{ padding: 18px 20px 20px; border-top: 1px solid rgba(255,255,255,0.06); }}
        .chat-area {{ min-height: 420px; display: flex; flex-direction: column; gap: 12px; padding: 18px; }}
        .bubble {{ padding: 12px 14px; border-radius: 16px; max-width: 90%; line-height: 1.55; font-size: 14px; }}
        .bubble.user {{ align-self: flex-end; background: linear-gradient(135deg, var(--accent), #6d28d9); color: white; }}
        .bubble.ai {{ align-self: flex-start; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.08); color: #e8ecff; }}
        .composer-row {{ display: flex; gap: 10px; }}
        textarea {{ flex: 1; border: 1px solid rgba(255,255,255,0.12); background: rgba(255,255,255,0.04); color: var(--text); border-radius: 16px; padding: 14px 16px; min-height: 56px; resize: vertical; outline: none; }}
        button {{ border: 0; border-radius: 16px; padding: 14px 16px; cursor: pointer; font-weight: 700; color: white; background: linear-gradient(135deg, var(--accent-2), var(--accent)); }}
        button:hover {{ filter: brightness(1.1); }}
        .side-panel {{ padding: 24px; display: flex; flex-direction: column; gap: 16px; }}
        .panel-block {{ background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08); border-radius: 18px; padding: 14px 16px; }}
        .panel-block h3 {{ margin: 0 0 8px; font-size: 16px; }}
        .panel-block p, .panel-block li {{ color: var(--muted); font-size: 13px; line-height: 1.6; }}
        .panel-block ul {{ padding-left: 18px; margin: 6px 0 0; }}
        .tiny {{ font-size: 12px; color: var(--muted); }}
        @media (max-width: 900px) {{
            .shell {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="shell">
        <div class="card">
            <div class="hero">
                <div class="badge">⚡ Dragy Hattewar AI Studio</div>
                <h1>สร้างสรรค์ไอเดียด้วย AI แบบทันที</h1>
                <p class="subtitle">พิมพ์ prompt ของคุณ แล้วรับคำตอบที่สวยงาม เหมือนหน้าต่างแชท AI ระดับมืออาชีพ พร้อมระบบ Quantum Core ที่ช่วยให้การตอบสนองดูมีความลึกและน่าสนใจ</p>
                <div class="chip-row">
                    <button class="chip" type="button" onclick="fillPrompt('สร้างสคริปต์ขายสินค้าให้ดูน่าคิดขึ้น')">สร้างสคริปต์ขาย</button>
                    <button class="chip" type="button" onclick="fillPrompt('ช่วยสรุปแนวคิดสำหรับโปรเจกต์ AI สั้น ๆ')">สรุปแนวคิด</button>
                    <button class="chip" type="button" onclick="fillPrompt('ช่วยเขียนข้อความโปรโมตสั้น ๆ สำหรับแบรนด์')">ข้อความโปรโมต</button>
                </div>
                <div class="stats">
                    <div class="stat"><strong>{status}</strong><span>สถานะควอนตัม</span></div>
                    <div class="stat"><strong>{location}</strong><span>ตำแหน่งเรโซแนนซ์</span></div>
                    <div class="stat"><strong>{timestamp}</strong><span>เวลาอัปเดต</span></div>
                </div>
            </div>
            <div class="chat-area" id="chat-area">
                <div class="bubble ai">สวัสดีครับ ผมคือ Dragy AI พร้อมช่วยคุณคิดค้นแนวคิด วางแผนงาน และสร้างสรรค์คำตอบแบบทันที</div>
            </div>
            <div class="composer">
                <div class="composer-row">
                    <textarea id="prompt-input" placeholder="พิมพ์ prompt ที่คุณต้องการเช่น: สร้างสคริปต์แนะนำสินค้าให้ดูน่าคิดขึ้น..."></textarea>
                    <button onclick="sendPrompt()">ส่ง</button>
                </div>
                <div class="tiny" style="margin-top: 8px;">กด Enter เพื่อส่งข้อความ, Shift+Enter เพื่อขึ้นบรรทัดใหม่</div>
            </div>
        </div>

        <div class="card side-panel">
            <div class="panel-block">
                <h3>🧠 Quantum Features</h3>
                <ul>
                    <li>ระบบควอนตัมจำลองเพื่อแสดงสถานะและเรโซแนนซ์ของเครือข่าย</li>
                    <li>รองรับ prompt สั้นเข้มข้นและคำสั่งสร้างสรรค์</li>
                    <li>แสดงผลลัพธ์แบบบับเบิลแชทที่อ่านง่าย</li>
                </ul>
            </div>
            <div class="panel-block">
                <h3>⚡ Ready to use</h3>
                <p>คุณสามารถพิมพ์ข้อความเพื่อทดสอบคำตอบจาก Dragy AI ได้ทันที และยังสามารถต่อยอดเป็นเว็บแอปเติมฟีเจอร์ต่อได้ในอนาคต</p>
            </div>
            <div class="panel-block">
                <h3>📡 Live Status</h3>
                <div class="tiny">{news_html}</div>
            </div>
        </div>
    </div>

    <script>
        const input = document.getElementById('prompt-input');
        const chatArea = document.getElementById('chat-area');

        function fillPrompt(text) {{
            input.value = text;
            input.focus();
        }}

        input.addEventListener('keydown', function (event) {{
            if (event.key === 'Enter' && !event.shiftKey) {{
                event.preventDefault();
                sendPrompt();
            }}
        }});

        async function sendPrompt() {{
            const text = input.value.trim();
            if (!text) return;

            chatArea.insertAdjacentHTML('beforeend', `<div class="bubble user">${{text}}</div>`);
            input.value = '';
            const loading = document.createElement('div');
            loading.className = 'bubble ai';
            loading.innerHTML = 'กำลังคิดคำตอบให้คุณ...';
            chatArea.appendChild(loading);

            try {{
                const response = await fetch('/api/chat', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ message: text }})
                }});
                const data = await response.json();
                loading.remove();
                const modeLabel = data.mode ? ` <span class="tiny">(${{data.mode}})</span>` : '';
                chatArea.insertAdjacentHTML('beforeend', `<div class="bubble ai">${{data.reply}}${{modeLabel}}</div>`);
                chatArea.scrollTop = chatArea.scrollHeight;
            }} catch (e) {{
                loading.remove();
                chatArea.insertAdjacentHTML('beforeend', `<div class="bubble ai">เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง</div>`);
            }}
        }}
    </script>
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
        return JSONResponse(status_code=400, content={"reply": "กรุณาพิมพ์ข้อความก่อนส่งครับ", "mode": "fallback", "ok": False})

    reply, mode = generate_ai_reply(payload.message, payload.history)
    return JSONResponse(content={"reply": reply, "mode": mode, "ok": True})


@app.post("/api/dragy/process")
async def dragy_process(payload: DragyRequest) -> JSONResponse:
    if not payload.prompt.strip():
        return JSONResponse(status_code=400, content={"status": "error", "message": "Prompt is required."})

    signature = payload.signature or hashlib.sha256((payload.prompt + dragy_system.secret_key).encode()).hexdigest()
    result = dragy_system.request_video_generation(payload.client_id, payload.prompt, signature)
    return JSONResponse(content=result)


@app.get("/api/dragy/demo")
async def dragy_demo() -> JSONResponse:
    demo_result = dragy_system.run_demonstration()
    return JSONResponse(content={"status": "ok", **demo_result})


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