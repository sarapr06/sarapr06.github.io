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


#channel widths in pixels
s1_w=339 #pixels
s_5=336
s_6=337
s_7=337
s_extra=334
#reading error st dev
stdev=statistics.stdev([s1_w, s_5, s_6, s_7, s_extra])
print("standard deviation:", stdev)

#conversion
pix=44.913e-6/218 #micrometer per pixel
    
deltaP=pix*math.sqrt((0.001/44.913)**2+(stdev/218)**2)
def deltax(length_px):
    length_m= length_px * pix #streak lengths in micrometers
    return length_m * np.sqrt((deltaP/pix)**2+(stdev/length_px)**2)
def error_v(deltax, x, deltat, t):
    v = x / t
    return v * np.sqrt((deltax/x)**2 + (deltat/t)**2)

#plotting v profile
distbot_px = np.array([299, 329, 287, 280, 42, 259, 36, 310, 32, 40, 80, 101, 183, 220, 220]) #distance from bottom of channel in px
lengths_px=np.array([75, 33, 119, 110, 29, 151, 47, 76, 47, 66, 86, 95, 157, 161, 163]) #streak lengths in px

lengths_m=lengths_px * pix #streak lengths in micrometers
distbox_m=distbot_px * pix #distance from bottom of channel in micrometers
length_err=deltax(lengths_px)
dist_err=deltax(distbot_px)

t_prof = straight_0001  #exposure time for the pic
v_profile = lengths_px*pix/t_prof #velocity profile in micrometers per second
dt=0.000000001
error_profile = error_v(length_err, lengths_m, dt, t_prof)

#fit to parabola
def model_function(x, a, b, c):
    return a * x**2 + b * x + c
popt, pcov = curve_fit(model_function, distbox_m, v_profile * 1e3)

#rsquared value
rsq=1 - (np.sum((v_profile*1e3 - model_function(distbox_m, *popt))**2) / np.sum((v_profile*1e3 - np.mean(v_profile*1e3))**2))
print("R squared value: ", rsq)

#velocity profile w error bars
print("n: ", popt, ", Covariance: ", pcov)
plt.errorbar(distbox_m, v_profile * 1e3, yerr=error_profile * 1e3, xerr = dist_err, fmt='o', ecolor='r', capthick=2, capsize=5, markersize=8, label=f'Data points', alpha=0.7)
plt.xlabel('Distance from bottom of channel (µm)')
plt.ylabel('Velocity (mm/s)')
plt.title('Velocity Profile Straight Channel with Parabolic Fit')
#plotting the fit
x_fit = np.linspace(min(distbox_m), max(distbox_m), 100)
y_fit = model_function(x_fit, *popt)
#equation of curve with error:
plt.plot(x_fit, y_fit, color='green', linewidth=2, label='Parabolic Fit')
plt.legend()
plt.grid()
plt.show()