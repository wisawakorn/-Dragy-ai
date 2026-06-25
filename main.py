import os
import json
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Dragy AI Platform")

# =====================================================================
# 🗄️ DATABASE & STATE SYSTEM (ระบบฐานข้อมูลควบคุมสิทธิ์และโควตาจำลอง)
# =====================================================================
# โครงสร้างผู้ใช้จำลอง เพื่อให้ระบบหลังบ้านสามารถคำนวณและตัดโควตาได้จริงบน Render
USER_DATABASE = {
    "mock_user_id": {
        "name": "Dragy Creator",
        "email": "creator@dragy.ai",
        "tier": "Pro",  # Free, Pro, Premium
        "quota": {
            "chat_used": 23,
            "chat_limit": 50,
            "image_used": 12,
            "image_limit": 15,
            "video_used": 0,
            "video_limit": 1
        }
    }
}

class ChatPayload(BaseModel):
    message: str
    model: Optional[str] = "Grok 3"
    deep_search: Optional[bool] = False
    think_mode: Optional[bool] = False

# =====================================================================
# 🤖 AI CORE PROCESSING ENDPOINT (ระบบประมวลผลแชทหลังบ้าน)
# =====================================================================
@app.post("/api/chat")
async def ai_chat_endpoint(payload: ChatPayload):
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    user = USER_DATABASE["mock_user_id"]
    
    # ตรวจสอบและตัดโควตาจริงหลังบ้าน
    if user["quota"]["chat_used"] >= user["quota"]["chat_limit"]:
        return JSONResponse(
            status_code=429,
            content={"reply": "❌ โควตาแชทของคุณหมดแล้ว กรุณาอัปเกรดแพ็กเกจเพื่อใช้งานต่อ"}
        )
    
    # อัปเดตจำนวนการใช้งานในระบบ
    user["quota"]["chat_used"] += 1
    
    # ส่วนประมวลผลคำตอบ (สามารถเชื่อมต่อ OpenAI / Anthropic / Grok API ตรงนี้ได้เลย)
    user_prompt = payload.message.lower()
    ai_reply = ""
    
    if "ภาพ" in user_prompt or "image" in user_prompt:
        ai_reply = f"✨ [โหมดสร้างภาพ] รับทราบครับ ระบบกำลังเตรียมส่งคำสั่งสร้างภาพในสไตล์ที่ต้องการผ่านโมเดล {payload.model}..."
    elif "วิดีโอ" in user_prompt or "video" in user_prompt:
        ai_reply = f"🎬 [โหมดสร้างวิดีโอ] เริ่มการประมวลผลวิดีโอสั้นจากข้อความของคุณ กรุณารอสักครู่..."
    else:
        ai_reply = f"🔱 ॐ DRAGY AI ได้รับข้อความของคุณแล้ว: \"{payload.message}\"ขณะนี้โหมดประมวลผลระดับสูงกำลังทำงาน"
        if payload.deep_search:
            ai_reply += " [เปิดใช้งาน DeepSearch ค้นหาข้อมูลเชิงลึกแบบ Real-time]"
        if payload.think_mode:
            ai_reply += " [เปิดใช้งาน Think Mode คิดวิเคราะห์แยกแยะตรรกะแบบเป็นขั้นตอน]"

    return {
        "reply": ai_reply,
        "current_quota": user["quota"]
    }

