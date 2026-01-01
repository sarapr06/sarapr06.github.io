import numpy as np

# Your data with uncertainties
P2_vals = np.array([0.271, 0.447, 0.266, 0.404])  # W
delta_P2 = np.array([0.001, 0.001, 0.001, 0.001])  # W
m_vals = np.array([0.038, 0.062, 0.035, 0.052])  # kg
delta_m = 0.001  # kg
cv_vals = np.array([92.8, 56.1, 98.2, 72.6])  # kJ/kgK
delta_cv = np.array([6.336, 3.777, 6.040, 3.587])  # kJ/kgK

# Convert Cv from kJ/kgK to J/kgK for unit consistency
cv_vals_J = cv_vals * 1000  # J/kgK
delta_cv_J = delta_cv * 1000  # J/kgK

print("Error Propagation for dT/dt = P₂ / (m * Cv)")
print("=" * 60)

for i in range(len(P2_vals)):
    print(f"\nTrial {chr(65+i)}:")
    
    # Calculate dT/dt
    dT_dt = P2_vals[i] / (m_vals[i] * cv_vals_J[i])
    
    # Partial derivatives
    d_dTdt_dP2 = 1 / (m_vals[i] * cv_vals_J[i])           # ∂(dT/dt)/∂P₂
    d_dTdt_dm = -P2_vals[i] / (m_vals[i]**2 * cv_vals_J[i])  # ∂(dT/dt)/∂m
    d_dTdt_dcv = -P2_vals[i] / (m_vals[i] * cv_vals_J[i]**2) # ∂(dT/dt)/∂Cv
    
    # Uncertainty in dT/dt
    delta_dT_dt = np.sqrt(
        (d_dTdt_dP2 * delta_P2[i])**2 +
        (d_dTdt_dm * delta_m)**2 +
        (d_dTdt_dcv * delta_cv_J[i])**2
    )
    
    print(f"dT/dt = {dT_dt:.3e} ± {delta_dT_dt:.3e} °C/s")
    print(f"Relative error in dT/dt: {delta_dT_dt/dT_dt*100:.2f}%")
    
    # Uncertainty contributions breakdown
    contrib_P2 = (d_dTdt_dP2 * delta_P2[i])**2
    contrib_m = (d_dTdt_dm * delta_m)**2
    contrib_cv = (d_dTdt_dcv * delta_cv_J[i])**2
    total_variance = contrib_P2 + contrib_m + contrib_cv
    
    print("Uncertainty contributions:")
    print(f"  From P₂: {np.sqrt(contrib_P2)/delta_dT_dt*100:.1f}%")
    print(f"  From m: {np.sqrt(contrib_m)/delta_dT_dt*100:.1f}%")
    print(f"  From Cv: {np.sqrt(contrib_cv)/delta_dT_dt*100:.1f}%")
    
    print("-" * 40)

# Summary table
print("\n" + "=" * 60)
print("SUMMARY TABLE: dT/dt Uncertainty Analysis")
print("=" * 60)
print(f"{'Trial':<6} {'P₂ (W)':<12} {'m (kg)':<10} {'Cv (kJ/kgK)':<12} {'dT/dt (°C/s)':<20} {'±Δ(dT/dt)':<15}")
print("-" * 60)

for i in range(len(P2_vals)):
    dT_dt = P2_vals[i] / (m_vals[i] * cv_vals_J[i])
    delta_dT_dt = np.sqrt(
        (delta_P2[i] / (m_vals[i] * cv_vals_J[i]))**2 +
        (P2_vals[i] * delta_m / (m_vals[i]**2 * cv_vals_J[i]))**2 +
        (P2_vals[i] * delta_cv_J[i] / (m_vals[i] * cv_vals_J[i]**2))**2
    )
    
    print(f"{chr(65+i):<6} {P2_vals[i]:<12.3f} {m_vals[i]:<10.3f} {cv_vals[i]:<12.1f} {dT_dt:<20.3e} {delta_dT_dt:<15.3e}")

print("\n" + "=" * 60)
print("KEY OBSERVATIONS:")
print("=" * 60)
print("1. dT/dt values are very small (~10⁻⁵ °C/s), confirming minimal heating from propeller")
print("2. The dominant uncertainty source varies by trial:")
print("   - Typically Cv uncertainty contributes most due to large relative error in Cv")
print("   - Mass uncertainty becomes more significant for smaller mass values")
print("   - P₂ uncertainty is usually the smallest contributor")
print("3. All dT/dt values have similar order of magnitude despite different conditions")