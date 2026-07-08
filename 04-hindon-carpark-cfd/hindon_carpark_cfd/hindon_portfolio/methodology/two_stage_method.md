# The Two-Stage Scalar Transport Method (OpenFOAM 12)

## The problem

In OpenFOAM 12, `fvModels` (which drive jet-fan momentum sources via `semiImplicitSource` or `accelerationSource`) are **silently ignored** when running:

```bash
foamRun -solver functions   # with subSolver incompressibleFluid
```

The solver runs without errors but the fans produce no thrust. The flow field is driven by boundary conditions only.

## The solution: two-stage approach

### Stage 1 — Establish the fan-driven flow field

Run the momentum solver directly, so `fvModels` are active:

```bash
foamRun -solver incompressibleFluid
```

This correctly couples the `accelerationSource` fan momentum into the UEqn, producing a converged jet-fan-driven flow field. Run to convergence (residuals < 1e-5).

### Stage 2 — Scalar transport on the frozen flow field

With the flow field converged and stored in the time directory, run scalar transport:

```bash
foamRun -solver functions   # with scalarTransport in functions
```

This reads the frozen velocity field and transports the scalar (CO or smoke) through it. The flow field does not update — it is "frozen."

## Why this works

The scalar transport function reads `U` from the stored field and uses it as a fixed advecting velocity. Because the fan-driven flow is already converged and stored, the scalar sees the correct, fan-influenced velocity field without needing the fans to be active during transport.

## Key finding

- Use `accelerationSource` for jet fans, not `vectorSemiImplicitSource` (which does not exist in OpenFOAM 12 and causes a silent no-op).
- Verify fan zones are active via `topoSet` + `checkMesh` before running Stage 1.
- The frozen-flow assumption is valid for steady-state CO transport where the flow timescale >> scalar timescale.

## Applicability

This two-stage pattern is used across all car park CFD projects (Hindon, DoubleTree) wherever scalar transport (CO, smoke) is required alongside jet-fan-driven ventilation.
