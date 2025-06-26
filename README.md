# Depot Heating Model

This project provides a simplified thermal analysis of a railway depot as a precursor to more detailed Computational Fluid Dynamics (CFD) modeling. The results and insights from this model are intended to inform and guide subsequent CFD studies by establishing baseline heating requirements and understanding key thermal behaviors.

This project simulates the thermal behavior of a railway depot to estimate the number of heating panels required to maintain a target indoor temperature under various conditions. The model accounts for heat losses through the building envelope, ventilation, and the effects of thermal mass from air and (optionally) the ground.

## Project Contents
- `depotHeatingModel.py`: Main Python script for running the thermal simulation and generating plots.
- `thermalBalance.ipynb`: Jupyter notebook for interactive exploration, scenario analysis, and schematic plotting. Includes detailed explanations and step-by-step calculations.
- `depot_sechmatic.png`: Schematic image of the energy balance model in the depot (can be generated from the notebook).
- `requirements.txt`: List of required Python packages.
- `HotRadiationDepot12/`: OpenFOAM case directory for CFD simulation of the depot with radiative heating.

## OpenFOAM Case: HotRadiationDepot12

This folder contains a full OpenFOAM case for CFD simulation of the depot with radiative heating.

### Structure

- `0/` – Initial and boundary conditions for all fields (e.g., T, U, p, G, etc.)
- `constant/` – Mesh, material properties, and radiation settings
- `system/` – Solver settings, mesh generation, and decomposition
- `Allrun` – Script to generate the mesh and run the case
- `Allclean` – Script to clean/reset the case

### Prerequisites

- OpenFOAM installed and sourced in your shell (e.g., `source /opt/openfoam*/etc/bashrc`)
- Parallel processing enabled if you want to use multiple cores

### How to Run

1. **Clean the case (optional, but recommended for a fresh start):**
   ```bash
   cd HotRadiationDepot12
   ./Allclean
   ```

2. **Run the full case (mesh generation, decomposition, simulation, reconstruction):**
   ```bash
   ./Allrun
   ```

   This script will:
   - Generate the base mesh (`blockMesh`)
   - Extract surface features (`surfaceFeatures`)
   - Run `snappyHexMesh` for mesh refinement
   - Decompose the domain for parallel run
   - Run the main solver in parallel
   - Reconstruct the results

3. **Post-processing:**
   - Results will be available in the `HotRadiationDepot12` directory after the run.
   - Use OpenFOAM tools (e.g., `paraFoam`) for visualization:
     ```bash
     paraFoam
     ```

### Notes

- You can edit the files in `system/`, `constant/`, and `0/` to change simulation parameters, mesh, or boundary conditions.
- The solver used is determined automatically by the `Allrun` script (`application=$(getApplication)`).
- For custom runs or debugging, you can execute the commands in `Allrun` step by step.

## Features
- Models heat transfer through walls, windows, shutters, roof, and floor
- Includes ventilation heat loss based on air changes per hour (ACH)
- Considers both insulated and uninsulated floor scenarios
- Calculates the number of heating panels needed to reach a target temperature
- Visualizes indoor temperature rise over time
- Jupyter notebook for interactive analysis and schematic visualization

## Requirements
- Python 3.x
- numpy
- matplotlib

Install dependencies with:
```bash
pip install numpy matplotlib
```

## Usage
### Python Script
1. Edit `depotHeatingModel.py` to set your desired parameters (dimensions, U-values, ventilation rate, etc.).
2. Set `ground_insulation = True` for an insulated floor (modern slab), or `False` for an uninsulated floor.
3. Run the script:
```bash
python depotHeatingModel.py
```

### Jupyter Notebook
- Open `thermalBalance.ipynb` in Jupyter or VSCode for interactive exploration.
- The notebook includes:
  - Schematic plotting of the depot's energy balance (see also `depot_sechmatic.png`).
  - Step-by-step parameter setup and scenario analysis.
  - Mathematical background and references.

## Input Parameters
- **Depot dimensions:** length, width, height (meters)
- **Envelope U-values:**
  - Walls, windows, shutters, roof, and floor (W/(m²·K))
  - Floor U-value is set to 0.2 for insulated, 1.5 for uninsulated
- **Thermal mass:**
  - Air is always included
  - Ground is included only if `ground_insulation = False`
