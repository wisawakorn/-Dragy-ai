from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    # แก้ไขโดยการย่อหน้า (Indent) เข้ามาให้ถูกต้อง
    return """
    <html> 
        <head> 
            <title>Dragy AI</title> 
        </head> 
        <body style="background:black;color:white;text-align:center;padding-top:100px;"> 
            <h1>ॐ Dragy AI</h1> 
            <h2>สวัสดีครับ 👋</h2> 
            <p>เว็บไซต์กำลังพัฒนา</p> 
        </body> 
    </html>"""