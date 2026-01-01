import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import stats
from scipy.optimize import curve_fit

def fit_fringe(N, deltax):
    slope, intercept, r_value, p_value, std_err =stats.linregress(N, deltax)
    return slope, intercept

def plots_with_errorbars(x_in, y_in, slope, intercept, x_er, y_er, title_suffix=""):
    plt.figure(figsize=(10, 6))
    
    plt.errorbar(x_in, y_in, xerr=x_er, yerr=y_er, 
                 fmt='o', capsize=5, capthick=2, markersize=8,
                 label=f'Data Points ', color='blue', alpha=0.7)
    
    x = np.linspace(min(x_in) - 10, max(x_in) + 10, 100) 
    y = slope * x + intercept
    plt.plot(x, y, color='red', linewidth=2, label='Line of Best Fit')
    plt.xlabel('Number of Fringes (N)')
    plt.ylabel('Distance Moved (μm)')
    plt.title(f'Number of Fringes per Distance Moved {title_suffix}')
    '''
    #if i want to add a box with slope value
    textstr = f'Slope = {slope:1e} μm/fringe'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    plt.text(0.05, 0.95, textstr, transform=plt.gca().transAxes, fontsize=12,
             verticalalignment='top', bbox=props)
    '''
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

def get_errors(delta_x, N):
    # Perform the linear fit and extract covariance
    coeffs, cov = np.polyfit(N, delta_x, 1, cov=True)
    slope, intercept = coeffs
    slope_err = np.sqrt(cov[0, 0])
    intercept_err = np.sqrt(cov[1, 1])

    print(f"Slope: {slope:.6e} ± {slope_err:.6e}")
    print(f"Intercept: {intercept:.6e} ± {intercept_err:.6e}")
    return slope_err, intercept_err


def get_residualsplot_with_errorbars(N, delta_x, slope, intercept, uncertainties):
    y_predicted = slope * N + intercept
    y_residuals =  delta_x - y_predicted
    plt.figure(figsize=(10, 6))
    plt.errorbar(y_predicted, y_residuals, xerr=uncertainties, 
                 fmt='o', capsize=5, capthick=2, markersize=8, linewidth=2,
                 label=f'Residuals', color='red')
    
    plt.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.7, label='Zero line')
    plt.xlabel("Predicted (μm)", fontsize=12)
    plt.ylabel("Residuals (Observed - Predicted) (μm)", fontsize=12)
    plt.title(f"Residuals Plot with Error Bars", fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()
    return y_residuals

def residual_analysis_chi_sq(N, delta_x, slope, intercept, uncert):
    y_predicted = slope * np.array(N) + intercept  # Predicted V values
    y_res = delta_x-y_predicted  # Residuals
    chi_squared = np.sum((y_res**2) / (np.array(uncert)**2))
    degrees_of_freedom = len(delta_x) - 2  # n - m (4 data points - 2 parameters)
    reduced_chi_squared = chi_squared / degrees_of_freedom
    print("\n" + "="*60)
    print("RESIDUAL ANALYSIS")
    print("="*60)
    print("Point | Obs (fringe) | Pred (fringe) | Residual ")
    print("-" * 45)
    for i in range(len(delta_x)):
        print(f"{i+1:5d} | {1e6*delta_x[i]:9.6f}micrometer | {1e6*y_predicted[i]:10.6f}micrometer | {1e6*y_res[i]:12.6f}micrometer")

    print(f"\nResiduals Statistics:")
    print(f"  Mean: {1e6*np.mean(y_res):.6f} micrometers")
    print(f"  Std Dev: {1e6*np.std(y_res):.6f} micrometers")
    print(f"\nChi-Squared Analysis:")
    print(f"  Chi-squared (χ²): {chi_squared:.6f}")
    print(f"  Degrees of freedom (ν): {degrees_of_freedom}")
    print(f"  Reduced chi-squared (χᵣ²): {reduced_chi_squared:.6f}")
    print("="*60)


#Part 1: linear fit to get wavelength
N=np.array([41,20,36,40, 41, 37, 36, 41, 21, 35])
deltax_deg=np.array([15,5,11,16, 15, 11, 11, 16, 5, 12])

delta_x= 1e-6*deltax_deg
delta_x_err = (0.1/deltax_deg)*delta_x
N_err=1

slope,int=fit_fringe(N, delta_x)
#print("Slope: ", slope, ", Int: ", int)
plots_with_errorbars(N, delta_x, slope, int, N_err, delta_x_err)
residuals = get_residualsplot_with_errorbars(N, delta_x, slope, int, delta_x_err)
#print("Wavelength: ", slope)
#print(get_errors(delta_x, N))
#residual_analysis_chi_sq(N, delta_x, slope, int, delta_x_err)


#Part 2: fit to get refractive index
lambda_g = slope
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

#Part 3: Aluminum
N=np.array([30,30,30,15,27])
ZPD=np.array([28.8,27.4,27.4,29.8,24.3])
L0=np.array([80.69,80.76,81.18,80.03,80.49]) * 1e-3
T_f=np.array([31.2, 29.3,30.1,30.6,25.4])
deltaT=T_f - ZPD
Lf=np.array([80.99,80.82,82.54,81.22,80.75]) * 1e-3

dT_n=N*lambda_g/(2*L0*23e-6)
dT=np.array([3.9, 4.1, 3.8, 2.3, 3.8])

def model_function(dT, alpha):
    L=L0
    wavelength=lambda_g
    return 2*L/wavelength * alpha * dT
popt, pcov = curve_fit(model_function, dT, N)
print("n: ", popt, ", Covariance: ", pcov)