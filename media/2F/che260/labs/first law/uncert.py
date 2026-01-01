import numpy as np

# Given uncertainties
delta_P_gauge = 0.02  # psig
delta_T = 0.01  # °C
delta_t = 0.2  # seconds
delta_mass_flow = 0.001  # kg (for mass flow rate uncertainty)

# Constants with uncertainties (if any)
delta_P_atm = 0.1  # psig (estimate for atmospheric pressure measurement)
delta_R_air = 0.1  # J/kgK (small uncertainty in gas constant)

# Your data
P_gauge = np.array([42.3, 79.3, 44.6, 75.3])  # psig
T = np.array([40.0, 40.40, 59.2, 59.3])  # °C
delta_t_vals = np.array([78.4, 69.5, 108.6, 100.5])  # seconds
P2_vals = np.array([0.27083141, 0.4470246, 0.26553863, 0.40361071])  # W

# Heater data for the ratio calculation
Q_heater_kJ = np.array([66.5, 40.6, 100.0, 108.6])  # kJ
delta_Q_heater = 0.1  # kJ = 100 J

# Convert to absolute temperature
T_K = T + 273.15

# Atmospheric pressure (with uncertainty)
P_atm = 14.39  # psia
P_abs = P_gauge + P_atm  # psia

print("Error Propagation Analysis")
print("=" * 50)

# Arrays to store results for the ratio calculation
delta_W_array = np.zeros(len(P_gauge))
W_array = np.zeros(len(P_gauge))

for i in range(len(P_gauge)):
    print(f"\nTrial {chr(65+i)}:")
    
    # 1. Error in rho2
    # rho2 = P_abs * 6894.76 / (R_air * T_K)
    
    # Partial derivatives for rho2
    d_rho_dP = 6894.76 / (287 * T_K[i])  # wrt P_abs
    d_rho_dT = -P_abs[i] * 6894.76 / (287 * T_K[i]**2)  # wrt T
    d_rho_dR = -P_abs[i] * 6894.76 / (287**2 * T_K[i])  # wrt R_air
    
    # Uncertainty in P_abs comes from both P_gauge and P_atm
    delta_P_abs = np.sqrt(delta_P_gauge**2 + delta_P_atm**2)
    
    # Total uncertainty in rho2
    delta_rho2 = np.sqrt(
        (d_rho_dP * delta_P_abs)**2 +
        (d_rho_dT * delta_T)**2 +
        (d_rho_dR * delta_R_air)**2
    )
    
    rho2 = P_abs[i] * 6894.76 / (287 * T_K[i])
    print(f"rho2 = {rho2:.4f} ± {delta_rho2:.4f} kg/m³")
    print(f"Relative error in rho2: {delta_rho2/rho2*100:.2f}%")
    
    # 2. Error in P2
    # P2 = P1_W * (n2/n1)**3 * rho2/rho1
    
    # Constants for P2 calculation
    P1_W = 0.001 * 745.7  # W
    n2_n1_ratio = 2000/4200
    rho1 = 1.293  # kg/m³
    
    # Partial derivatives for P2
    d_P2_d_rho2 = P1_W * (n2_n1_ratio)**3 / rho1
    
    # Uncertainty in P2 (only depends on rho2 uncertainty in this case)
    delta_P2 = np.sqrt((d_P2_d_rho2 * delta_rho2)**2)
    
    print(f"P2 = {P2_vals[i]:.8f} ± {delta_P2:.8f} W")
    print(f"Relative error in P2: {delta_P2/P2_vals[i]*100:.2f}%")
    
    # 3. Error in Work
    # Work = P2 * delta_t
    
    # Partial derivatives for Work
    d_Work_dP2 = delta_t_vals[i]  # wrt P2
    d_Work_dt = P2_vals[i]        # wrt delta_t
    
    # Uncertainty in Work
    delta_Work = np.sqrt(
        (d_Work_dP2 * delta_P2)**2 +
        (d_Work_dt * delta_t)**2
    )
    
    Work = P2_vals[i] * delta_t_vals[i]
    print(f"Work = {Work:.8f} ± {delta_Work:.8f} J")
    print(f"Relative error in Work: {delta_Work/Work*100:.2f}%")
    
    # Store for ratio calculation
    delta_W_array[i] = delta_Work
    W_array[i] = Work
    
    print("-" * 30)

# Now calculate uncertainty for the ratio W_propeller / Q_heater
print("\n" + "="*60)
print("ERROR PROPAGATION FOR W_propeller / Q_heater RATIO")
print("="*60)

for i in range(len(P_gauge)):
    print(f"\nTrial {chr(65+i)}:")
    
    # Convert Q_heater to Joules for consistency
    Q_heater_J = Q_heater_kJ[i] * 1000  # J
    delta_Q_heater_J = delta_Q_heater * 1000  # J
    
    # Calculate the ratio R = W_propeller / Q_heater
    R = W_array[i] / Q_heater_J
    
    # Partial derivatives for the ratio
    dR_dW = 1 / Q_heater_J           # ∂R/∂W
    dR_dQ = -W_array[i] / Q_heater_J**2  # ∂R/∂Q
    
    # Uncertainty in the ratio
    delta_R = np.sqrt(
        (dR_dW * delta_W_array[i])**2 +
        (dR_dQ * delta_Q_heater_J)**2
    )
    
    # Convert to percentage
    R_percent = R * 100
    delta_R_percent = delta_R * 100
    
    print(f"W_propeller = {W_array[i]:.2f} ± {delta_W_array[i]:.2f} J")
    print(f"Q_heater = {Q_heater_J:.1f} ± {delta_Q_heater_J:.1f} J")
    print(f"Ratio R = W/Q = {R:.8f} ± {delta_R:.8f}")
    print(f"Percentage: {R_percent:.6f}% ± {delta_R_percent:.6f}%")
    print(f"Relative error in ratio: {delta_R/R*100:.2f}%")
    
    # Uncertainty contributions breakdown
    contrib_W = (dR_dW * delta_W_array[i])**2
    contrib_Q = (dR_dQ * delta_Q_heater_J)**2
    total_variance = contrib_W + contrib_Q
    
    print(f"Uncertainty contribution from W: {np.sqrt(contrib_W)/delta_R*100:.1f}%")
    print(f"Uncertainty contribution from Q: {np.sqrt(contrib_Q)/delta_R*100:.1f}%")

# Final summary table
print("\n" + "="*60)
print("FINAL SUMMARY TABLE")
print("="*60)
print(f"{'Trial':<6} {'W (J)':<12} {'±ΔW':<10} {'Q (kJ)':<10} {'Ratio (%)':<12} {'±ΔRatio (%)':<15}")
print("-" * 60)

for i in range(len(P_gauge)):
    Q_heater_J = Q_heater_kJ[i] * 1000
    R = W_array[i] / Q_heater_J
    delta_R = np.sqrt(
        (delta_W_array[i] / Q_heater_J)**2 +
        (W_array[i] * delta_Q_heater * 1000 / Q_heater_J**2)**2
    )
    
    print(f"{chr(65+i):<6} {W_array[i]:<12.2f} {delta_W_array[i]:<10.2f} {Q_heater_kJ[i]:<10.1f} {R*100:<12.6f} {delta_R*100:<15.6f}")