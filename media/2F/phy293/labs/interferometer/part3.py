import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import stats
from scipy.optimize import curve_fit

#Part 3: Aluminum
N=np.array([30,30,30,15,27])
ZPD=np.array([28.8,27.4,27.4,29.8,24.3])
L0=np.array([80.69,80.76,81.18,80.03,80.49]) * 1e-3
T_f=np.array([31.2, 29.3,30.1,30.6,25.4])
deltaT=T_f - ZPD
Lf=np.array([80.99,80.82,82.54,81.22,80.75]) * 1e-3
lambda_g=497e-9

dT_n=N*lambda_g/(2*L0*23e-6)
dT=np.array([3.9, 4.1, 3.8, 2.3, 3.8])

def model_function(dT, alpha):
    L=L0
    wavelength=lambda_g
    return 2*L/wavelength * alpha * dT
popt, pcov = curve_fit(model_function, dT, N)
print("n: ", popt, ", Covariance: ", pcov)

#chisquared for alpha
y_predicted = model_function(dT, *popt)
y_res = N - y_predicted
chi_squared = np.sum((y_res**2) / (N))
degrees_of_freedom = len(N) - 1  # n - m (5 data points - 1 parameter)
reduced_chi_squared = chi_squared / degrees_of_freedom
print("\n" + "="*60)
print("RESIDUAL ANALYSIS FOR ALUMINUM THERMAL EXPANSION FIT")
print("="*60)
print("Point | Obs (fringe) | Pred (fringe) | Residual ")
print("-" * 45)
for i in range(len(N)):
    print(f"{i+1:5d} | {N[i]:9.6f} | {y_predicted[i]:10.6f} | {y_res[i]:12.6f}")
print(f"\nResiduals Statistics:")
print(f"  Mean: {np.mean(y_res):.6f}")
print(f"  Std Dev: {np.std(y_res):.6f}")
print(f"\nChi-Squared Analysis:")
print(f"  Chi-squared (χ²): {chi_squared:.6f}")
print(f"  Degrees of freedom (ν): {degrees_of_freedom}")
print(f"  Reduced chi-squared (χᵣ²): {reduced_chi_squared:.6f}")
#residuals fit
plt.errorbar(dT, y_res, yerr=1, xerr=0.1, fmt='o', ecolor='r', capthick=2, capsize=5, markersize=8, label='Residuals', alpha=0.7)
plt.axhline(0, color='black', linestyle='--')
plt.xlabel('Delta T (°C)')
plt.ylabel('Residuals (fringes)')
plt.title('Residuals of Aluminum Thermal Expansion Fit')
plt.legend()
plt.grid()
plt.show()
#plot
#with error bars of N+-1, theat +- 0.1
plt.errorbar(dT, N, yerr=1, xerr=0.1, fmt='o', ecolor='r', capthick=2, capsize=5, markersize=8, label='Data points', alpha=0.7)
plt.xlabel('Delta T (°C)')
plt.ylabel('Number of Fringes')
plt.title('Thermal Expansion of Aluminum Fit')
#plotting the fit
x_fit = np.linspace(min(dT), max(dT), 5)
y_fit = model_function(x_fit, *popt)
plt.plot(x_fit, y_fit, 'b-', label='Linear fit')
plt.legend()
plt.grid()
plt.show()
