# MCC5 Car Park Ventilation CFD

The **benchmark parking-ventilation CFD workflow** in OpenFOAM 12 — the reference methodology that subsequent car park projects were built on.

## Overview

A full 3D car park ventilation study covering the complete pipeline from geometry generation to reporting. Established the standard workflow for jet-fan-ventilated enclosed car parks: normal-operation airflow, fire scenario, and post-processed engineering deliverables.

## Workflow

| Stage | Method |
|---|---|
| Geometry | Python-generated STL |
| Meshing | `blockMesh` + `snappyHexMesh` |
| Flow solve | Parallel `simpleFoam` |
| Fire scenario | `foamRun -solver fluid` |
| Post-processing | ParaView + python-docx reporting |

## Key methodology

- Jet-fan-driven car park ventilation with a resolved flow field.
- Fire scenario for smoke/thermal behaviour.
- Automated reporting pipeline (python-docx) turning simulation output into client documentation.

## Repository contents

```
02-mcc5-carpark-cfd/
├── README.md
├── methodology/          workflow notes, meshing strategy
├── scripts/              STL generation, run scripts, post-processing
└── results/              summary figures & report excerpts
```

## Environment

WSL2 Ubuntu · OpenFOAM 12 Foundation · 16 cores · ParaView 5.10

---

> This project is the established workflow reference for parking-ventilation CFD. Client-confidential geometry is represented by methodology and scripts rather than proprietary model files.

*Tools: OpenFOAM 12 · snappyHexMesh · simpleFoam · ParaView · python-docx.*
