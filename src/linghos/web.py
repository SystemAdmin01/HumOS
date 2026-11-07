"""
HumOS Cockpit - Interactive Dynamic Web Server & API for LINGHOS.
Provides the HTTP server hosting the Cybernetic Visual Compiler interface
and the JSON REST endpoints for compilation, code generation, dynamic symbol learning,
and scenario persistence (saving, loading, listing, and last-session auto-restore).
"""
import http.server
import json
import os
import sys
import webbrowser
from typing import Dict, Any
from .compiler import LINGHOSCompiler, GLOBAL_REGISTRY
from .models import SymbolType
from .storage import GLOBAL_STORAGE

compiler_instance = LINGHOSCompiler()

def get_html_content() -> str:
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
    def _send_json(self, data: Any, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def _read_json(self) -> Dict[str, Any]:
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length <= 0:
            return {}
        body = self.rfile.read(content_length).decode("utf-8")
        try:
            return json.loads(body)
        except Exception:
            return {}

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            content = get_html_content()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))
        elif path == "/api/symbols":
            symbols = GLOBAL_REGISTRY.list_all()
            self._send_json(symbols)
        elif path == "/api/scenarios":
            scenarios = GLOBAL_STORAGE.list_scenarios()
            self._send_json(scenarios)
        elif path == "/api/last_session":
            last = GLOBAL_STORAGE.get_last_session()
            self._send_json(last or {})
        elif path.startswith("/api/scenario/"):
            safe_name = path[len("/api/scenario/"):]
            scenario = GLOBAL_STORAGE.get_scenario(safe_name)
            if scenario:
                self._send_json(scenario)
            else:
                self._send_json({"error": "Scenario non trovato"}, status=404)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        path = self.path.split("?")[0]
        data = self._read_json()

        if path == "/api/compile":
            code = data.get("code", "")
            cs_exposed = data.get("cs_exposed", False)
            cs_unlocked = data.get("cs_unlocked", False)
            result = compiler_instance.compile(code, cs_exposed_override=cs_exposed, cs_unlocked_override=cs_unlocked)
            self._send_json(result)

        elif path == "/api/generate_code":
            generated_code = compiler_instance.generate_code_from_state(data)
            self._send_json({"code": generated_code})

        elif path == "/api/add_symbol":
            name = data.get("name", "")
            desc = data.get("description", "")
            syntax = data.get("syntax_sample", "")
            type_str = data.get("type", "SKILL")
            stype = SymbolType.SKILL
            for st in SymbolType:
                if st.name.lower() == type_str.lower() or st.value.lower() == type_str.lower():
                    stype = st
                    break
            sym = GLOBAL_REGISTRY.learn(name, stype, description=desc, syntax_sample=syntax, persist=True)
            self._send_json(sym.to_dict())

        elif path == "/api/remove_symbol":
            name = data.get("name", "")
            success = GLOBAL_REGISTRY.remove(name)
            self._send_json({"success": success, "symbols": GLOBAL_REGISTRY.list_all()})

        elif path == "/api/save_scenario":
            name = data.get("name", "Scenario_SensoTitolo")
            code = data.get("code", "")
            targets = data.get("targets", [])
            custom_symbols = [s for s in GLOBAL_REGISTRY.list_all() if s.get("custom")]
            notes = data.get("notes", "")
            saved = GLOBAL_STORAGE.save_scenario(
                name=name,
                code=code,
                targets=targets,
                custom_symbols=custom_symbols,
                notes=notes
            )
            self._send_json({"status": "ok", "scenario": saved})

        elif path == "/api/auto_save":
            code = data.get("code", "")
            targets = data.get("targets", [])
            custom_symbols = [s for s in GLOBAL_REGISTRY.list_all() if s.get("custom")]
            GLOBAL_STORAGE.save_last_session({
                "name": data.get("name", "Ultima_Sessione"),
                "code": code,
                "targets": targets,
                "custom_symbols": custom_symbols,
                "saved_at": data.get("timestamp", "")
            })
            self._send_json({"status": "auto_saved"})

        elif path == "/api/delete_scenario":
            safe_name = data.get("safe_name", "")
            success = GLOBAL_STORAGE.delete_scenario(safe_name)
            self._send_json({"status": "ok" if success else "not_found"})

        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
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
    print(f"\033[96m║   - Dynamic Symbol Learner, Scenario Persistence & Auto-Restore          ║\033[0m")
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
