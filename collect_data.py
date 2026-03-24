import json, sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer

class StoreHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'''
            <html><body style="margin:0; touch-action:none; font-family:sans-serif;">
            <input id="t" type="text" placeholder="Satz hier eintippen..." style="width:100%; height:5vh; font-size:1.5em;">
            <canvas id="c" style="border:1px solid black; width:100vw; height:75vh; cursor:crosshair;"></canvas>
            <button onclick="save()" style="width:100%; height:15vh; font-size:2em; background:#4CAF50; color:white;">SAVE</button>
            <script>
                let c=document.getElementById('c'), ctx=c.getContext('2d'), points=[], drawing=false;
                c.width=window.innerWidth; c.height=window.innerHeight*0.75;
                ctx.lineWidth=2; ctx.lineCap='round';
                const getXY = (e) => {
                    let r = c.getBoundingClientRect();
                    let t = e.touches ? e.touches[0] : e;
                    return {x: Math.round(t.clientX - r.left), y: Math.round(t.clientY - r.top)};
                };
                c.onpointerdown = (e) => { drawing=true; let p=getXY(e); points.push({x:p.x, y:p.y, s:1}); ctx.moveTo(p.x, p.y); };
                c.onpointermove = (e) => { 
                    if(!drawing) return; let p=getXY(e); points.push({x:p.x, y:p.y, s:0});
                    ctx.lineTo(p.x, p.y); ctx.stroke();
                };
                c.onpointerup = () => { drawing=false; ctx.beginPath(); };
                function save() {
                    let text = document.getElementById('t').value;
                    if(!text || points.length < 5) { alert('Text fehlt oder zu wenig gemalt!'); return; }
                    fetch('/', {method:'POST', body: JSON.stringify({text: text, strokes: points})});
                    points=[]; ctx.clearRect(0,0,c.width,c.height); document.getElementById('t').value='';
                }
            </script></body></html>
        ''')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        with open('handwriting_data.jsonl', 'a') as f:
            f.write(data.decode() + '\n')
        self.send_response(200)
        self.end_headers()

print("Server läuft! Öffne auf dem Tablet: http://192.168.178.50:8000")
HTTPServer(('0.0.0.0', 8000), StoreHandler).serve_forever()
