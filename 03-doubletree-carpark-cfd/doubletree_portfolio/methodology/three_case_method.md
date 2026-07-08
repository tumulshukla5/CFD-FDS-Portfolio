# Three-Case Methodology — DoubleTree Car Park CFD

## Case A: Steady Airflow

**Solver:** `simpleFoam` (parallel, 16 cores)

The 8 ACJF-315 jet fans are modelled as `semiImplicitSource` momentum sources in `fvModels`. Run directly with `foamRun -solver incompressibleFluid` to ensure fan momentum is correctly coupled into the UEqn.

```bash
mpirun -np 16 --oversubscribe foamRun -solver incompressibleFluid -parallel
reconstructPar -latestTime
```

Key setting: run to convergence (residuals < 1e-5 on U, p). The converged velocity field is the input to Case B.

## Case B: CO Transport (Frozen-Flow Two-Stage)

**Solver:** `foamRun -solver functions` with `scalarTransport` includeFunc

The converged Case A velocity field is copied as a fixed (frozen) advecting field. CO is introduced as a boundary condition representing vehicle exhaust. The scalar transport equation is solved over 3600 s (1 hour) of simulated time.

```bash
# copy Case A latest time as initial condition
cp -r ../caseA_airflow/2000 0
foamRun -solver functions
```

**Critical note:** do NOT run `fvModels` (fan sources) during Case B — the flow field is already established. The scalar reads U from the stored field without re-running the fans.

## Case C: Fire & Smoke Transient

**Solver:** `foamRun -solver fluid` (buoyant incompressible)

A 4 MW car fire is represented as heat and smoke sources:
- Temperature source: calibrated to match target fire HRR
- Smoke source: mass fraction source in the fire cell zone
- Jet fans remain active as momentum sources throughout

Results are extracted at multiple time steps (10, 15 min) to show the developing fire scenario.

## Solver choice summary

| Case | Solver | Why |
|---|---|---|
| A | `incompressibleFluid` directly | So `fvModels` fan sources are active |
| B | `functions` with `scalarTransport` | Frozen-flow; no need to re-solve momentum |
| C | `fluid` (buoyant) | Buoyancy coupling needed for fire plume |
