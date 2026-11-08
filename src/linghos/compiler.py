"""
LINGHOS Compiler & Bidirectional Code Generator.
Performs lexical analysis, AST generation, semantic validation, symbol learning,
dynamic telemetry synthesis, and inverse code generation from visual state.
"""
import re
import time
from typing import Dict, List, Optional, Any, Set, Tuple
from .models import (
    Target, VirtualMachine, VMType, Priority, CSState,
    SymbolType, LearnedSymbol, TelemetryLog
)
from .kernel import HumOSKernel
from .storage import GLOBAL_STORAGE
from .syntax import find_block_end, normalize_script, strip_inline_comment

class SymbolRegistry:
    """Dynamic symbol table that learns new symbols, skills, and macros from input."""
    def __init__(self):
        self.symbols: Dict[str, LearnedSymbol] = {}
        self._init_standard_library()
        self._load_persisted_symbols()

    def _init_standard_library(self):
        standard = [
            ("Defense_Mode", SymbolType.MODULE, "Macro-famiglia difensiva e contenimento minacce", "#include Defense_Mode"),
            ("Attack_Mode", SymbolType.MODULE, "Macro-famiglia controffensiva e risposta d'attacco", "#include Attack_Mode"),
            ("Executive_Control", SymbolType.MODULE, "Regolazione esecutiva e focus atomico", "#include <Executive_Control>"),
            ("Hardware_Regulation", SymbolType.MODULE, "Controllo biofeedback e raffreddamento Hardware", "#include <Hardware_Regulation>"),
            ("Ice_shield", SymbolType.SKILL, "Abbatte conducibilità emotiva e previene thermal throttling", "Call >> Ice_shield;"),
            ("Double_Bottom_Shield", SymbolType.SKILL, "Firewall semantico: separa la carica tossica dal dato puro", "Call >> Double_Bottom_Shield;"),
            ("Poison_skills", SymbolType.SKILL, "Controffensiva chirurgica verbale/logica ad alta precisione", "Call>> (Poison_skills)"),
            ("isolation", SymbolType.SKILL, "Procedure operative per blindare e isolare la sandbox", "Call >> isolation"),
            ("analyst", SymbolType.SKILL, "Evoca agente cognitivo iper-razionale distaccato", "Call >> analyst"),
            ("sniffer", SymbolType.SKILL, "Modulo telemetrico silente per estrapolare flussi di dati", "Call >> sniffer(IN&OUT_resources)"),
            ("RAM_Diagnostic", SymbolType.SKILL, "Audit telemetrico dei thread orfani in memoria volatile", "Call >> RAM_Diagnostic"),
            ("Drop_All_Background_Threads", SymbolType.SKILL, "Flush totale della RAM mentale da loop e ruminazioni", "Call >> Drop_All_Background_Threads"),
            ("Physiological_Sigh", SymbolType.SKILL, "Clamp biologico per scaricare spike acuti di cortisolo", "Execute >> Physiological_Sigh(Rapporto_4_7_8)"),
            ("LP_Ambient_VM", SymbolType.VM, "Virtual Machine ambientale a bassa priorità (-64MB RAM)", "@Start>(LP_Ambient_VM){ ON>targets; }"),
            ("HP_EXT_Defense_VM", SymbolType.VM, "Virtual Machine difensiva corazzata esterna (-256MB RAM)", "@Start>(HP_EXT_Defense_VM){ ON>target; }"),
            ("PRS_VM", SymbolType.VM, "Sandbox personale per elaborare impulsi interni prima del commit", "@Start>(PRS_VM){ ON>emotion; }"),
            ("Lockdown_Mode", SymbolType.DIRECTIVE, "Abbattimento Core, chiusura ponti e azzeramento Fidelity", "/SET_Lockdown_Mode{ ... }"),
            ("DDS", SymbolType.DIRECTIVE, "Dynamic Defense Systems - interrupt clamp in tempo reale", "OVR >> (DDS, ADS)"),
            ("ADS", SymbolType.DIRECTIVE, "Adaptive Defense Systems - pattern recognition euristico", "OVR >> (DDS, ADS)"),
            ("G.A.P.protocol", SymbolType.SKILL, "Gestione Attiva Paranoie - interrupt immediato su loop caotici", "Call >> G.A.P.protocol;"),
        ]
        for name, stype, desc, syntax in standard:
            self.symbols[name.lower()] = LearnedSymbol(name=name, sym_type=stype, description=desc, syntax_sample=syntax, custom=False)

    def _load_persisted_symbols(self):
        persisted = GLOBAL_STORAGE.load_custom_symbols()
        for p in persisted:
            name = p.get("name", "")
            if not name:
                continue
            key = name.lower().strip()
            if key not in self.symbols:
                type_str = p.get("type", "Cognitive Skill / Tool")
                # resolve SymbolType
                stype = SymbolType.SKILL
                for st in SymbolType:
                    if st.value == type_str or st.name == type_str:
                        stype = st
                        break
                self.symbols[key] = LearnedSymbol(
                    name=name,
                    sym_type=stype,
                    description=p.get("description", "Simbolo custom persistito"),
                    syntax_sample=p.get("syntax_sample", f"Call >> {name};"),
                    custom=True
                )

    def learn(self, name: str, sym_type: SymbolType, description: str = "", syntax_sample: str = "", persist: bool = True) -> LearnedSymbol:
        key = name.lower().strip()
        if key not in self.symbols:
            desc = description or f"Simbolo appreso dinamicamente ({sym_type.value})"
            sample = syntax_sample or f"Call >> {name};"
            sym = LearnedSymbol(name=name.strip(), sym_type=sym_type, description=desc, syntax_sample=sample, custom=True)
            self.symbols[key] = sym
            if persist:
                GLOBAL_STORAGE.save_custom_symbols([sym.to_dict()])
            return sym
        return self.symbols[key]

    def remove(self, name: str) -> bool:
        key = name.lower().strip()
        if key in self.symbols:
            # Only remove custom symbols
            if self.symbols[key].custom:
                del self.symbols[key]
                GLOBAL_STORAGE.remove_custom_symbol(name)
                return True
        return False

    def list_all(self) -> List[Dict[str, Any]]:
        return [sym.to_dict() for sym in self.symbols.values()]

