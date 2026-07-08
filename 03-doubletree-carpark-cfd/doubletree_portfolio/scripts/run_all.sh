#!/bin/bash
# run_all.sh — DoubleTree by Hilton Car Park CFD
# Three-case run sequence: airflow → CO → fire/smoke
# OpenFOAM 12, 16 cores

set -e
BASE=$(pwd)

echo "=== Case A: Steady Airflow ==="
cd "$BASE/caseA_airflow"
blockMesh
topoSet
decomposePar
mpirun -np 16 --oversubscribe foamRun -solver incompressibleFluid -parallel
reconstructPar -latestTime
echo "Case A done"

echo "=== Case B: CO Transport (frozen-flow) ==="
cd "$BASE/caseB_CO"
# copy converged flow field
cp -r "$BASE/caseA_airflow/$(ls "$BASE/caseA_airflow" | grep -E '^[0-9]+$' | sort -n | tail -1)" 0
foamRun -solver functions
echo "Case B done"

echo "=== Case C: Fire & Smoke Transient ==="
cd "$BASE/caseC_fire"
foamRun -solver fluid
echo "Case C done"

echo "=== All cases complete ==="
