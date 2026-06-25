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
    "chat_used": 26,
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
# 🤖 BACKEND API: อัปเดตโครงสร้างดึงคำตอบให้ปลอดภัยและดึงข้อความได้ชัวร์
# =====================================================================
@app.post("/api/chat")
async def ai_chat_endpoint(payload: ChatPayload):
    if not payload.message.strip():
        return JSONResponse(status_code=400, content={"reply": "กรุณาพิมพ์ข้อความก่อนส่งครับ"})
    
    # ถ้ายังไม่ได้ตั้งค่าคีย์บน Render ให้แสดงคำแนะนำวิธีใส่คีย์แทน
    if not GEMINI_API_KEY:
        return JSONResponse(
            status_code=200, 
            content={
                "reply": "⚠️ <b>ไม่พบ GEMINI_API_KEY บนระบบ!</b><br>โปรดไปที่หน้าแดชบอร์ด Render ของคุณ -> เมนู <b>Environment</b> -> เพิ่มตัวแปรชื่อ <code>GEMINI_API_KEY</code> แล้วใส่ API Key จาก Google AI Studio ลงไปครับ จากนั้นตัวแปรนี้จะคุยได้ทันที",
                "quota": GLOBAL_QUOTA
            }
        )

    # สะสมจำนวนใช้งานในโควตา
    GLOBAL_QUOTA["chat_used"] += 1
    
    system_instruction = "คุณคือ ॐ DRAGY AI แพลตฟอร์ม AI อัจฉริยะที่เชี่ยวชาญด้านศิลปะ ภาพ วิดีโอ และความรู้รอบตัว จงตอบคำถามเป็นภาษาไทยด้วยน้ำเสียงสุภาพและเป็นมืออาชีพ"
    
    # จัดโครงสร้างประวัติการคุยให้ตรงตามข้อกำหนดของ Google
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

    # ส่งคำขอหา Google Gemini Direct Endpoints
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    body = {
        "contents": contents_payload,
        "systemInstruction": { "parts": [{"text": system_instruction}] },
        "generationConfig": { "temperature": 0.7, "maxOutputTokens": 2048 }
    }

    try:
        response = requests.post(url, headers=headers, json=body, timeout=25)
        response_json = response.json()
        
        # ค้นหาข้อความคำตอบอย่างละเอียด ป้องกันโครงสร้างขัดแย้ง
        if "candidates" in response_json and len(response_json["candidates"]) > 0:
            candidate = response_json["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"] and len(candidate["content"]["parts"]) > 0:
                ai_reply = candidate["content"]["parts"][0]["text"]
                # จัดรูปแบบขึ้นบรรทัดใหม่ให้แสดงบน HTML ได้สวยงาม และตัด Markdown ที่เกินออก
                ai_reply = ai_reply.replace("\n", "<br>").replace("**", "")
            else:
                ai_reply = f"⚠️ ได้รับโครงสร้างข้อมูลที่ไม่สมบูรณ์จาก API: {str(response_json)}"
        elif "error" in response_json:
            ai_reply = f"❌ เกิดข้อผิดพลาดจาก Google Gemini API: {response_json['error'].get('message', 'ไม่ทราบสาเหตุ')}"
        else:
            ai_reply = f"⚠️ ปฏิเสธการประมวลผล หรือคีย์ API ไม่ถูกต้อง (Response: {str(response_json)})"
            
    except Exception as e:
        ai_reply = f"❌ ขัดข้องในการเชื่อมโยงเครือข่าย: {str(e)}"

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
            .glow-purple { box-shadow: 0 0 50px rgba(147, 51, 234, 0.25); }
            .glow-gold-icon { text-shadow: 0 0 20px rgba(234, 179, 8, 0.6); }
            .text-gradient { background: linear-gradient(to right, #60a5fa, #c084fc, #f472b6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
            .custom-scrollbar::-webkit-scrollbar { width: 5px; }
            .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
            .custom-scrollbar::-webkit-scrollbar-thumb { background: #231145; border-radius: 10px; }
        </style>
    </head>
    <body class="text-gray-200 min-h-screen flex overflow-hidden">

        <aside class="w-64 bg-[#060310]/95 border-r border-purple-950/40 p-4 flex flex-col justify-between hidden md:flex flex-shrink-0 z-20">
            <div>
                <div class="flex flex-col px-1 py-3 mb-4 border-b border-purple-950/30">
                    <div class="text-2xl font-bold text-white flex items-center gap-1">
                        <span class="text-yellow-500 font-bold glow-gold-icon">ॐ</span> DRAGY AI
                    </div>
                    <span class="text-[9px] text-gray-500 uppercase tracking-widest mt-1">Create Images • Videos • Knowledge</span>
                </div>

                <button onclick="window.location.reload()" class="w-full bg-transparent border border-purple-900/40 hover:border-purple-600/40 hover:bg-purple-950/10 text-gray-300 rounded-xl py-2 px-4 flex items-center justify-between text-sm transition mb-5">
                    <span class="flex items-center gap-2"><i data-lucide="plus" class="w-4 h-4"></i> New Chat</span>
                    <span class="text-[11px] text-gray-500 border border-gray-800 px-1.5 py-0.5 rounded">⌘ K</span>
                </button>

                <nav class="space-y-1">
                    <a href="/" class="flex items-center gap-3 px-3 py-2.5 bg-purple-950/30 text-purple-300 rounded-xl text-sm font-medium"><i data-lucide="home" class="w-4.5 h-4.5"></i> หน้าแรก</a>
                    <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 hover:text-gray-200 hover:bg-white/5 rounded-xl text-sm transition"><i data-lucide="message-square" class="w-4.5 h-4.5"></i> AI Chat</a>
                    <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 hover:text-gray-200 hover:bg-white/5 rounded-xl text-sm transition"><i data-lucide="image" class="w-4.5 h-4.5"></i> AI Image</a>
                    <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 hover:text-gray-200 hover:bg-white/5 rounded-xl text-sm transition"><i data-lucide="video" class="w-4.5 h-4.5"></i> AI Video</a>
                </nav>
            </div>
            
            <div class="space-y-4">
                <div class="bg-[#0b051c] border border-purple-950/60 rounded-2xl p-3.5 text-xs text-gray-400 space-y-2.5">
                    <div class="flex justify-between items-center text-[11px] text-gray-500">
                        <span>สิทธิ์การใช้งาน (Pro)</span>
                        <span class="text-green-400 text-[10px]">Active</span>
                    </div>
                    <div class="space-y-1">
                        <div class="flex justify-between text-[11px]">
                            <span>ข้อความแชท</span>
                            <span id="quota-txt" class="text-gray-300 font-medium">26 / 50</span>
                        </div>
                    </div>
                </div>
            </div>
        </aside>

        <main class="flex-1 flex flex-col justify-between p-4 md:p-6 relative overflow-hidden z-10">
            <div class="flex justify-end items-center gap-3 flex-shrink-0 z-20">
                <button class="bg-blue-600 text-white text-xs font-medium py-2 px-4 rounded-xl shadow-lg">Sign In with Google</button>
            </div>

            <div id="main-scroll-area" class="flex-1 w-full max-w-3xl mx-auto my-4 overflow-y-auto custom-scrollbar flex flex-col justify-start px-2">
                <div id="welcome-view" class="w-full flex flex-col items-center text-center pt-10 pb-4 space-y-6 flex-shrink-0">
                    <div class="relative w-36 h-36 flex items-center justify-center bg-gradient-to-b from-purple-600/10 to-transparent rounded-full border border-purple-500/10 glow-purple">
                        <span class="text-6xl text-yellow-500 font-bold glow-gold-icon select-none">ॐ</span>
                    </div>
                    <div class="space-y-2">
                        <h1 class="text-4xl font-bold tracking-tight text-gradient">สวัสดีครับ ยินดีต้อนรับ 👋</h1>
                        <p class="text-lg text-gray-400 font-light">วันนี้ให้ <span class="text-purple-400 font-medium">ॐ DRAGY AI</span> ขับเคลื่อนไอเดียอะไรดี?</p>
                    </div>
                </div>
                <div id="chat-box" class="w-full hidden space-y-5 text-sm pb-6"></div>
            </div>

            <div class="w-full max-w-3xl mx-auto flex-shrink-0 z-20">
                <div class="bg-[#0f0722]/90 border border-purple-500/20 rounded-3xl p-4 flex flex-col gap-2">
                    <textarea id="user-input" class="w-full bg-transparent text-gray-200 placeholder-gray-600 text-sm focus:outline-none resize-none h-12" placeholder="พิมพ์ข้อความสั่งการ AI หรือป้อนคำสั่งสร้างสรรค์งานพุทธศิลป์ วิดีโอ..."></textarea>
                    <div class="flex justify-between items-center border-t border-purple-950/60 pt-2">
                        <div class="flex gap-2 text-xs text-gray-500">
                            <span class="px-2 py-1 bg-purple-950/40 rounded-lg">🧭 DeepSearch</span>
                            <span class="px-2 py-1 bg-purple-950/40 rounded-lg">💡 Think</span>
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

                // User chat bubble
                box.innerHTML += `<div class="flex justify-end mb-4"><div class="bg-purple-600 text-white px-4 py-2.5 rounded-2xl rounded-tr-none max-w-[85%] shadow-md">${text}</div></div>`;
                input.value = '';

                // Loader view
                const loadingId = "loader-" + Date.now();
                box.innerHTML += `
                    <div id="${loadingId}" class="flex flex-col items-start w-full opacity-70 mb-4">
                        <div class="text-[11px] text-gray-500 mb-1">ॐ DRAGY ENGINE กำลังประมวลผล...</div>
                        <div class="bg-[#0d061a] border border-purple-950/60 px-4 py-2.5 rounded-2xl rounded-tl-none flex items-center gap-1.5">
                            <div class="w-2 h-2 bg-purple-500 rounded-full animate-bounce"></div>
                            <div class="w-2 h-2 bg-purple-500 rounded-full animate-bounce [animation-delay:0.2s]"></div>
                            <div class="w-2 h-2 bg-purple-500 rounded-full animate-bounce [animation-delay:0.4s]"></div>
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

                    // AI chat bubble
                    box.innerHTML += `
                        <div class="flex flex-col items-start mb-4">
                            <span class="text-[11px] text-yellow-500 font-medium mb-1">ॐ DRAGY ENGINE</span>
                            <div class="bg-[#0d061a] border border-purple-950/60 text-gray-200 px-4 py-3 rounded-2xl rounded-tl-none max-w-[85%] shadow-sm leading-relaxed">
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
                    box.innerHTML += `<div class="text-red-400 text-xs mb-4">⚠️ เกิดข้อผิดพลาดในการเชื่อมต่อเน็ตหลังบ้าน หรือเซิร์ฟเวอร์ยังอัปเดตไม่เสร็จสิ้น</div>`;
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