#!/bin/bash
# run_stages.sh — Hindon Gaur Mall car park CFD
# Four-stage run sequence: mesh → airflow → CO → fire/smoke
# OpenFOAM 12, WSL2 Ubuntu, 16 cores

set -e

echo "=== Stage 1: blockMesh ==="
blockMesh

echo "=== Stage 1: topoSet (fan zones) ==="
topoSet

echo "=== Stage 1: Steady jet-fan flow field ==="
# IMPORTANT: use -solver incompressibleFluid directly so fvModels (fans) are active
mpirun -np 16 --oversubscribe foamRun -solver incompressibleFluid -parallel
reconstructPar -latestTime

echo "=== Stage 2: CO transport without fans (baseline) ==="
# copy converged 0/ from a no-fan run; foamRun -solver functions for scalar
cp -r latestTime 0
foamRun -solver functions   # scalarTransport includeFunc

echo "=== Stage 3: CO transport WITH fans ==="
# use the fan-driven flow field from Stage 1
foamRun -solver functions

echo "=== Stage 4: Fire/smoke transient ==="
# fire source defined in fvModels; use fluid solver for buoyancy
foamRun -solver fluid

echo "=== All stages complete ==="
