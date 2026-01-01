import numpy as np
import statistics
import math
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit


#exposure times
#used 2,5,6,7,10
exp_times=np.array([3.77349854e-002, 3.59344482e-002, 3.59344482e-002, 3.59344482e-002, 6.45294189e-002])
dt=np.array([0.00000001e-002, 0.00000001e-002, 0.00000001e-002, 0.00000001e-002, 0.00000001e-002]) #error in time measure

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

#velocities about a bend
dbendbefore_px=np.array([133, 51, 47, 37, 50]) 
dbendafter_px=np.array([142, 72, 45, 43, 62])

dbendbefore_m=dbendbefore_px * pix
dbendafter_m=dbendafter_px * pix
dbendb_err=deltax(dbendbefore_px)
dbenda_err=deltax(dbendafter_px)

v_bend_before = dbendbefore_m / exp_times
v_bend_after = dbendafter_m / exp_times
vbb_err= error_v(dbendb_err, dbendbefore_m, dt, exp_times)
vba_err= error_v(dbenda_err, dbendafter_m, dt, exp_times)

#errors
print("Velocities before bend, L (mm/s): ", v_bend_before[0:3]*1e3)
print("Errors before bend L: ", vbb_err[0:3]*1e3)
print("Velocities after bend L (mm/s): ", v_bend_after*1e3)
print("Errors after bendL : ", vba_err[0:3]*1e3)

print("Velocities before bend, R (mm/s): ", v_bend_before[3:5]*1e3)
print("Errors before bend R: ", vbb_err[3:5]*1e3)
print("Velocities after bend R (mm/s): ", v_bend_after[3:5]*1e3)
print("Errors after bend R : ", vba_err[3:5]*1e3)

