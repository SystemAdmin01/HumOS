"""
HumOS Storage Manager
Handles persistent storage of user scenarios, custom skills, targets, rules, and last session state.
Stores data in JSON files in ~/.humos/scenarios/ and a local ./scenarios/ fallback.
"""
import os
import json
import time
import re
from typing import Dict, List, Optional, Any

DEFAULT_STORAGE_DIR = os.path.expanduser("~/.humos")

class StorageManager:
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = base_dir or DEFAULT_STORAGE_DIR
        self.scenarios_dir = os.path.join(self.base_dir, "scenarios")
        self.last_session_file = os.path.join(self.base_dir, "last_session.json")
        self.custom_symbols_file = os.path.join(self.base_dir, "custom_symbols.json")
        self._ensure_dirs()

    def _ensure_dirs(self):
        try:
            os.makedirs(self.scenarios_dir, exist_ok=True)
        except Exception as e:
            # Fallback to local scenarios directory if home dir is restricted
            self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "user_data"))
            self.scenarios_dir = os.path.join(self.base_dir, "scenarios")
            self.last_session_file = os.path.join(self.base_dir, "last_session.json")
            self.custom_symbols_file = os.path.join(self.base_dir, "custom_symbols.json")
            os.makedirs(self.scenarios_dir, exist_ok=True)

    def _sanitize_filename(self, name: str) -> str:
        clean = re.sub(r'[^a-zA-Z0-9_\- ]', '', name).strip()
        if not clean:
            clean = "scenario_" + time.strftime("%Y%m%d_%H%M%S")
        return clean.replace(" ", "_")

    def save_scenario(self, name: str, code: str, targets: Optional[List[Dict[str, Any]]] = None,
                      custom_symbols: Optional[List[Dict[str, Any]]] = None,
                      notes: str = "", metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Save a named scenario to persistent storage."""
        safe_name = self._sanitize_filename(name)
        file_path = os.path.join(self.scenarios_dir, f"{safe_name}.json")
        
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        created_at = now
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    old_data = json.load(f)
                    created_at = old_data.get("created_at", now)
            except Exception:
                pass

        payload = {
            "name": name.strip(),
            "safe_name": safe_name,
            "code": code,
            "targets": targets or [],
            "custom_symbols": custom_symbols or [],
            "notes": notes,
            "metadata": metadata or {},
            "created_at": created_at,
            "updated_at": now
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

        # Also update last session
        self.save_last_session(payload)
        
        # Save custom symbols if provided
        if custom_symbols:
            self.save_custom_symbols(custom_symbols)

        return payload

    def get_scenario(self, name_or_safe_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve a scenario by name."""
        safe_name = self._sanitize_filename(name_or_safe_name)
        file_path = os.path.join(self.scenarios_dir, f"{safe_name}.json")
        if not os.path.exists(file_path):
            # Check without sanitize if exact match
            for fname in os.listdir(self.scenarios_dir):
                if fname.endswith(".json"):
                    fpath = os.path.join(self.scenarios_dir, fname)
                    try:
                        with open(fpath, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            if data.get("name", "").lower() == name_or_safe_name.lower():
                                return data
                    except Exception:
                        continue
            return None

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def list_scenarios(self) -> List[Dict[str, Any]]:
        """List all saved scenarios with summary metadata."""
        items = []
        if not os.path.exists(self.scenarios_dir):
            return items

        for fname in os.listdir(self.scenarios_dir):
            if fname.endswith(".json"):
                fpath = os.path.join(self.scenarios_dir, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        items.append({
                            "safe_name": data.get("safe_name", fname[:-5]),
                            "name": data.get("name", fname[:-5]),
                            "created_at": data.get("created_at", ""),
                            "updated_at": data.get("updated_at", ""),
                            "target_count": len(data.get("targets", [])),
                            "symbol_count": len(data.get("custom_symbols", [])),
                            "notes": data.get("notes", ""),
                            "code_preview": (data.get("code", "")[:120] + "...") if len(data.get("code", "")) > 120 else data.get("code", "")
                        })
                except Exception:
                    continue

        # Sort by updated_at descending
        items.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
        return items

    def delete_scenario(self, safe_name: str) -> bool:
        """Delete a scenario file."""
        safe = self._sanitize_filename(safe_name)
        file_path = os.path.join(self.scenarios_dir, f"{safe}.json")
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False

    def save_last_session(self, data: Dict[str, Any]):
        """Persist auto-save state for next app startup."""
        try:
            with open(self.last_session_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def get_last_session(self) -> Optional[Dict[str, Any]]:
        """Retrieve last saved session state."""
        if os.path.exists(self.last_session_file):
            try:
                with open(self.last_session_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return None
        return None

    def save_custom_symbols(self, symbols: List[Dict[str, Any]]):
        """Save persistent custom symbols."""
        try:
            existing = self.load_custom_symbols()
            lookup = {s["name"].lower(): s for s in existing}
            for s in symbols:
                if s.get("custom", True):
                    lookup[s["name"].lower()] = s
            with open(self.custom_symbols_file, "w", encoding="utf-8") as f:
                json.dump(list(lookup.values()), f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def load_custom_symbols(self) -> List[Dict[str, Any]]:
        """Load persistent custom symbols."""
        if os.path.exists(self.custom_symbols_file):
            try:
                with open(self.custom_symbols_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def remove_custom_symbol(self, name: str) -> bool:
        """Remove a custom symbol from persistent storage."""
        symbols = self.load_custom_symbols()
        filtered = [s for s in symbols if s.get("name", "").lower() != name.lower()]
        try:
            with open(self.custom_symbols_file, "w", encoding="utf-8") as f:
                json.dump(filtered, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

# Global storage instance
GLOBAL_STORAGE = StorageManager()
