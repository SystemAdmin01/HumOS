#!/usr/bin/env python3
"""
HumOS Cockpit - Direct Executable Entrypoint.
"""
import sys
import os

# Ensure package directory is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from linghos.web import start_cockpit

def main():
    start_cockpit(port=8080, auto_open=True)

if __name__ == "__main__":
    main()
