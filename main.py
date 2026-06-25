import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="ॐ DRAGY AI - Production Engine")

# ดึงสิทธิ์ความปลอดภัยผ่าน Environment Variable ของ Render
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# โครงสร้างสำหรับรับประวัติการแชท (Chat History Context) และคำสั่งจากหน้าบ้าน
class ChatMessage(BaseModel):
    role: str      # 'user' หรือ 'model'
    parts: str     # ข้อความที่ส่ง

class ChatPayload(BaseModel):
    message: str
    model: Optional[str] = "Grok 3"
    deep_search: Optional[bool] = False
    think_mode: Optional[bool] = False
    history: List[ChatMessage] = []

# =====================================================================
# 🤖 BACKEND API: เชื่อมต่อ REAL GEMINI API ENGINE + MEMORY CONTEXT
# =====================================================================
@app.post("/api/chat")
async def ai_chat_endpoint(payload: ChatPayload):
    if not payload.message.strip():
        return JSONResponse(status_code=400, content={"reply": "กรุณาพิมพ์ข้อความ..."})
    
    if not GEMINI_API_KEY:
        return JSONResponse(
            status_code=500, 
            content={"reply": "❌ ตรวจไม่พบ GEMINI_API_KEY! กรุณาเพิ่มค่านี้ในเมนู Environment บนหน้าเว็บ Render ก่อนใช้งานครับ"}
        )

    # 1. ระบบดัดแปลง Prompt ตามสถานะปุ่มกดสวิตช์หน้าบ้าน (Think / DeepSearch)
    system_instruction = "คุณคือ ॐ DRAGY AI แพลตฟอร์ม AI อัจฉริยะที่เชี่ยวชาญด้านศิลปะ ภาพ วิดีโอ และความรู้รอบตัว จงตอบคำถามเป็นภาษาไทยด้วยน้ำเสียงสุภาพ เป็นมืออาชีพ และน่าเชื่อถือ"
    
    current_prompt = payload.message
    if payload.think_mode:
        current_prompt = f"[โหมดวิเคราะห์ลึก]: จงแสดงตรรกะเหตุผลหรือสรุปความรอบคอบแยกเป็นหัวข้อย่อยก่อนให้คำตอบสุทธิกับผู้ใช้จากคำถามนี้: {current_prompt}"
    if payload.deep_search:
        current_prompt = f"[โหมดสืบค้นเชิงลึก]: จงพยายามทำตัวเหมือนคุณได้อัปเดตข้อมูลสดใหม่ ค้นหาความจริงอย่างละเอียดรอบด้านเพื่อตอบคำถามนี้: {current_prompt}"

    # 2. ฟอร์แมตโครงสร้างประวัติการคุยเพื่อให้ AI จำบริบทได้ (Gemini API Format)
    contents_payload = []
    for msg in payload.history:
        contents_payload.append({
            "role": msg.role,
            "parts": [{"text": msg.parts}]
        })
    
    # เพิ่มข้อความปัจจุบันเข้าไปท้ายสุดของคิวสนทนา
    contents_payload.append({
        "role": "user",
        "parts": [{"text": current_prompt}]
    })

    # 3. ส่งคำขอตรงไปยัง Endpoint หลักของ Google Gemini 1.5 Flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    body = {
        "contents": contents_payload,
        "systemInstruction": {
            "parts": [{"text": system_instruction}]
        },
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2048
        }
    }

    try:
        response = requests.post(url, headers=headers, json=body, timeout=30)
        response_json = response.json()
        
        # แกะเอาข้อความผลลัพธ์จากเซิร์ฟเวอร์ Google
        if "candidates" in response_json and len(response_json["candidates"]) > 0:
            ai_reply = response_json["candidates"][0]["content"]["parts"][0]["text"]
            # แปลงสัญญลักษณ์ขึ้นบรรทัดใหม่จาก \n เป็น <br> สำหรับ HTML Rendering
            ai_reply = ai_reply.replace("\n", "<br>")
        else:
            ai_reply = f"⚠️ ปฏิเสธการตอบกลับจาก AI: {response_json.get('error', {}).get('message', 'ไม่สามารถประมวลผลได้')}"
            
    except Exception as e:
        ai_reply = f"❌ เกิดข้อผิดพลาดในระบบการเชื่อมต่อโครงข่าย: {str(e)}"

    return {
        "reply": ai_reply,
        "usage_update": {
            "chat_used": 1,  # ส่งสัญญาณบอกหน้าบ้านว่าตัดโควตาจริงสำเร็จ
            "image_used": 0
        }
    }

