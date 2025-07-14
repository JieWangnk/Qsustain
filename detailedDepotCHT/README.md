# Depot Radiant Heat Transfer (CHT) Simulation

## Overview

This OpenFOAM case simulates **Conjugate Heat Transfer (CHT)** in a depot building with radiant heating panels. The simulation models natural convection, radiation heat transfer, and turbulent flow in a realistic depot geometry with 12 radiant heating panels providing thermal comfort.

## Geometry Description

The depot consists of six main components:

- **DepotCelling**: Roof structure (29,252 faces)
- **DepotWall**: External walls (10,323 faces) 
- **DepotFloor**: Ground floor (15,570 faces)
- **DepotPanel12**: 12 radiant heating panels (27,648 faces)
- **DepotWindow**: Windows for natural lighting (11,264 faces)
- **DepotShutter**: Ventilation shutters (1,620 faces)

**Dimensions**: 102m × 37.5m × 7.8m (Length × Width × Height)  
**Total Volume**: ~28,800 m³

## Physical Setup

### Operating Conditions
- **External Temperature**: -3°C (270.15 K)
- **Initial Air Temperature**: 8°C (281.15 K)
- **Radiant Panel Heat Flux**: 503.7 W/m²
- **Working Fluid**: Air (perfect gas)

### Heat Transfer Mechanisms
1. **Natural Convection**: Buoyancy-driven flow due to temperature differences
2. **Radiation**: P1 radiation model for thermal radiation exchange
3. **Conduction**: Through solid boundaries

## Mesh Details

- **Total Cells**: 333,858
- **Total Faces**: 1,097,261  
- **Total Points**: 429,085
- **Mesh Generator**: snappyHexMesh with 3 refinement levels
- **Refinement**: Higher resolution near heating panels and features

### Refinement Levels
- **Level 0**: Background mesh (10,752 cells)
- **Level 1**: Intermediate refinement (125,632 cells)  
- **Level 2**: Fine resolution near panels (197,474 cells)

## Solver Configuration

### Solver: `foamRun` (OpenFOAM 12)
- **Application**: `fluid` solver
- **Mode**: Steady-state SIMPLE algorithm
- **Turbulence**: k-ε RAS model
- **Thermodynamics**: Compressible perfect gas

### Numerical Schemes
- **Time**: Steady-state
- **Gradient**: Gauss linear
- **Divergence**: Bounded Gauss upwind
- **Laplacian**: Gauss linear corrected

## Boundary Conditions

### Temperature (T)
- **Structural boundaries** (Ceiling, Walls, Floor, Window, Shutter): Fixed temperature 270.15 K
- **Radiant panels**: Heat flux boundary with 503.7 W/m² surface heating

### Velocity (U)
- **All boundaries**: No-slip wall conditions

### Radiation (G)
- **All boundaries**: Marshak radiation with emissivity = 1.0

### Turbulence (k, ε)
- **All boundaries**: Wall functions for near-wall treatment

## Running the Simulation

### Method 1: Using Allrun Script

**Serial execution:**
```bash
./Allrun
```

**Parallel execution:**
```bash
./Allrun parallel
```

### Method 2: Manual Steps

1. **Generate base mesh:**
```bash
blockMesh
```

2. **Generate complex geometry mesh:**
```bash
snappyHexMesh -overwrite
```

3. **Run simulation:**
```bash
foamRun
```

### Parallel Execution
```bash
decomposePar
mpirun -np 4 foamRun -parallel
reconstructPar
```

## Post-Processing

### Visualization
- Open in ParaView: `paraFoam`
- View results at different time steps
- Analyze temperature distribution, velocity vectors, and radiation patterns

### Key Results to Examine
1. **Temperature field**: Air temperature distribution throughout depot
2. **Velocity field**: Natural convection flow patterns
3. **Radiation field (G)**: Thermal radiation intensity
4. **Surface heat transfer**: Heat flux on all boundaries

## File Structure

```
detailedDepotCHT/
├── 0/                          # Initial conditions
│   ├── T                       # Temperature field
│   ├── U                       # Velocity field
│   ├── p, p_rgh               # Pressure fields
│   ├── k, epsilon             # Turbulence fields
│   └── G                       # Radiation field
├── constant/
│   ├── polyMesh/              # Mesh files
│   ├── triSurface/            # STL geometry files
│   ├── physicalProperties     # Fluid properties
│   ├── radiationProperties    # Radiation model setup
│   └── fvModels               # Heat source models
├── system/
│   ├── controlDict            # Simulation control
│   ├── fvSchemes             # Numerical schemes
│   ├── fvSolution            # Solver settings
│   ├── snappyHexMeshDict     # Mesh generation
│   └── decomposeParDict      # Parallel decomposition
├── Allrun                     # Execution script
├── Allclean                   # Cleanup script
└── README.md                  # This file
```

## Expected Results

### Performance Indicators
- **Convergence**: Residuals < 1e-3 for all variables
- **Heat balance**: Energy conservation across domain
- **Temperature rise**: Significant warming from radiant panels
- **Flow patterns**: Thermal plumes from heated panels

### Typical Output
- **Runtime**: ~2-4 hours (serial), ~30-60 minutes (4 cores)
- **Memory**: ~4-8 GB RAM
- **Storage**: ~500 MB - 2 GB result files

## Troubleshooting

### Common Issues
1. **Mesh generation fails**: Check STL file quality and orientation
2. **Convergence problems**: Adjust relaxation factors in fvSolution
3. **Memory issues**: Use parallel execution or coarser mesh
4. **Boundary condition errors**: Verify patch names match mesh

### Performance Tips
- Use parallel execution for faster results
- Monitor residuals for convergence
- Adjust time step for stability
- Check mesh quality with `checkMesh`

## References

- [OpenFOAM User Guide](https://www.openfoam.com/documentation/user-guide)
- [OpenFOAM Heat Transfer](https://www.openfoam.com/documentation/tutorial-guide/tutorialse4.php)
- [snappyHexMesh Guide](https://www.openfoam.com/documentation/tutorial-guide/tutorialse3.php)

## Case Information

- **Created**: July 2025
- **OpenFOAM Version**: 12
- **Solver**: foamRun (fluid)
- **Physics**: Natural convection + Radiation
- **Application**: Building HVAC analysis