import numpy as np
import matplotlib.pyplot as plt

# Depot dimensions

length = 100.0        # m
width = 38.0          # m
height = 0.5*(8.5+5.8)         # m

wall_area_total = 2 * height * (length + width)  # m²
# Wall breakdown
side_wall_area = height * length  # each long side
window_area = 0.5 * side_wall_area * 2  # 50% of both long sides
shutter_area = 22.5  # total 22.5 m²
solid_wall_area = wall_area_total - window_area - shutter_area

ground_insulation = False # True for insulated floor, False for uninsulated floor

# U-values
U_solid_wall = 1.6      # W/(m²·K) Cavity wall, no insulation
U_window = 5.0          # W/(m²·K) Single glazed
U_shutter = 4.5         # W/(m²·K)
U_roof = 5.0            # W/(m²·K) Perspex/Glass
if ground_insulation:
    U_floor = 0.2           # W/(m²·K)  # 0.2 W/(m²·K) for insulated floor
else:
    U_floor = 1.5           # W/(m²·K)  # 1.5 W/(m²·K) for uninsulated floor

roof_area = length * width                 # m²
floor_area = roof_area                     # m²

# Temperature setup
inside_temp_target = 16.0    # °C
initial_inside_temp = -3.0   # °C
outside_temp = -3.0          # °C

panel_single_energy = [36266]  # W
# panel references: 1,2,3,4,5,6,7,8
ref_panel_names = [
    "Panel 6 (36266 W)"
]

# Ground & air thermal properties
if ground_insulation:
    ground_thermal_capacity = 0
else:
    ground_thermal_capacity = floor_area * 120e3  # ~4.6×10^8 J/K

air_density = 1.225         # kg/m³
specific_heat_air = 1005    # J/(kg·K)

# Ventilation
enable_ventilation = True  # not decided yet !
air_change_rate_per_hour = 5 # ACH (5-8 or 8-12 ACH found in the literature)

# Simulation time
time_step = 3600 # seconds
total_simulation_time = 24 * 3600  # 24 hours
time_steps = int(total_simulation_time / time_step)
time = np.linspace(0, total_simulation_time, time_steps) / 3600  # in hours

# DERIVED PARAMETERS

volume_air = height * width * length  # m³
thermal_capacity_air = volume_air * air_density * specific_heat_air  # J/K
total_thermal_capacity = thermal_capacity_air + ground_thermal_capacity
if total_thermal_capacity <= 0:
    raise ValueError("Total thermal capacity is zero or negative.")


# FUNCTIONS
def calculate_heat_loss(delta_T):
    wall_loss = (
        solid_wall_area * U_solid_wall +
        window_area * U_window +
        shutter_area * U_shutter
    ) * delta_T
    roof_loss = roof_area * U_roof * delta_T
    floor_loss = floor_area * U_floor * delta_T
    return wall_loss + roof_loss + floor_loss

def calculate_ventilation_loss(delta_T):
    if not enable_ventilation:
        return 0.0
    air_flow_rate = (air_change_rate_per_hour * volume_air) / 3600  # m³/s
    return air_density * specific_heat_air * air_flow_rate * delta_T  # W

def simulate_heating(panel_power):
    temps = np.zeros(time_steps)
    temps[0] = initial_inside_temp

    for t in range(1, time_steps):
        delta_T = temps[t-1] - outside_temp
        heat_loss = calculate_heat_loss(delta_T) + calculate_ventilation_loss(delta_T)
        net_heat = panel_power - heat_loss
        temps[t] = temps[t-1] + (net_heat * time_step) / total_thermal_capacity
    return temps

# MAIN CALCULATION LOOP
panel_results = []
for panel_idx, panel_power in enumerate(panel_single_energy):
    min_panels = 20
    max_panels = 50
    found = False
    for num_panels in range(min_panels, max_panels + 1):
        total_power = panel_power * num_panels
        temperature_profile = simulate_heating(total_power)
        final_temp = temperature_profile[-1]
        if final_temp >= inside_temp_target:
            panel_results.append({
                'panel_type': ref_panel_names[panel_idx],  # Use correct panel name
                'num_panels': num_panels,
                'temperature_profile': temperature_profile
            })
            found = True
            #break
    if not found:
        panel_results.append({
            'panel_type': ref_panel_names[panel_idx],  # Use correct panel name
            'num_panels': 'Not sufficient (max limit reached)',
            'temperature_profile': None
        })

# RESULTS AND PLOTS

plt.figure(figsize=(12, 6))
for result in panel_results:
    if result['temperature_profile'] is not None:
        plt.plot(time, result['temperature_profile'], label=f"{result['panel_type']} x {result['num_panels']}")
    else:
        print(f"{result['panel_type']}: Insufficient heating even with {max_panels} panels.")

plt.axhline(inside_temp_target, color='red', linestyle='--', label='Target Temp (16°C)')
plt.xlabel('Time (hours)')
plt.ylabel('Temperature (°C)')
plt.title('Indoor Temperature Rise with Different Fixed Panel Types \n Ground loss conditions based on the thermal conductivity of the floor {} W/(m²·K) and air change rate {} per hour'.format(U_floor, air_change_rate_per_hour))
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, fontsize=10)
plt.grid(True)
plt.tight_layout()
plt.subplots_adjust(bottom=0.22)  # Add extra space at the bottom for the legend
plt.show()

# ========================
# TEXTUAL SUMMARY
# ========================

print("Heating Panel Summary:")
for result in panel_results:
    print(f"- {result['panel_type']}: Panels needed = {result['num_panels']}")
