# PS13 PROJECT — MASTER CONTEXT (carry-over prompt)
*Paste this whole file as your first message in a new Claude chat to restore full project context.*

## PROJECT
PS13: Hardware Trojan Detection & Side-Channel Timing Leakage Analysis.
Official ask: parse gate-level structural Verilog netlists, build an AST/DAG,
analyze topology/connectivity/fan-in/fanout/logic-depth/sequential elements,
and identify security-sensitive structures, using Python (Pyverilog,
NetworkX, Icarus Verilog). Verify with test netlists.

## HARDWARE PLATFORM
- Board: Digilent Nexys A7-100T
- FPGA: Xilinx Artix-7 XC7A100T-1CSG324C
- Tool: Vivado
- XDC: standard Nexys A7-100T general .xdc (all lines commented by default;
  nothing active yet — must uncomment + rename ports per signal used)

### Key XDC facts already confirmed
- Clock: CLK100MHZ on pin E3, LVCMOS33, 100 MHz (`create_clock ... -period 10.00`)
- 16 switches SW[0:15]: all LVCMOS33 **except SW[8]/SW[9] which are LVCMOS18**
- 16 LEDs LED[0:15], all LVCMOS33; plus 2 RGB LEDs (LED16_R/G/B, LED17_R/G/B)
- Buttons: CPU_RESETN (active-low, pin C12), BTNC/BTNU/BTNL/BTNR/BTND
- 7-segment: CA–CG + DP, AN[0:7] (8-digit multiplexed, active-low anodes)
- Other available but unused: Pmod JA/JB/JC/JD/JXADC, VGA, Micro SD,
  ADXL362 accelerometer, ADT7420 temp sensor, PDM mic, PWM audio,
  USB-UART, PS/2, Ethernet PHY, Quad SPI flash

### Planned ALU I/O mapping (not yet coded)
- Operand A = SW[7:0], Operand B = SW[15:8]
- Opcode = 5 pushbuttons (BTNU/D/L/R/C) as selector — NOT extra switches,
  because both 8-bit operands already consume all 16 switches
- Result = LED[7:0]; flags (carry/zero/overflow) = LED[15:13] or RGB LEDs
- Reset = CPU_RESETN
- Optional: 7-segment shows result in hex

## PROJECT ARCHITECTURE (LOCKED)
```
8-bit ALU (clean reference)
   ├─> Trojan Injection ─> Trojan-infected ALU ─┐
   └─> SCA/Timing experiment ────────────────────┤
                                                  ▼
                                        Vivado Synthesis
                                                  ▼
                          Gate-level structural Verilog netlist
                          (LUTs / MUXes / FFs, cells/nets/ports)
                                                  ▼
                                   OUR ANALYZER (Python)
        1. Netlist parser → 2. AST/DAG → 3. Circuit graph (NetworkX)
        → 4. Feature extraction (fan-in, fanout, depth, cell type,
             connectivity, signal paths)
        → 5. Trojan identification (suspicious regions, scored not
             hard-coded rules)
        → 6. Trojan analysis (trigger / payload / affected output /
             logic cone / propagation)
        → 7. SCA/Timing analysis (Vivado timing reports: delay, slack,
             critical paths, reference-vs-suspect comparison)
        → 8. Security analysis (combine structural + timing evidence)
        → 9. Verification (vs known ground truth)
        → 10. Final report generator
```

### Two distinct detection paths (do not conflate)
- **A. Structural/Trojan path**: netlist → AST/DAG → topology → connectivity
  → fan-in/fanout → logic structures → suspicious region → Trojan analysis.
  Question: "Is there a suspicious hardware structure, and what does it do?"
- **B. Side-channel/timing path**: design → Vivado implementation → timing
  info → relevant paths → delay/slack/critical paths → reference vs suspect
  comparison → timing anomaly → security analysis.
  Question: "Does the implementation show a measurable timing characteristic
  that could indicate leakage or anomaly?"
  Rule: never call an arbitrary timing difference an "SCA attack" — need a
  defined observable, measurement procedure, reference condition, and a
  statistical comparison criterion.

## REPO STRUCTURE (LOCKED)
```
PS13_Hardware_Security/
├── README.md
├── requirements.txt
├── FPGA/Nexys_A7_100T/
│   ├── vivado/ALU8.xpr
│   ├── rtl/alu8.v, alu8_top.v, trojan_alu8.v
│   ├── testbench/tb_alu8.v
│   └── constraints/nexys_a7_100t.xdc
├── NETLISTS/clean/, T1/, T2/, T3/   (synthesized structural .v per variant)
├── ANALYZER/parser/, graph/, features/, detection/,
│            trojan_analysis/, sca/, security/, verification/
├── DATA/features/, timing/, ground_truth/   (ground_truth is HIDDEN from
│                                              the analyzer during detection)
├── REPORTS/structural/, trojan/, sca/, final/
├── SCRIPTS/run_parser.py, extract_features.py, detect_trojan.py,
│           analyze_trojan.py, analyze_timing.py, run_full_analysis.py
└── TESTS/test_parser.py, test_graph.py, test_features.py,
          test_detection.py, test_timing.py
```
Data flow through the repo: Vivado (RTL in `FPGA/`) → synthesized netlist
lands in `NETLISTS/<variant>/` → Python (`ANALYZER/` + `SCRIPTS/`) parses it
→ intermediate results (features, timing) saved as JSON in `DATA/` →
final human-readable output in `REPORTS/`. `.bit` goes to the Nexys A7;
everything else stays on the PC. JSON is not analysis, just structured
storage/exchange between Python modules — generated and consumed by
scripts, not hand-written.

