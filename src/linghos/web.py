"""
HumOS Cockpit - Interactive Dynamic Web Server & API for LINGHOS.
Provides the HTTP server hosting the Cybernetic Visual Compiler interface
and the JSON REST endpoints for compilation, code generation, and dynamic symbol learning.
"""
import http.server
import json
import os
import sys
import webbrowser
from typing import Dict, Any
from .compiler import LINGHOSCompiler, GLOBAL_REGISTRY
from .models import SymbolType

compiler_instance = LINGHOSCompiler()

def get_html_content() -> str:
    # Handle PyInstaller _MEIPASS extraction directory if bundled as an executable
    base_dir = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
    candidates = [
        os.path.join(base_dir, "cockpit.html"),
        os.path.join(base_dir, "linghos", "cockpit.html"),
        os.path.join(os.path.dirname(__file__), "cockpit.html")
    ]
    for path in candidates:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
    return "<h1>Cockpit Template Not Found</h1>"

class HumOSHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            content = get_html_content()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))
        elif self.path == "/api/symbols":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            symbols = GLOBAL_REGISTRY.list_all()
            self.wfile.write(json.dumps(symbols).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/compile":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)
            
            code = data.get("code", "")
            cs_exposed = data.get("cs_exposed", False)
            cs_unlocked = data.get("cs_unlocked", False)
            
            result = compiler_instance.compile(code, cs_exposed_override=cs_exposed, cs_unlocked_override=cs_unlocked)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode("utf-8"))

        elif self.path == "/api/generate_code":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)
            
            generated_code = compiler_instance.generate_code_from_state(data)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"code": generated_code}).encode("utf-8"))

        elif self.path == "/api/add_symbol":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)
            
            name = data.get("name", "")
            desc = data.get("description", "")
            syntax = data.get("syntax_sample", "")
            
            sym = GLOBAL_REGISTRY.learn(name, SymbolType.SKILL, description=desc, syntax_sample=syntax)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(sym.to_dict()).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Silence default access logs to keep CLI clean
        pass

class ReusableHTTPServer(http.server.HTTPServer):
    allow_reuse_address = True

def start_cockpit(port: int = 8080, auto_open: bool = True):
    current_port = port
    server = None
    for attempt in range(25):
        try:
            server = ReusableHTTPServer(("127.0.0.1", current_port), HumOSHTTPRequestHandler)
            break
        except OSError as e:
            if e.errno == 48:
                current_port += 1
            else:
                raise e

    if not server:
        print(f"\033[91mError: Could not bind to any port between {port} and {port + 25}\033[0m")
        return

    url = f"http://127.0.0.1:{current_port}"
    print(f"\n\033[96m╔══════════════════════════════════════════════════════════════════════════╗\033[0m")
    print(f"\033[96m║   ⚡ HUMOS // LINGHOS INTERACTIVE VISUAL COMPILER ONLINE                 ║\033[0m")
    print(f"\033[96m║   Access Cockpit:   \033[92m{url:<53}\033[96m║\033[0m")
    print(f"\033[96m║   - Dynamic Threat Proximity Arena (Weight & Criticality Radius)         ║\033[0m")
    print(f"\033[96m║   - Active Defense Drag & Drop with Live Code Synthesis                  ║\033[0m")
    print(f"\033[96m║   - Dynamic Symbol Learner & Universal Inspector Modals                  ║\033[0m")
    print(f"\033[96m║   Press Ctrl+C to shutdown and secure Core vault.                        ║\033[0m")
    print(f"\033[96m╚══════════════════════════════════════════════════════════════════════════╝\033[0m\n")
    
    if auto_open:
        try:
            webbrowser.open(url)
        except Exception:
            pass
            
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\033[92mCockpit offline. Host memory secured.\033[0m")
        server.server_close()
