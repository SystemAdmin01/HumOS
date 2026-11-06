<div align="center">

# 🧠 HumOS — Human Operating System

### *Your brain runs on an OS. HumOS gives you root access.*

**An engineering-based cognitive framework for ADHD, neurodivergence, and overthinkers.**  
*Turn mental chaos into structured clarity — using the same logic as a computer.*

---

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.txt)
[![Language](https://img.shields.io/badge/language-LINGHOS%20%7C%20Python-cyan.svg)]()
[![Framework](https://img.shields.io/badge/framework-HumOS%20v2.1-purple.svg)]()
[![Status](https://img.shields.io/badge/status-Active%20Development-green.svg)]()
[![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)]()

</div>

---

<div align="center">

> **"Your mind is not broken. It just needs a better operating system."**

</div>

---

## 🖥️ What is HumOS?

HumOS is a **cognitive operating system** — a framework that maps the human mind  
to computer architecture concepts:

| Human Mind | HumOS Concept |
|-----------|---------------|
| Working memory | **RAM** |
| Anxiety / stress loops | **CPU overload / infinite loop** |
| Emotional triggers | **Threat variables** |
| Self-regulation tools | **Defense skills** |
| Rumination | **Background thread leak** |
| Emotional boundaries | **Firewall / Sandbox** |
| Focus mode | **Atomic task execution** |
| Panic / overwhelm | **Thermal throttling** |

You write **LINGHOS code** to describe your mental state — and the system  
gives you back a **visual threat map, telemetry, and an operational solution**.

---

## ⚡ LINGHOS — The Language of the Mind

**LINGHOS** is the DSL (Domain Specific Language) of HumOS.  
It compiles your cognitive state into actionable defense strategies.

```linghos
// Situation: someone toxic is draining your resources

#include <Defense_Mode>

Get: Marco(mrk)[8], Sara(sara)[5];
Set_CriticVal >> mrk = [9]

Main() {
    @Start>(HP_EXT_Defense_VM) {
        ON> mrk, sara;
    }

    IF(CS_EXPOSED) {
        Call >> Ice_shield;
        Call >> Double_Bottom_Shield;
        OVR >> (DDS, ADS);
    }

    /SET_Lockdown_Mode {
        Take_DOWN(all) > (mrk)'s_Core
        Close(all) > (mrk)'s_bridges
    }

    <<@end
}
```

**Output:** the system renders a live visual arena showing threat proximity to your Core,  
activates defense shields between you and the threats, and generates telemetry  
(RAM %, BPM, CS state, thermal status).

---

## 🚀 Quick Start

### Option 1 — Run the App (macOS, one click)

1. Download the latest release: [**HumOS.app.zip**](https://github.com/SystemAdmin01/HumOS/releases)
2. Extract → double-click **HumOS.app**
3. The browser opens at `http://127.0.0.1:8080` — the **Cockpit** is live.

> If macOS shows a security warning: **Right-click → Open → Open anyway**  
> (only needed the first time)

### Option 2 — Run from source

```bash
git clone https://github.com/SystemAdmin01/HumOS.git
cd HumOS
chmod +x HumOS_Cockpit.command
./HumOS_Cockpit.command
```

Requires Python 3.11+. No other dependencies.

---

## 🗂️ Repository Structure

```
HumOS/
│
├── README.md                   ← You are here
├── LICENSE.txt
│
├── /ITA/                        ← 🇮🇹 Italian System Area
│   ├── LINGHOS.md              — Full language reference (IT)
│   ├── HUMOS_DOC.md            — Framework documentation (IT)
│   └── protocols/              — LINGHOS protocols (IT)
│
├── /ENG/                        ← 🇬🇧 English System Area
│   ├── LINGHOS_EN.md           — Full language reference (EN)
│   ├── HUMOS_DOC_EN.md         — Framework documentation (EN)
│   └── protocols/              — LINGHOS protocols (EN)
│       └── GAP-001_complete_EN.md  ← Active Paranoia Management patch
│
├── /updates/                   ← 🩹 System Patches & Updates
│   ├── PATCH_00_SAFE_MODE.md   — Safe Mode Offline protocol
│   └── GAP-001_gap_protocol.md — G.A.P. Protocol patch notes
│
├── /src/                       ← 🐍 Python Compiler & Cockpit
│   ├── app.py                  — Entry point (run this)
│   ├── linghos/
│   │   ├── compiler.py         — LINGHOS compiler & symbol registry
│   │   ├── parser.py           — Lexer & AST parser
│   │   ├── kernel.py           — HumOS runtime kernel
│   │   ├── models.py           — Data models (Target, Shield, VM…)
│   │   ├── web.py              — HTTP server & REST API
│   │   └── cockpit.html        — Interactive Cockpit UI
│   └── HumOS_Cockpit.command   — macOS launcher (double-click)
│
└── /examples/                  ← 📋 Example LINGHOS scripts
```

---

## 🛡️ The Cockpit — Interactive Visual Compiler

<p align="center">
  <img src="ED71A99B-1E11-4043-BCCF-796DD6B3237E.png" alt="HumOS Cockpit Preview" width="850"/>
</p>

The HumOS Cockpit is a **browser-based visual compiler** that:

- 🎯 **Renders a live threat proximity arena** — threats orbit your Core at a distance proportional to their emotional weight and criticality score
- 🛡️ **Shows active defense shields** between your Core and each threat, labelled and removable
- 🖱️ **Drag & drop defense tools** from the palette onto the arena
- 📡 **Real-time telemetry** — RAM %, BPM, CS state, thermal throttling indicator
- 🤖 **Learns new symbols** — any unknown keyword in your code is absorbed into the registry
- 📝 **Bidirectional compilation** — write LINGHOS code → see the visual output; or drag tools visually → see the generated code
- 🗑️ **Delete learned skills** and symbols from the registry
- 📖 **Built-in LINGHOS command guide** — every command explained inline

---

## 📡 LINGHOS Command Reference

| Command | Syntax | What it does |
|---------|--------|-------------|
| **Include module** | `#include <Defense_Mode>` | Loads a macro family |
| **Declare target** | `Get: Name(alias)[weight];` | Registers a human variable/threat |
| **Set criticality** | `Set_CriticVal >> alias = [val]` | Assigns threat level 1–10 |
| **Start VM** | `@Start>(VM_Name){ ON> target; }` | Sandboxes a target in a virtual machine |
| **Call skill** | `Call >> Ice_shield;` | Activates a cognitive defense tool |
| **Conditional** | `IF(CS_EXPOSED){ ... }` | Executes a block if the condition is true |
| **Override defenses** | `OVR >> (DDS, ADS)` | Engages dynamic defense overrides |
| **Lockdown** | `/SET_Lockdown_Mode{ Take_DOWN > (alias)'s_Core }` | Full emotional detachment from target |
| **Behavior mode** | `BE> worm_like` | Sets interaction posture |
| **Echo log** | `Echo("message")` | Writes a message to the telemetry log |
| **End session** | `<<@end` | Closes and purges volatile buffers |
| **GAP Protocol** | `Call >> G.A.P.protocol;` | Interrupts infinite paranoia loops |

---

## 🩹 Protocols & Patches

Protocols are ready-to-use LINGHOS programs for specific cognitive situations.

| ID | Name | Description |
|----|------|-------------|
| `PATCH-00` | Safe Mode Offline | Full system lockdown — offline mode |
| `GAP-001` | G.A.P. Protocol | Breaks infinite paranoia loops on chaotic input X |

→ See [`/updates/`](https://github.com/SystemAdmin01/HumOS/tree/main/updates) and [`/ENG/protocols/`](https://github.com/SystemAdmin01/HumOS/tree/main/ENG/protocols)

---

## 🌐 Choose Your Language

<div align="center">

| 🇮🇹 Italian | 🇬🇧 English |
|------------|------------|
| [**→ Area Italiana**](./ITA/) | [**→ English Area**](./ENG/) |
| Documentazione completa in italiano | Full documentation in English |

</div>

---

## 🧩 Core Concepts

**CS — Core Self**  
The protected kernel of your identity. Can be `SECURE`, `EXPOSED`, or `UNLOCKED`.  
Everything in HumOS is designed to protect and regulate the CS.

**Target**  
Any person, situation, or stimulus that exerts pressure on your system.  
Each target has an emotional `weight` (1–10) and a `criticality` score (1–10).

**Defense Skills**  
Cognitive tools deployed as shields — `Ice_shield`, `Double_Bottom_Shield`, `isolation`, `analyst`, `sniffer`, `Poison_skills`, and more.

**Virtual Machine (VM)**  
A mental sandbox that isolates a target so it cannot access the Core directly.

**RAM**  
Cognitive working memory. Orphan threads (rumination, paranoia loops) are the main source of RAM leaks.

---

## 📄 License

MIT — see [LICENSE.txt](LICENSE.txt)

---

<div align="center">

**HumOS** — *Engineering the mind. One protocol at a time.*  
Built by [SystemAdmin01](https://github.com/SystemAdmin01)

</div>
