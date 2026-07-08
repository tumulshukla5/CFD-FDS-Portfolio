# Hindon Gaur Mall — Car Park Ventilation CFD

3D **OpenFOAM 12** replication of a mall car park ventilation study, where the **two-stage scalar-transport method** was established.

## Overview

A car park ventilation CFD study that resolved a key OpenFOAM 12 workflow limitation and codified the two-stage method used across subsequent car park projects.

## The two-stage method

The core methodological contribution. OpenFOAM 12's `fvModels` (which drive jet-fan momentum sources) are **silently ignored** when running `foamRun -solver functions` with `subSolver incompressibleFluid` — they only wire into the momentum equation when running `foamRun -solver incompressibleFluid` directly. This drove a two-stage approach:

1. **Stage 1** — run `incompressibleFluid` *with* `fvModels` to produce a jet-fan-driven, converged flow field.
2. **Stage 2** — run scalar transport reading that frozen flow field.

## Key findings

- `accelerationSource` confirmed more reliable than `vectorSemiImplicitSource` (which does not exist in OF12).
- Three jet-fan zones confirmed active via `topoSet`.
- Established the frozen-flow pattern later reused on the DoubleTree project.

## Repository contents

```
04-hindon-carpark-cfd/
├── README.md
├── methodology/          two-stage method write-up
├── scripts/              topoSet setup, staged run scripts
└── results/              flow field & scalar transport summaries
```

---

> Where the two-stage scalar-transport method was established — a reusable pattern for jet-fan car park CFD in OpenFOAM 12.

*Tools: OpenFOAM 12 · incompressibleFluid · scalarTransport · topoSet.*
