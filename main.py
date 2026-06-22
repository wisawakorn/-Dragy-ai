from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
return """

<!DOCTYPE html>

<html>
<head>
<title>Dragy AI</title>

<style>
body{
background:#0f172a;
color:white;
font-family:Arial;
text-align:center;
padding-top:50px;
}

h1{
font-size:60px;
}

.btn{
padding:15px 25px;
background:#3b82f6;
color:white;
border:none;
border-radius:10px;
font-size:18px;
cursor:pointer;
margin:10px;
}

.card{
background:#1e293b;
padding:20px;
margin:20px auto;
width:300px;
border-radius:15px;
}
</style>

</head>
<body>

<h1>🚀 Dragy AI</h1>

<h3>AI Chat + AI Image + AI Video</h3>

<button class="btn">
Login with Google
</button>

<div class="card">
<h2>Free</h2>
<p>15 ภาพ/วัน</p>
<p>2 วิดีโอ/วัน</p>
</div>

<div class="card">
<h2>Pro</h2>
<p>100 ภาพ/เดือน</p>
<p>30 วิดีโอ/เดือน</p>
</div>

<div class="card">
<h2>Premium</h2>
<p>500 ภาพ/เดือน</p>
<p>50 วิดีโอ/เดือน</p>
</div>

</body>
</html>
"""
