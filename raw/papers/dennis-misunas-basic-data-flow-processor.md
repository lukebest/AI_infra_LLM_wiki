---
source_url: https://dl.acm.org/doi/10.1145/641675.642111
ingested: 2026-06-24
sha256: b454aed8689c2396e10b1792e129f5e145101f80c9a2e35395b53693e53443d7
---

# A Preliminary Architecture for a Basic Data-Flow Processor (ISCA 1975)

**Authors:** Jack B. Dennis, David P. Misunas — Project MAC, MIT

**Venue:** 2nd Annual Symposium on Computer Architecture, 1975
**Support:** NSF GJ-34671

## Motivation

- Data-flow program representation: data-driven execution, parallelism in program structure
- Von Neumann adaptations for parallel computation suffer processor switching + memory/processor interconnection limits
- Elementary processor [6,7] implements Karp–Miller schema for signal processing (stream/sample loops)
- **Basic machine** extends Dennis & Fosseen [5] with conditionals and iteration — step toward Fortran-level data-flow

## Elementary Processor (summary)

- Program = directed graph: operators, links, tokens on arcs
- **Instruction Cell**: instruction reg + 2 operand regs → operation packet when enabled
- **Arbitration Network**: round-robin + switch by opcode → Operation Units (pipelined)
- **Distribution Network**: route data packets to destination operand registers by address
- Speed-independent async module designs [7]

## Basic Data-Flow Language

- **Data links**: tokens carry values (as elementary)
- **Control links**: tokens carry true/false
- **Decider**: predicate → control token
- **Boolean operator**: combine control tokens
- **T-gate / F-gate**: pass/absorb data on true/false control
- **Merge**: select data from true/false input per control token
- Output arc must be empty to fire (all actors/links)

## Basic Processor (without two-level memory)

- Fig. 9: + Decision Units, Control Network
- Gate/merge not separate instructions: gating codes in Cells; merge via multi-destination distribution
- Instruction Cell formats (Fig. 10): operators, deciders, Boolean ops, control distribution, forwarding
- Receivers (Fig. 11): value flag + gate flag; gating codes none/true/false/cons
- Control packets: `{gate,true|false,addr}` or `{value,true|false,addr}`

## Two-Level Memory

- Only **active** instructions occupy Instruction Cells
- **Instruction Memory**: groups of 3 locations per Cell; commands `{a,retrieve}` / `{a,store}`
- **Cell Block** per major address; minor address within block
- **Association Table**: `{minor, status}` — free / engaged / occupied
- **Stack**: LRU order for displacement of occupied Cells
- Procedure 1: packet arrival → allocate/preempt Cell → retrieve instruction → update operands → fire if enabled
- Procedure 2: instruction packet arrival → engaged→occupied → fire if enabled

## Conclusion / Future

- Elementary: stream signal processing
- Basic: step toward numerical/Fortran-like data-flow
- Still needed: arrays, concurrent procedures, vector parallelism, full general-purpose model [4]

## Key References in Paper

- [4] Dennis 1974 — generalized data flow procedure language
- [5] Dennis & Fosseen — basic data flow schemas
- [6] Dennis & Misunas 1974 ACM — elementary parallel signal processing architecture
- [7] CSG Memo 101 — elementary processor async design
- [8] Karp & Miller — parallel computation graph model