# =====================================================================
# 🌐 FRONTEND: ดีไซน์สุดพรีเมียม สไตล์ Grok Vibe ผสม มณฑลาสีทองเรืองแสง
# =====================================================================
@app.get("/", response_class=HTMLResponse)
async def home_interface():
    return """
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dragy AI</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <script src="https://unpkg.com/lucide@latest"></script>
        <style>
            body { font-family: 'Prompt', sans-serif; }
            .bg-cosmic-dark {
                background: radial-gradient(circle at 60% 30%, #150933 0%, #080314 60%, #030108 100%);
            }
            .glow-purple {
                box-shadow: 0 0 50px rgba(147, 51, 234, 0.25);
            }
            .glow-gold-icon {
                text-shadow: 0 0 20px rgba(234, 179, 8, 0.6);
            }
            .text-gradient {
                background: linear-gradient(to right, #60a5fa, #c084fc, #f472b6);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .custom-scrollbar::-webkit-scrollbar { width: 5px; }
            .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
            .custom-scrollbar::-webkit-scrollbar-thumb { background: #231145; border-radius: 10px; }
        </style>
    </head>
    <body class="bg-cosmic-dark text-gray-200 min-h-screen flex overflow-hidden">

        <!-- ================= SIDEBAR ================= -->
        <aside class="w-64 bg-[#060310]/95 border-r border-purple-950/40 p-4 flex flex-col justify-between hidden md:flex flex-shrink-0 z-20">
            <div>
                <!-- Logo Brand -->
                <div class="flex items-center gap-3 px-2 py-3 mb-4">
                    <div class="w-8 h-8 bg-gradient-to-tr from-purple-600 to-indigo-600 rounded-xl flex items-center justify-center font-bold text-white text-lg shadow-md shadow-purple-500/20">D</div>
                    <span class="text-xl font-bold text-white tracking-wide">Dragy AI</span>
                </div>

                <!-- New Chat Button -->
                <button onclick="window.location.reload()" class="w-full bg-transparent border border-purple-900/40 hover:border-purple-600/40 hover:bg-purple-950/10 text-gray-300 rounded-xl py-2 px-4 flex items-center justify-between text-sm transition duration-200 mb-5">
                    <span class="flex items-center gap-2"><i data-lucide="plus" class="w-4 h-4"></i> New Chat</span>
                    <span class="text-[11px] text-gray-500 border border-gray-800 px-1.5 py-0.5 rounded">⌘ K</span>
                </button>

                <!-- Menu Lists -->
                <nav class="space-y-1">
                    <a href="/" class="flex items-center gap-3 px-3 py-2.5 bg-purple-950/30 text-purple-300 rounded-xl text-sm font-medium"><i data-lucide="home" class="w-4.5 h-4.5"></i> หน้าแรก</a>
                    <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 hover:text-gray-200 hover:bg-white/5 rounded-xl text-sm transition"><i data-lucide="message-square" class="w-4.5 h-4.5"></i> AI Chat</a>
                    <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 hover:text-gray-200 hover:bg-white/5 rounded-xl text-sm transition"><i data-lucide="image" class="w-4.5 h-4.5"></i> AI Image</a>
                    <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 hover:text-gray-200 hover:bg-white/5 rounded-xl text-sm transition"><i data-lucide="video" class="w-4.5 h-4.5"></i> AI Video</a>
                </nav>
            </div>

            <!-- Quota Tracking Systems -->
            <div class="space-y-4">
                <div class="bg-[#0b051c] border border-purple-950/60 rounded-2xl p-3.5 text-xs text-gray-400 space-y-2.5">
                    <div class="flex justify-between items-center text-[11px] text-gray-500">
                        <span>การทำงานระบบ Real AI</span>
                        <span id="ai-status" class="text-green-400 text-[10px]">Online</span>
                    </div>
                    <div class="space-y-1">
                        <div class="flex justify-between text-[11px]">
                            <span class="text-gray-400">จำนวนครั้งส่งคำขอ</span>
                            <span id="local-counter" class="text-gray-300 font-medium">0 เซสชัน</span>
                        </div>
                    </div>
                </div>
                <div class="text-center p-1 text-[11px] text-gray-600">
                    Engine V2.5 Stable
                </div>
            </div>
        </aside>

        <!-- ================= MAIN WORKSPACE ================= -->
        <main class="flex-1 flex flex-col justify-between p-4 md:p-6 relative overflow-hidden z-10">
            
            <!-- Header Bar -->
            <div class="flex justify-end items-center gap-3 flex-shrink-0 z-20">
                <button class="flex items-center gap-1 px-3 py-1.5 bg-[#120724] border border-purple-950 rounded-xl text-xs text-gray-300 hover:bg-[#1d0c3a] transition">
                    <i data-lucide="globe" class="w-3.5 h-3.5"></i> TH <i data-lucide="chevron-down" class="w-3 h-3"></i>
                </button>
                <button class="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-medium py-2 px-4 rounded-xl shadow-lg shadow-blue-600/20 transition">
                    Sign In with Google
                </button>
            </div>

            <!-- Scrollable Chat Body -->
            <div id="main-scroll-area" class="flex-1 w-full max-w-3xl mx-auto my-4 overflow-y-auto custom-scrollbar flex flex-col justify-start px-2">
                
                <!-- Initial Landing Page -->
                <div id="welcome-view" class="w-full flex flex-col items-center text-center pt-10 pb-4 space-y-6 flex-shrink-0">
                    <div class="relative w-36 h-36 flex items-center justify-center bg-gradient-to-b from-purple-600/10 to-transparent rounded-full border border-purple-500/10 glow-purple">
                        <div class="absolute inset-1 border border-dashed border-yellow-500/20 rounded-full animate-[spin_120s_linear_infinite]"></div>
                        <span class="text-6xl text-yellow-500 font-bold glow-gold-icon select-none">ॐ</span>
                    </div>
                    <div class="space-y-2">
                        <h1 class="text-4xl md:text-5xl font-bold tracking-tight text-gradient">สวัสดีครับ 👋</h1>
                        <p class="text-lg text-gray-400 font-light">วันนี้ให้ <span class="text-purple-400 font-medium">ॐ DRAGY AI</span> รับใช้เรื่องใดดีครับ?</p>
                    </div>
                </div>

                <!-- Chat Box Screen -->
                <div id="chat-box" class="w-full hidden space-y-5 text-sm pb-6"></div>
            </div>

            <!-- Control Bar Component -->
            <div class="w-full max-w-3xl mx-auto flex-shrink-0 z-20">
                <div class="bg-[#0f0722]/90 border border-purple-500/20 rounded-3xl p-4 shadow-2xl focus-within:border-purple-500/50 transition duration-200">
                    <textarea id="user-input" class="w-full bg-transparent text-gray-200 placeholder-gray-600 text-sm focus:outline-none resize-none h-14 custom-scrollbar" placeholder="พิมพ์คุยกับ AI ของจริงสดๆ ตรงนี้ได้เลย..."></textarea>
                    
                    <div class="flex justify-between items-center mt-2 pt-2 border-t border-purple-950/60">
                        <div class="flex items-center gap-1.5">
                            <button id="btn-deepsearch" onclick="toggleFeature('deepsearch')" class="flex items-center gap-1 px-3 py-1.5 text-xs font-medium text-gray-500 border border-purple-950 bg-transparent rounded-xl hover:text-gray-300 transition duration-150">
                                <i data-lucide="compass" class="w-3.5 h-3.5"></i> DeepSearch
                            </button>
                            <button id="btn-think" onclick="toggleFeature('think')" class="flex items-center gap-1 px-3 py-1.5 text-xs font-medium text-gray-500 border border-purple-950 bg-transparent rounded-xl hover:text-gray-300 transition duration-150">
                                <i data-lucide="lightbulb" class="w-3.5 h-3.5"></i> Think
                            </button>
                        </div>
                        <div class="flex items-center gap-2">
                            <div class="relative">
                                <select id="model-select" class="appearance-none bg-[#150b2e] border border-purple-950 px-3 py-1.5 pr-7 text-xs text-gray-400 rounded-xl focus:outline-none cursor-pointer hover:text-gray-200 transition">
                                    <option value="Gemini 1.5 Flash">Gemini Core (Live)</option>
                                </select>
                                <i data-lucide="chevron-down" class="w-3 h-3 text-gray-500 absolute right-2.5 top-2.5 pointer-events-none"></i>
                            </div>
                            <button id="submit-btn" onclick="submitChatRequest()" class="p-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl shadow-lg shadow-blue-600/30 transition duration-150">
                                <i data-lucide="arrow-up" class="w-4 h-4"></i>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Shortcuts Grid (คลิกเพื่อยิงข้อความด่วนเข้า AI ทันที) -->
                <div id="shortcuts-grid" class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 mt-4">
                    <div onclick="clickShortcut('ช่วยอธิบายสัญลักษณ์ โอม (ॐ) ในเชิงพุทธศิลป์และความเป็นสิริมงคลหน่อย')" class="bg-[#0b0519]/60 border border-purple-950/50 hover:border-purple-500/30 p-3 rounded-2xl cursor-pointer flex flex-col justify-between h-20 transition duration-200 group">
                        <p class="text-[11px] text-gray-400 group-hover:text-gray-200 leading-tight">ความหมายมงคล <span class="block text-gray-600 text-[10px]">สัญลักษณ์ ॐ</span></p>
                        <div class="text-xs text-yellow-500">🔱</div>
                    </div>
                    <div onclick="clickShortcut('ช่วยวางไอเดียเขียนสคริปต์ทำคลิปสั้นสไตล์พุทธศิลป์ร่วมสมัยลง TikTok ให้ปังหน่อย')" class="bg-[#0b0519]/60 border border-purple-950/50 hover:border-purple-500/30 p-3 rounded-2xl cursor-pointer flex flex-col justify-between h-20 transition duration-200 group">
                        <p class="text-[11px] text-gray-400 group-hover:text-gray-200 leading-tight">สคริปต์คลิปสั้น <span class="block text-gray-600 text-[10px]">ลงขายงานบน TikTok</span></p>
                        <div class="text-xs text-cyan-400">🎵</div>
                    </div>
                    <div onclick="clickShortcut('สรุปเทรนด์เทคโนโลยี AI ล่าสุดของปีนี้ให้ฟังหน่อยว่ามีอะไรว้าวบ้าง')" class="bg-[#0b0519]/60 border border-purple-950/50 hover:border-purple-500/30 p-3 rounded-2xl cursor-pointer flex flex-col justify-between h-20 transition duration-200 group">
                        <p class="text-[11px] text-gray-400 group-hover:text-gray-200 leading-tight">สรุปข่าวเทคโนโลยี <span class="block text-gray-600 text-[10px]">AI โลกวันนี้</span></p>
                        <i data-lucide="newspaper" class="w-4 h-4 text-blue-400"></i>
                    </div>
                    <div onclick="clickShortcut('แต่งกลอนสุภาพสรรเสริญความเจริญรุ่งเรืองและสติปัญญาให้หน่อย')" class="bg-[#0b0519]/60 border border-purple-950/50 hover:border-purple-500/30 p-3 rounded-2xl cursor-pointer flex flex-col justify-between h-20 transition duration-200 group">
                        <p class="text-[11px] text-gray-400 group-hover:text-gray-200 leading-tight">แต่งกลอนสุภาพ <span class="block text-gray-600 text-[10px]">เสริมสติปัญญา</span></p>
                        <i data-lucide="lightbulb" class="w-4 h-4 text-purple-400"></i>
                    </div>
                </div>

                <div class="w-full text-center text-[10px] text-gray-600 mt-4">
                    ॐ DRAGY PLATFORM POWERED BY REAL GEMINI INTELLIGENCE ENGINE
                </div>
            </div>
        </main>

        <!-- ================= APP SCRIPTS & CORE MEMORY LOGIC ================= -->
        <script>
            lucide.createIcons();
            
            let featureState = { deepsearch: false, think: false };
            let chatMemoryContext = []; // อาร์เรย์เก็บประวัติแชทของเซสชันปัจจุบันส่งต่อให้ AI
            let totalRequests = 0;

            const userInput = document.getElementById('user-input');
            const mainScrollArea = document.getElementById('main-scroll-area');
            const chatBox = document.getElementById('chat-box');
            const welcomeView = document.getElementById('welcome-view');
            const shortcutsGrid = document.getElementById('shortcuts-grid');

            function toggleFeature(type) {
                featureState[type] = !featureState[type];
                const btn = document.getElementById(`btn-${type}`);
                if (featureState[type]) {
                    btn.classList.remove('text-gray-500', 'border-purple-950');
                    btn.classList.add(type === 'deepsearch' ? 'text-blue-400' : 'text-yellow-400', 'border-purple-500/30', 'bg-purple-950/30');
                } else {
                    btn.classList.add('text-gray-500', 'border-purple-950');
                    btn.classList.remove('text-blue-400', 'text-yellow-400', 'border-purple-500/30', 'bg-purple-950/30');
                }
            }

            function clickShortcut(text) {
                userInput.value = text;
                submitChatRequest();
            }

            async function submitChatRequest() {
                const text = userInput.value.trim();
                if (!text) return;

                // ซ่อนการ์ดหน้าแรกเมื่อเริ่มสนทนา
                welcomeView.classList.add('hidden');
                shortcutsGrid.classList.add('hidden');
                chatBox.classList.remove('hidden');

                // 1. เพิ่มกล่องคำถามของผู้ใช้บนหน้าจอ
                const userDiv = document.createElement('div');
                userDiv.className = 'flex flex-col items-end w-full animate-fade-in';
                userDiv.innerHTML = `<div class="bg-purple-600/90 text-white px-4 py-2.5 rounded-2xl rounded-tr-none max-w-[85%] shadow-md">${text}</div>`;
                chatBox.appendChild(userDiv);
                
                userInput.value = '';
                mainScrollArea.scrollTop = mainScrollArea.scrollHeight;

                // สร้างสถานะกำลังโหลด (Loading Spinner)
                const loadingDiv = document.createElement('div');
                loadingDiv.className = 'flex flex-col items-start w-full opacity-70';
                loadingDiv.id = 'loading-placeholder';
                loadingDiv.innerHTML = `
                    <div class="text-[11px] text-gray-500 mb-1">ॐ DRAGY ENGINEกำลังคิด...</div>
                    <div class="bg-[#0d061a] border border-purple-950/60 text-gray-500 px-4 py-2.5 rounded-2xl rounded-tl-none flex items-center gap-2">
                        <div class="w-2 h-2 bg-purple-500 rounded-full animate-bounce"></div>
                        <div class="w-2 h-2 bg-purple-500 rounded-full animate-bounce [animation-delay:0.2s]"></div>
                        <div class="w-2 h-2 bg-purple-500 rounded-full animate-bounce [animation-delay:0.4s]"></div>
                    </div>
                `;
                chatBox.appendChild(loadingDiv);
                mainScrollArea.scrollTop = mainScrollArea.scrollHeight;

                try {
                    // 2. ยิงแฮนด์เชกข้อมูลหลังบ้าน FastAPI
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            message: text,
                            model: "Gemini 1.5 Flash",
                            deep_search: featureState.deepsearch,
                            think_mode: featureState.think,
                            history: chatMemoryContext // ส่ง Memory ของเดิมไปด้วยเพื่อให้คุยต่อเนื่องรู้เรื่อง
                        })
                    });
                    const data = await response.json();

                    // ลบตัว Loading ออก
                    document.getElementById('loading-placeholder').remove();

                    // 3. เพิ่มกล่องคำตอบจากใจจริงของ Gemini AI บนหน้าจอ
                    const aiDiv = document.createElement('div');
                    aiDiv.className = 'flex flex-col items-start w-full';
                    aiDiv.innerHTML = `
                        <div class="flex items-center gap-1.5 mb-1 text-[11px] text-yellow-500 font-medium tracking-wider">
                            <span>ॐ DRAGY ENGINE</span>
                        </div>
                        <div class="bg-[#0d061a] border border-purple-950/60 text-gray-200 px-4 py-3 rounded-2xl rounded-tl-none max-w-[85%] shadow-sm leading-relaxed text-[13.5px]">
                            ${data.reply}
                        </div>
                    `;
                    chatBox.appendChild(aiDiv);

                    // 4. บันทึกประวัติการแชท (Memory Context Stack) เอาไว้รันคราวหน้า
                    chatMemoryContext.push({ role: "user", parts: text });
                    chatMemoryContext.push({ role: "model", parts: data.reply.replace(/<br>/g, "\\n") });

                    // อัปเดตตัวแปรแสดงสถานะที่แถบด้านซ้ายมือ
                    totalRequests++;
                    document.getElementById('local-counter').innerText = `${totalRequests} ครั้ง`;

                } catch (err) {
                    console.error("Communication error:", err);
                    document.getElementById('loading-placeholder').innerHTML = `<div class="text-red-500 p-2">การเชื่อมต่อล้มเหลว กรุณาลองใหม่อีกครั้ง</div>`;
                }

                mainScrollArea.scrollTop = mainScrollArea.scrollHeight;
            }

            userInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    submitChatRequest();
                }
            });
        </script>
    </body>
    </html>"""