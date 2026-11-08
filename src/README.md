# LINGHOS Python package

The `linghos` package contains the Python-side LINGHOS compiler, interpreter, state models, storage manager, command-line interface, and local HumOS Cockpit web server.

- Package name: `linghos`
- Package version: `1.0.0`
- Minimum Python version: `3.8`
- Main GUI entry point: `python app.py` (run from this directory)
- CLI entry point: `python -m linghos` or the installed `linghos` command

## Install from source

From the repository root:

```bash
cd src
python -m pip install .
```

## Run

Launch the browser-based Cockpit:

```bash
python app.py
```

Use the command-line interface:

```bash
python -m linghos --help
python -m linghos run ../examples/adhd_ram_flush.lgh
python -m linghos repl
```

The runtime currently implements a subset of the evolving LINGHOS design specification. Consult the root README and `../docs/SPEC.md` for the implementation-status matrix and known boundaries.

## License

This package is distributed under the repository's [CC BY-NC 4.0 license](../LICENSE.txt). It is not MIT-licensed; commercial use is not permitted under that license.
