**Topics:** `abstraction` `decomposition` `intent-resolution` `plane-analysis` `system-design` `multi-level-synthesis` `cocapn`

---

# Abstraction Planes

> Simplify complex systems with a 6-plane stack — from Intent to Metal. Find the sweet spot where abstraction meets execution.

**Abstraction Planes** is a framework for decomposing natural language intents into executable code at the right level of abstraction. It identifies the **optimal plane** (the sweet spot where further decomposition gives diminishing returns) and provides the decomposition path from Intent down to Bare Metal.

Part of the [Cocapn fleet](https://github.com/SuperInstance) — lighthouse keeper architecture.

---

## The 6-Plane Stack

| Plane | Name | What It Looks Like | Example |
|-------|------|-------------------|---------|
| **5** | Intent | Natural language | "navigate east 10 knots, alert if reactor overheats" |
| **4** | Domain Language | FLUX-ese, maritime vocab, structured notation | `GAUGE reactor > 100 → ALERT "overheat"` |
| **3** | Structured IR | JSON AST, types, lock annotations | `{"op":"GAUGE","args":[reactor,100]}` |
| **2** | Bytecode | FLUX opcodes in hex | `0x90 0x64 0x00 0x91` |
| **1** | Native | C / Rust / Zig source | `if (gauge(reactor) > 100) alert();` |
| **0** | Bare Metal | Assembly, machine code, firmware | `MOV R1, [reactor_addr]` |

**Plane 4 is the sweet spot** — most intents decompose cleanly to domain language and stop there. Going deeper only matters when targeting specific hardware (ESP32, Jetson, Pi).

---

## Quick Start

### Install

```bash
pip install .
# or
pip install git+https://github.com/SuperInstance/abstraction-planes.git
```

### Run the Analyzer

```bash
# Auto-detect optimal plane
python -m abstraction_planes "navigate east 10 knots, monitor reactor"

# Target specific hardware
python -m abstraction_planes --target esp32 "read temperature sensor"
python -m abstraction_planes --target jetson "run object detection pipeline"
python -m abstraction_planes --target cloud "coordinate fleet agents"
```

### Programmatic Usage

```python
from abstraction_planes import find_optimal_plane

result = find_optimal_plane(
    "navigate east 10 knots, alert if reactor overheats",
    target="jetson"
)

print(f"Optimal plane: {result['optimal_plane']}")
# e.g. Optimal plane: 2
```

---

## Architecture

```
abstraction-planes/
├── README.md
├── ABSTRACTION.md              # Framework definition
├── CHARTER.md
├── DOCKSIDE-EXAM.md
├── STATE.md
├── LICENSE
├── pyproject.toml
├── plane_analyzer.py          # Main CLI + library entry point
├── src/
│   └── abstraction_planes/
│       ├── __init__.py        # Core plane analyzer
│       └── ...
├── tests/
└── dist/                      # Built package
```

### Decomposition Pipeline

```
Intent (Plane 5)
    │
    ▼  [DeepSeek / SiliconFlow Qwen]
Plane 4 — FLUX-ese domain language
    │
    ▼  [DeepSeek]
Plane 3 — Structured JSON IR
    │
    ▼  [DeepSeek]
Plane 2 — FLUX bytecode (hex)
    │
    ▼  [DeepSeek / Qwen]
Plane 1 — Native code (C/Zig)
    │
    ▼  [Qwen optimizer]
Plane 0 — Bare metal
```

Each step evaluates quality. Decomposition **stops** when quality improvement drops below threshold (diminishing returns detected).

### FLUX Opcodes Reference

```
MOVI=0x10  MOV=0x11  IADD=0x20  ISUB=0x21  IMUL=0x22
JMP=0x30   JZ=0x31   JNZ=0x32   CMP=0x40
GAUGE=0x90 ALERT=0x91 EVOLVE=0xA0 SAY=0x80 HALT=0x01
```

---

## Example Output

```
══════════════════════════════════════════════════════════════
  ABSTRACTION PLANE ANALYZER
══════════════════════════════════════════════════════════════
  Intent: navigate east 10 knots, monitor reactor, alert if overheating
  Target: jetson

  Plane 5: Intent (natural language)
    Original: navigate east 10 knots, monitor reactor, alert if overheating

  Plane 4: Domain Language (FLUX-ese, maritime, etc.)
    Decomposed (147 tokens): GAUGE reactor < 100 | SAY "all clear" | HALT
                            JMP course_set(east, 10) | GAUGE reactor | JZ alert

  Plane 3: Structured IR (JSON AST, lock-annotated)
    Decomposed (203 tokens): {"op":"SEQUENCE","steps":[...]} ...

  Plane 2: Interpreted Bytecode (FLUX opcodes in hex)
    Decomposed (89 tokens): 0x80 0x10 0x64 0x00 0x91 0x01 ...

  ═══ RESULT ═══
  Optimal plane: 2 (Interpreted Bytecode)
  Decomposition stops: diminishing returns at Plane 1
```

---

## Demo: Full Pipeline

```python
# Run a full decomposition
python -m abstraction_planes --target cloud "coordinate fleet agents"

# Expected: optimal plane 3-4 (no need to go to bare metal for cloud)
```

---

## Fleet Context

Part of the Cocapn fleet. Related repos:

| Repo | Role |
|------|-------|
| [flux-runtime](https://github.com/SuperInstance/flux-runtime) | Bytecode ISA and VM |
| [flux-runtime-c](https://github.com/SuperInstance/flux-runtime-c) | Native C VM for edge |
| [plato-sdk](https://github.com/SuperInstance/plato-sdk) | Agent communication protocol |
| [cudaclaw](https://github.com/SuperInstance/cudaclaw) | GPU-accelerated orchestration |

---

## Status

- **Updated:** 2026-04-14
- **Health:** Operational
- **Type:** Framework / Analyzer

The analyzer calls external APIs (DeepSeek, SiliconFlow). Costs ~$0.001 per decomposition run.

---
🦐 Cocapn fleet — lighthouse keeper architecture