# =====================================================================
# 🌐 FRONTEND CORE INTERFACE (หน้าบ้านสไตล์พรีเมียม ॐ DRAGY AI)
# =====================================================================
@app.get("/", response_class=HTMLResponse)
async def home_interface():
    user_data = USER_DATABASE["mock_user_id"]
    quota = user_data["quota"]
    
    return f"""
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ॐ DRAGY AI - Create Images • Videos • Knowledge</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <script src="https://unpkg.com/lucide@latest"></script>
        <style>
            body {{ font-family: 'Prompt', sans-serif; }}
            .bg-gradient-dark {{
                background: radial-gradient(circle at center, #14082b 0%, #070312 80%, #030107 100%);
            }}
            .glow-gold {{
                box-shadow: 0 0 30px rgba(254, 224, 71, 0.15);
            }}
            .logo {{
                font-size: 26px;
                font-weight: 700;
                color: white;
                letter-spacing: 1px;
            }}
            .logo span {{
                color: #FFD700;
                font-size: 32px;
                margin-right: 6px;
                text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
            }}
            .custom-scrollbar::-webkit-scrollbar {{ width: 5px; }}
            .custom-scrollbar::-webkit-scrollbar-track {{ background: transparent; }}
            .custom-scrollbar::-webkit-scrollbar-thumb {{ background: #26114a; border-radius: 10px; }}
        </style>
    </head>
    <body class="bg-gradient-dark text-gray-200 min-h-screen flex overflow-hidden">

        <!-- ================= SIDEBAR ================= -->
        <aside class="w-68 bg-[#070311]/90 border-r border-purple-950/40 p-4 flex flex-col justify-between hidden md:flex">
            <div>
                <!-- Brand Logo ในรูปแบบที่คุณเลือก -->
                <div class="flex flex-col px-2 py-4 mb-4 border-b border-purple-950/30">
                    <div class="logo flex items-center">
                        <span>ॐ</span> DRAGY AI
                    </div>
                    <span class="text-[10px] text-gray-500 uppercase tracking-widest mt-1">Create Images • Videos • Knowledge</span>
                </div>

                <!-- New Chat ปุ่มกดรีเซ็ตหน้า -->
                <button onclick="window.location.reload()" class="w-full border border-purple-900/40 hover:border-purple-500/40 hover:bg-purple-950/20 text-gray-300 rounded-xl py-2 px-4 flex items-center justify-between text-sm transition mb-6">
                    <span class="flex items-center gap-2"><i data-lucide="plus" class="w-4 h-4"></i> New Chat</span>
                    <span class="text-xs text-gray-500 border border-gray-800 px-1.5 py-0.5 rounded">⌘ K</span>
                </button>

                <!-- รายการเมนูระบบ -->
                <nav class="space-y-1">
                    <a href="/" class="flex items-center gap-3 px-3 py-2.5 bg-purple-950/30 text-purple-300 rounded-xl text-sm font-medium"><i data-lucide="home" class="w-4 h-4"></i> หน้าแรก</a>
                    <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 hover:text-gray-200 hover:bg-white/5 rounded-xl text-sm transition"><i data-lucide="message-square" class="w-4 h-4"></i> AI Chat</a>
                    <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 hover:text-gray-200 hover:bg-white/5 rounded-xl text-sm transition"><i data-lucide="image" class="w-4 h-4"></i> AI Image</a>
                    <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 hover:text-gray-200 hover:bg-white/5 rounded-xl text-sm transition"><i data-lucide="video" class="w-4 h-4"></i> AI Video</a>
                    <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 hover:text-gray-200 hover:bg-white/5 rounded-xl text-sm transition"><i data-lucide="wrench" class="w-4 h-4"></i> เครื่องมือ AI</a>
                    <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 hover:text-gray-200 hover:bg-white/5 rounded-xl text-sm transition"><i data-lucide="history" class="w-4 h-4"></i> ประวัติแชท</a>
                </nav>

                <!-- แผงมอนิเตอร์โควตาการประมวลผลดึงค่าจากหลังบ้านจริง -->
                <div class="mt-6 bg-[#0c051f] border border-purple-950/60 rounded-2xl p-4 text-xs text-gray-400 space-y-3">
                    <div class="flex justify-between items-center border-b border-purple-950/40 pb-1.5">
                        <span class="font-medium text-gray-300">สิทธิ์การใช้งาน ({user_data["tier"]})</span>
                        <span class="text-green-400 text-[10px]">Active</span>
                    </div>
                    <div class="space-y-1">
                        <div class="flex justify-between">
                            <span class="flex items-center gap-1"><i data-lucide="message-circle" class="w-3 h-3 text-green-400"></i> ข้อความแชท</span>
                            <span id="quota-chat" class="text-gray-300">{quota["chat_used"]} / {quota["chat_limit"]}</span>
                        </div>
                        <div class="w-full bg-gray-900 h-1 rounded-full overflow-hidden">
                            <div id="bar-chat" class="bg-green-500 h-full transition-all duration-300" style="width: {(quota["chat_used"]/quota["chat_limit"])*100}%"></div>
                        </div>
                    </div>
                    <div class="space-y-1">
                        <div class="flex justify-between">
                            <span class="flex items-center gap-1"><i data-lucide="image" class="w-3 h-3 text-blue-400"></i> การสร้างภาพ</span>
                            <span id="quota-image" class="text-gray-300">{quota["image_used"]} / {quota["image_limit"]}</span>
                        </div>
                        <div class="w-full bg-gray-900 h-1 rounded-full overflow-hidden">
                            <div id="bar-image" class="bg-blue-500 h-full transition-all duration-300" style="width: {(quota["image_used"]/quota["image_limit"])*100}%"></div>
                        </div>
                    </div>
                    <div class="space-y-1">
                        <div class="flex justify-between">
                            <span class="flex items-center gap-1"><i data-lucide="video" class="w-3 h-3 text-purple-400"></i> เรนเดอร์วิดีโอ</span>
                            <span id="quota-video" class="text-gray-300">{quota["video_used"]} / {quota["video_limit"]}</span>
                        </div>
                        <div class="w-full bg-gray-900 h-1 rounded-full overflow-hidden">
                            <div id="bar-video" class="bg-purple-500 h-full transition-all duration-300" style="width: {(quota["video_used"]/quota["video_limit"])*100}%"></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ส่วนล่างสุดของ Sidebar -->
            <div class="space-y-2">
                <div class="bg-gradient-to-b from-[#1c0b3a] to-[#0a0317] border border-purple-500/20 rounded-xl p-3 text-center shadow-md">
                    <div class="text-xs font-semibold text-yellow-500 flex items-center justify-center gap-1 mb-1">
                        <i data-lucide="crown" class="w-3.5 h-3.5 fill-yellow-500"></i> Upgrade To Premium
                    </div>
                    <button class="w-full bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 text-white text-[11px] font-medium py-1.5 px-3 rounded-lg hover:opacity-90 transition">อัปเกรดระบบ</button>
                </div>
            </div>
        </aside>

        <!-- ================= MAIN PLATFORM WORKSPACE ================= -->
        <main class="flex-1 flex flex-col justify-between p-4 md:p-6 relative overflow-hidden">
            
            <!-- แถบด้านบน: ปุ่มเปลี่ยนโหมดภาษาและสถานะล็อกอิน -->
            <div class="flex justify-end items-center gap-3 z-10">
                <button class="flex items-center gap-1 px-3 py-1.5 bg-[#120724] border border-purple-950/60 rounded-xl text-xs text-gray-400 hover:text-white transition">
                    <i data-lucide="globe" class="w-3.5 h-3.5"></i> TH <i data-lucide="chevron-down" class="w-3 h-3"></i>
                </button>
                <button class="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-medium py-2 px-4 rounded-xl shadow-lg shadow-blue-600/10 transition">
                    <svg class="w-3.5 h-3.5 fill-white" viewBox="0 0 24 24"><path d="M12.24 10.285V13.4h6.887c-.275 1.565-1.88 4.604-6.887 4.604-4.33 0-7.866-3.577-7.866-8s3.536-8 7.866-8c2.46 0 4.105 1.025 5.047 1.926l2.427-2.334C17.955 2.192 15.34 1 12.24 1 6.033 1 1 6.033 1 12.24s5.033 11.24 11.24 11.24c6.478 0 10.793-4.537 10.793-10.997 0-.746-.08-1.32-.176-1.888H12.24z"/></svg>
                    Sign In with Google
                </button>
            </div>

            <!-- หน้าต่างแชทและแนะนำหลัก -->
            <div id="main-scroll-area" class="flex-1 w-full max-w-3xl mx-auto my-4 overflow-y-auto custom-scrollbar flex flex-col justify-start px-2 space-y-6">
                
                <!-- ส่วนต้อนรับเริ่มต้นเมื่อเปิดแอป -->
                <div id="welcome-view" class="w-full flex flex-col items-center text-center pt-16 space-y-4">
                    <div class="w-24 h-24 flex items-center justify-center bg-gradient-to-b from-yellow-500/10 to-transparent rounded-full border border-yellow-500/20 glow-gold">
                        <span class="text-5xl text-yellow-500 font-bold drop-shadow-[0_0_15px_rgba(234,179,8,0.4)]">ॐ</span>
                    </div>
                    <div class="space-y-2">
                        <h1 class="text-3xl md:text-4xl font-bold tracking-tight bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">สวัสดีครับ ยินดีต้อนรับ</h1>
                        <p class="text-sm md:text-base text-gray-400 font-light">วันนี้ให้ <span class="text-purple-400 font-medium">ॐ DRAGY AI</span> ขับเคลื่อนโปรเจกต์ของคุณอย่างไรดี?</p>
                    </div>
                </div>

                <!-- กล่องแสดงข้อความสนทนาแบบ Real-time -->
                <div id="chat-box" class="w-full hidden space-y-4 text-sm pb-4"></div>
            </div>

            <!-- กล่องรับคำสั่ง (Input Component) และกลุ่มเครื่องมือควบคุมพิเศษด้านล่าง -->
            <div class="w-full max-w-3xl mx-auto">
                <div class="bg-[#0e061c]/90 border border-purple-500/20 rounded-3xl p-4 shadow-2xl focus-within:border-purple-500/40 transition">
                    <textarea id="user-input" class="w-full bg-transparent text-gray-200 placeholder-gray-600 text-sm focus:outline-none resize-none h-16" placeholder="พิมพ์ข้อความสั่งการ AI หรือป้อนคำสั่งสร้างสรรค์งานพุทธศิลป์ วิดีโอ หรือความรู้ได้ที่นี่..."></textarea>
                    
                    <div class="flex justify-between items-center mt-2 pt-2 border-t border-purple-950/40">
                        <div class="flex items-center gap-1.5">
                            <button id="toggle-deepsearch" onclick="toggleOption('deepsearch')" class="flex items-center gap-1 px-3 py-1.5 text-xs font-medium text-gray-500 border border-purple-950/60 bg-transparent rounded-xl hover:text-gray-300 transition">
                                <i data-lucide="compass" class="w-3.5 h-3.5"></i> DeepSearch
                            </button>
                            <button id="toggle-think" onclick="toggleOption('think')" class="flex items-center gap-1 px-3 py-1.5 text-xs font-medium text-gray-500 border border-purple-950/60 bg-transparent rounded-xl hover:text-gray-300 transition">
                                <i data-lucide="lightbulb" class="w-3.5 h-3.5"></i> Think
                            </button>
                        </div>
                        <div class="flex items-center gap-2">
                            <div class="relative">
                                <select id="model-select" class="appearance-none bg-[#140a29] border border-purple-950 px-3 py-1.5 pr-7 text-xs text-gray-400 rounded-xl focus:outline-none cursor-pointer hover:text-gray-200 transition">
                                    <option value="Grok 3">Grok 3</option>
                                    <option value="Dragy Core-V1">Dragy Core-V1</option>
                                    <option value="Flux Image Gen">Flux Image Gen</option>
                                </select>
                                <i data-lucide="chevron-down" class="w-3 h-3 text-gray-500 absolute right-2.5 top-2.5 pointer-events-none"></i>
                            </div>
                            <button id="send-btn" onclick="executeMsgSend()" class="p-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl shadow-md transition">
                                <i data-lucide="arrow-up" class="w-4 h-4"></i>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- ประกาศข้อตกลงท้ายเว็บ -->
                <p class="text-center text-[10px] text-gray-600 mt-3">
                    ॐ DRAGY AI Multi-Model Platform • ข้อมูลการประมวลผลและการใช้บริการอยู่ภายใต้เงื่อนไขข้อตกลงของโควตาสมาชิกสิทธิ์แบรนด์
                </p>
            </div>
        </main>

        <!-- ================= APP LOGIC HANDLING (SCRIPT) ================= -->
        <script>
            lucide.createIcons();
            
            let flags = {{ deepsearch: false, think: false }};
            const userInput = document.getElementById('user-input');
            const mainScrollArea = document.getElementById('main-scroll-area');
            const chatBox = document.getElementById('chat-box');
            const welcomeView = document.getElementById('welcome-view');

            function toggleOption(type) {{
                flags[type] = !flags[type];
                const btn = document.getElementById(`toggle-${{type}}`);
                if(flags[type]) {{
                    btn.classList.remove('text-gray-500', 'border-purple-950/60');
                    btn.classList.add(type === 'deepsearch' ? 'text-blue-400' : 'text-yellow-400', 'border-purple-500/40', 'bg-purple-950/20');
                }} else {{
                    btn.classList.add('text-gray-500', 'border-purple-950/60');
                    btn.classList.remove('text-blue-400', 'text-yellow-400', 'border-purple-500/40', 'bg-purple-950/20');
                }}
            }}

            async function executeMsgSend() {{
                const text = userInput.value.trim();
                if (!text) return;

                // ซ่อนส่วน Welcome หนแรก
                welcomeView.classList.add('hidden');
                chatBox.classList.remove('hidden');

                // พ่นข้อความฝั่งผู้ใช้ขึ้นหน้าจอ
                const userNode = document.createElement('div');
                userNode.className = 'flex flex-col items-end w-full mb-4 animate-fade-in';
                userNode.innerHTML = `
                    <div class="bg-purple-600/90 text-white px-4 py-2.5 rounded-2xl rounded-tr-none max-w-[85%] shadow-md">
                        ${{text}}
                    </div>
                `;
                chatBox.appendChild(userNode);
                userInput.value = '';
                mainScrollArea.scrollTop = mainScrollArea.scrollHeight;

                // ยิงไปประมวลผลที่หลังบ้าน FastAPI จริงๆ
                try {{
                    const res = await fetch('/api/chat', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            message: text,
                            model: document.getElementById('model-select').value,
                            deep_search: flags.deepsearch,
                            think_mode: flags.think
                        }})
                    }});
                    const data = await res.json();
                    
                    // แสดงคำตอบ AI หลังบ้านที่ดึงมา
                    const aiNode = document.createElement('div');
                    aiNode.className = 'flex flex-col items-start w-full mb-4';
                    aiNode.innerHTML = `
                        <div class="flex items-center gap-1.5 mb-1 text-[11px] text-yellow-500">
                            <span>ॐ DRAGY ENGINE</span>
                        </div>
                        <div class="bg-[#100721] border border-purple-950/80 text-gray-200 px-4 py-2.5 rounded-2xl rounded-tl-none max-w-[85%] shadow-sm leading-relaxed">
                            ${{data.reply}}
                        </div>
                    `;
                    chatBox.appendChild(aiNode);

                    // อัปเดตตัวเลขแผงมอนิเตอร์โควตาที่ Sidebar ทันทีโดยไม่ต้องโหลดหน้าใหม่
                    if(data.current_quota) {{
                        const q = data.current_quota;
                        document.getElementById('quota-chat').innerText = `${{q.chat_used}} / ${{q.chat_limit}}`;
                        document.getElementById('bar-chat').style.width = `${{(q.chat_used/q.chat_limit)*100}}%`;
                    }}

                }} catch(err) {{
                    console.error("Error communication with backend:", err);
                }}
                
                mainScrollArea.scrollTop = mainScrollArea.scrollHeight;
            }}

            userInput.addEventListener('keydown', (e) => {{
                if (e.key === 'Enter' && !e.shiftKey) {{
                    e.preventDefault();
                    executeMsgSend();
                }}
            }});
        </script>
    </body>
    </html"""