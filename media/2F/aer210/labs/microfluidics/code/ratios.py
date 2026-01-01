import numpy as np
import statistics
import math
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

#channel widths in pixels
s1_w=339 #pixels
s_5=336
s_6=337
s_7=337
s_extra=334
#reading error st dev
stdev=statistics.stdev([s1_w, s_5, s_6, s_7, s_extra])
print("standard deviation:", stdev)

w=np.array([335, 632, 351, 972]) #channel widths in pixels (gradual, then sharp)
exp_time = np.array([6.45294189e-002, 6.45294189e-002, 4.36706543e-002, 4.36706543e-002])
dt=np.array([0.00000001e-002, 0.00000001e-002, 0.00000001e-002, 0.00000001e-002]) #error in time measure
px=np.array([74, 35,114,41]) # streaks before and after

#conversion
pix=44.913e-6/218 #micrometer per pixel
m=px * pix #streak lengths in micrometers

deltaP=pix*math.sqrt((0.001/44.913)**2+(stdev/218)**2)
def deltax(length_px):
    length_m= length_px * pix #streak lengths in micrometers
    return length_m * np.sqrt((deltaP/pix)**2+(stdev/length_px)**2)
def error_v(deltax, x, deltat, t):
    v = x / t
    return v * np.sqrt((deltax/x)**2 + (deltat/t)**2)

dm=deltax(px)
v= m/exp_time 
verr= error_v(dm, m, dt, exp_time)
print("Velocities at different heights (mm/s): ", v*1e3)
print("Errors at different heights: ", verr*1e3)
ratios = np.array([v[1]/v[0], v[3]/v[2]])
print("Velocity ratios (after/before): ", ratios)
error_v1v0=ratios[0] * np.sqrt((verr[0]/v[0])**2 + (verr[1]/v[1])**2)
error_v3v2=ratios[1] * np.sqrt((verr[2]/v[2])**2 + (verr[3]/v[3])**2)
print("Errors in velocity ratios: ", np.array([error_v1v0, error_v3v2]))


w_m=w * pix
w_error = deltax(w)
print("Channel widths (micrometers): ", w_m*1e6)
print("Channel width errors (micrometers): ", w_error*1e6)
ratios_w = np.array([w_m[0]/w_m[1], w_m[2]/w_m[3]])
error_w1w0=ratios_w[0] * np.sqrt((w_error/w_m[0])**2 + (w_error/w_m[1])**2)
error_w3w2=ratios_w[1] * np.sqrt((w_error/w_m[2])**2 + (w_error/w_m[3])**2)
print("Width ratios (before/after): ", ratios_w)
print("Errors in width ratios: ", np.array([error_w1w0, error_w3w2]))