- **Ventilation:** Air changes per hour (ACH)
- **Heating panels:**
  - Power per panel (W)
  - Range of panel counts to test
- **Temperatures:**
  - Initial, outside, and target indoor temperature (°C)

## Insulated vs. Uninsulated Floor
- **Insulated floor:**
  - `U_floor = 0.2` W/(m²·K)
  - Ground thermal mass is excluded
- **Uninsulated floor:**
  - `U_floor = 1.5` W/(m²·K)
  - Ground thermal mass is included (using kappa value for dense concrete)

## Output
- **Plot:** Indoor temperature vs. time for each tested panel configuration
- **Text summary:** Number of panels required to reach the target temperature
- **Schematic:** See `depot_sechmatic.png` or generate from the notebook

## Example Output
```
Heating Panel Summary:
- Panel 6 (36266 W): Panels needed = 24
...
```

## Interpretation
Use the plot and summary to determine the minimum number of panels needed for your scenario. Adjust parameters as needed to explore different insulation or ventilation strategies.

---

## Mathematical Model (External Material)

The following section provides a detailed description of the mathematical model underlying this project. This is included as external material for reference and for users interested in the theoretical background.

The code numerically solves a **first-order ordinary differential equation (ODE)** that describes the energy balance of the depot. The fundamental principle is the first law of thermodynamics: the change in the internal energy of the system is equal to the net heat added to the system.

The core equation for the indoor temperature ($T_{in}$) over time ($t$) is:

$$\frac{dT_{in}}{dt} = \frac{Q_{net}}{C_{total}}$$

### 1. Total Thermal Capacity ($C_{total}$)
This represents the system's resistance to temperature change. In the model, it's the sum of the thermal capacity of the air and the ground.

$$C_{total} = C_{air} + C_{ground}$$

- **Air Thermal Capacity ($C_{air}$):**
  $$C_{air} = V_{air} \cdot \rho_{air} \cdot c_{p,air}$$
- **Ground Thermal Capacity ($C_{ground}$):**
  The assumed value discussed above.

### 2. Net Heat Flow Rate ($Q_{net}$)
This is the rate at which energy is added to the system (in Watts, or Joules per second). It's the difference between the heat generated by the panels and the heat lost to the environment.

$$Q_{net} = Q_{panels} - Q_{loss}$$

- **Heating Power ($Q_{panels}$):**
  $$Q_{panels} = N_{panels} \cdot P_{panel}$$
- **Total Heat Loss ($Q_{loss}$):**
  $$Q_{loss} = Q_{conduction} + Q_{ventilation}$$

### 3. Heat Loss Mechanisms
Heat loss is driven by the temperature difference between the inside and outside, $\Delta T = T_{in} - T_{out}$.

- **Conduction Loss ($Q_{conduction}$):**
  $$Q_{conduction} = (\sum_{i} U_i A_i) \cdot \Delta T$$
  $$\sum U_i A_i = (U_{solid}A_{solid} + U_{win}A_{win} + U_{shut}A_{shut} + U_{roof}A_{roof} + U_{floor}A_{floor})$$

- **Ventilation Loss ($Q_{ventilation}$):**
  $$Q_{ventilation} = \dot{m}_{air} \cdot c_{p,air} \cdot \Delta T$$
  Where the mass flow rate of air ($\dot{m}_{air}$) is determined by the Air Changes per Hour (ACH) and the building volume ($V_{air}$):
  $$\dot{m}_{air} = \frac{ACH \cdot V_{air}}{3600} \cdot \rho_{air}$$

### 4. Numerical Solution
The code does not solve the differential equation analytically. Instead, it uses the **Euler method**, a numerical technique to approximate the solution over discrete time steps ($\Delta t$). The temperature at the next time step ($T_{t+1}$) is found from the temperature at the current time step ($T_t$):

$$T_{t+1} = T_t + \Delta T_{in}$$

Where the change in temperature is calculated as:

$$\Delta T_{in} = \frac{Q_{net} \cdot \Delta t}{C_{total}}$$

This is exactly what the simulation loop implements:

`temps[t] = temps[t-1] + (net_heat * time_step) / total_thermal_capacity`

This is a valid and common approach for this type of thermal simulation.

---

For questions or improvements, please open an issue or submit a pull request. 