---
type: Raw Source
title: Corner To Corner Route (6×8 AIC folded multi-ring)
ingested: 2026-08-13
source_file: raw/articles/corner-to-corner-route.html
description: Interactive true-proportion reticle viz of a 6×8 AIC folded multi-ring NoC; shortest-path latency with RBRG turn service.
---

# Corner To Corner Route

Interactive visualization (title: *Corner To Corner Route*). Immutable original: [corner-to-corner-route.html](corner-to-corner-route.html).

Working-layer synthesis: [AIC Folded Multi-Ring NoC](/concepts/aic-folded-multi-ring-noc.md).

## What the viz encodes

- **Floorplan:** 26,000 × 33,000 µm reticle (true proportion); core field 25,000 × 32,000 µm after 500 µm edge; 6×8 = 48 cores.
- **Pitch:** 3130 µm (X), 5340 µm (Y).
- **Wire delay law:** `ceil(µm / 400)` cycles (400 µm/cycle), except RBRG turns which use a fixed service, and CS/PIPE station passes which have 0 base cycles.
- **Default extras:** all Advanced latency parameters start at 0 (straight / near / far / CS / PIPE / inject / eject / FIFO waits).

## Station graph (extracted from viz JS)

- 12 horizontal rails × 16 vertical rails of **RBRG** stations (`B:hi:vi`).
- On each horizontal rail, 8 **CS or PIPE** mid-stations (`M:hi:c`); type is CS when `hi%2 == c%2`, else PIPE.
- Core `eid = r*8+c` injects onto the mid-station of rail `hi = 2*r + (c%2)`.

## Directed micro-edge kinds

| kind | typical ℓ | base cycles | notes |
|------|-----------|-------------|-------|
| inject / eject | 105 µm | 1 | Core ↔ CS access |
| harm (H arm) | 1125 µm | 3 | Horizontal arm |
| gap | 40 µm | 1 | Inter-station gap (H or V) |
| vspan | 4460 µm | 12 | Vertical span between even/odd rails |
| straight RBRG | 420 µm | 2 | Same-axis through RBRG |
| near turn | 315 µm geom. | 10 | 5 ingress + 5 egress |
| far turn | 525 µm geom. | 10 | 5 ingress + 5 egress |
| hfold | 5180 µm | 13 | Left/right row-pair wrap |
| vfold | 405 µm | 2 | Top/bottom column wrap |
| cs / pipe | 0 | 0 | Mid-station pass; extras optional |

RBRG turn geometry is inclusive of the 10-cycle service (not added on top of `ceil(ℓ/400)`).

## Routing legality (shortest path)

Phase machine for core-to-core:

- Same row (`sr == dr`): **H-only**. Axis-changing RBRG turns (`trans`) are illegal.
- Different rows: phase 0 (H) → first `H2V` turn → phase 1 (V) → `V2H` only when `floor(hi/2) == dest_row` → phase 2 (H on dest row) → eject.
- Objective: minimize `(total_cyc, um, turns, steps, edge-id tiebreak)`.

Default UI pair is Core 00 → Core 47 (corner to corner).
