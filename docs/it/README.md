# HumOS — Hub della documentazione italiana

HumOS (Human Operating System) è un framework di gestione cognitiva che applica concetti dei sistemi operativi alla memoria di lavoro, all'attenzione, ai loop ricorrenti, ai confini personali e all'autoregolazione. L'implementazione combina il linguaggio **LINGHOS**, un runtime Python, il modello di protocollo **G.A.P.** e la GUI browser-based **HumOS Cockpit**.

Il repository contiene sia software implementato sia documentazione architetturale in evoluzione. Prima di considerare un primitivo documentato o una proprietà di sicurezza come una garanzia del runtime, consulta le note sullo stato d'implementazione nelle specifiche.

## Per iniziare

- [README principale del progetto](../../README.md) — panoramica, architettura, avvio rapido ed esempi.
- [Specifica LINGHOS](../SPEC_IT.md) — sintassi e riferimento architetturale.
- [Guida sviluppatori](../GUIDE_IT.md) — walkthrough dell'implementazione ed esempi d'integrazione.
- [Note sul linguaggio LINGHOS](LINGHOS.md) — concetti e storia del linguaggio.
- [Documento Framework HumOS](HumOS-Framework.md) — framework concettuale completo.
- [GUI HumOS Cockpit](../../src/linghos/cockpit.html) — editor visuale e console runtime.
- [Esempi eseguibili](../../examples/) — script e dimostrazione d'integrazione Python.

## Governance e sicurezza

- [Linee guida per i contributi](CONTRIBUTING.md)
- [Politica di sicurezza](SECURITY.md)
- [Protocollo G.A.P.-001](../../protocols/it/GAP-001-protocol.md)
- [Licenza](../../LICENSE.txt) — Creative Commons Attribuzione - Non Commerciale 4.0 Internazionale (CC BY-NC 4.0).

## Comandi runtime

Dalla root del repository:

```bash
python3 src/app.py
```

Per la CLI del package, dalla cartella `src/` dopo l'installazione:

```bash
python3 -m linghos --help
```

I metadati del pacchetto dichiarano Python 3.8 o superiore. Consulta il README principale e i metadati del package per i dettagli aggiornati.

---

[English documentation hub](../en/README.md) · [Repository su GitHub](https://github.com/SystemAdmin01/HumOS)
