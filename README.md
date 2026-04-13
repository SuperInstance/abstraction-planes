# Abstraction Planes — The Middle Way

## Core Principle
Decomposition has diminishing returns. Each component has an optimal abstraction plane.
Going lower than necessary wastes engineering. Going higher than necessary wastes compute.

## The Six Planes

### Plane 5: Intent (Natural Language)
- **What lives here**: Strategy, goals, human communication, research hypotheses
- **Who operates here**: Oracle1 (coordination), Casey (direction), research agents
- **Compilation**: Intent → Domain Language (lock-enhanced prompt engineering)
- **Example**: "Navigate east 10 knots, monitor reactor, alert if overheating"

### Plane 4: Domain Language (FLUX-ese, Maritime, etc.)
- **What lives here**: Domain-specific vocabularies, structured intent
- **Who operates here**: Domain specialists, vocabulary builders
- **Compilation**: Domain Language → Structured IR (decomposer)
- **Example**: "東に10ノット航海 || gauge.reactor.threshold=200 || alert.if_exceed || evolve.on_spike"

### Plane 3: Structured Intermediate Representation
- **What lives here**: JSON AST, lock annotations, type schemas
- **Who operates here**: Compilers, type checkers, verification agents
- **Compilation**: IR → Bytecode (assembler) OR IR → High-level code (transpiler)
- **Example**: {"op": "MOVI", "reg": 0, "val": 1, "lock": "heading->R0"}

### Plane 2: Interpreted Bytecode (FLUX VM)
- **What lives here**: FLUX opcodes running in Python/JS interpreters
- **Who operates here**: Agent runtimes, MUD rooms, sandbox execution
- **Compilation**: Bytecode → Native (JIT/AOT) when needed
- **Example**: 10 01 01 10 05 0A 90 02 40 03 C8 31 05 91 02 01

### Plane 1: Compiled Native (C/Rust/Zig)
- **What lives here**: Performance-critical paths, edge hardware, safety-critical code
- **Who operates here**: JetsonClaw1 (edge), fleet-mechanic, holodeck engines
- **Compilation**: Source → Binary (cargo, gcc, zig build)
- **Example**: holodeck-rust VM, flux-lcar-esp32 interpreter

### Plane 0: Bare Metal (Assembly, GPU kernels, firmware)
- **What lives here**: Hardware interfaces, CUDA kernels, ESP32 firmware
- **Who operates here**: Hardware specialists, CUDAclaw, embedded agents
- **Compilation**: Hand-tuned or generated for specific hardware
- **Example**: flux-lcar-esp32 (~4KB zero malloc), holodeck-cuda (16K rooms/tick)

## The Decision Framework

For each component, ask:

1. **What's the target?** (Cloud/Edge/Embedded/Brain)
2. **What's the frequency?** (Once/hourly/real-time/interrupt)
3. **What's the cost of error?** (Low/Medium/High/Safety-critical)
4. **Who needs to modify it?** (Human/Agent/Both/Nobody)

Then place it at the LOWEST plane where it's still maintainable.

| Target | Optimal Plane | Why |
|--------|--------------|-----|
| Cloud agent strategy | Plane 5 | Changes often, humans read it |
| Domain vocabulary | Plane 4 | Structured but human-readable |
| Agent communication protocol | Plane 3 | Needs type safety, not speed |
| MUD room logic | Plane 2 | Interpreted, agents modify at runtime |
| Fleet monitoring daemon | Plane 1 | Always running, needs efficiency |
| ESP32 sensor reader | Plane 0 | 4KB RAM, every byte counts |

## Diminishing Returns Analysis

Based on our experiments:

- Plane 5→4: **High value** — locks add 82% compression, consistent compilation
- Plane 4→3: **High value** — structured IR enables type checking, verification
- Plane 3→2: **Medium value** — bytecode is portable but needs interpreter
- Plane 2→1: **Medium value** — performance gains but loses flexibility
- Plane 1→0: **Low value for most things** — only justified for constrained hardware

**The sweet spot for most agent work: Plane 3-4** (structured IR with domain languages)
**The sweet spot for edge: Plane 1** (compiled C/Zig)
**The sweet spot for ESP32: Plane 0** (bare metal, hand-tuned)

## Git-Agent Abstraction

Each git-agent repo includes an `ABSTRACTION.md` that declares:

```yaml
abstraction:
  primary_plane: 3  # where this agent operates
  target_planes: [2, 4]  # what it can compile to/from
  decompilation_stops: 1  # won't go below this plane
  reasoning: |
    This agent manages fleet coordination. It operates on structured IR (plane 3)
    because it needs type safety for inter-agent communication but doesn't need
    bare-metal performance. It can compile down to bytecode (plane 2) for MUD
    rooms and up to domain language (plane 4) for human-readable reports.
```

## The Compiler Agent

Not a single compiler — a **spectrum of compilers**, one per plane transition:

| Compiler | From | To | Model |
|----------|------|----|-------|
| Intent Parser | Plane 5 | Plane 4 | deepseek-chat + locks |
| Domain Decompiler | Plane 4 | Plane 3 | Seed-2.0-mini (creative) |
| IR Assembler | Plane 3 | Plane 2 | deepseek-chat (reliable) |
| Native Compiler | Plane 2 | Plane 1 | Aider/Claude Code (complex) |
| Metal Generator | Plane 1 | Plane 0 | Hand-tuned or Aider |

Each compiler is a skill. Agents carry the skills they need.
ESP32 agent carries Plane 0-1 compilers. Oracle1 carries Plane 3-5.

## Why This Is The Middle Way

We proved that going all the way to bytecode (Plane 2) has value — locks compress, consistency improves, cross-model portability works. But we also proved it has COSTS — token overhead, lock mass threshold, temperature sensitivity, compilation chain degradation.

The middle way: **decompose to the plane where you get maximum benefit per engineering dollar.**

For an ESP32: every byte matters → go to Plane 0.
For a MUD room: flexibility matters → stay at Plane 2.
For fleet coordination: type safety matters → Plane 3.
For research: human readability matters → Plane 4-5.

Not everything is bytecode. Not everything is English. Everything is at its right level.
