"""
Command-Line Interface for LINGHOS.
"""
import sys
import os
import argparse
from .kernel import HumOSKernel
from .parser import LINGHOSParser
from .ui import render_banner, render_system_status, render_targets_and_vms, render_log_stream
from .models import CSState

def run_command(args):
    filepath = args.file
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' does not exist.")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    kernel = HumOSKernel()
    if args.cs_exposed:
        kernel.cs_state = CSState.EXPOSED
    if args.cs_unlocked:
        kernel.cs_state = CSState.UNLOCKED

    parser = LINGHOSParser(kernel)
    parser.execute_script(code)

    print(render_banner())
    print(render_system_status(kernel))
    print(render_targets_and_vms(kernel))
    print(render_log_stream(kernel))

def repl_command(args):
    print(render_banner())
    print("\033[93m[LINGHOS Interactive Terminal Active - Enter instructions or 'exit' to quit]\033[0m\n")
    
    kernel = HumOSKernel()
    parser = LINGHOSParser(kernel)
    
    while True:
        try:
            line = input("\033[96mLINGHOS (SysAdmin) >> \033[0m")
            if not line.strip():
                continue
            if line.strip().lower() in ("exit", "quit"):
                print("\033[92mSystem shutting down safely. Core vault sealed.\033[0m")
                break
            if line.strip().lower() == "status":
                print(render_system_status(kernel))
                print(render_targets_and_vms(kernel))
                continue
            if line.strip().lower() == "logs":
                print(render_log_stream(kernel))
                continue
                
            parser.execute_script(line)
            # Print latest log
            if kernel.telemetry_logs:
                last_log = kernel.telemetry_logs[-1]
                print(f"\033[2m{last_log.timestamp}\033[0m [\033[93m{last_log.phase}\033[0m] {last_log.message}")
        except (KeyboardInterrupt, EOFError):
            print("\n\033[92mSafe exit acknowledged.\033[0m")
            break

def main():
    parser = argparse.ArgumentParser(description="LINGHOS - Cognitive Operating System CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Run file command
    run_parser = subparsers.add_parser("run", help="Execute a .lgh or .linghos script file")
    run_parser.add_argument("file", help="Path to the LINGHOS script")
    run_parser.add_argument("--cs-exposed", action="store_true", help="Simulate condition where CS is exposed")
    run_parser.add_argument("--cs-unlocked", action="store_true", help="Simulate condition where CS is breached / unlocked")

    # REPL command
    subparsers.add_parser("repl", help="Start the interactive SysAdmin prompt")

    # Web Cockpit GUI command
    gui_parser = subparsers.add_parser("gui", help="Launch the interactive Visual Cockpit in browser")
    gui_parser.add_argument("--port", type=int, default=8080, help="Local port (default: 8080)")
    gui_parser.add_argument("--no-browser", action="store_true", help="Do not open browser automatically")

    web_parser = subparsers.add_parser("web", help="Alias for 'gui'")
    web_parser.add_argument("--port", type=int, default=8080, help="Local port (default: 8080)")
    web_parser.add_argument("--no-browser", action="store_true", help="Do not open browser automatically")

    args = parser.parse_args()

    if args.command == "run":
        run_command(args)
    elif args.command == "repl":
        repl_command(args)
    elif args.command in ("gui", "web"):
        from .web import start_cockpit
        start_cockpit(port=args.port, auto_open=not args.no_browser)
    else:
        # Default behavior: show banner and help
        print(render_banner())
        parser.print_help()

if __name__ == "__main__":
    main()
