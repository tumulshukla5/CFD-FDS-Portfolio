# DoubleTree by Hilton — Car Park Ventilation CFD

A full **three-case OpenFOAM 12 replication** of a PHOENICS parking-ventilation study, validated against the original commercial-code targets.

## Overview

Replication of a car park ventilation study (Guwahati) originally performed in PHOENICS, reproduced in OpenFOAM 12 across three scenarios: steady airflow, CO transport, and a fire/smoke transient. The OpenFOAM results were calibrated to match the PHOENICS benchmark within engineering tolerance.

## Model

| Parameter | Value |
|---|---|
| Domain | 93 × 30 × 3.4 m |
| Mesh | ~631,700 cells |
| Jet fans | 8 × ACJF-315 |
| Cases | A: steady airflow · B: CO transport · C: fire/smoke transient |

## Three-case methodology

**Case A — Steady airflow.** Jet-fan-driven flow field established with the fans as momentum sources.

**Case B — CO transport.** Frozen-flow two-stage method: the converged Case A flow field is read by a scalar-transport stage carrying the CO field.

**Case C — Fire/smoke transient.** The demanding case, requiring:
- `pRefCell` in the PIMPLE block
- incompressible `physicalProperties`
- correct `fvModels` placement for sources
- **empirical calibration** of temperature (6.6 K/s) and smoke (0.00419 kg/kg/s) sources to match the PHOENICS targets — achieved within **2–12% on temperature** and **8–34% on smoke** during the fire-active phase

## Deliverables

All **8 MP4 animations** generated via the ParaView Python API, with documented fixes (AnimationTime set before UpdatePipeline; explicit colorbar text colour).

## Repository contents

```
03-doubletree-carpark-cfd/
├── README.md
├── methodology/          three-case method, calibration notes
├── scripts/              case setup, ParaView animation scripts
└── results/              calibration tables, animation stills
```

---

> Benchmark replication project: OpenFOAM 12 reproducing a PHOENICS study to validate the open-source workflow against commercial-code results.

*Tools: OpenFOAM 12 · scalar transport · ParaView Python API · PHOENICS (benchmark).*
