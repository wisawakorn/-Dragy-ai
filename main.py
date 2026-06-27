import os
import time
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="ॐ DRAGY AI - Scroll Fix")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

GLOBAL_QUOTA = {
    "chat_used": 27,
    "chat_limit": 50
}

class ChatMessage(BaseModel):
    role: str
    parts: str

class ChatPayload(BaseModel):
    message: str
    model: Optional[str] = "Gemini 2.5 Flash"
    deep_search: Optional[bool] = False
    think_mode: Optional[bool] = False
    history: List[ChatMessage] = []

# =====================================================================
# 🤖 BACKEND API
# =====================================================================
@app.post("/api/chat")
async def ai_chat_endpoint(payload: ChatPayload):
    if not payload.message.strip():
        return JSONResponse(status_code=400, content={"reply": "กรุณาพิมพ์ข้อความก่อนส่งครับ"})
    
    if not GEMINI_API_KEY:
        return JSONResponse(
            status_code=200, 
            content={"reply": "⚠️ ไม่พบ <code>GEMINI_API_KEY</code> บน Render! กรุณาตรวจสอบแท็บ Environment ครับ"}
        )

    GLOBAL_QUOTA["chat_used"] += 1
    
    system_instruction = "คุณคือ ॐ DRAGY AI ปัญญาประดิษฐ์ผู้เชี่ยวชาญระดับสูงด้านพุทธศิลป์ ความรู้ทั่วไป วิดีโอ และการสร้างสรรค์คอนเทนต์ จงตอบคำถามเป็นภาษาไทยอย่างสละสลวย"
    
    contents_payload = []
    for msg in payload.history:
        contents_payload.append({
            "role": msg.role,
            "parts": [{"text": msg.parts}]
        })
    
    contents_payload.append({
        "role": "user",
        "parts": [{"text": payload.message}]
    })

    models_to_try = [
        "gemini-3.5-flash",
        "gemini-2.5-flash",
        "gemini-3.1-flash-litest"
    ]
    
    ai_reply = ""
    success = False

    for model_name in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        body = {
            "contents": contents_payload,
            "systemInstruction": { "parts": [{"text": system_instruction}] },
            "generationConfig": { "temperature": 0.7, "maxOutputTokens": 4096 }
        }

        for attempt in range(2):
            try:
                response = requests.post(url, headers=headers, json=body, timeout=15)
                response_json = response.json()
                
                if "candidates" in response_json and len(response_json["candidates"]) > 0:
                    candidate = response_json["candidates"][0]
                    if "content" in candidate and "parts" in candidate["content"] and len(candidate["content"]["parts"]) > 0:
                        ai_reply = candidate["content"]["parts"][0]["text"].replace("\n", "<br>")
                        success = True
                        break
                
                if "error" in response_json:
                    break
                        
                time.sleep(0.5)
            except Exception:
                pass
        
        if success:
            break

    if not success:
        ai_reply = "🔱 <b>ระบบเครือข่ายขัดข้องชั่วคราว</b><br>โปรดลองใหม่อีกครั้งในอีกสักครู่ครับ"

    return {
        "reply": ai_reply,
        "quota": GLOBAL_QUOTA
    }

