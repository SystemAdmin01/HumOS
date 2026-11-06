"""
LINGHOS Python Package - Cognitive Execution Runtime & Visual Compiler for HumOS.
"""
from .models import Target, VirtualMachine, VMType, Priority, CSState, TelemetryLog, SymbolType, LearnedSymbol
from .kernel import HumOSKernel
from .parser import LINGHOSParser
from .compiler import LINGHOSCompiler, GLOBAL_REGISTRY
from .ui import render_banner, render_system_status, render_targets_and_vms, render_log_stream
from .web import start_cockpit

def execute(script_content: str, kernel: HumOSKernel = None) -> HumOSKernel:
    """
    Executes a LINGHOS script string and returns the updated HumOSKernel.
    """
    parser = LINGHOSParser(kernel)
    return parser.execute_script(script_content)

def run_file(filepath: str, kernel: HumOSKernel = None) -> HumOSKernel:
    """
    Reads and executes a .lgh or .linghos file.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return execute(content, kernel)

def compile_script(script_content: str, cs_exposed: bool = False, cs_unlocked: bool = False) -> dict:
    """
    Compiles a LINGHOS script into full AST, dynamic telemetry, diagnostics, and solution steps.
    """
    compiler = LINGHOSCompiler()
    return compiler.compile(script_content, cs_exposed, cs_unlocked)

__all__ = [
    "HumOSKernel",
    "LINGHOSParser",
    "LINGHOSCompiler",
    "GLOBAL_REGISTRY",
    "Target",
    "VirtualMachine",
    "VMType",
    "Priority",
    "CSState",
    "TelemetryLog",
    "SymbolType",
    "LearnedSymbol",
    "execute",
    "run_file",
    "compile_script",
    "start_cockpit",
    "render_banner",
    "render_system_status",
    "render_targets_and_vms",
    "render_log_stream"
]
