# Registro generale degli aggiornamenti / General Changelog

Questo è il registro centrale di HumOS. Raccoglie le generazioni/versioni del progetto, gli aggiornamenti G.A.P., le funzionalità, le correzioni e le modifiche documentali. L'indice dei file originali è in [`updates/README.md`](README.md).

This is HumOS's central change history. It records project generations and versions, G.A.P. updates, features, fixes, and documentation changes. The index of original source files is in [`updates/README.md`](README.md).

**Stato / Status:** “In preparazione / Unreleased” indica contenuti presenti in un branch o in una PR aperta; non significa che siano già rilasciati o integrati in `main`.

## In preparazione / Unreleased

- **Documentazione:** creato questo registro generale e collegato dalla pagina principale e dall'indice `updates/`.
- **Archivio:** aggiunti i sorgenti ricevuti `GAP_2.0.cpp` e la specifica HumOS V.18.3.1. Sono mantenuti come riferimenti storici, senza considerarli parte del runtime corrente.
- **Parser e sicurezza:** consolidati gli aggiornamenti su normalizzazione LINGHOS, controlli delle richieste HTTP, test di regressione e workflow CI; vedere il branch/PR di consolidamento per lo stato della revisione.
- **Documentazione:** distinti i protocolli G.A.P. con nomi simili, aggiornati i collegamenti e chiarito lo stato non implementato dei materiali concettuali storici.

- **Documentation:** add this general log and link it from the main README and the `updates/` index.
- **Archive:** add the supplied `GAP_2.0.cpp` source and HumOS V.18.3.1 specification as historical references, not as current runtime components.
- **Parser and security:** consolidate LINGHOS normalization, HTTP request checks, regression tests, and the CI workflow; see the consolidation branch/PR for review status.
- **Documentation:** distinguish similarly named G.A.P. protocols, repair links, and clarify that historical conceptual materials are not implemented features.

## Versioni e riferimenti storici / Versions and historical references

### HumOS V.18.3.1

- **Tipo / Type:** specifica concettuale e proposta LINGHOS fornita come documento Word / conceptual specification and LINGHOS proposal supplied as a Word document.
- **Stato / Status:** riferimento storico archiviato; non è il contratto normativo corrente né descrive necessariamente funzioni implementate / archived historical reference; it is not the current normative contract and does not necessarily describe implemented features.
- **Data di pubblicazione / Publication date:** non indicata nella fonte / not stated in the source.
- **File:** [`HumOS_V18.3.1_Specifica_Completa_e_Tool_LINGHOS.docx`](HumOS_V18.3.1_Specifica_Completa_e_Tool_LINGHOS.docx).

### G.A.P. 2.0

- **Tipo / Type:** demo C++ autonoma che classifica evidenze dichiarate / standalone C++ demo for classifying reported evidence.
- **Stato / Status:** esempio archiviato, non collegato al runtime Python / archived example, not connected to the Python runtime.
- **Identità / Identity:** il file si chiama `GAP_2.0.cpp`; il suo header lo descrive come “HumOS V.18.4.0 — G.A.P. 2.0” e scioglie G.A.P. come “Gestione Attiva delle Percezioni e delle Evidenze”. È diverso dal protocollo G.A.P.-001 del repository (“Active Paranoia Management”). / The file is named `GAP_2.0.cpp`; its header labels it “HumOS V.18.4.0 — G.A.P. 2.0” and expands G.A.P. as “Gestione Attiva delle Percezioni e delle Evidenze”. This differs from the repository's G.A.P.-001 protocol (“Active Paranoia Management”).
- **Data di pubblicazione / Publication date:** non indicata nella fonte / not stated in the source.
- **File:** [`GAP_2.0.cpp`](GAP_2.0.cpp).

### PATCH 00 — SAFE_MODE_OFFLINE

- **Tipo / Type:** proposta concettuale di autogestione, pubblicata in inglese e italiano / conceptual self-management proposal, available in English and Italian.
- **Stato / Status:** riferimento storico non implementato; le affermazioni biologiche e le soglie non sono validate dal software / historical, unimplemented reference; biological claims and thresholds are not validated by the software.
- **File:** [English](Patch00-ENG.md) · [Italiano](Patch00-ITA.md).
- **Versione e data / Version and date:** il testo originale contiene etichette di versione incoerenti; non è indicata una data di pubblicazione / the source contains inconsistent version labels and gives no publication date.

### Riferimenti software correnti / Current software references

- **Pacchetto Python / Python package:** `1.0.0` — [metadati](../src/pyproject.toml).
- **Specifica architetturale / Architecture specification:** `2.1.0-REV4` — [inglese](../docs/SPEC.md), [italiano](../docs/SPEC_IT.md).
- **Protocollo G.A.P. documentato / Documented G.A.P. protocol:** [G.A.P.-001 in English](../protocols/en/GAP-001-protocol.md) · [G.A.P.-001 in italiano](../protocols/it/GAP-001-protocol.md).

Questi identificatori appartengono a linee diverse e non sono intercambiabili. Una proposta o un documento archiviato non implica che la funzionalità sia presente nel software; consulta sempre la specifica corrente per i limiti di implementazione.

These identifiers belong to separate version lines and are not interchangeable. A proposal or archived document does not imply that a feature exists in the software; consult the current specification for implementation boundaries.

Le versioni o date mancanti non vengono ricostruite per supposizione. / Missing dates or version numbers are not inferred.

## Come registrare i prossimi aggiornamenti / How to record future updates

- Aggiungi ogni nuova voce in cima alla cronologia, sotto `In preparazione / Unreleased` o sotto la versione/data effettiva.
- Indica se il contenuto è **implementato**, **proposto** o **archiviato**. Non indicare una proposta come rilasciata.
- Usa una data `YYYY-MM-DD` e un ambito chiaro, per esempio `[Feature]`, `[G.A.P.]`, `[LINGHOS]`, `[Security]`, `[Docs]` o `[Fix]`.
- Se esiste una versione, indica la linea corretta (pacchetto, specifica, generazione concettuale o protocollo) e collega i file pertinenti.
- Riporta compatibilità, limiti e verifiche eseguite quando sono pertinenti.

- Add each new item at the top of `Unreleased` or under its actual version/date.
- Mark it **implemented**, **proposed**, or **archived**. Do not label a proposal as released.
- Use an ISO date (`YYYY-MM-DD`) and a clear area such as `[Feature]`, `[G.A.P.]`, `[LINGHOS]`, `[Security]`, `[Docs]`, or `[Fix]`.
- When a version exists, identify the correct version line (package, specification, conceptual generation, or protocol) and link the relevant files.
- Record compatibility, limitations, and checks when relevant.

### Modello / Template

```markdown
## Unreleased

### Added
- [Feature] **Implemented** — what changed; link to code/docs; note relevant checks.

### Changed
- [Docs] **Proposed** — what changed and what remains only a proposal.

### Fixed
- [Fix] **Implemented** — problem corrected and verification performed.

## [Version or generation] — YYYY-MM-DD
- [G.A.P.] **Archived** — source material and its relationship to the current protocol.
```
