import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import stats
from scipy.optimize import curve_fit

#Part 2: fit to get refractive index
lambda_g = 497e-9
thickness = 7.70e-3
N_f1=np.array([10,27,20,26,26,13,15,7,7,10,10])
N_f=np.array([14, 19, 56,  21, 56,   9, 25, 16, 14,  4, 22])
theta=np.array([254.5,261,251.5,261,251.5,260,253.5,260.5,254.5,259.5,254])
delta_theta_rads=math.pi/180*abs(257.5-theta)
print(257.5-theta)
t_div_l=thickness/lambda_g

N=t_div_l*delta_theta_rads**2*(1-1/1.5)
print(N)

def model_function(x, n):
    return t_div_l * x**2 * (1 - 1/n)

popt, pcov = curve_fit(model_function, delta_theta_rads, N_f)
print("n: ", popt, ", Covariance: ", pcov)


#chisquared for n
y_predicted = model_function(delta_theta_rads, *popt)
y_res = N_f - y_predicted
chi_squared = np.sum((y_res**2) / (N_f))
degrees_of_freedom = len(N_f) - 1  # n - m (11 data points - 1 parameter)
reduced_chi_squared = chi_squared / degrees_of_freedom
print("\n" + "="*60)
print("RESIDUAL ANALYSIS FOR REFRACTIVE INDEX FIT")
print("="*60)
print("Point | Obs (fringe) | Pred (fringe) | Residual ")
print("-" * 45)
for i in range(len(N_f)):
    print(f"{i+1:5d} | {N_f[i]:9.6f} | {y_predicted[i]:10.6f} | {y_res[i]:12.6f}")
print(f"\nResiduals Statistics:")
print(f"  Mean: {np.mean(y_res):.6f}")
print(f"  Std Dev: {np.std(y_res):.6f}")
print(f"\nChi-Squared Analysis:")
print(f"  Chi-squared (χ²): {chi_squared:.6f}")
print(f"  Degrees of freedom (ν): {degrees_of_freedom}")
print(f"  Reduced chi-squared (χᵣ²): {reduced_chi_squared:.6f}")
#residuals fit
plt.errorbar(delta_theta_rads, y_res, yerr=1, xerr=0.1*math.pi/180, fmt='o', ecolor='r', capthick=2, capsize=5, markersize=8, label='Residuals', alpha=0.7)
plt.axhline(0, color='black', linestyle='--')
plt.xlabel('Delta Theta (radians)')
plt.ylabel('Residuals (fringes)')
plt.title('Residuals of Refractive Index Fit')
plt.legend()
plt.grid()
plt.show()


#plot
#with error bars of N+-1, theat +- 0.1
plt.errorbar(delta_theta_rads, N_f, yerr=1, xerr=0.1*math.pi/180, fmt='o', ecolor='r', capthick=2, capsize=5, markersize=8, label='Data points', alpha=0.7)
x_fit = np.linspace(min(delta_theta_rads), max(delta_theta_rads), 100)
y_fit = model_function(x_fit, *popt)
plt.plot(x_fit, y_fit, color='red', label='Fitted Curve')
plt.xlabel('Delta Theta (radians)')
plt.ylabel('Number of Fringes')
plt.title('Refractive Index Fit')
plt.legend()
plt.grid()
plt.show()

