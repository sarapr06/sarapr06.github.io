import math
import matplotlib
import matplotlib.pyplot as plt 
import numpy as np
from scipy import stats


R = [99.17, 2699.9, 26890, 101460]
R_err = [0.26, 10.40, 103.78, 252.92]

V2 = [6.494,6.5, 6.5,6.5]
V_err2 = [0.00525, 0.00525, 0.00525, 0.00525]
I2 = [0.0648e-3,0.0018e-3, -0.00001e-3, -0.00003e-3]	
I_err2 = [0.00513e-3, 0.00500e-3, 0.000500e-3, 0.000500e-3]

V1 = [6.496,6.5, 6.5,6.5]
V_err1 = [0.00525, 0.00525, 0.00525, 0.00525]
I1 = [0.0650e-3, 0.002e-3, -0.0003e-3, -0.0003e-3]
I_err1 = [0.00513e-3, 0.00500e-3, 0.000500e-3, 0.000500e-3]

R_a_values = []
R_a_err_vals=[]
R_v_values = []
R_v_err_vals=[]


def cct1(V, I, R, V_err, I_err, R_err, R_amm_vals, R_amm_err):
    for i in range(len(R)):
        R_amm = (V[i]/I[i]) - R[i]
        R_total_err = (((V[i]/I[i])**2)*((V_err[i]/V[i])**2 + (I_err[i]/I[i])**2) + (R_err[i])**2)**0.5
        print("R_amm =", R_amm, "±", R_total_err)
        R_amm_vals.append(R_amm)
        R_amm_err.append(R_total_err)
    R_av=sum(R_amm_vals)/len(R_amm_vals)
    R_av_err=sum(R_amm_err)/len(R_amm_err)
    print("average resistance:", str(R_av))
    print("average uncert:" , str(R_av_err)) 
    return R_av, R_av_err

def cct2(V, I, R, V_err, I_err, R_err, R_v_values, R_err_vals):
    #Step 1:
    for i in range(len(R)):
        R_v=R[i]*V[i]/(R[i]*I[i]-V[i])
        R_v_err = R_v*((R_err[i]/R[i])**2+(V_err[i]/V[i])**2+(1/(R[i]*I[i]-V[i]))**2*(((R[i]*I[i])**2)*((R_err[i]/R[i])**2+(I_err[i]/I[i])**2)+(V_err[i])**2))**0.5
        print("R_voltmeter =", R_v, "±", R_v_err)
        R_v_values.append(R_v) 
        R_err_vals.append(R_v_err)
    R_av=sum(R_v_values)/len(R_v_values)
    R_av_err=sum(R_err_vals)/len(R_err_vals)
    print("average resistance:", str(R_av))
    print("average uncert:" , str(R_av_err))
    return R_av, R_av_err


def plot_function_lin_reg(I1, V1, I_err1, V_err1, num, L):
    #plotting
    slope, intercept, r_value, p_value, std_err = stats.linregress(I1, V1)
    r_squared = r_value**2
    n = len(I1)# Calculate standard errors for slope and intercept
    # standard error calculations
    x_mean = np.mean(I1)
    y_mean = np.mean(V1)
    ss_xx = np.sum((np.array(I1) - x_mean)**2)
    ss_yy = np.sum((np.array(V1) - y_mean)**2)
    ss_xy = np.sum((np.array(I1) - x_mean) * (np.array(V1) - y_mean))
    # error of the estimate
    s_yx = np.sqrt((ss_yy - slope * ss_xy) / (n - 2))

    # error of slope
    slope_error = s_yx / np.sqrt(ss_xx)
    L.append(slope)
    L.append(slope_error)
    
    intercept_error = s_yx * np.sqrt(1/n + x_mean**2/ss_xx)

    plt.figure(figsize=(10,6))
    plt.errorbar(I1,V1,xerr=I_err1, yerr=V_err1, fmt='o', capsize=5, capthick=2, markersize=8, linewidth=2, label='Data points')
    
    x_fit = np.linspace(min(I1), max(I1), 100)
    y_fit = slope * x_fit + intercept
    plt.plot(x_fit, y_fit, 'r-', linewidth=2, label=f'Best fit line')
    plt.xlabel('Current (A)', fontsize=12)
    plt.ylabel('Voltage (V)', fontsize=12)
    plt.title(f"Voltage vs Current for Circuit {num} with Error Bars", fontsize=14)
    plt.grid(True, alpha=0.3)
    
    textstr = f'''Linear Regression Results:
    Slope = {slope:.2e} ± {slope_error:.2e} V/A
    Y-intercept = {intercept:.4f} ± {intercept_error:.4f} V
    R² = {r_squared:.4f}'''
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    print("\n" + "="*50)
    print(f"LINEAR REGRESSION RESULTS FOR CIRCUIT {num}")
    print("="*50)
    print(f"Slope: {slope:.6e} ± {slope_error:.6e} V/A")
    print(f"Y-intercept: {intercept:.6f} ± {intercept_error:.6f} V")
    print(f"R-squared: {r_squared:.6f}")
    print(f"Correlation coefficient: {r_value:.6f}")
    print("="*50)

