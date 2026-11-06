#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"

echo "========================================================"
echo "⚡ Avvio HumOS // LINGHOS Visual Compiler & Cockpit..."
echo "========================================================"

PYTHON_BIN=""
for candidate in \
    "/usr/local/bin/python3" \
    "/opt/homebrew/bin/python3" \
    "/Library/Frameworks/Python.framework/Versions/Current/bin/python3" \
    "/Library/Frameworks/Python.framework/Versions/3.15/bin/python3" \
    "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3" \
    "/Library/Frameworks/Python.framework/Versions/3.11/bin/python3" \
    "/usr/bin/python3" \
    "$(which python3 2>/dev/null)"
do
    if [ -x "$candidate" ]; then
        PYTHON_BIN="$candidate"
        break
    fi
done

if [ -z "$PYTHON_BIN" ]; then
    echo "❌ Errore: Python 3 non trovato nel sistema!"
    read -p "Premi [Invio] per uscire..."
    exit 1
fi

# Trova app.py sia che venga avviato come .app sia come script normale
if [[ "$DIR" == */Contents/MacOS ]]; then
    APP_PATH="$DIR/../Resources/app.py"
    cd "$DIR/../Resources"
else
    APP_PATH="$DIR/app.py"
    cd "$DIR"
fi

echo "✓ Trovato Python: $PYTHON_BIN"
echo "✓ Avvio server e apertura browser in corso..."
echo ""

"$PYTHON_BIN" "$APP_PATH"

EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "⚠️ Il server è terminato con codice di errore: $EXIT_CODE"
    read -p "Premi [Invio] per chiudere..."
fi
