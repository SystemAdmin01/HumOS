# Updates & Release Notes — HumOS

Questa sezione raccoglie gli aggiornamenti architetturali, le patch e i protocolli tecnici rilasciati nel corso dell'evoluzione di HumOS e LINGHOS.

---

## Indice

| File | Versione | Tipo | Data |
|---|---|---|---|
| [V18.4.0.md](V18.4.0.md) | V.18.4.0 | Specifica architetturale completa | Nov 2026 |
| [V18.4.1_AntiBurocrazia.md](V18.4.1_AntiBurocrazia.md) | V.18.4.1 | Patch — percorso minimo e modalità QUICK | Nov 2026 |
| [GAP_2.0.md](GAP_2.0.md) | G.A.P. 2.0 | Modulo C++ compilabile — Gestione Attiva delle Percezioni | Nov 2026 |
| [Patch00-ITA.md](Patch00-ITA.md) | Patch 00 | Patch di stabilizzazione (ITA) | — |
| [Patch00-ENG.md](Patch00-ENG.md) | Patch 00 | Patch di stabilizzazione (ENG) | — |

---

## Versioni principali

### V.18.4.1 · Patch Anti-Burocrazia _(corrente)_
> → [`V18.4.1_AntiBurocrazia.md`](V18.4.1_AntiBurocrazia.md)

Riduce il percorso predefinito: i moduli si attivano solo quando aggiungono valore. Introduce la modalità **QUICK** (default) e **DEEP** (su richiesta). Rende facoltativo il report strutturato. Separa il motore G.A.P. dalla persistenza.

---

### V.18.4.0 · Specifica Aggiornata
> → [`V18.4.0.md`](V18.4.0.md)

Corregge le quattro rigidità della V.18.3.1: allineamento esclusivo agli obiettivi core, potatura irreversibile (`PRUNED`), valutazione binaria delle evidenze, confusione tra simulazione e esecuzione reale. Introduce G.A.P. 2.0 con quattro stati epistemici, categorie di input Multiple (`CORE`, `MAINTENANCE`, `EXPLORATION`, `SOCIAL`) e protezione esplicita del sonno.

---

### G.A.P. 2.0 · Modulo C++ Compilabile
> → [`GAP_2.0.md`](GAP_2.0.md)

Implementazione dimostrativa in C++17 del motore di classificazione epistemica. Separa percezioni, osservazioni ed evidenze. Classifica lo stato delle ipotesi in quattro esiti: `SUPPORTED`, `DISCONFIRMED`, `INSUFFICIENT`, `CONFLICTING`. Nessuna conclusione automatica dall'assenza di prove.

```bash
# Compilare ed eseguire il demo
c++ -std=c++17 -Wall -Wextra -pedantic GAP_2.0.cpp -o gap_demo
./gap_demo
```

---

## Principio di versionamento

```
V.{major}.{minor}.{patch}
  │        │        └─ Patch / bugfix / aggiustamenti minori
  │        └────────── Aggiornamenti modulari (nuovi componenti o regole)
  └─────────────────── Revisione architetturale maggiore
```

---

*[← Torna alla root del progetto](../README.md)*
