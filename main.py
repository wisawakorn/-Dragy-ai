import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="ॐ DRAGY AI")

# ดึงสิทธิ์ความปลอดภัยผ่าน Environment Variable ของ Render
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# ตัวแปรระบบจำลองโควตา
GLOBAL_QUOTA = {
    "chat_used": 24,
    "chat_limit": 50
}

class ChatMessage(BaseModel):
    role: str
    parts: str

class ChatPayload(BaseModel):
    message: str
    model: Optional[str] = "Gemini 1.5 Flash"
    deep_search: Optional[bool] = False
    think_mode: Optional[bool] = False
    history: List[ChatMessage] = []

# =====================================================================
# 🤖 BACKEND API
# =====================================================================
@app.post("/api/chat")
async def ai_chat_endpoint(payload: ChatPayload):
    if not payload.message.strip():
        return JSONResponse(status_code=400, content={"reply": "กรุณาพิมพ์ข้อความ..."})
    
    if not GEMINI_API_KEY:
        return JSONResponse(
            status_code=200, 
            content={"reply": "⚠️ ตรวจไม่พบ GEMINI_API_KEY บน Render! กรุณาเพิ่มค่านี้ในเมนู Environment ก่อนใช้งานครับ"}
        )

    GLOBAL_QUOTA["chat_used"] += 1
    
    system_instruction = "คุณคือ ॐ DRAGY AI แพลตฟอร์ม AI อัจฉริยะที่เชี่ยวชาญด้านศิลปะ ภาพ วิดีโอ และความรู้รอบตัว จงตอบคำถามเป็นภาษาไทย"
    
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

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    body = {
        "contents": contents_payload,
        "systemInstruction": { "parts": [{"text": system_instruction}] },
        "generationConfig": { "temperature": 0.7, "maxOutputTokens": 2048 }
    }

    try:
        response = requests.post(url, headers=headers, json=body, timeout=20)
        response_json = response.json()
        
        if "candidates" in response_json and len(response_json["candidates"]) > 0:
            candidate = response_json["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"] and len(candidate["content"]["parts"]) > 0:
                ai_reply = candidate["content"]["parts"][0]["text"]
                ai_reply = ai_reply.replace("\n", "<br>")
            else:
                ai_reply = f"⚠️ ได้รับโครงสร้างข้อมูลไม่สมบูรณ์จาก API: {str(response_json)}"
        elif "error" in response_json:
            ai_reply = f"❌ เกิดข้อผิดพลาดจาก Google Gemini API: {response_json['error'].get('message', 'ไม่ทราบสาเหตุ')}"
        else:
            ai_reply = "🔱 ระบบประมวลผลเสร็จสิ้น แต่ไม่มีเนื้อหาคำตอบส่งกลับมา"
            
    except Exception as e:
        ai_reply = f"❌ เกิดข้อผิดพลาดชั่วคราว: {str(e)}"

    return {
        "reply": ai_reply,
        "quota": GLOBAL_QUOTA
    }

