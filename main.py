from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Dragy AI")

@app.get("/", response_class=HTMLResponse)
async def home():
return """

<!DOCTYPE html>

<html lang="th">
<head>
<meta charset="UTF-8">
<title>Dragy AI</title>

<style>

body{
margin:0;
background:#050816;
color:white;
font-family:Arial,sans-serif;
}

.sidebar{
position:fixed;
left:0;
top:0;
width:260px;
height:100vh;
background:#0b1020;
padding:20px;
}

.logo{
font-size:40px;
font-weight:bold;
margin-bottom:30px;
}

.menu{
padding:12px;
margin-top:10px;
border-radius:10px;
background:#111827;
cursor:pointer;
}

.main{
margin-left:280px;
padding:40px;
text-align:center;
}

.om{
font-size:120px;
color:#ffd700;
}

.chatbox{
width:80%;
height:80px;
background:#111827;
border-radius:20px;
margin:auto;
margin-top:30px;
padding:20px;
}

input{
width:100%;
background:none;
border:none;
color:white;
font-size:20px;
outline:none;
}

.card{
display:inline-block;
width:250px;
margin:10px;
background:#111827;
padding:20px;
border-radius:20px;
}

button{
padding:12px 20px;
border:none;
border-radius:10px;
background:#7c3aed;
color:white;
cursor:pointer;
}

</style>

</head>

<body>

<div class="sidebar">

<div class="logo">
ॐ Dragy AI
</div>

<div class="menu">🏠 หน้าแรก</div>
<div class="menu">💬 AI Chat</div>
<div class="menu">🖼 AI Image</div>
<div class="menu">🎬 AI Video</div>
<div class="menu">⚙ เครื่องมือ AI</div>

</div>

<div class="main">

<div class="om">ॐ</div>

<h1>สวัสดีครับ 👋</h1>

<h2>วันนี้ให้ Dragy AI ช่วยอะไรดี?</h2>

<div class="chatbox">
<input placeholder="พิมพ์ข้อความที่นี่...">
</div>

<br>

<button>Login with Google</button>

<br><br>

<div class="card">
<h2>Free</h2>
<p>15 ภาพ/วัน</p>
<p>1 วิดีโอ/วัน</p>
</div>

<div class="card">
<h2>Pro Starter</h2>
<p>100 ภาพ/เดือน</p>
<p>20 วิดีโอ/เดือน</p>
<p>99 บาท/เดือน</p>
</div>

<div class="card">
<h2>Pro Premium</h2>
<p>500 ภาพ/เดือน</p>
<p>50 วิดีโอ/เดือน</p>
<p>199 บาท/เดือน</p>
</div>

</div>

</body>
</html>
"""
