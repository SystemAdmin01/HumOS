"""
LINGHOS Native Syntax Parser and Interpreter.
Parses .lgh and .linghos scripts into executable HumOS Kernel directives.
"""
import re
from typing import Optional
from .kernel import HumOSKernel
from .syntax import find_block_end, normalize_script, strip_inline_comment

class LINGHOSParser:
    def __init__(self, kernel: Optional[HumOSKernel] = None):
        self.kernel = kernel or HumOSKernel()

    def execute_script(self, code: str):
        """
        Executes a complete LINGHOS script line-by-line / block-by-block.
        """
        lines = normalize_script(code).split("\n")
        
        i = 0
        total_lines = len(lines)
        
        while i < total_lines:
            raw_line = lines[i]
            # Strip comments that start at the beginning of the line
            line = strip_inline_comment(raw_line).strip()
            
            if not line:
                i += 1
                continue

            # 1. Macro Directives: #include
            if line.startswith("#include"):
                match = re.search(r'#include\s+<?([A-Za-z0-9_]+)>?', line)
                if match:
                    self.kernel.include(match.group(1))
                i += 1
                continue

            # 2. Variable Declaration: Get: Target(alias)[weight], ...
            if line.startswith("Get:"):
                # Format: Get: Sara(sa)[4], Matiew(ma)[3], Giulia(giu); or Marco[8]
                targets_block = line[4:].strip().rstrip(";")
                items = targets_block.split(",")
                for item in items:
                    item = item.strip()
                    # 1) Match with alias: Name(alias)[weight] or Name(alias)
                    m = re.match(r'([A-Za-z0-9_]+)\s*\(\s*([A-Za-z0-9_]+)\s*\)\s*(?:\[(\d+)\])?', item)
                    if m:
                        name = m.group(1)
                        alias = m.group(2)
                        weight = int(m.group(3)) if m.group(3) else 1
                        self.kernel.register_target(name, alias, weight)
                        continue

                    # 2) Match without alias: Name[weight] or Name
                    m_no_alias = re.match(r'([A-Za-z0-9_]+)\s*(?:\[(\d+)\])?', item)
                    if m_no_alias:
                        name = m_no_alias.group(1)
                        weight = int(m_no_alias.group(2)) if m_no_alias.group(2) else 1
                        alias = name[:3].lower()
                        self.kernel.register_target(name, alias, weight)
                i += 1
                continue

            # 3. Critical Value Setting: Set_CriticVal>>target=[value]
            if "Set_CriticVal" in line:
                m = re.search(r'Set_CriticVal\s*>>\s*([A-Za-z0-9_]+)\s*=\s*\[?(\d+)\]?', line)
                if m:
                    target_ref = m.group(1)
                    val = int(m.group(2))
                    self.kernel.set_critic_val(target_ref, val)
                i += 1
                continue

            # 4. Virtual Machine Spawn: @Start>(VM_Name){ ... ON>targets; ... }
            if line.startswith("@Start>"):
                m = re.search(r'@Start>\s*\(\s*([A-Za-z0-9_]+)\s*\)', line)
                vm_name = m.group(1) if m else "General_VM"
                
                # Locate the complete VM block before scanning its contents.
                block_end = find_block_end(lines, i)
                if block_end is None:
                    self.kernel.log("ERROR", "PARSER", "Unclosed @Start block; script execution stopped.", level="ERROR")
                    return self.kernel

                targets = []
                for sub_line in lines[i + 1:block_end]:
                    sub_line = strip_inline_comment(sub_line).strip()
                    if "ON>" in sub_line:
                        on_targets = sub_line.split("ON>", 1)[1].rstrip(";").strip()
                        targets = [t.strip() for t in on_targets.split(",") if t.strip()]

                self.kernel.start_vm(vm_name, targets)
                i = block_end + 1
                continue

            # 5. Direct Skill Invocation: Call >> skill(args)
            if re.search(r'\bCall\s*>>', line, re.IGNORECASE):
                m = re.search(r'Call\s*>>\s*\(?\s*([A-Za-z0-9_]+)\s*\)?(?:\s*\((.*?)\))?', line, re.IGNORECASE)
                if m:
                    skill_name = m.group(1)
                    args = m.group(2) or ""
                    self.kernel.call_skill(skill_name, args)
                i += 1
                continue

            # 6. Mode Selection: /SET_Lockdown_Mode or /SET_Attack_Mode
            if "/SET_Lockdown_Mode" in line or "/SET_LOCKDOWN_MODE" in line:
                # Locate the complete lockdown block before scanning its contents.
                target_to_lockdown = "ALL"
                block_end = find_block_end(lines, i)
                if block_end is None:
                    self.kernel.log("ERROR", "PARSER", "Unclosed /SET_Lockdown_Mode block; script execution stopped.", level="ERROR")
                    return self.kernel

                for sub_line in lines[i + 1:block_end]:
                    sub_line = strip_inline_comment(sub_line).strip()
                    if "Take_DOWN" in sub_line:
                        m_target = re.search(r'>\s*\(?([A-Za-z0-9_]+)\)?', sub_line)
                        if m_target:
                            target_to_lockdown = m_target.group(1)
                    if "OVR" in sub_line:
                        ovr_match = re.search(r'OVR\s*>>\s*\((.*?)\)', sub_line)
                        if ovr_match:
                            systems = [s.strip() for s in ovr_match.group(1).split(",")]
                            self.kernel.override_defenses(systems)
                self.kernel.set_lockdown_mode(target_to_lockdown)
                i = block_end + 1
                continue

            if "/SET_Attack_Mode" in line:
                self.kernel.set_attack_mode()
                i += 1
                continue

            # 7. Take_DOWN or Close commands outside of a set block
            if "Take_DOWN" in line:
                m_target = re.search(r'>\s*\(?([A-Za-z0-9_]+)\)?', line)
                target_ref = m_target.group(1) if m_target else "TARGET"
                t = self.kernel.targets.get(target_ref)
                if t:
                    t.core_connected = False
                self.kernel.log("ISOLATE", "CORE_DETACH", f"Take_DOWN > ({target_ref})'s_Core [Abstract emotional severance complete]")
                i += 1
                continue

            if "Close(all)" in line or "Close(" in line:
                m_target = re.search(r'>\s*\(?([A-Za-z0-9_]+)\)?', line)
                target_ref = m_target.group(1) if m_target else "TARGET"
                t = self.kernel.targets.get(target_ref)
                if t:
                    t.bridges_open = False
                self.kernel.log("ISOLATE", "BRIDGE_CLOSE", f"Close(all) > ({target_ref})'s_bridges [Conduits closed]")
                i += 1
                continue

            # 8. Defense Override: OVR >> (DDS, ADS)
            if "OVR" in line and ">>" in line:
                ovr_match = re.search(r'OVR\s*>>\s*\(?(.*?)\)?$', line)
                if ovr_match:
                    systems = [s.strip(" ()") for s in ovr_match.group(1).split(",")]
                    self.kernel.override_defenses(systems)
                i += 1
                continue

            # 9. Behavior modifier: BE > worm_like
            if line.startswith("BE>") or line.startswith("BE >"):
                behavior = line.split(">")[1].strip()
                self.kernel.set_behavior(behavior)
                i += 1
                continue

            # 10. Conditional Checks: IF(CS_EXPOSED) or IF(CS_UNLOCKED)
            if line.startswith("IF(") or line.startswith("IF ("):
                m_cond = re.search(r'IF\s*\(\s*([A-Za-z0-9_]+)', line)
                condition = m_cond.group(1) if m_cond else ""
                
                # In simulation/execution, if the condition is not met we can check if it should be triggered
                # or execute if the kernel is set to evaluate or force it
                is_true = self.kernel.evaluate_condition(condition)
                
                block_end = find_block_end(lines, i)
                if block_end is None:
                    self.kernel.log("ERROR", "PARSER", f"Unclosed IF({condition}) block; script execution stopped.", level="ERROR")
                    return self.kernel
                nested_lines = lines[i + 1:block_end]

                if is_true:
                    self.kernel.log("BRANCH", "IF_TRUE", f"Condition '{condition}' is TRUE -> Executing branch.")
                    self.execute_script("\n".join(nested_lines))
                else:
                    self.kernel.log("BRANCH", "IF_STANDBY", f"Conditional trigger '{condition}' armed in standby (Core vault is secure).")
                i = block_end + 1
                continue

            # 11. Custom instructions: Echo("...")
            if line.startswith("Echo("):
                m_echo = re.search(r'Echo\s*\(\s*["\'](.*?)["\']\s*\)', line)
                if m_echo:
                    self.kernel.log("CONSOLE", "ECHO", m_echo.group(1))
                i += 1
                continue

            # 12. End block
            if "<<@end" in line:
                self.kernel.log("TERMINATION", "SYS_STABLE", "<<@end -> Volatile emergency buffers purged. Host OS stable.")
                i += 1
                continue

            # Other commands or lines (e.g. Main(), LP=..., HP=...)
            i += 1

        return self.kernel