# =====================================================================
# 🌐 FRONTEND
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
        </style>
    </head>
    <body class="text-gray-200 min-h-screen flex overflow-hidden">

        <!-- SIDEBAR -->
        <aside class="w-64 bg-[#060310]/95 border-r border-purple-950/40 p-4 flex flex-col justify-between hidden md:flex flex-shrink-0">
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
                    <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 text-sm"><i data-lucide="history" class="w-4.5 h-4.5"></i> ประวัติแชท</a>
                </nav>
            </div>
            
            <div class="bg-[#0b051c] border border-purple-950/60 rounded-2xl p-3.5 text-xs text-gray-400">
                <div class="flex justify-between mb-1">
                    <span>สิทธิ์การใช้งาน (Pro)</span>
                    <span class="text-green-400">Active</span>
                </div>
                <div class="flex justify-between text-[11px] text-gray-500">
                    <span>ข้อความแชท</span>
                    <span id="quota-txt">24 / 50</span>
                </div>
            </div>
        </aside>

        <!-- MAIN CONTENT -->
        <main class="flex-1 flex flex-col justify-between p-4 md:p-6 overflow-hidden">
            <div class="flex justify-end items-center gap-3">
                <button class="bg-blue-600 text-white text-xs font-medium py-2 px-4 rounded-xl shadow-lg">Sign In with Google</button>
            </div>

            <div id="main-scroll-area" class="flex-1 w-full max-w-3xl mx-auto my-4 overflow-y-auto flex flex-col px-2">
                <div id="welcome-view" class="w-full flex flex-col items-center text-center pt-10 pb-4 space-y-4">
                    <span class="text-6xl text-yellow-500 font-bold glow-gold-icon">ॐ</span>
                    <h1 class="text-4xl font-bold text-gradient">สวัสดีครับ ยินดีต้อนรับ</h1>
                    <p class="text-gray-400">วันนี้ให้ ॐ DRAGY AI ขับเคลื่อนโปรเจกต์ของคุณอย่างไรดี?</p>
                </div>
                <div id="chat-box" class="w-full hidden space-y-4 text-sm pb-6"></div>
            </div>

            <!-- INPUT BAR -->
            <div class="w-full max-w-3xl mx-auto">
                <div class="bg-[#0f0722]/90 border border-purple-500/20 rounded-3xl p-4 flex flex-col gap-2">
                    <textarea id="user-input" class="w-full bg-transparent text-gray-200 placeholder-gray-600 text-sm focus:outline-none resize-none h-12" placeholder="พิมพ์ข้อความสั่งการ AI หรือป้อนคำสั่งสร้างสรรค์งานพุทธศิลป์ วิดีโอ..."></textarea>
                    <div class="flex justify-between items-center border-t border-purple-950/60 pt-2">
                        <div class="flex gap-2 text-xs text-gray-500">
                            <button id="btn-deep" class="px-2 py-1 bg-purple-950/40 rounded-lg flex items-center gap-1">🧭 DeepSearch</button>
                            <button id="btn-think" class="px-2 py-1 bg-purple-950/40 rounded-lg flex items-center gap-1">💡 Think</button>
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

                // บับเบิ้ลผู้ใช้ขวาบนตามโครงสร้างของไฟล์ image_74aab4.png
                box.innerHTML += `<div class="flex justify-end mb-4"><div class="bg-purple-600 text-white px-4 py-2 rounded-2xl rounded-tr-none max-w-[85%]">${text}</div></div>`;
                input.value = '';

                // โหลดเดอร์แอนิเมชันตอนรอคำตอบจริง
                const loadingId = "loader-" + Date.now();
                box.innerHTML += `
                    <div id="${loadingId}" class="flex flex-col items-start mb-4">
                        <div class="text-[11px] text-gray-500 mb-1">ॐ DRAGY ENGINE กําลังประมวลผล...</div>
                        <div class="bg-[#0d061a] border border-purple-950/60 px-4 py-2 rounded-2xl rounded-tl-none flex gap-1 items-center">
                            <div class="w-1.5 h-1.5 bg-purple-500 rounded-full animate-bounce"></div>
                            <div class="w-1.5 h-1.5 bg-purple-500 rounded-full animate-bounce [animation-delay:0.2s]"></div>
                        </div>
                    </div>
                `;
                
                const s = document.getElementById('main-scroll-area');
                s.scrollTop = s.scrollHeight;

                try {
                    const res = await fetch('/api/chat', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ message: text, history: historyContext })
                    });
                    const data = await res.json();
                    document.getElementById(loadingId).remove();

                    // แสดงข้อความคำตอบจริงจากโมเดล AI
                    box.innerHTML += `
                        <div class="flex flex-col items-start mb-4">
                            <span class="text-[11px] text-yellow-500 font-medium mb-1">ॐ DRAGY ENGINE</span>
                            <div class="bg-[#0d061a] border border-purple-950/60 text-gray-200 px-4 py-3 rounded-2xl rounded-tl-none max-w-[85%]">
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
                    box.innerHTML += `<div class="text-red-400 text-xs mb-4">⚠️ เกิดข้อผิดพลาดระบบเครือข่ายปลายทาง</div>`;
                }
                
                s.scrollTop = s.scrollHeight;
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