# =====================================================================
# 🌐 FRONTEND: แก้ไข Layout ให้แสดงผลตัวเลื่อนขึ้นลงหน้าจออัตโนมัติ
# =====================================================================
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ॐ DRAGY AI - Create Images • Videos • Knowledge</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <script src="https://unpkg.com/lucide@latest"></script>
        <style>
            body { font-family: 'Prompt', sans-serif; background: radial-gradient(circle at 60% 30%, #150933 0%, #080314 60%, #030108 100%); }
            .glow-gold-icon { text-shadow: 0 0 20px rgba(234, 179, 8, 0.6); }
            .text-gradient { background: linear-gradient(to right, #60a5fa, #c084fc, #f472b6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
            
            /* Custom Scrollbar ปรับแต่งแถบเลื่อนให้สวยงามเข้ากับธีมมืด */
            ::-webkit-scrollbar { width: 6px; height: 6px; }
            ::-webkit-scrollbar-track { background: rgba(15, 7, 34, 0.3); }
            ::-webkit-scrollbar-thumb { background: rgba(147, 51, 234, 0.4); border-radius: 10px; }
            ::-webkit-scrollbar-thumb:hover { background: rgba(147, 51, 234, 0.7); }
        </style>
    </head>
    <body class="text-gray-200 h-screen w-screen flex overflow-hidden">

        <!-- SIDEBAR -->
        <aside class="w-64 bg-[#060310]/95 border-r border-purple-950/40 p-4 flex flex-col justify-between hidden md:flex flex-shrink-0 h-full">
            <div>
                <div class="flex flex-col px-1 py-3 mb-4 border-b border-purple-950/30">
                    <div class="text-2xl font-bold text-white flex items-center gap-1">
                        <span class="text-yellow-500 font-bold glow-gold-icon">ॐ</span> DRAGY AI
                    </div>
                    <span class="text-[9px] text-gray-500 uppercase tracking-widest mt-1">Create Images • Videos • Knowledge</span>
                </div>
                <nav class="space-y-1">
                    <a href="/" class="flex items-center gap-3 px-3 py-2.5 bg-purple-950/30 text-purple-300 rounded-xl text-sm font-medium"><i data-lucide="home" class="w-4.5 h-4.5"></i> หน้าแรก</a>
                    <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 text-sm"><i data-lucide="message-square" class="w-4.5 h-4.5"></i> AI Chat</a>
                    <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 text-sm"><i data-lucide="image" class="w-4.5 h-4.5"></i> AI Image</a>
                    <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 text-sm"><i data-lucide="video" class="w-4.5 h-4.5"></i> AI Video</a>
                    <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 text-sm"><i data-lucide="wrench" class="w-4.5 h-4.5"></i> เครื่องมือ AI</a>
                </nav>
            </div>
            
            <div class="bg-[#0b051c] border border-purple-950/60 rounded-2xl p-3.5 text-xs text-gray-400">
                <div class="flex justify-between mb-1">
                    <span>สิทธิ์การใช้งาน (Pro)</span>
                    <span class="text-green-400">Active</span>
                </div>
                <div class="flex justify-between text-[11px] text-gray-500">
                    <span>ข้อความแชท</span>
                    <span id="quota-txt">27 / 50</span>
                </div>
            </div>
        </aside>

        <!-- MAIN VIEWPORT -->
        <main class="flex-1 flex flex-col h-full overflow-hidden relative">
            
            <!-- HEADER BAR -->
            <div class="flex justify-end items-center gap-3 p-4 border-b border-purple-950/10 flex-shrink-0">
                <button class="bg-blue-600 text-white text-xs font-medium py-2 px-4 rounded-xl shadow-lg">Sign In with Google</button>
            </div>

            <!-- CHAT AREA (แก้ให้มีระบบเลื่อนตรงนี้) -->
            <div id="main-scroll-area" class="flex-1 w-full max-w-3xl mx-auto overflow-y-auto px-4 py-4 space-y-4 flex flex-col">
                <div id="welcome-view" class="w-full flex flex-col items-center text-center pt-12 pb-4 space-y-4">
                    <span class="text-6xl text-yellow-500 font-bold glow-gold-icon">ॐ</span>
                    <h1 class="text-4xl font-bold text-gradient">สวัสดีครับ ยินดีต้อนรับ</h1>
                    <p class="text-gray-400">วันนี้ให้ ॐ DRAGY AI ขับเคลื่อนโปรเจกต์ของคุณอย่างไรดี?</p>
                </div>
                <div id="chat-box" class="w-full hidden space-y-6 text-sm pb-10"></div>
            </div>

            <!-- FOOTER INPUT BAR (ล็อกให้อยู่ด้านล่างสุดเสมออย่างสวยงาม) -->
            <div class="w-full max-w-3xl mx-auto p-4 flex-shrink-0 bg-transparent">
                <div class="bg-[#0f0722]/95 border border-purple-500/20 rounded-3xl p-4 flex flex-col gap-2 shadow-2xl backdrop-blur-md">
                    <textarea id="user-input" class="w-full bg-transparent text-gray-200 placeholder-gray-600 text-sm focus:outline-none resize-none h-12" placeholder="พิมพ์ข้อความสั่งการ AI..."></textarea>
                    <div class="flex justify-between items-center border-t border-purple-950/60 pt-2">
                        <div class="flex gap-2 text-xs text-gray-500">
                            <button class="px-2 py-1 bg-purple-950/40 rounded-lg flex items-center gap-1">🧭 DeepSearch</button>
                            <button class="px-2 py-1 bg-purple-950/40 rounded-lg flex items-center gap-1">💡 Think</button>
                        </div>
                        <button onclick="sendPayload()" class="p-2 bg-blue-600 text-white rounded-xl shadow-lg hover:bg-blue-700 transition">
                            <i data-lucide="arrow-up" class="w-4 h-4"></i>
                        </button>
                    </div>
                </div>
            </div>
        </main>

        <script>
            lucide.createIcons();
            let historyContext = [];

            async function sendPayload() {
                const input = document.getElementById('user-input');
                const text = input.value.trim();
                if(!text) return;

                document.getElementById('welcome-view').classList.add('hidden');
                const box = document.getElementById('chat-box');
                box.classList.remove('hidden');

                // ฝั่ง User (ขวา)
                box.innerHTML += `
                    <div class="flex justify-end mb-4">
                        <div class="bg-purple-600 text-white px-4 py-2.5 rounded-2xl rounded-tr-none max-w-[85%] shadow-md break-words">
                            ${text}
                        </div>
                    </div>
                `;
                input.value = '';

                const loadingId = "loader-" + Date.now();
                box.innerHTML += `
                    <div id="${loadingId}" class="flex flex-col items-start mb-4 animate-fade-in">
                        <div class="text-[11px] text-gray-500 mb-1 flex items-center gap-1">
                            <i data-lucide="cpu" class="w-3 h-3 text-purple-400"></i> ॐ DRAGY ENGINE กำลังประมวลผล...
                        </div>
                        <div class="bg-[#0d061a] border border-purple-950/60 px-4 py-3 rounded-2xl rounded-tl-none flex gap-1.5 items-center shadow-inner">
                            <div class="w-2 h-2 bg-purple-500 rounded-full animate-bounce"></div>
                            <div class="w-2 h-2 bg-purple-500 rounded-full animate-bounce [animation-delay:0.2s]"></div>
                            <div class="w-2 h-2 bg-purple-500 rounded-full animate-bounce [animation-delay:0.4s]"></div>
                        </div>
                    </div>
                `;
                lucide.createIcons();
                scrollToBottom();

                try {
                    const res = await fetch('/api/chat', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ message: text, history: historyContext })
                    });
                    const data = await res.json();
                    document.getElementById(loadingId).remove();

                    // ฝั่ง AI (ซ้าย)
                    box.innerHTML += `
                        <div class="flex flex-col items-start mb-4">
                            <span class="text-[11px] text-yellow-500 font-medium mb-1 flex items-center gap-1">
                                <span class="glow-gold-icon">ॐ</span> DRAGY ENGINE
                            </span>
                            <div class="bg-[#0d061a] border border-purple-950/60 text-gray-200 px-4 py-3.5 rounded-2xl rounded-tl-none max-w-[85%] leading-relaxed shadow-lg break-words">
                                ${data.reply}
                            </div>
                        </div>
                    `;
                    
                    historyContext.push({role: "user", parts: text});
                    historyContext.push({role: "model", parts: data.reply});
                    
                    if(data.quota) {
                        document.getElementById('quota-txt').innerText = data.quota.chat_used + " / 50";
                    }
                } catch(e) {
                    if(document.getElementById(loadingId)) document.getElementById(loadingId).remove();
                    box.innerHTML += `<div class="text-red-400 text-xs mb-4">⚠️ ระบบขัดข้อง ไม่สามารถติดต่อหลังบ้านได้</div>`;
                }
                
                scrollToBottom();
            }

            function scrollToBottom() {
                const s = document.getElementById('main-scroll-area');
                s.scrollTo({
                    top: s.scrollHeight,
                    behavior: 'smooth'
                });
            }

            document.getElementById('user-input').addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendPayload();
                }
            });
        </script>
    </body>
    </html>"""
    import hashlib
import time
import random
import json
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

# -------------------------------------------------------------
# 1. จำลองอัลกอริทึมควอนตัม (Quantum Algorithm Simulation)
# -------------------------------------------------------------
class QuantumCore:
    def __init__(self):
        self.state = "SUPERPOSITION"
        self.entangled_data = {}

    def collapse_state(self, user_location):
        """
        จำลองการยุบสถานะคลื่นความน่าจะเป็นให้กลายเป็นข้อมูลจริง
        ตามตำแหน่งของผู้ใช้ (Observer Effect)
        """
        # สุ่มค่าความซับซ้อนแบบควอนตัม
        q_bit = random.choice([0, 1])
        
        # Entanglement: เชื่อมโยงข่าวกับตำแหน่งทันที
        if "Sakon Nakhon" in user_location:
            news_feed = [
                {"type": "Royal", "title": "ทรงพระกรุณาโปรดเกล้าฯ โครงการอีสานเขียว"},
                {"type": "Religion", "title": "โอวาทหลวงปู่มั่น: ความเพียรคือกุญแจ"},
                {"type": "Local", "title": "สภาพอากาศสกลนคร: เมฆมาก มีฝนฟ้าคะนอง"}
            ]
        else:
            news_feed = [
                {"type": "Global", "title": "Quantum Computing ก้าวหน้าไปอีกขั้น"},
                {"type": "Philosophy", "title": "สตอicism: ศิลปะแห่งการนิ่งสงบ"}
            ]
            
        return {
            "status": "COLLAPSED",
            "q_bit": q_bit,
            "location_resonance": user_location,
            "news_feed": news_feed,
            "timestamp": datetime.now().isoformat()
        }

# Initialize Core
q_core = QuantumCore()

# -------------------------------------------------------------
# 2. หน้าเว็บ UI (สไตล์เฉลิมชัย + Hacker)
# -------------------------------------------------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>Dragy Hattewar | Quantum Private Server</title>
    <style>
        body { background: #050505; color: #FFD700; font-family: 'Sarabun', sans-serif; text-align: center; padding: 50px; }
        .container { border: 2px solid #FFD700; padding: 20px; max-width: 800px; margin: auto; box-shadow: 0 0 20px #b8860b; }
        h1 { text-shadow: 0 0 10px #FF4500; }
        .terminal { background: #000; color: #0f0; padding: 15px; text-align: left; font-family: monospace; margin-top: 20px; border-left: 5px solid #FFD700; }
        .news-item { border-bottom: 1px solid #333; padding: 10px; text-align: left; }
        .tag { background: #333; color: #fff; padding: 2px 5px; font-size: 0.8em; border-radius: 3px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>👑 DRAGY HATTEWAR 👑</h1>
        <p>Private Quantum Server | Domain: .Dragy</p>
        <hr style="border-color: #FFD700;">
        
        <div id="dashboard">
            <h3>📡 Quantum Status: {{ status }}</h3>
            <p>Location Resonance: {{ location }}</p>
            
            <div class="terminal">
                > Initializing Dragy Core... OK<br>
                > Quantum Entanglement... STABLE<br>
                > Loading Sacred Art Assets... DONE<br>
                > User Detected: {{ location }}<br>
                > System Time: {{ timestamp }}
            </div>

            <h3 style="margin-top: 30px; color: #fff;">📰 ข่าวสารตามภูมิประเทศ (Real-time)</h3>
            {% for news in news %}
            <div class="news-item">
                <span class="tag">{{ news.type }}</span> {{ news.title }}
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

# -------------------------------------------------------------
# 3. Routes การทำงาน
# -------------------------------------------------------------
@app.route('/')
def home():
    # จำลองการดึงตำแหน่งผู้ใช้ (ในจริงอาจใช้ IP Lookup)
    user_loc = "Sakon Nakhon, TH" 
    
    # เรียกใช้ Quantum Core
    data = q_core.collapse_state(user_loc)
    
    return render_template_string(HTML_TEMPLATE, 
                                  status=data['status'],
                                  location=data['location_resonance'],
                                  timestamp=data['timestamp'],
                                  news=data['news_feed'])

@app.route('/api/quantum-status')
def api_status():
    return jsonify({"server": "Dragy Private Node", "domain": ".Dragy", "security": "Quantum Encrypted"})

if __name__ == '__main__':
    print("==========================================")
    print(" STARTING DRAGY QUANTUM SERVER")
    print(" Access via: http://www.drady-hattewar.Dragy")
    print("==========================================")
    app.run(host='0.0.0.0', port=80, debug=True)
