import os
from fastapi import FastAPI, Depends, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session

from database.connection import engine, Base, get_db
from database.models import User

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dragy AI")

SECRET_KEY = os.getenv("SECRET_KEY", "dragy_super_secret_2026")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    user = request.session.get('user')
    if user:
        return f"""
        <html>
            <head><title>Dragy AI - แผงควบคุม</title><meta charset="utf-8"></head>
            <body style="font-family: Arial, sans-serif; padding: 40px; text-align: center;">
                <h1>ยินดีต้อนรับสู่ Dragy AI 🎉</h1>
                <img src="{user.get('picture')}" width="100" style="border-radius:50%; border: 3px solid #6c63ff;"><br><br>
                <p><b>ผู้ใช้งาน:</b> {user.get('name')}</p>
                <p><b>อีเมล:</b> {user.get('email')}</p>
                <hr style="width: 50%; margin: 20px auto;">
                <h3>📊 สิทธิ์การใช้งานคงเหลือของคุณ:</h3>
                <p style="font-size: 18px;">🖼️ โควตารูปภาพ: <b>{user.get('image_quota')}</b> / 15 ภาพ</p>
                <p style="font-size: 18px;">🎬 โควตาวิดีโอ: <b>{user.get('video_quota')}</b> / 5 วิดีโอ</p>
                <br>
                <a href="/logout"><button style="padding: 10px 20px; background-color: #ff4757; color: white; border: none; border-radius: 5px; cursor: pointer;">ออกจากระบบ</button></a>
            </body>
        </html>
        """
    return """
    <html>
        <head><title>Dragy AI - เข้าสู่ระบบ</title><meta charset="utf-8"></head>
        <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 100px; background-color: #f4f4f9;">
            <div style="background: white; padding: 40px; display: inline-block; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1);">
                <h1 style="color: #333;">Dragy AI 🚀</h1>
                <p style="color: #666;">ระบบสร้างสเตตัส ภาพ และวิดีโอด้วย AI อัจฉริยะ</p>
                <br>
                <a href="/login">
                    <button style="padding: 12px 24px; font-size: 16px; background-color: #4285F4; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                        🔑 ล็อกอินด้วย Google Account
                    </button>
                </a>
            </div>
        </body>
    </html>
    """

@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    if "localhost" not in str(redirect_uri):
        redirect_uri = str(redirect_uri).replace("http://", "https://")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth")
async def auth(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')
    if user_info:
        email = user_info.get('email')
        name = user_info.get('name')
        picture = user_info.get('picture')
        
        db_user = db.query(User).filter(User.email == email).first()
        if not db_user:
            db_user = User(email=email, name=name, picture=picture)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
        
        request.session['user'] = {
            'email': db_user.email,
            'name': db_user.name,
            'picture': db_user.picture,
            'image_quota': db_user.image_quota,
            'video_quota': db_user.video_quota
        }
    return RedirectResponse(url='/')

@app.get("/logout")
def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')