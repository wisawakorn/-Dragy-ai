from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
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
        <link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600&display=swap" rel="stylesheet">
        <script src="https://unpkg.com/lucide@latest"></script>
        <style>
            body { font-family: 'Prompt', sans-serif; }
            .bg-gradient-dark {
                background: radial-gradient(circle at center, #1a0b36 0%, #0b0518 70%, #05020a 100%);
            }
            .glow-purple {
                text-shadow: 0 0 20px rgba(168, 85, 247, 0.6);
            }
        </style>
    </head>
    <body class="bg-gradient-dark text-gray-200 min-h-screen flex overflow-hidden">

        <aside class="w-64 bg-[#0a0516]/80 border-r border-purple-950/40 p-4 flex flex-col justify-between hidden md:flex">
            <div>
                <div class="flex items-center gap-3 px-2 py-3 mb-4">
                    <div class="w-8 h-8 bg-gradient-to-tr from-purple-600 to-indigo-500 rounded-lg flex items-center justify-center font-bold text-white text-xl shadow-lg shadow-purple-500/30">D</div>
                    <span class="text-xl font-semibold text-white tracking-wide">Dragy AI</span>
                </div>

                <button class="w-full border border-purple-900/60 hover:border-purple-500/50 hover:bg-purple-950/20 text-gray-300 rounded-xl py-2 px-4 flex items-center justify-between text-sm transition mb-6">
                    <span class="flex items-center gap-2"><i data-lucide="plus" class="w-4 h-4"></i> New Chat</span>
                    <span class="text-xs text-gray-500 border border-gray-700/50 px-1.5 py-0.5 rounded">⌘ K</span>
                </button>

                <nav class="space-y-1">
                    <a href="#" class="flex items-center gap-3 px-3 py-2.5 bg-purple-950/40 text-purple-300 rounded-xl text-sm font-medium"><i data-lucide="home" class="w-4 h-4"></i> หน้าแรก</a>
                    <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 hover:text-gray-200 hover:bg-white/5 rounded-xl text-sm transition"><i data-lucide="message-square" class="w-4 h-4"></i> AI Chat</a>
                    <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 hover:text-gray-200 hover:bg-white/5 rounded-xl text-sm transition"><i data-lucide="image" class="w-4 h-4"></i> AI Image</a>
                    <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 hover:text-gray-200 hover:bg-white/5 rounded-xl text-sm transition"><i data-lucide="video" class="w-4 h-4"></i> AI Video</a>
                    <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 hover:text-gray-200 hover:bg-white/5 rounded-xl text-sm transition"><i data-lucide="wrench" class="w-4 h-4"></i> เครื่องมือ AI</a>
                    <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 hover:text-gray-200 hover:bg-white/5 rounded-xl text-sm transition"><i data-lucide="history" class="w-4 h-4"></i> ประวัติแชท</a>
                    <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 hover:text-gray-200 hover:bg-white/5 rounded-xl text-sm transition"><i data-lucide="user" class="w-4 h-4"></i> โปรไฟล์</a>
                    <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 hover:text-gray-200 hover:bg-white/5 rounded-xl text-sm transition"><i data-lucide="settings" class="w-4 h-4"></i> การตั้งค่า</a>
                </nav>

                <div class="mt-6 bg-[#110924]/60 border border-purple-950/50 rounded-xl p-3 text-xs text-gray-400 space-y-3">
                    <div class="flex justify-between items-center">
                        <span>การใช้งานวันนี้</span>
                        <a href="#" class="text-purple-400 text-[10px] hover:underline">รีเซ็ตใน 14:30:12</a>
                    </div>
                    <div class="space-y-1">
                        <div class="flex justify-between text-[11px]">
                            <span class="flex items-center gap-1.5"><i data-lucide="image" class="w-3 h-3 text-blue-400"></i> ภาพ</span>
                            <span class="text-gray-300">12 / 15</span>
                        </div>
                        <div class="w-full bg-gray-800 h-1.5 rounded-full overflow-hidden">
                            <div class="bg-blue-500 h-full rounded-full" style="width: 80%"></div>
                        </div>
                    </div>
                    <div class="space-y-1">
                        <div class="flex justify-between text-[11px]">
                            <span class="flex items-center gap-1.5"><i data-lucide="video" class="w-3 h-3 text-purple-400"></i> วิดีโอ</span>
                            <span class="text-gray-300">0 / 1</span>
                        </div>
                        <div class="w-full bg-gray-800 h-1.5 rounded-full overflow-hidden">
                            <div class="bg-purple-500 h-full rounded-full" style="width: 0%"></div>
                        </div>
                    </div>
                    <div class="space-y-1">
                        <div class="flex justify-between text-[11px]">
                            <span class="flex items-center gap-1.5"><i data-lucide="message-circle" class="w-3 h-3 text-green-400"></i> แชท</span>
                            <span class="text-gray-300">23 / 50</span>
                        </div>
                        <div class="w-full bg-gray-800 h-1.5 rounded-full overflow-hidden">
                            <div class="bg-green-500 h-full rounded-full" style="width: 46%"></div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="space-y-3">
                <div class="bg-gradient-to-b from-[#210c43] to-[#120526] border border-purple-500/20 rounded-xl p-3 text-center shadow-lg">
                    <div class="text-sm font-semibold text-yellow-500 flex items-center justify-center gap-1.5 mb-1">
                        <i data-lucide="crown" class="w-4 h-4 fill-yellow-500"></i> Dragy AI Pro
                    </div>
                    <p class="text-[11px] text-gray-400 mb-2">ปลดล็อกทุกฟีเจอร์ เริ่มต้นเพียง <span class="text-purple-400 font-bold">฿99</span> / เดือน</p>
                    <button class="w-full bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 hover:opacity-90 text-white text-xs font-medium py-2 px-3 rounded-lg shadow-md transition">อัปเกรดตอนนี้</button>
                </div>
                
                <div class="flex bg-[#110924] p-1 rounded-xl text-xs text-gray-400">
                    <button class="flex-1 flex items-center justify-center gap-1.5 py-1.5 rounded-lg hover:text-gray-200"><i data-lucide="sun" class="w-3.5 h-3.5"></i> Light</button>
                    <button class="flex-1 flex items-center justify-center gap-1.5 py-1.5 rounded-lg bg-[#211142] text-white font-medium shadow-sm"><i data-lucide="moon" class="w-3.5 h-3.5 text-purple-400"></i> Dark</button>
                </div>
            </div>
        </aside>

        <main class="flex-1 flex flex-col justify-between p-6 relative overflow-y-auto">
            
            <div class="flex justify-end items-center gap-3 z-10">
                <button class="p-2 text-gray-400 hover:text-gray-200 transition"><i data-lucide="sun" class="w-5 h-5"></i></button>
                <button class="flex items-center gap-1 px-3 py-1.5 bg-[#170e2b] border border-purple-950 rounded-xl text-sm text-gray-300 hover:bg-[#23173d] transition">
                    <i data-lucide="globe" class="w-4 h-4"></i> TH <i data-lucide="chevron-down" class="w-3 h-3"></i>
                </button>
                <a href="#" class="text-sm text-gray-300 hover:text-white px-3 transition">เข้าสู่ระบบ</a>
                <button class="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium py-2 px-4 rounded-xl shadow-lg shadow-blue-600/20 transition">
                    <svg class="w-4 h-4 fill-white" viewBox="0 0 24 24"><path d="M12.24 10.285V13.4h6.887c-.275 1.565-1.88 4.604-6.887 4.604-4.33 0-7.866-3.577-7.866-8s3.536-8 7.866-8c2.46 0 4.105 1.025 5.047 1.926l2.427-2.334C17.955 2.192 15.34 1 12.24 1 6.033 1 1 6.033 1 12.24s5.033 11.24 11.24 11.24c6.478 0 10.793-4.537 10.793-10.997 0-.746-.08-1.32-.176-1.888H12.24z"/></svg>
                    Login with Google
                </button>
            </div>

            <div class="max-w-4xl w-full mx-auto my-auto flex flex-col items-center text-center z-10 space-y-8">
                <div class="relative w-28 h-28 flex items-center justify-center bg-gradient-to-b from-purple-600/20 to-transparent rounded-full p-4 border border-purple-500/10">
                    <div class="text-5xl font-bold text-yellow-500/90 glow-purple">ॐ</div>
                    <div class="absolute inset-0 bg-purple-500/10 blur-xl rounded-full"></div>
                </div>

                <div class="space-y-3">
                    <h1 class="text-4xl md:text-5xl font-bold tracking-tight bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">สวัสดีครับ 👋</h1>
                    <p class="text-lg md:text-xl text-gray-400 font-light">วันนี้ให้ <span class="text-purple-400 font-medium">Dragy AI</span> ช่วยอะไรดี?</p>
                </div>

                <div class="w-full bg-[#130b24]/90 border border-purple-500/20 rounded-3xl p-4 shadow-2xl focus-within:border-purple-500/40 transition">
                    <textarea class="w-full bg-transparent text-gray-200 placeholder-gray-600 text-sm focus:outline-none resize-none h-20" placeholder="พิมพ์ข้อความอะไรก็ได้..."></textarea>
                    
                    <div class="flex justify-between items-center mt-2 pt-2 border-t border-purple-950/50">
                        <div class="flex items-center gap-2">
                            <button class="p-2 text-gray-500 hover:text-gray-300 border border-purple-950/40 rounded-xl bg-purple-950/10 hover:bg-purple-950/30 transition"><i data-lucide="paperclip" class="w-4 h-4"></i></button>
                            <button class="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-gray-400 hover:text-gray-200 border border-purple-950/40 rounded-xl bg-purple-950/10 hover:bg-purple-950/30 transition"><i data-lucide="compass" class="w-3.5 h-3.5 text-blue-400"></i> DeepSearch</button>
                            <button class="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-gray-400 hover:text-gray-200 border border-purple-950/40 rounded-xl bg-purple-950/10 hover:bg-purple-950/30 transition"><i data-lucide="lightbulb" class="w-3.5 h-3.5 text-yellow-400"></i> Think</button>
                        </div>
                        <div class="flex items-center gap-2">
                            <button class="flex items-center gap-1 px-3 py-1.5 bg-[#170e2b] border border-purple-950 text-xs text-gray-400 rounded-xl hover:text-gray-200 transition">Grok 3 <i data-lucide="chevron-down" class="w-3 h-3"></i></button>
                            <button class="p-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl shadow-md shadow-blue-600/30 transition"><i data-lucide="arrow-up" class="w-4 h-4"></i></button>
                        </div>
                    </div>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 w-full text-left">
                    <div class="bg-[#0e071c]/80 border border-purple-950/60 p-3 rounded-2xl hover:border-purple-500/20 cursor-pointer hover:bg-purple-950/10 transition flex items-center gap-2.5">
                        <div class="w-8 h-8 rounded-xl bg-black flex items-center justify-center font-bold text-teal-400 text-sm">🎵</div>
                        <div>
                            <div class="text-[11px] font-medium text-gray-200">ช่วยคิดไอเดียคอนเทนต์</div>
                            <div class="text-[9px] text-gray-500">สำหรับ TikTok</div>
                        </div>
                    </div>
                    <div class="bg-[#0e071c]/80 border border-purple-950/60 p-3 rounded-2xl hover:border-purple-500/20 cursor-pointer hover:bg-purple-950/10 transition flex items-center gap-2.5">
                        <div class="w-8 h-8 rounded-xl bg-blue-950/40 text-blue-400 flex items-center justify-center text-sm"><i data-lucide="newspaper" class="w-4 h-4"></i></div>
                        <div>
                            <div class="text-[11px] font-medium text-gray-200">สรุปข่าวเทคโนโลยี</div>
                            <div class="text-[9px] text-gray-500">ล่าสุดให้หน่อย</div>
                        </div>
                    </div>
                    <div class="bg-[#0e071c]/80 border border-purple-950/60 p-3 rounded-2xl hover:border-purple-500/20 cursor-pointer hover:bg-purple-950/10 transition flex items-center gap-2.5">
                        <div class="w-8 h-8 rounded-xl bg-red-950/40 text-red-500 flex items-center justify-center text-sm"><i data-lucide="youtube" class="w-4 h-4"></i></div>
                        <div>
                            <div class="text-[11px] font-medium text-gray-200">เขียนสคริปต์ YouTube</div>
                            <div class="text-[9px] text-gray-500">เกี่ยวกับ AI</div>
                        </div>
                    </div>
                    <div class="bg-[#0e071c]/80 border border-purple-950/60 p-3 rounded-2xl hover:border-purple-500/20 cursor-pointer hover:bg-purple-950/10 transition flex items-center gap-2.5">
                        <div class="w-8 h-8 rounded-xl bg-yellow-950/40 text-yellow-500 flex items-center justify-center text-sm">🔱</div>
                        <div>
                            <div class="text-[11px] font-medium text-gray-200">สร้างภาพพุทธศิลป์</div>
                            <div class="text-[9px] text-gray-500">สไตล์สมจริง</div>
                        </div>
                    </div>
                    <div class="bg-[#0e071c]/80 border border-purple-950/60 p-3 rounded-2xl hover:border-purple-500/20 cursor-pointer hover:bg-purple-950/10 transition flex items-center gap-2.5">
                        <div class="w-8 h-8 rounded-xl bg-indigo-950/40 text-indigo-400 flex items-center justify-center text-sm"><i data-lucide="languages" class="w-4 h-4"></i></div>
                        <div>
                            <div class="text-[11px] font-medium text-gray-200">แปลภาษา</div>
                            <div class="text-[9px] text-gray-500">ไทย -> อังกฤษ</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="w-full flex flex-col items-center gap-4 z-10">
                <div class="flex items-center gap-1 text-[11px] text-gray-600 bg-black/20 px-3 py-1 rounded-full border border-purple-950/20">
                    <i data-lucide="info" class="w-3.5 h-3.5"></i> Dragy AI อาจให้ข้อมูลที่ไม่ถูกต้อง โปรดตรวจสอบความถูกต้องอีกครั้ง
                </div>
                
                <div class="animate-bounce p-1.5 bg-[#170e2b] border border-purple-950 rounded-full cursor-pointer hover:bg-[#23173d]">
                    <div class="w-8 h-8 flex items-center justify-center text-sm text-purple-400 font-bold bg-purple-950/30 rounded-full shadow-inner">ॐ</div>
                </div>
            </div>

            <button class="absolute bottom-6 right-6 w-10 h-10 bg-[#120a21] border border-purple-950/80 rounded-full flex items-center justify-center text-gray-500 hover:text-gray-300 transition shadow-lg"><i data-lucide="help-circle" class="w-5 h-5"></i></button>
        </main>

        <script>
            lucide.createIcons();
        </script>
    </body>
    </html>"""