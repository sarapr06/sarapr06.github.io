import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

SPECTROMETER_RESOLUTION = 3  # nm

# Part 1a: calculating energies from wavelengths
def calculate_energy(w):
    energy=[]
    for wavelengths in w:
        wavelengths_m = wavelengths * 1e-9
        h = 6.626070040e-34
        c = 3e8
        eV= 1.60218e-19
        energies = (h * c) / (wavelengths_m*eV)
        energy.append(energies)
    return np.array(energy)

def calculate_wavelength(e):
    wavelength=[]
    for energies in e:
        h = 6.626070040e-34
        c = 3e8
        eV= 1.60218e-19
        wavelengths_m = (h * c) / (energies*eV)
        wavelengths = wavelengths_m * 1e9
        wavelength.append(wavelengths)
    return np.array(wavelength)


#part 1b: calibrating spectrometer for true vs. measured wave-lengths
def calibrate_spectrometer(true, measured):
    slope, intercept, r_value, p_value, std_err =stats.linregress(measured, true)
    return slope, intercept

def get_errors_calibration(measured, expected):
    coefficients, covariance = np.polyfit(measured, expected, 1, cov=True)
    slope, intercept = coefficients
    slope_error = np.sqrt(covariance[0, 0])
    intercept_error = np.sqrt(covariance[1, 1])
    x_mean = np.mean(measured)
    y_mean = np.mean(expected)
    ss_xx = np.sum((measured - x_mean)**2)
    ss_yy = np.sum((measured - y_mean)**2)
    ss_xy = np.sum((measured - x_mean) * (expected - y_mean))
    
    s_yx = np.sqrt((ss_yy - slope * ss_xy) / (len(measured) - 2))
    slope_error = s_yx / np.sqrt(ss_xx)
    intercept_error = s_yx * np.sqrt(1/len(measured) + x_mean**2/ss_xx)

    print(f"Slope: {slope:.6f} ± {slope_error:.6f}")
    print(f"Intercept: {intercept:.6f} ± {intercept_error:.6f}")
    return slope_error, intercept_error

def true_value_with_error(measured, slope, slope_error, intercept, intercept_error, resolution=3):
    true_values = slope * measured + intercept
    uncertainties = np.sqrt((measured * slope_error)**2 + 
                           intercept_error**2 + 
                           (slope * resolution)**2)
    return true_values, uncertainties

# ENERGY calibration functions  
def true_energy_with_error(measured_energy, energy_slope, energy_slope_error, energy_intercept, energy_intercept_error, energy_uncertainty=0.03):
    true_energies = energy_slope * measured_energy + energy_intercept
    uncertainties = np.sqrt((measured_energy * energy_slope_error)**2 + 
                           energy_intercept_error**2 + 
                           (energy_slope * energy_uncertainty)**2)
    
    return true_energies, uncertainties

