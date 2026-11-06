"""
Terminal UI and Visual Telemetry Renderer for HumOS/LINGHOS.
"""
from typing import List
from .kernel import HumOSKernel
from .models import CSState

# ANSI Color Codes
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

def render_banner():
    banner = f"""{CYAN}{BOLD}
╔══════════════════════════════════════════════════════════════════════════════╗
║   __    _____ _   _  ____ _   _  ___  ____                                   ║
║  |  |  |_   _| \\ | |/ ___| | | |/ _ \\/ ___|   HUMAN OPERATING SYSTEM         ║
║  |  |    | | |  \\| | |  _| |_| | | | \\___ \\   Cognitive Execution Runtime    ║
║  |  |___ | | | |\\  | |_| |  _  | |_| |___) |  Incident Response SysAdmin v1.0║
║  |______||_| |_| \\_|\\____|_| |_|\\___/|____/                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝{RESET}"""
    return banner

def render_system_status(kernel: HumOSKernel) -> str:
    lines = []
    lines.append(f"{BOLD}┌──[ SYSTEM TELEMETRY & HARDWARE VITALS ]" + "─" * 40 + "┐" + RESET)
    
    # RAM Bar
    ram = kernel.ram_usage_pct
    ram_color = GREEN if ram < 60 else (YELLOW if ram < 85 else RED)
    bar_len = 20
    filled = int((ram / 100) * bar_len)
    ram_bar = f"{ram_color}[{'█' * filled}{'░' * (bar_len - filled)}] {ram}%{RESET}"
    
    # CS Vault Status
    cs_color = GREEN if kernel.cs_state == CSState.SECURE else (YELLOW if kernel.cs_state == CSState.EXPOSED else RED)
    cs_display = f"{cs_color}{kernel.cs_state.value}{RESET}"
    
    lines.append(f"│  {BOLD}RAM Allocation:{RESET}  {ram_bar:<38} │")
    lines.append(f"│  {BOLD}Core CS Vault:{RESET}   {cs_display:<48} │")
    lines.append(f"│  {BOLD}Hardware Vitals:{RESET} BPM: {kernel.heart_rate_bpm:<4} | Thermal Throttling: {'YES (CRITICAL)' if kernel.thermal_throttling else 'NONE (STABLE)'} │")
    
    # Defense engines
    dds = f"{GREEN}OVERCLOCK{RESET}" if kernel.dds_override else f"{DIM}NORMAL{RESET}"
    ads = f"{GREEN}OVERCLOCK{RESET}" if kernel.ads_override else f"{DIM}NORMAL{RESET}"
    ice = f"{CYAN}ENGAGED{RESET}" if kernel.ice_shield_active else f"{DIM}OFFLINE{RESET}"
    lines.append(f"│  {BOLD}Active Engines:{RESET}  DDS: {dds} | ADS: {ads} | Ice Shield: {ice} │")
    
    lines.append(f"{BOLD}└──" + "─" * 76 + "┘" + RESET)
    return "\n".join(lines)

def render_targets_and_vms(kernel: HumOSKernel) -> str:
    lines = []
    
    # Targets table
    lines.append(f"\n{BOLD}┌──[ TARGET TRIAGE & MALWARE TAXONOMY ]" + "─" * 41 + "┐" + RESET)
    if not kernel.targets:
        lines.append("│  No targets declared.                                                        │")
    else:
        # Deduplicate targets by name
        unique_targets = {t.name: t for t in kernel.targets.values()}.values()
        for t in unique_targets:
            critic_col = RED if t.critic_val >= 8 else (YELLOW if t.critic_val >= 5 else GREEN)
            core_col = GREEN if t.core_connected else RED
            core_str = "CONNECTED" if t.core_connected else "TEARDOWN"
            bridges_str = "OPEN" if t.bridges_open else "CLOSED"
            lines.append(f"│  • {BOLD}{t.name:<10}{RESET} (alias: {t.alias:<3}) | Pesi: [{t.weight}/10] | CriticVal: {critic_col}[{t.critic_val}/10]{RESET} | Fidelity: {t.fidelity_level}% │")
            lines.append(f"│    ↳ Core: {core_col}{core_str:<9}{RESET} | Bridges: {core_col}{bridges_str:<7}{RESET}                                  │")
    lines.append(f"{BOLD}└──" + "─" * 76 + "┘" + RESET)

    # Virtual Machines
    lines.append(f"\n{BOLD}┌──[ ACTIVE VIRTUAL MACHINES (SANDBOX HYPERVISOR) ]" + "─" * 29 + "┐" + RESET)
    if not kernel.vms:
        lines.append("│  No sandboxes active. Core directly exposed to input.                       │")
    else:
        for vm in kernel.vms.values():
            p_color = RED if "High" in vm.priority.value else CYAN
            targets_str = ", ".join(vm.targets)
            lines.append(f"│  [VM] {BOLD}{vm.id:<25}{RESET} Type: {vm.vm_type.value:<16} Priority: {p_color}{vm.priority.name}{RESET} │")
            lines.append(f"│       ↳ Target Isolation: [{targets_str}] (Cost: -{vm.ram_cost_mb}MB RAM)                    │")
    lines.append(f"{BOLD}└──" + "─" * 76 + "┘" + RESET)

    return "\n".join(lines)

def render_log_stream(kernel: HumOSKernel) -> str:
    lines = []
    lines.append(f"\n{BOLD}┌──[ INCIDENT RESPONSE LOG & AUDIT TRAIL ]" + "─" * 38 + "┐" + RESET)
    for log in kernel.telemetry_logs[-15:]:
        color = RESET
        if log.level == "ERROR":
            color = RED
        elif log.level == "WARN":
            color = YELLOW
        elif log.level == "CRITICAL":
            color = f"{RED}{BOLD}"
        elif log.phase == "DETECT":
            color = BLUE
        elif log.phase == "CLASSIFY":
            color = MAGENTA
        elif log.phase == "ISOLATE":
            color = YELLOW
        elif log.phase == "COUNTER":
            color = CYAN
        elif log.phase == "ESCALATE":
            color = RED
            
        lines.append(f"│ {DIM}{log.timestamp}{RESET} [{color}{log.phase:<8}{RESET}] [{log.subsystem:<14}] {log.message}")
    lines.append(f"{BOLD}└──" + "─" * 76 + "┘" + RESET)
    return "\n".join(lines)
