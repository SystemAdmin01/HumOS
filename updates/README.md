# Updates & Release Notes — HumOS

Questa sezione raccoglie gli aggiornamenti architetturali, le specifiche operative e i moduli di sicurezza rilasciati nel corso dell'evoluzione di HumOS e LINGHOS.

---

## Indice dei rilasci

| Documento | Versione / Modulo | Descrizione |
|---|---|---|
| [**`V18.3.1.md`**](V18.3.1.md) | **HumOS V.18.3.1** | Specifica architetturale completa, codice LINGHOS (`.lghos`), moduli `STIMULUS_GATEKEEPER`, `TRAJECTORY_PLANNER` e ChatGPT Interface Protocol. |
| [**`GAP_2.0.md`**](GAP_2.0.md) | **G.A.P. 2.0** | Specifiche e sorgente C++ compilabile del modulo per la Gestione Attiva delle Percezioni e classificazione epistemica a 4 stati. |
| [**`Patch00-ITA.md`**](Patch00-ITA.md) | **Patch 00 (ITA)** | Patch di stabilizzazione e modalità provvisoria (Safe Mode). |
| [**`Patch00-ENG.md`**](Patch00-ENG.md) | **Patch 00 (ENG)** | Safe Mode Stabilization Patch (English reference). |

---

## Panoramica dei componenti principali

### 1. HumOS V.18.3.1 — Specifica Architetturale & LINGHOS
> 📄 Consulta il documento completo: [**`V18.3.1.md`**](V18.3.1.md)

* **Kernel Metrics & State:** Gestione dei regimi `HYPERFOCUS` e `LOW_FRICTION`, budget energetico biologico e tracciamento del rapporto Segnale/Rumore (`SNR`).
* **STIMULUS_GATEKEEPER:** Pre-filtro deterministico in ingresso con esiti `PASS`, `QUARANTINE`, `DROP_TO_BACKLOG`, `DEFER`.
* **TRAJECTORY_PLANNER:** Motore di validazione causale lungo il percorso critico con esiti `COMMIT`, `BLOCKED`, `PRUNED`.
* **ChatGPT Interface Protocol:** Regole di interazione vincolanti per AI (divieto di compiacenza, output syslog deterministico, gestione Day Runtime vs Night Build).

---

### 2. G.A.P. 2.0 — Gestione Attiva delle Percezioni ed Evidenze
> 📄 Consulta il documento completo: [**`GAP_2.0.md`**](GAP_2.0.md)

Modulo architetturale e C++17 per separare rigorosamente **percezioni**, **osservazioni** ed **evidenze**, classificando lo stato epistemico in 4 esiti:
* `SUPPORTED`: Evidenze attendibili e verificabili supportano l'ipotesi.
* `DISCONFIRMED`: Evidenze attendibili contraddicono l'ipotesi.
* `INSUFFICIENT`: Dati assenti o insufficienti (*l'assenza di prova non è prova di assenza*).
* `CONFLICTING`: Evidenze attendibili ma discordanti; revisione richiesta.

Include la procedura `release_attention()` per archiviare i casi senza cancellarli e liberare la RAM cognitiva attiva.

---

*[← Torna alla root del progetto](../README.md)*
