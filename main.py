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
    <title>Dragy AI | Studio</title>
    <style>
        :root {{
            --bg: #070b1d;
            --panel: rgba(9, 14, 32, 0.92);
            --panel-soft: rgba(12, 18, 42, 0.88);
            --border: rgba(255, 255, 255, 0.11);
            --text: #eef4ff;
            --muted: #8fa4c6;
            --accent: #8b5cf6;
            --accent-2: #22d3ee;
            --accent-3: #f59e0b;
            --surface: rgba(255, 255, 255, 0.04);
        }}
        * {{ box-sizing: border-box; }}
        body {{
            margin: 0;
            font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: var(--text);
            background: radial-gradient(circle at top left, #181c3a 0%, #070b1d 42%, #02040b 100%);
            min-height: 100vh;
        }}
        .app-shell {{ display: grid; grid-template-columns: 260px 1fr; min-height: 100vh; }}
        .sidebar {{ background: linear-gradient(180deg, rgba(11, 18, 44, 0.95), rgba(6, 9, 20, 0.95)); border-right: 1px solid rgba(255,255,255,0.07); padding: 28px 20px; display: flex; flex-direction: column; gap: 22px; }}
        .brand {{ display: flex; align-items: center; gap: 14px; margin-bottom: 8px; }}
        .brand-logo {{ width: 36px; height: 36px; border-radius: 14px; background: linear-gradient(135deg, var(--accent), var(--accent-2)); display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; }}
        .brand-text {{ display: grid; gap: 2px; }}
        .brand-text strong {{ font-size: 16px; }}
        .brand-text span {{ color: var(--muted); font-size: 12px; }}
        .nav-list {{ list-style: none; padding: 0; margin: 0; display: grid; gap: 10px; }}
        .nav-item {{ display: flex; align-items: center; justify-content: space-between; padding: 12px 14px; border-radius: 16px; background: rgba(255,255,255,0.03); color: var(--text); cursor: pointer; transition: background 0.2s; }}
        .nav-item.active, .nav-item:hover {{ background: rgba(139,92,246,0.16); }}
        .nav-item span {{ font-size: 14px; }}
        .nav-icon {{ width: 18px; height: 18px; margin-right: 10px; display: inline-flex; align-items: center; justify-content: center; }}
        .status-card {{ padding: 18px; border-radius: 22px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); }}
        .status-card h3 {{ margin: 0 0 12px; font-size: 14px; color: var(--muted); }}
        .status-badge {{ display: inline-flex; align-items: center; gap: 8px; padding: 8px 12px; border-radius: 999px; background: rgba(139,92,246,0.16); color: #e9d5ff; font-size: 12px; }}
        .sidebar-footer {{ margin-top: auto; display: grid; gap: 10px; }}
        .pro-box {{ padding: 16px; border-radius: 22px; border: 1px solid rgba(255,255,255,0.08); background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02)); }}
        .pro-box strong {{ display: block; font-size: 14px; margin-bottom: 6px; }}
        .pro-box p {{ margin: 0; color: var(--muted); font-size: 13px; line-height: 1.55; }}
        .button-primary {{ display: inline-flex; align-items: center; justify-content: center; gap: 8px; padding: 12px 16px; border-radius: 14px; background: linear-gradient(135deg, var(--accent-2), var(--accent)); color: white; border: 0; cursor: pointer; width: 100%; font-weight: 700; }}
        .main-panel {{ padding: 28px 32px; display: flex; flex-direction: column; gap: 24px; }}
        .top-bar {{ display: flex; align-items: center; justify-content: flex-end; gap: 14px; }}
        .top-chip {{ display: inline-flex; align-items: center; gap: 8px; padding: 10px 14px; border-radius: 999px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08); color: var(--text); font-size: 13px; }}
        .hero-panel {{ background: linear-gradient(180deg, rgba(14,23,54,0.95), rgba(7, 11, 26, 0.95)); border: 1px solid rgba(255,255,255,0.08); border-radius: 28px; padding: 36px; display: grid; gap: 18px; position: relative; overflow: hidden; }}
        .hero-panel::after {{ content: ''; position: absolute; inset: 0; background: radial-gradient(circle at top right, rgba(139,92,246,0.18), transparent 28%), radial-gradient(circle at bottom left, rgba(34,211,238,0.12), transparent 24%); pointer-events: none; }}
        .hero-panel h1 {{ margin: 0; font-size: 44px; line-height: 1.05; }}
        .hero-panel p {{ margin: 0; color: var(--muted); max-width: 720px; font-size: 16px; line-height: 1.8; }}
        .hero-actions {{ display: flex; flex-wrap: wrap; gap: 12px; align-items: center; }}
        .hero-actions .pill {{ padding: 10px 14px; border-radius: 999px; border: 1px solid rgba(255,255,255,0.08); background: rgba(255,255,255,0.04); color: var(--text); font-size: 13px; }}
        .prompt-card {{ background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08); border-radius: 26px; padding: 26px; display: grid; gap: 18px; }}
        .prompt-header {{ display: flex; align-items: center; justify-content: space-between; gap: 12px; }}
        .prompt-header h2 {{ margin: 0; font-size: 20px; }}
        .prompt-header span {{ color: var(--muted); font-size: 13px; }}
        .prompt-input {{ display: grid; gap: 14px; }}
        .prompt-input textarea {{ width: 100%; min-height: 130px; resize: vertical; padding: 18px 20px; border-radius: 22px; border: 1px solid rgba(255,255,255,0.08); background: rgba(255,255,255,0.04); color: var(--text); font-size: 15px; line-height: 1.7; }}
        .prompt-row {{ display: flex; flex-wrap: wrap; gap: 12px; justify-content: space-between; align-items: center; }}
        .prompt-row button {{ min-width: 140px; }}
        .suggestion-list {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }}
        .suggestion-card {{ padding: 16px 18px; border-radius: 20px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); cursor: pointer; transition: transform 0.2s, border-color 0.2s; }}
        .suggestion-card:hover {{ transform: translateY(-2px); border-color: rgba(139,92,246,0.22); }}
        .suggestion-card strong {{ display: block; margin-bottom: 6px; font-size: 14px; }}
        .suggestion-card span {{ color: var(--muted); font-size: 13px; line-height: 1.6; }}
        .chat-log {{ display: grid; gap: 12px; }}
        .chat-message {{ padding: 16px 18px; border-radius: 20px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08); }}
        .chat-message.user {{ background: linear-gradient(135deg, rgba(139,92,246,0.8), rgba(99,102,241,0.85)); color: white; text-align: right; }}
        .chat-message.ai {{ background: rgba(255,255,255,0.04); color: var(--text); }
        .chat-message p {{ margin: 0; line-height: 1.8; font-size: 14px; }}
        .chat-badge {{ display: inline-flex; align-items: center; gap: 8px; padding: 8px 12px; border-radius: 999px; background: rgba(255,255,255,0.06); color: var(--muted); font-size: 12px; }}
        .top-actions {{ display: flex; gap: 12px; flex-wrap: wrap; justify-content: flex-end; }}
        .top-actions button {{ border-radius: 999px; padding: 10px 16px; background: rgba(255,255,255,0.06); color: var(--text); border: 1px solid rgba(255,255,255,0.08); cursor: pointer; }}
        .top-button-primary {{ background: linear-gradient(135deg, var(--accent-2), var(--accent)); color: white; border: none; }}
        .footer-notice {{ margin-top: 16px; color: var(--muted); font-size: 13px; }}
        @media (max-width: 1100px) {{ .app-shell {{ grid-template-columns: 1fr; }} .sidebar {{ order: 2; }} }}
        @media (max-width: 720px) {{ .hero-panel h1 {{ font-size: 30px; }} .suggestion-list {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="app-shell">
        <aside class="sidebar">
            <div class="brand">
                <div class="brand-logo">D</div>
                <div class="brand-text">
                    <strong>Dragy AI</strong>
                    <span>AI Studio</span>
                </div>
            </div>
            <div class="top-actions">
                <button class="top-button-primary">Login with Google</button>
            </div>
            <ul class="nav-list">
                <li class="nav-item active"><span>หน้าแรก</span></li>
                <li class="nav-item"><span>AI Chat</span></li>
                <li class="nav-item"><span>AI Image</span></li>
                <li class="nav-item"><span>AI Video</span></li>
                <li class="nav-item"><span>เครื่องมือ AI</span></li>
                <li class="nav-item"><span>ประวัติแชท</span></li>
                <li class="nav-item"><span>โปรไฟล์</span></li>
                <li class="nav-item"><span>การตั้งค่า</span></li>
            </ul>
            <div class="status-card">
                <h3>วันนี้คุณใช้งาน</h3>
                <div class="chip-row">
                    <span class="chip">ภาพ 12/15</span>
                    <span class="chip">วิดีโอ 0/1</span>
                    <span class="chip">แชท 23/50</span>
                </div>
            </div>
            <div class="pro-box">
                <strong>Dragy AI Pro</strong>
                <p>ปลดล็อกทุกฟีเจอร์ เริ่มต้นเพียง ฿99 / เดือน</p>
            </div>
        </aside>
        <main class="main-panel">
            <div class="top-bar">
                <span class="top-chip">TH</span>
                <span class="top-chip">Dark</span>
                <button class="top-button-primary">เข้าสู่ระบบ</button>
            </div>
            <section class="hero-panel">
                <h1>สวัสดีครับ 👋</h1>
                <p>วันนี้ให้ Dragy AI ช่วยอะไรดี? พิมพ์คำถามหรือไอเดียของคุณ แล้วรับคำตอบทันทีในรูปแบบแชท AI ที่สวยงามและใช้งานง่าย</p>
                <div class="hero-actions">
                    <span class="pill">DeepSearch</span>
                    <span class="pill">Think</span>
                    <span class="pill">Grok 3</span>
                </div>
            </section>
            <section class="prompt-card">
                <div class="prompt-header">
                    <div>
                        <h2>เริ่มต้นแชทกับ Dragy AI</h2>
                        <span>พิมพ์คำสั่งที่คุณต้องการ แล้วระบบจะตอบกลับในทันที</span>
                    </div>
                    <button class="button-primary" onclick="sendPrompt()">ส่งคำสั่ง</button>
                </div>
                <div class="prompt-input">
                    <textarea id="prompt-input" placeholder="พิมพ์ข้อความ หรือคำถาม เช่น ช่วยเขียนโพสต์ขายของให้สั้นและน่าอ่าน"></textarea>
                </div>
                <div class="suggestion-list">
                    <button class="suggestion-card" onclick="fillPrompt('เขียนโพสต์ขายสินค้าให้สั้นและน่าอ่าน')">
                        <strong>ขายของบน TikTok</strong>
                        <span>ออกแบบโพสต์โฆษณาให้ตรงใจลูกค้า</span>
                    </button>
                    <button class="suggestion-card" onclick="fillPrompt('สรุปข่าวเทคโนโลยีล่าสุดให้อ่านง่าย')">
                        <strong>สรุปข่าว</strong>
                        <span>สรุปข่าวเทคโนโลยีในแบบสั้นกระชับ</span>
                    </button>
                    <button class="suggestion-card" onclick="fillPrompt('ช่วยเขียนสคริปต์วิดีโอสำหรับ YouTube')">
                        <strong>วิดีโอ AI</strong>
                        <span>เขียนสคริปต์สำหรับวิดีโอได้ทันที</span>
                    </button>
                    <button class="suggestion-card" onclick="fillPrompt('แปลข้อความจากไทยเป็นอังกฤษอย่างเป็นมืออาชีพ')">
                        <strong>แปลภาษา</strong>
                        <span>แปลประโยคให้เป็นมืออาชีพ</span>
                    </button>
                </div>
            </section>
            <section class="prompt-card">
                <div class="prompt-header">
                    <h2>ผลลัพธ์ล่าสุด</h2>
                </div>
                <div class="chat-log" id="chat-area">
                    <div class="chat-message ai">
                        <p>สวัสดีครับ ผมคือ Dragy AI พร้อมช่วยคุณคิดค้นแนวคิด วางแผนงาน และสร้างสรรค์คำตอบแบบทันที</p>
                    </div>
                </div>
                <p class="footer-notice">ผลลัพธ์จะปรากฏที่นี่เมื่อคุณส่งคำสั่ง</p>
            </section>
        </main>
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

            const userBubble = document.createElement('div');
            userBubble.className = 'chat-message user';
            userBubble.innerHTML = `<p>${{text}}</p>`;
            chatArea.appendChild(userBubble);
            input.value = '';

            const loading = document.createElement('div');
            loading.className = 'chat-message ai';
            loading.innerHTML = '<p>กำลังคิดคำตอบให้คุณ...</p>';
            chatArea.appendChild(loading);
            chatArea.scrollTop = chatArea.scrollHeight;

            try {{
                const response = await fetch('/api/chat', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ message: text }})
                }});
                const data = await response.json();
                loading.remove();
                const replyBubble = document.createElement('div');
                replyBubble.className = 'chat-message ai';
                replyBubble.innerHTML = `<p>${{data.reply}}</p>${{data.mode ? `<div class="chat-badge">${{data.mode}}</div>` : ''}`;
                chatArea.appendChild(replyBubble);
                chatArea.scrollTop = chatArea.scrollHeight;
            }} catch (e) {{
                loading.remove();
                const errorBubble = document.createElement('div');
                errorBubble.className = 'chat-message ai';
                errorBubble.innerHTML = '<p>เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง</p>';
                chatArea.appendChild(errorBubble);
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