# PLOTTING FUNCTIONS WITH ERROR BARS
def plots_with_errorbars(x_in, y_in, slope, intercept, x_errors=None, y_errors=None, title_suffix=""):
    plt.figure(figsize=(10, 6))
    if x_errors is None:
        x_errors = np.full_like(x_in, SPECTROMETER_RESOLUTION)
    if y_errors is None:
        y_errors = np.full_like(y_in, SPECTROMETER_RESOLUTION)
    plt.errorbar(x_in, y_in, xerr=x_errors, yerr=y_errors, 
                 fmt='o', capsize=5, capthick=2, markersize=8,
                 label=f'Data Points ±{SPECTROMETER_RESOLUTION} nm', color='blue', alpha=0.7)
    
    x = np.linspace(min(x_in) - 50, max(x_in) + 50, 100) 
    y = slope * x + intercept
    plt.plot(x, y, color='red', linewidth=2, label='Calibration Line')
    plt.xlabel('Measured Wavelength (nm)')
    plt.ylabel('True Wavelength (nm)')
    plt.title(f'Spectrometer Calibration {title_suffix}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

def energy_plots_with_errorbars(x_in, y_in, slope, intercept):
    plt.figure(figsize=(10, 6))
    energy_uncertainty=np.array([0.0185059,  0.0191744,  0.01607251, 0.01058204, 0.00950004, 0.00926188])
    x_errors = np.full_like(x_in, energy_uncertainty)
    y_errors = np.full_like(y_in, energy_uncertainty)
    plt.errorbar(x_in, y_in, xerr=x_errors, yerr=y_errors, 
                 fmt='s', capsize=5, capthick=2, markersize=8,
                 label=f'Data Points with Error', color='green', alpha=0.7)
    x = np.linspace(min(x_in) - 0.5, max(x_in) + 0.5, 100) 
    y = slope * x + intercept
    plt.plot(x, y, color='red', linewidth=2, label='Calibration Line')
    
    plt.xlabel('Measured Energy (eV)')
    plt.ylabel('True Energy (eV)')
    plt.title('Energy Calibration with Error Bars')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

def get_residualsplot_with_errorbars(measured, actual, slope, intercept, uncertainties, type):
    y_predicted = slope * np.array(measured) + intercept
    y_residuals = np.array(actual) - y_predicted
    if uncertainties is None:
        uncertainties = np.full_like(measured, SPECTROMETER_RESOLUTION)
    
    plt.figure(figsize=(10, 6))
    plt.errorbar(y_predicted, y_residuals, yerr=uncertainties, 
                 fmt='o', capsize=5, capthick=2, markersize=8, linewidth=2,
                 label=f'Residuals', color='red')
    
    plt.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.7, label='Zero line')
    if uncertainties is None:
        # Add ±2.5 nm bands
        plt.axhline(y=SPECTROMETER_RESOLUTION, color='gray', linestyle=':', alpha=0.5)
        plt.axhline(y=-SPECTROMETER_RESOLUTION, color='gray', linestyle=':', alpha=0.5)

    plt.xlabel(f"Predicted {type[0]} ({type[1]})", fontsize=12)
    plt.ylabel(f"Residuals (Observed - Predicted) ({type[1]})", fontsize=12)
    plt.title(f"{type[0]} Residuals Plot with Error Bars", fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    return y_residuals

def get_residualsplot(measured, actual, slope, intercept):
    y_predicted = slope * np.array(measured) + intercept
    y_residuals = np.array(actual) - y_predicted

    plt.figure(figsize=(10, 6))
    plt.errorbar(y_predicted, y_residuals, fmt='o', capsize=5, capthick=2, 
                markersize=8, linewidth=2, label='Wavelength Residuals', color='red')
    plt.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.7, label='Zero line')

    # Labels 
    plt.xlabel('Predicted Energies (eV)', fontsize=12)
    plt.ylabel('Energy Residuals (Observed - Predicted) (eV)', fontsize=12)
    plt.title("Energies Residuals Plot", fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

def chi_squared_analysis(measured, actual, slope, intercept, error):
    predicted = slope * measured + intercept
    residuals = actual - predicted
    chi_sq = np.sum((residuals/error)**2)
    reduced_chi_sq = chi_sq / (len(measured)-2)
    
    print("\n" + "="*60)
    print("RESIDUAL ANALYSIS")
    print("="*60)
    print("Point | Actual | Predicted | Residual")
    print("-" * 45)
    for i in range(len(measured)):
        print(f"{i+1:5d} | {actual[i]:9.6f} | {predicted[i]:10.6f} | {residuals[i]:12.6f}")

    print(f" \n Residuals Statistics:")
    print(f"  Mean: {np.mean(residuals):.6f}")
    print(f"  Std Dev: {np.std(residuals):.6f}")
    print(f" \n Chi-Squared Analysis:")
    print(f"  Chi-squared (χ²): {chi_sq:.6f}")
    print(f"  Degrees of freedom (ν): {len(measured)-2}")
    print(f"  Reduced chi-squared (χᵣ²): {reduced_chi_sq:.6f}")
    print("="*60)

def plots(x_in,y_in, slope, intercept):
    plt.scatter(x_in, y_in, color='blue', label='Data Points')
    x = np.linspace(min(x_in), max(x_in), 100) 
    y = slope*x+intercept
    plt.plot(x, y, color='red', label='Calibration Line')
    plt.xlabel('Measured Energies (eV)')
    plt.ylabel('True Energies (eV)')
    plt.title('Spectrometer Calibration')
    plt.legend()
    plt.show()

def errors_with_calib(measured, slope, slope_err, intercept_err, resolution=2.5):
    errors=[]
    for i in measured:
        error = np.sqrt((i*slope_err)**2 + intercept_err**2 + (slope*resolution)**2)
        errors.append(error)
    return np.array(errors)

def transition_quantnum(transitions):
    print("Quantum number changes:")
    print("Transition | Δn | Δl | ΔJ")
    print("-" * 30)
    for i, state in enumerate(transitions):
        delta_n = state[0] - state[3]
        delta_l = state[1] - state[4]
        delta_J = state[2] - state[5]
        print(f"{i+1:2} | {delta_n:2} | {delta_l:2} | {delta_J:2}")


#data
wavelengths_acc = np.array([404.6565, 407.7837, 435.8328, 546.0735, 576.9598, 579.0663])
wavelengths_exp = np.array([409.4, 402.2, 439.3, 541.4, 571.4, 578.7])
energies_acc = calculate_energy(wavelengths_acc)
energies_exp = calculate_energy(wavelengths_exp)

transitions = [ # (n, l, J) for upper and lower states
    (2, 1, 1, 1, 0, 0),  # 1s2p(1) → 1s²(0)
    (3, 0, 1, 2, 1, 2),  # 1s3s(1) → 1s2p(2)
    (3, 1, 1, 2, 0, 1),  # 1s3p(1) → 1s2s(1)
    (3, 2, 3, 2, 1, 2),  # 1s3d(3) → 1s2p(2)
    (3, 2, 2, 2, 1, 1),  # 1s3d(2) → 1s2p(1)
    (3, 1, 1, 2, 0, 0),  # 1s3p(1) → 1s2s(0)
    (4, 2, 1, 2, 1, 2)   # 1s4d(1) → 1s2p(2)
]