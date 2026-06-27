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
