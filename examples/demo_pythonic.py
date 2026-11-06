"""
Example: Running LINGHOS natively in Python.
"""
from linghos import HumOSKernel, Priority, render_banner, render_system_status, render_targets_and_vms, render_log_stream

def main():
    print(render_banner())
    
    # 1. Initialize Kernel
    sys = HumOSKernel()
    
    # 2. Include Modules
    sys.include("Defense_Mode")
    sys.include("Attack_Mode")
    
    # 3. Register Targets & Weights
    sara = sys.register_target("Sara", alias="sa", weight=4)
    matiew = sys.register_target("Matiew", alias="ma", weight=3)
    giulia = sys.register_target("Giulia", alias="giu", weight=9)
    sys.set_critic_val("giu", 9)
    
    # 4. Spawn Virtual Machines
    sys.start_vm("LP_Ambient_VM", ["sa", "ma"])
    sys.start_vm("HP_EXT_Defense_VM", ["giu"])
    
    # 5. Invoke Skills
    sys.call_skill("isolation")
    sys.call_skill("analyst")
    sys.call_skill("sniffer", "IN&OUT_resources")
    
    # 6. Apply Lockdown Mode
    sys.set_lockdown_mode("giu")
    sys.override_defenses(["DDS", "ADS"])
    
    # 7. Render Telemetry Dashboard
    print(render_system_status(sys))
    print(render_targets_and_vms(sys))
    print(render_log_stream(sys))

if __name__ == "__main__":
    main()
