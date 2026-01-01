import numpy as np
import statistics
import math
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit


#exposure times
straight_0001 = 0.134124756
straight_0005=4.81567383e-002
straight_0006 = 6.45294189e-002
straight_0007=6.45294189e-002
straight_extra = 2.31628418e-002
exp_time=np.array([straight_0001, straight_0005, straight_0006, straight_0007, straight_extra])

pix=44.913e-6/218 #micrometer per pixel
#channel widths in pixels
s1_w=339 #pixels
s_5=336
s_6=337
s_7=337
s_extra=334
#reading error st dev
stdev=statistics.stdev([s1_w, s_5, s_6, s_7, s_extra])

deltaP=pix*math.sqrt((0.001/44.913)**2+(stdev/218)**2)
def deltax(length_px):
    length_m= length_px * pix #streak lengths in micrometers
    return length_m * np.sqrt((deltaP/pix)**2+(stdev/length_px)**2)
def error_v(deltax, x, deltat, t):
    v = x / t
    return v * np.sqrt((deltax/x)**2 + (deltat/t)**2)

#different heights
#streak lengths at same heights from channel width
#choose for distance from bottom to be 133px
d133_px=np.array([499, 150, 192, 169])
d133_m=d133_px * pix
d133_err=deltax(d133_px)
t133=exp_time[0:4] #exposure times for these lengths
v133=d133_m / t133

#errors
dt= np.array([0.000000001, 0.00000001e-002, 0.00000001e-002, 0.00000001e-002]) #error in time measure
error133 = error_v(d133_err, d133_m, dt, t133)

#heights from chip
from_chip=np.array([9,6,4.5,3.2,15])
heights=from_chip[0:4]

print("Velocities at 133px from bottom (mm/s): ", v133*1e3)
print("Errors at 133px from bottom: ", error133*1e3)

#fit to linear
def model_function(x, a, b):
    return a * x + b
popt, pcov = curve_fit(model_function, heights, v133 * 1e3)
#r squared value
rsq=1 - (np.sum((v133*1e3 - model_function(heights, *popt))**2) / np.sum((v133*1e3 - np.mean(v133*1e3))**2))
print("R squared value: ", rsq)

print("n: ", popt, ", Covariance: ", pcov)
#plotting velocities at 133px from bottom
plt.errorbar(heights, v133*1e3, yerr=error133*1e3, xerr = 0.1, fmt='o', ecolor='r', capthick=2, capsize=5, markersize=8, label=f'Data points', alpha=0.7)
plt.xlabel('Height of the syringe from chip interface (cm)')
plt.ylabel('Velocity (mm/s)')
plt.title('Velocities of the Middle of the Straight Channel for 4 Different Heights')
#linear fit
x_fit = np.linspace(min(heights), max(heights), 100)
y_fit = model_function(x_fit, *popt)
plt.plot(x_fit, y_fit, 'b-', label='Linear fit')
plt.legend()
plt.grid()
plt.show()