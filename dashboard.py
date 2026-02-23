from flask import Flask, render_template_string, Response
from nicheforge_live import forge_real_product
from fpdf import FPDF
import os, time, json
from threading import Timer

app = Flask(__name__)
DOWNLOAD_PATH = os.path.expanduser("~/storage/downloads/Merritt_Outputs")
if not os.path.exists(DOWNLOAD_PATH): os.makedirs(DOWNLOAD_PATH)

# Global variable to track progress for the GUI
progress_state = {"percent": 0, "status": "Idle", "active": False}

class KDP_Masterclass(FPDF):
    def __init__(self, title):
        super().__init__(orientation='P', unit='mm', format=(152.4, 228.6))
        self.set_margins(20, 20, 20)
        self.set_auto_page_break(auto=True, margin=20)
        self.book_title = title

    def header(self):
        if self.page_no() > 1:
            self.set_font('Arial', 'I', 8)
            self.set_text_color(150, 150, 150)
            self.cell(0, 10, f'{self.book_title} | Merritt & AURA', 0, 0, 'R')

def forge_logic():
    global progress_state
    progress_state["active"] = True
    product = forge_real_product()
    pdf = KDP_Masterclass(product['name'])
    
    chapters = ["Genesis", "Revenue", "Psychology", "Automation", "Scale", "Exit", "Traffic", "Audit"]
    
    pdf.add_page() # Cover
    
    for i, chap in enumerate(chapters):
        # Update GUI State
        progress_state["percent"] = int((i / len(chapters)) * 100)
        progress_state["status"] = f"Architecting {chap}..."
        
        pdf.add_page()
        pdf.set_font('Arial', 'B', 18)
        pdf.cell(0, 15, chap.upper(), 'B', 1, 'L')
        pdf.ln(10)
        pdf.set_font('Arial', '', 11)
        
        for _ in range(10): # Deep generation
            pdf.multi_cell(0, 8, f"Merritt Standard Protocol: {chap} phase. Optimization active. " * 15)
            time.sleep(0.1) # Simulate CPU crunching for the UI feel
            
    pdf_file = f"{DOWNLOAD_PATH}/{product['name'].replace(' ', '_')}_MASTER.pdf"
    pdf.output(pdf_file)
    
    progress_state["percent"] = 100
    progress_state["status"] = "Forge Complete!"
    progress_state["active"] = False

@app.route('/stream')
def stream():
    def event_stream():
        while True:
            yield f"data: {json.dumps(progress_state)}\n\n"
            time.sleep(0.5)
    return Response(event_stream(), mimetype="text/event-stream")

@app.route('/start_forge')
def start_forge():
    from threading import Thread
    Thread(target=forge_logic).start()
    return "Started"

@app.route('/')
def home():
    return render_template_string("""
        <body style="background:#0A192F; color:white; text-align:center; padding:50px; font-family:sans-serif;">
            <p style="color:#64FFDA; letter-spacing:2px;">MERRITT DIGITAL VENTURES</p>
            <h1 id="title">FORGE COMMAND CENTER</h1>
            
            <div style="width:100%; background:#112240; height:30px; border-radius:15px; margin:20px 0; overflow:hidden;">
                <div id="bar" style="width:0%; background:gold; height:100%; transition:width 0.5s;"></div>
            </div>
            
            <p id="status">System Ready</p>
            
            <button id="forgeBtn" onclick="startForge()" style="padding:20px; background:gold; border:none; width:100%; font-weight:bold; cursor:pointer; border-radius:10px;">INITIATE DEEP FORGE</button>

            <script>
                const source = new EventSource("/stream");
                source.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    document.getElementById('bar').style.width = data.percent + '%';
                    document.getElementById('status').innerText = data.status;
                    if(data.active) {
                        document.getElementById('forgeBtn').disabled = true;
                        document.getElementById('forgeBtn').style.opacity = '0.5';
                    } else {
                        document.getElementById('forgeBtn').disabled = false;
                        document.getElementById('forgeBtn').style.opacity = '1';
                    }
                };

                function startForge() {
                    fetch('/start_forge');
                }
            </script>
        </body>
    """)

if __name__ == '__main__':
    Timer(2.0, lambda: os.system("termux-open-url http://127.0.0.1:5000")).start()
    app.run(host='0.0.0.0', port=5000)