# Global registry singleton
GLOBAL_REGISTRY = SymbolRegistry()

class LINGHOSCompiler:
    """
    Compiler that analyzes LINGHOS scripts, dynamically learns new symbols,
    computes thermodynamic telemetry, and generates operational reports.
    """
    def __init__(self, registry: Optional[SymbolRegistry] = None):
        self.registry = registry or GLOBAL_REGISTRY

    def compile(self, code: str, cs_exposed_override: bool = False, cs_unlocked_override: bool = False) -> Dict[str, Any]:
        start_time = time.time()
        kernel = HumOSKernel()
        
        if cs_exposed_override:
            kernel.cs_state = CSState.EXPOSED
        if cs_unlocked_override:
            kernel.cs_state = CSState.UNLOCKED

        diagnostics: List[Dict[str, str]] = []
        newly_learned: List[str] = []

        # Quote-aware normalization: structural characters inside strings/comments
        # must not be interpreted as grammar delimiters.
        lines = normalize_script(code).split("\n")

        # Parsing State
        double_bottom_shield = False
        atom_task = None
        has_main = False
        target_vms: Dict[str, str] = {} # target_alias -> vm_name

        i = 0
        total_lines = len(lines)

        while i < total_lines:
            raw_line = lines[i]
            line_no = i + 1
            line = strip_inline_comment(raw_line).strip()
            
            if not line:
                i += 1
                continue

            if "Main()" in line:
                has_main = True
                i += 1
                continue

            # 1. #include
            if line.startswith("#include"):
                m = re.search(r'#include\s+<?([A-Za-z0-9_]+)>?', line)
                if m:
                    mod = m.group(1)
                    kernel.include(mod)
                    if mod.lower() not in self.registry.symbols:
                        sym = self.registry.learn(mod, SymbolType.MODULE, f"Modulo macro utente '{mod}'", f"#include {mod}")
                        newly_learned.append(sym.name)
                else:
                    diagnostics.append({"line": line_no, "level": "WARN", "msg": "Sintassi #include non riconosciuta"})
                i += 1
                continue

            # 2. Get: Variables
            if line.startswith("Get:"):
                block = line[4:].strip().rstrip(";")
                items = block.split(",")
                for item in items:
                    item = item.strip()
                    m = re.match(r'([A-Za-z0-9_]+)\s*\(\s*([A-Za-z0-9_]+)\s*\)\s*(?:\[(\d+)\])?', item)
                    if m:
                        name, alias = m.group(1), m.group(2)
                        w = int(m.group(3)) if m.group(3) else 1
                        target = kernel.register_target(name, alias, w)
                        self.registry.learn(alias, SymbolType.TARGET, f"Target identificato: {name} ({alias})", f"Get: {name}({alias})[{w}];")
                        continue
                    m_simple = re.match(r'([A-Za-z0-9_]+)\s*(?:\[(\d+)\])?', item)
                    if m_simple:
                        name = m_simple.group(1)
                        w = int(m_simple.group(2)) if m_simple.group(2) else 1
                        alias = name[:3].lower()
                        target = kernel.register_target(name, alias, w)
                        self.registry.learn(alias, SymbolType.TARGET, f"Target identificato: {name}", f"Get: {name}[{w}];")
                i += 1
                continue

            # 3. Set_CriticVal >> target = [val]
            if "Set_CriticVal" in line:
                m = re.search(r'Set_CriticVal\s*>>\s*([A-Za-z0-9_]+)\s*=\s*\[?(\d+)\]?', line)
                if m:
                    t_ref = m.group(1)
                    val = int(m.group(2))
                    kernel.set_critic_val(t_ref, val)
                else:
                    diagnostics.append({"line": line_no, "level": "WARN", "msg": "Direttiva Set_CriticVal non valida"})
                i += 1
                continue

            # 4. @Start>(VM_Name){ ... ON>targets; ... }
            if line.startswith("@Start>"):
                m = re.search(r'@Start>\s*\(\s*([A-Za-z0-9_]+)\s*\)', line)
                vm_name = m.group(1) if m else "General_VM"
                if vm_name.lower() not in self.registry.symbols:
                    sym = self.registry.learn(vm_name, SymbolType.VM, f"Template VM custom '{vm_name}'", f"@Start>({vm_name}){{ ON>targets; }}")
                    newly_learned.append(sym.name)

                block_end = find_block_end(lines, i)
                if block_end is None:
                    diagnostics.append({"line": line_no, "level": "ERROR", "msg": "Blocco @Start non chiuso; compilazione interrotta."})
                    i = total_lines
                    break

                targets = []
                for sub_line in lines[i + 1:block_end]:
                    sub_line = strip_inline_comment(sub_line).strip()
                    if "ON>" in sub_line:
                        on_targets = sub_line.split("ON>", 1)[1].rstrip(";").strip()
                        targets = [t.strip() for t in on_targets.split(",") if t.strip()]

                kernel.start_vm(vm_name, targets)
                for t in targets:
                    target_vms[t] = vm_name
                i = block_end + 1
                continue

            # 5. Call >> Skill(args)
            if re.search(r'\bCall\s*>>', line, re.IGNORECASE):
                m = re.search(r'Call\s*>>\s*\(?\s*([A-Za-z0-9_]+)\s*\)?(?:\s*\((.*?)\))?', line, re.IGNORECASE)
                if m:
                    skill_name = m.group(1)
                    args = m.group(2) or ""
                    kernel.call_skill(skill_name, args)
                    if "double_bottom" in skill_name.lower():
                        double_bottom_shield = True
                    if skill_name.lower() not in self.registry.symbols:
                        sym = self.registry.learn(skill_name, SymbolType.SKILL, f"Skill/agente dinamico '{skill_name}'", f"Call >> {skill_name}")
                        newly_learned.append(sym.name)
                i += 1
                continue

            # 6. /SET_Lockdown_Mode
            if "/SET_Lockdown_Mode" in line or "/SET_LOCKDOWN_MODE" in line:
                target_to_lockdown = "ALL"
                block_end = find_block_end(lines, i)
                if block_end is None:
                    diagnostics.append({"line": line_no, "level": "ERROR", "msg": "Blocco /SET_Lockdown_Mode non chiuso; compilazione interrotta."})
                    i = total_lines
                    break

                for sub_line in lines[i + 1:block_end]:
                    sub_line = strip_inline_comment(sub_line).strip()
                    if "Take_DOWN" in sub_line:
                        m_target = re.search(r'>\s*\(?([A-Za-z0-9_]+)\)?', sub_line)
                        if m_target:
                            target_to_lockdown = m_target.group(1)
                    if "Close" in sub_line:
                        m_target = re.search(r'>\s*\(?([A-Za-z0-9_]+)\)?', sub_line)
                        if m_target:
                            target_to_lockdown = m_target.group(1)
                    if "OVR" in sub_line:
                        ovr_match = re.search(r'OVR\s*>>\s*\((.*?)\)', sub_line)
                        if ovr_match:
                            systems = [s.strip() for s in ovr_match.group(1).split(",")]
                            kernel.override_defenses(systems)
                kernel.set_lockdown_mode(target_to_lockdown)
                i = block_end + 1
                continue

            # 7. /SET_Attack_Mode
            if "/SET_Attack_Mode" in line:
                kernel.set_attack_mode()
                i += 1
                continue

            # 8. Take_DOWN or Close standalone
            if "Take_DOWN" in line:
                m_target = re.search(r'>\s*\(?([A-Za-z0-9_]+)\)?', line)
                t_ref = m_target.group(1) if m_target else "TARGET"
                t = kernel.targets.get(t_ref)
                if t:
                    t.core_connected = False
                    t.fidelity_level = 0
                kernel.log("ISOLATE", "CORE_DETACH", f"Take_DOWN > ({t_ref})'s_Core [Distacco emotivo eseguito]")
                i += 1
                continue

            if "Close(all)" in line or "Close(" in line:
                m_target = re.search(r'>\s*\(?([A-Za-z0-9_]+)\)?', line)
                t_ref = m_target.group(1) if m_target else "TARGET"
                t = kernel.targets.get(t_ref)
                if t:
                    t.bridges_open = False
                kernel.log("ISOLATE", "BRIDGE_CLOSE", f"Close(all) > ({t_ref})'s_bridges [Ponti materiali chiusi]")
                i += 1
                continue

            # 9. OVR >> (DDS, ADS)
            if "OVR" in line and ">>" in line:
                ovr_match = re.search(r'OVR\s*>>\s*\(?(.*?)\)?$', line)
                if ovr_match:
                    systems = [s.strip(" ()") for s in ovr_match.group(1).split(",")]
                    kernel.override_defenses(systems)
                i += 1
                continue

            # 10. BE > behavior
            if line.startswith("BE>") or line.startswith("BE >"):
                behavior = line.split(">")[1].strip()
                kernel.set_behavior(behavior)
                i += 1
                continue

            # 11. IF(condition)
            if line.startswith("IF(") or line.startswith("IF ("):
                m_cond = re.search(r'IF\s*\(\s*([A-Za-z0-9_]+)', line)
                cond = m_cond.group(1) if m_cond else ""
                
                # Check condition logic
                is_true = kernel.evaluate_condition(cond)
                
                block_end = find_block_end(lines, i)
                if block_end is None:
                    diagnostics.append({"line": line_no, "level": "ERROR", "msg": f"Blocco IF({cond}) non chiuso; compilazione interrotta."})
                    i = total_lines
                    break
                nested_lines = lines[i + 1:block_end]

                if is_true:
                    kernel.log("BRANCH", "IF_TRUE", f"Condizione '{cond}' VERIFICATA -> Esecuzione blocco interno.")
                    # Compile inner commands
                    inner_res = self.compile("\n".join(nested_lines), cs_exposed_override, cs_unlocked_override)
                    # Merge internal actions
                    if inner_res["telemetry"]["ice_shield"]:
                        kernel.call_skill("Ice_shield")
                    if inner_res["telemetry"]["worm_like"]:
                        kernel.set_behavior("worm_like")
                    if inner_res["telemetry"]["poison_engaged"]:
                        kernel.call_skill("Poison_skills")
                else:
                    kernel.log("BRANCH", "IF_STANDBY", f"Clausola condizionale '{cond}' armata in standby (Core sicuro).")
                i = block_end + 1
                continue

            # 12. Echo
            if line.startswith("Echo("):
                m_echo = re.search(r'Echo\s*\(\s*["\'](.*?)["\']\s*\)', line)
                if m_echo:
                    kernel.log("CONSOLE", "ECHO", m_echo.group(1))
                    if "atom" in m_echo.group(1).lower():
                        atom_task = m_echo.group(1)
                i += 1
                continue

            # 13. <<@end
            if "<<@end" in line:
                kernel.log("TERMINATION", "SYS_STABLE", "<<@end -> Buffer volatili purificati. Host OS nominale.")
                i += 1
                continue

            i += 1

        # Semantic Diagnostics & Validation
        unique_targets = list({t.name: t for t in kernel.targets.values()}.values())
        for t in unique_targets:
            if t.threat_score >= 7.0 and t.alias not in target_vms and t.name not in target_vms:
                diagnostics.append({
                    "line": 0,
                    "level": "CRITICAL",
                    "msg": f"Target critico '{t.name}' (Threat Score {t.threat_score}) senza VM di sandboxing attiva! Rischio di impatto diretto sul Nucleo."
                })
            if t.critic_val >= 8 and (t.core_connected or t.bridges_open):
                diagnostics.append({
                    "line": 0,
                    "level": "WARN",
                    "msg": f"Target ad alta minaccia '{t.name}' con Core o Ponti ancora aperti! Si raccomanda /SET_Lockdown_Mode."
                })

        # Thermodynamic Telemetry Calculation
        # RAM Base + Targets impact + VM impact - Flushes
        computed_ram = 25
        for t in unique_targets:
            # Emotional weight occupies memory lanes!
            computed_ram += int(t.weight * 3.5 + t.critic_val * 2.5)
        for vm in kernel.vms.values():
            computed_ram += int(vm.ram_cost_mb / 32)
        
        # If background threads dropped:
        if any("drop_all_background" in l.message.lower() for l in kernel.telemetry_logs):
            computed_ram = 18
        
        computed_ram = min(100, max(12, computed_ram))
        kernel.ram_usage_pct = computed_ram

        # Heart Rate BPM dynamics
        base_bpm = 72
        if any(t.critic_val >= 8 for t in unique_targets):
            base_bpm += 28
        elif any(t.critic_val >= 5 for t in unique_targets):
            base_bpm += 14

        if kernel.ice_shield_active:
            base_bpm = max(58, base_bpm - 25)
            kernel.thermal_throttling = False
        elif computed_ram >= 85:
            kernel.thermal_throttling = True

        kernel.heart_rate_bpm = base_bpm

        # Synthesize Operational Solution Report
        solution_steps = self._generate_solution_steps(kernel, unique_targets, target_vms, double_bottom_shield, atom_task)

        compile_time_ms = round((time.time() - start_time) * 1000, 2)

        return {
            "compiler_meta": {
                "lines_compiled": total_lines,
                "compile_time_ms": compile_time_ms,
                "newly_learned_symbols": newly_learned,
                "has_main": has_main,
                "diagnostics": diagnostics
            },
            "telemetry": {
                "ram_pct": kernel.ram_usage_pct,
                "heart_rate_bpm": kernel.heart_rate_bpm,
                "thermal_throttling": kernel.thermal_throttling,
                "cs_state": kernel.cs_state.value,
                "dds_override": kernel.dds_override,
                "ads_override": kernel.ads_override,
                "ice_shield": kernel.ice_shield_active,
                "double_bottom": double_bottom_shield,
                "worm_like": kernel.worm_like_behavior,
                "poison_engaged": kernel.poison_skills_engaged,
                "active_mode": kernel.active_mode or "STANDBY"
            },
            "targets": [t.to_dict() for t in unique_targets],
            "vms": [vm.to_dict() for vm in kernel.vms.values()],
            "solution_steps": solution_steps,
            "logs": [{"ts": l.timestamp, "phase": l.phase, "subsystem": l.subsystem, "msg": l.message, "level": l.level} for l in kernel.telemetry_logs],
            "symbols": self.registry.list_all()
        }

    def _generate_solution_steps(self, kernel: HumOSKernel, targets: List[Target], target_vms: Dict[str, str], double_bottom: bool, atom_task: Optional[str]) -> List[str]:
        steps = []
        
        # 1. Proximity & Triage analysis
        high_risk = [t for t in targets if t.threat_score >= 6.5]
        ambient = [t for t in targets if t.threat_score < 6.5]
        
        if high_risk:
            h_details = ", ".join([f"{t.name} (Raggio: {t.proximity_radius}px | Pesi:[{t.weight}] Critic:[{t.critic_val}])" for t in high_risk])
            steps.append(f"<b>1. Rilevamento Minaccia ad Alta Prossimità:</b> I target [{h_details}] hanno superato la soglia di guardia, avvicinandosi all'orbita interna del Nucleo.")
        elif ambient:
            a_names = ", ".join([t.name for t in ambient])
            steps.append(f"<b>1. Triage Ambientale:</b> I target [{a_names}] mantengono una distanza di sicurezza (orbita esterna a basso impatto).")

        # 2. Sandboxing
        if kernel.vms:
            for vm in kernel.vms.values():
                t_str = ", ".join(vm.targets)
                steps.append(f"<b>2. Sandboxing Attivo [{vm.id}]:</b> Target [{t_str}] isolati all'interno di un'istanza {vm.vm_type.value} ({vm.priority.name}). Zero dispersione sulla RAM primaria.")
        elif high_risk:
            steps.append("<b>⚠️ Vulnerabilità Perimetrale:</b> Rilevate minacce ravvicinate prive di sandbox. Trascinare una VM sulla minaccia per isolarla.")

        # 3. Lockdown
        locked = [t for t in targets if not t.core_connected and not t.bridges_open]
        if locked:
            names = ", ".join([t.name for t in locked])
            steps.append(f"<b>3. Protocollo Lockdown Integrale:</b> Su [{names}] è stato effettuato l'abbattimento emotivo (Take_DOWN Core) e la sigillatura dei canali materiali (Close Bridges). Fidelity revocata a 0%.")

        # 4. Shields
        shields_active = []
        if double_bottom:
            shields_active.append("Double-Bottom Shield (Firewall Semantico)")
        if kernel.ice_shield_active:
            shields_active.append("Ice Shield (Stabilizzazione Termica)")
        if kernel.dds_override and kernel.ads_override:
            shields_active.append("Overclock DDS/ADS (Gyrostabilizzatore Real-time)")

        if shields_active:
            steps.append(f"<b>4. Barriere Difensive Schierate:</b> Attivati {', '.join(shields_active)}. Il Nucleo opera in isolamento criogenico e non risponde a stimoli tossici.")

        # 5. Escalation / Behavior
        if kernel.worm_like_behavior:
            steps.append("<b>5. Postura Mimetica Worm:</b> Interazione ridotta a estrazione asimmetrica di risorse, con azzeramento di ogni gratitudine o connessione affettiva.")
        if kernel.poison_skills_engaged:
            steps.append("<b>6. Controffensiva Letale (Poison Skills):</b> Attacco al CS rilevato. Autorizzata confutazione logica istantanea mirata alle falle strutturali dell'avversario (One Shot, One Death).")

        # 6. Task Paralysis
        if atom_task:
            steps.append(f"<b>7. Risoluzione Blocco Esecutivo:</b> RAM ripulita e core focalizzati sul micro-task atomico: <i>'{atom_task}'</i>.")

        if not steps:
            steps.append("<b>Sistema in Stato Nominale:</b> Nessuna minaccia in orbita di collisione. Digitare o trascinare istruzioni per simulare un incidente.")

        return steps

    def generate_code_from_state(self, state: Dict[str, Any]) -> str:
        """
        Reverse-compilation / Code Generation:
        Generates clean LINGHOS source code from the current visual canvas state.
        """
        lines = []
        lines.append("// LINGHOS Generated Architecture Script")
        lines.append("// Compiled via HumOS Interactive Cybernetic Cockpit\n")

        # Modules
        lines.append("#include Defense_Mode")
        if state.get("attack_mode") or state.get("poison_engaged"):
            lines.append("#include Attack_Mode")
        lines.append("")

        # Targets
        targets = state.get("targets", [])
        if targets:
            decl_parts = []
            for t in targets:
                decl_parts.append(f"{t['name']}({t['alias']})[{t['weight']}]")
            lines.append(f"Get: {', '.join(decl_parts)};")

            for t in targets:
                if t.get("critic_val", 1) > 1:
                    lines.append(f"Set_CriticVal>>{t['alias']}=[{t['critic_val']}]")
            lines.append("")

        lines.append("LP=low priority")
        lines.append("HP=High priority\n")
        lines.append("Main(){")

        # VMs
        vms = state.get("vms", [])
        for vm in vms:
            targets_str = ", ".join(vm.get("targets", []))
            lines.append(f"\t@Start>({vm['type']}){{")
            lines.append(f"\t\tON>{targets_str};")
            lines.append("\t}\n")

        # Skills & Shields
        if state.get("isolation"):
            lines.append("\tCall >> isolation")
        if state.get("analyst"):
            lines.append("\tCall >> analyst")
        if state.get("sniffer"):
            lines.append("\tCall >> sniffer(IN&OUT_resources)")
        if state.get("double_bottom"):
            lines.append("\tCall >> Double_Bottom_Shield")

        # Lockdown
        locked_targets = [t for t in targets if not t.get("core_connected", True) or not t.get("bridges_open", True)]
        if locked_targets:
            lines.append("\n\t/SET_Lockdown_Mode{")
            for lt in locked_targets:
                if not lt.get("core_connected", True):
                    lines.append(f"\t\tTake_DOWN(all)>({lt['alias']})'s_Core")
                if not lt.get("bridges_open", True):
                    lines.append(f"\t\tClose(all)>({lt['alias']})'s_bridges")
            if state.get("dds_override") or state.get("ads_override"):
                lines.append("\t\tOVR >>(DDS, ADS)")
            lines.append("\t}\n")
        elif state.get("dds_override") or state.get("ads_override"):
            lines.append("\tOVR >>(DDS, ADS)\n")

        # Attack mode & Ice Shield
        if state.get("ice_shield") or state.get("worm_like"):
            lines.append("\tIF(CS_EXPOSED){")
            lines.append("\t\t/SET_Attack_Mode{")
            if state.get("ice_shield"):
                lines.append("\t\t\tcall >> Ice_shield;")
            if state.get("worm_like"):
                lines.append("\t\t\tBE>worm_like")
            lines.append("\t\t}")
            lines.append("\t}\n")

        # Poison Skills
        if state.get("poison_engaged"):
            lines.append("\tIF(CS_UNLOCKED){")
            lines.append("\t\tCall>> (Poison_skills){")
            lines.append("\t\t\tall_instruments(attack)")
            lines.append("\t\t}")
            lines.append("\t}\n")

        lines.append("\t<<@end")
        lines.append("}")
        return "\n".join(lines)
