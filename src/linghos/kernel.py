"""
HumOS SysAdmin Kernel and LINGHOS Execution Runtime.
"""
from typing import Dict, List, Optional, Set
import datetime
from .models import Target, VirtualMachine, VMType, Priority, CSState, TelemetryLog

class HumOSKernel:
    def __init__(self):
        # System Hardware & Vitals
        self.ram_usage_pct: int = 42
        self.heart_rate_bpm: int = 74
        self.thermal_throttling: bool = False
        
        # Security Layer & Vault
        self.cs_state: CSState = CSState.SECURE
        self.root_access_granted_to: Set[str] = set()
        
        # Subsystems & Engines
        self.included_modules: Set[str] = set()
        self.active_mode: Optional[str] = None
        self.dds_override: bool = False
        self.ads_override: bool = False
        self.ice_shield_active: bool = False
        self.worm_like_behavior: bool = False
        self.poison_skills_engaged: bool = False
        
        # Entities & Sandboxes
        self.targets: Dict[str, Target] = {}  # by alias or name
        self.vms: Dict[str, VirtualMachine] = {}
        self.sniffer_buffer: List[Dict[str, str]] = []
        self.telemetry_logs: List[TelemetryLog] = []

    def log(self, phase: str, subsystem: str, message: str, level: str = "INFO"):
        ts = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        entry = TelemetryLog(timestamp=ts, phase=phase, subsystem=subsystem, message=message, level=level)
        self.telemetry_logs.append(entry)
        return entry

    # --- Directives ---

    def include(self, module_name: str):
        cleaned = module_name.strip("<> \t\n")
        self.included_modules.add(cleaned)
        self.log("INIT", "MODULE_LOADER", f"Loaded module specification: #{cleaned}")

    def register_target(self, name: str, alias: str, weight: int = 1) -> Target:
        target = Target(name=name, alias=alias, weight=weight)
        self.targets[alias] = target
        self.targets[name] = target
        self.log("DETECT", "TARGET_TRIAGE", f"Registered target '{name}' (alias: {alias}) with weight [{weight}]")
        return target

    def set_critic_val(self, target_ref: str, value: int):
        target = self.targets.get(target_ref)
        if target:
            target.critic_val = value
            level = "WARN" if value >= 7 else "INFO"
            self.log("CLASSIFY", "THREAT_EVAL", f"Set CriticVal >> {target.name} = [{value}/10]", level=level)
            if value >= 8:
                self.ram_usage_pct = min(100, self.ram_usage_pct + 15)
        else:
            self.log("ERROR", "TARGET_TRIAGE", f"Target '{target_ref}' not found for Set_CriticVal", level="ERROR")

    def start_vm(self, vm_identifier: str, target_refs: List[str]) -> VirtualMachine:
        # Determine VM type and priority
        cleaned = vm_identifier.strip("() \t\n")
        priority = Priority.HP if "HP" in cleaned else Priority.LP
        
        if "Ambient" in cleaned or "LP_Ambient" in cleaned:
            vm_type = VMType.AMBIENT
            ram = 64
        elif "EXT_Defense" in cleaned or "Defense_VM" in cleaned:
            vm_type = VMType.DEFENSE_EXT
            ram = 256
        elif "PRS" in cleaned:
            vm_type = VMType.DEFENSE_PRS
            ram = 128
        else:
            vm_type = VMType.FOCUS
            ram = 32

        vm_id = f"VM_{len(self.vms)+1}_{cleaned}"
        vm = VirtualMachine(id=vm_id, vm_type=vm_type, priority=priority, targets=target_refs, ram_cost_mb=ram)
        self.vms[vm_id] = vm
        
        target_names = [self.targets[ref].name if ref in self.targets else ref for ref in target_refs]
        self.log("ISOLATE", "HYPERVISOR", f"Spawned {vm_type.value} VM ({priority.value}) ON targets: {', '.join(target_names)} [RAM: -{ram}MB]")
        return vm

    def call_skill(self, skill_name: str, args: str = ""):
        skill = skill_name.strip()
        if "isolation" in skill.lower():
            self.log("ISOLATE", "SANDBOX_MGR", "Enforced strict boundary sandboxing. Zero bleed-through to Core.")
        elif "analyst" in skill.lower():
            self.log("ISOLATE", "COGNITIVE_AGENT", "Summoned Analyst sub-agent: Detached, hyper-rational state active.")
        elif "sniffer" in skill.lower():
            self.log("COUNTER", "SNIFFER", f"Silent Telemetry Sniffer online. Recording metadata: {args or 'IN&OUT_resources'}")
            self.sniffer_buffer.append({"type": "SNIFFER_PROBE", "status": "LISTENING", "scope": args})
        elif "ice_shield" in skill.lower():
            self.ice_shield_active = True
            self.thermal_throttling = False
            self.heart_rate_bpm = max(60, self.heart_rate_bpm - 15)
            self.log("COUNTER", "ICE_SHIELD", "Ice Shield deployed: Thermal and emotional conductivity set to MIN. Cold logic engaged.")
        elif "poison_skills" in skill.lower():
            self.poison_skills_engaged = True
            self.log("ESCALATE", "POISON_SKILLS", "CALL TO ARMS: Poison Skills engaged. Surgical logical retaliation armed (One Shot, One Death).", level="CRITICAL")
        elif "ram_diagnostic" in skill.lower():
            self.log("DIAG", "SYS_METRICS", f"RAM Diagnostic: Current usage at {self.ram_usage_pct}%.")
        elif "drop_all_background_threads" in skill.lower():
            self.ram_usage_pct = 20
            self.log("MAINT", "RAM_FLUSH", "All orphan threads and background loops dropped. Memory cleared.")
        else:
            self.log("EXEC", "SKILL_CALL", f"Invoked skill: Call >> {skill}({args})")

    def set_lockdown_mode(self, target_ref: str):
        self.active_mode = "Lockdown_Mode"
        target = self.targets.get(target_ref)
        name = target.name if target else target_ref
        
        if target:
            target.core_connected = False
            target.bridges_open = False
            target.fidelity_level = 0
            
        self.log("ISOLATE", "LOCKDOWN", f"/SET_Lockdown_Mode applied on [{name}]:")
        self.log("ISOLATE", "CORE_DETACH", f"  ↳ Take_DOWN(all) > ({name})'s_Core [Abstract emotional severance complete]")
        self.log("ISOLATE", "BRIDGE_CLOSE", f"  ↳ Close(all) > ({name})'s_bridges [Material bridges and info conduits closed]")
        self.log("ISOLATE", "FIDELITY", f"  ↳ Set Fidelity_Level = 0 [All Root privileges permanently revoked]")

    def override_defenses(self, systems: List[str]):
        if "DDS" in systems:
            self.dds_override = True
        if "ADS" in systems:
            self.ads_override = True
        self.log("ISOLATE", "DEFENSE_ENGINES", f"OVR >> ({', '.join(systems)}) [Dynamic & Adaptive engines in real-time overclock]")

    def set_attack_mode(self):
        self.active_mode = "Attack_Mode"
        self.log("COUNTER", "MODE_SWITCH", "/SET_Attack_Mode engaged. Counter-offensive stance confirmed.")

    def set_behavior(self, behavior: str):
        if "worm_like" in behavior.lower():
            self.worm_like_behavior = True
            self.log("COUNTER", "BEHAVIOR_MOD", "Behavior updated: BE > worm_like [Passive, long-term extraction, zero emotional investment].")

    def evaluate_condition(self, condition: str) -> bool:
        cond = condition.strip().upper()
        if "CS_EXPOSED" in cond:
            return self.cs_state in (CSState.EXPOSED, CSState.UNLOCKED)
        if "CS_UNLOCKED" in cond:
            return self.cs_state == CSState.UNLOCKED
        return False