## BENCHMARK / TROJAN PLAN
- Clean design: 8-bit ALU (ADD/SUB/AND/OR/XOR/NOT/INC/DEC, adjustable)
- T1 (first, current target): Rare-combination combinational Trojan
  (trigger = rare input combo → payload → altered output). Ground truth
  known and hidden from analyzer during detection.
- T2 (later): more complex combinational Trojan, larger/less obvious cone
- T3 (later, postponed): sequential Trojan (state/temporal trigger)
- Detection score must combine multiple structural indicators, not a
  single hard-coded rule (e.g. NOT just "fanout > X").

| Trojan | Type | Main challenge | Key analyzer features exercised |
|---|---|---|---|
| T1 | Rare-combination combinational | Rare trigger condition | connectivity, fan-in/out, logic cone |
| T2 | Complex combinational | Less obvious trigger/payload, larger cone | topology, connectivity, path analysis |
| T3 | Sequential | Trigger depends on state/time | FFs, sequential paths, state analysis |

T1/T2/T3 are controlled benchmark designs to prove the framework isn't
built around one specific Trojan shape — not a claim these are the only
detectable Trojan types. SCA/timing analysis is a parallel branch applied
across all three benchmarks, not a 4th Trojan. Implementation order:
T1 → complete analyzer → T2 → improve analyzer → T3 → sequential extension
→ SCA/timing evaluation across all three. **Only T1 is to be implemented
right now.**

## DEVELOPMENT ORDER (STEP TRACKER)
1. Clean ALU RTL — **NOT STARTED**
2. Nexys A7 implementation (XDC) — not started
3. Simulate clean ALU — not started
4. Synthesize clean ALU (Vivado) — not started
5. Inspect clean gate-level netlist — not started
6. Build T1 Trojan RTL — not started
7. Simulate Trojan-infected design — not started
8. Synthesize Trojan-infected design — not started
9. Export structural netlist — not started
10. Build netlist parser (Python/Pyverilog) — not started
11. Build AST/DAG/circuit graph (NetworkX) — not started
12. Extract cells/nets/connectivity/fan-in/fanout/depth/paths/seq elements — not started
13. Suspicious-structure scoring — not started
14. Blind test analyzer on Trojan netlist — not started
15. Phase-3 trigger/payload/output/impact analysis — not started
16. Timing/SCA module (Vivado timing reports) — not started
17. Automated report generator — not started
18. Verify vs clean + Trojan test netlists — not started
19. Improve accuracy / reduce false positives — not started
20. Add T2 — not started
21. Add T3 (sequential) — deferred
22. Optional recovery/remediation — optional/future

## CURRENT STATE
**LEVEL 1 — System architecture locked.**
Confirmed: PS13 scope, Nexys A7-100T, Vivado, 8-bit ALU, T1 Trojan type,
SCA/timing inclusion, full analyzer pipeline (parser→AST/DAG→graph→
features→Trojan ID→Trojan analysis→SCA→security report→verification).

**Not yet implemented:** clean ALU RTL, XDC wiring, FPGA validation,
Trojan injection, synthesized netlist, Python parser, AST/DAG, NetworkX
graph, feature extractor, Trojan detector, timing/SCA module, report
generator.

**Immediate next step:** Write and verify the clean 8-bit ALU RTL,
matching the XDC port plan above, then bring it up on the Nexys A7 before
touching the Trojan.

## HOW TO ASSIST (persistent instructions)
- Preserve this architecture; don't swap the ALU or jump to sequential
  Trojan without strong reason.
- Build incrementally, following the step tracker above.
- Verilog: synthesizable, explained, clean/Trojan/testbench clearly
  separated, consider Vivado synthesis + Nexys A7 implementation.
- Python: modular, explained, no unexplained black-box libraries,
  explainability prioritized over cleverness.
- Netlist analysis: distinguish cells vs nets, logical vs FPGA-primitive
  structure, account for synthesis optimization — don't assume RTL
  structure survives synthesis unchanged.
- SCA: keep structural and timing analysis separate; use real Vivado
  timing data, never invented numbers.
- XDC: treat the uploaded Nexys A7-100T .xdc as authoritative; never
  invent pin assignments.
