# Abstraction Planes — The Middle Way

**Find the right altitude for every task. Too low is engineering waste. Too high is compute waste.**

## What It Does

This framework provides a decision-making tool for software architecture, helping you place each component at its optimal level of abstraction. It defines six "planes" of abstraction, from human intent down to bare metal, and offers a simple method to choose the right one. The goal is to ship faster and run leaner by avoiding over-engineering and under-optimization.

## In the Fleet Ecosystem

Within the Cocapn fleet, Abstraction Planes is the **navigation chart for system design**. It informs how components across different repos—from high-level agent strategy (`oracle1`) to embedded hardware control (`flux-lcar-esp32`)—should be built and connected. It's the philosophy that ensures the fleet's software stack is both maintainable and efficient.

## The Six Planes (The Map)

| Plane | Name | What Lives Here | Example |
|-------|------|-----------------|---------|
| 5 | Intent | Natural language, goals, strategy | "Navigate east 10 knots, monitor reactor" |
| 4 | Domain Language | Structured vocabularies (FLUX-ese, Maritime) | `東に10ノット航海 \|\| gauge.reactor.threshold=200` |
| 3 | Structured IR | JSON AST, type schemas, lock annotations | `{"op": "MOVI", "reg": 0, "val": 1}` |
| 2 | Interpreted Bytecode | FLUX VM opcodes in Python/JS | `10 01 01 10 05 0A 90 02...` |
| 1 | Compiled Native | Performance-critical C/Rust/Zig | `holodeck-rust` VM, edge compute |
| 0 | Bare Metal | Assembly, GPU kernels, firmware | `flux-lcar-esp32` (~4KB firmware) |

## Quick Start: How to Place a Component

For any component, ask four questions:
1.  **Target:** Cloud, Edge, Embedded, or Brain?
2.  **Frequency:** Once, hourly, real-time, or interrupt?
3.  **Cost of Error:** Low, Medium, High, or Safety-critical?
4.  **Who Modifies It:** Human, Agent, Both, or Nobody?

**The Rule:** Place it at the **lowest plane where it's still maintainable** by its intended modifier.

**Example:** A cloud agent's coordination logic changes often and is read by humans. It belongs in **Plane 5 (Intent)**. An ESP32 motor driver is safety-critical and never changes after deployment. It belongs in **Plane 0 (Bare Metal)**.

## Learn More

*   **Deep Dive:** Read the full philosophy in [`ABSTRACTION.md`](ABSTRACTION.md).
*   **Practical Exam:** See the framework applied in [`DOCKSIDE-EXAM.md`](DOCKSIDE-EXAM.md).
*   **Tool:** Experiment with the [`plane_analyzer.py`](plane_analyzer.py) script.

## Related Repos

*   [`oracle1`](https://github.com/cocapn/oracle1) – High-level coordination (Plane 5)
*   [`flux`](https://github.com/cocapn/flux) – Domain language & VM (Planes 4 & 2)
*   [`flux-lcar-esp32`](https://github.com/cocapn/flux-lcar-esp32) – Embedded firmware (Planes 1 & 0)

**Set your course. Find your plane.**