def residuals_plot(I1, V1, I_err1, V_err1, num):
    # Calculate predicted values and residuals
    slope, intercept, r_value, p_value, std_err = stats.linregress(I1, V1)
    y_predicted = slope * np.array(I1) + intercept  # Predicted V values
    
    V_residuals = np.array(V1) - y_predicted  

    plt.figure(figsize=(10, 6))

    plt.errorbar(y_predicted, V_residuals, yerr=V_err1, fmt='o', capsize=5, capthick=2, 
                markersize=8, linewidth=2, label='Voltage Residuals', color='red')

    plt.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.7, label='Zero line')

    # Labels 
    plt.xlabel('Predicted Voltage (V)', fontsize=12)
    plt.ylabel('Voltage Residuals (Observed - Predicted) (V)', fontsize=12)
    plt.title(f"Voltage Residuals Plot for Circuit {num}", fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()
    # Calculate reduced chi-squared
    chi_squared = np.sum((V_residuals**2) / (np.array(V_err1)**2))
    degrees_of_freedom = len(V1) - 2  # n - m (4 data points - 2 parameters)
    reduced_chi_squared = chi_squared / degrees_of_freedom
    # Print voltage residual analysis only
    print("\n" + "="*60)
    print("VOLTAGE RESIDUAL ANALYSIS")
    print("="*60)
    print("Point | Obs V (V) | Pred V (V) | V Residual (V)")
    print("-" * 45)
    for i in range(len(I1)):
        print(f"{i+1:5d} | {V1[i]:9.6f} | {y_predicted[i]:10.6f} | {V_residuals[i]:12.6f}")

    print(f"\nVoltage Residuals Statistics:")
    print(f"  Mean: {np.mean(V_residuals):.6f} V")
    print(f"  Std Dev: {np.std(V_residuals):.6f} V")
    print(f"\nChi-Squared Analysis:")
    print(f"  Chi-squared (χ²): {chi_squared:.6f}")
    print(f"  Degrees of freedom (ν): {degrees_of_freedom}")
    print(f"  Reduced chi-squared (χᵣ²): {reduced_chi_squared:.6f}")
    print("="*60)


def calculate_power_source_resistanceR1(m1, R_v, m1_err, R_v_err):
    R1 = (m1 * R_v) / (m1 + R_v)
    
    # ΔR1 = sqrt((Δm1/m1)² + (ΔR_v/R_v)² + ((Δm1)² + (ΔR_v)²)/(m1 + R_v)²)
    
    term1 = (m1_err / m1)**2
    term2 = (R_v_err / R_v)**2  
    term3 = (m1_err**2 + R_v_err**2) / ((m1 + R_v)**2)
    
    R1_err = R1*np.sqrt(term1 + term2 + term3)
    print("R1 =", R1, "±", R1_err)
def calculate_power_source_resistanceR2(m2, R_a, m2_err, R_a_err):
    
    R2 = m2 + R_a
    
    R2_err = np.sqrt(m2_err**2 + R_a_err**2)
    print("R2 =", R2, "±", R2_err)

R_a, R_a_err=cct1(V1, I1, R, V_err1, I_err1, R_err, R_a_values, R_a_err_vals)
R_v, R_v_err=cct2(V2, I2, R, V_err2, I_err2, R_err, R_v_values, R_v_err_vals)
L1=[] #stores slope, error of slope respectively for cct1
L2=[] #stores slope, error of slope respectively for cct2
plot_function_lin_reg(I1, V1, I_err1, V_err1, 1, L1)
plot_function_lin_reg(I2, V2, I_err2, V_err2, 2, L2)
residuals_plot(I1, V1, I_err1, V_err1, 1)
residuals_plot(I2, V2, I_err2, V_err2, 2)
calculate_power_source_resistanceR1(L1[0], R_v, L1[1], R_v_err)
calculate_power_source_resistanceR2(L2[0], R_a, L2[1], R_a_err)
