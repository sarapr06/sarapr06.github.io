import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import stats


P=np.array([42.3, 79.3, 44.6, 75.3]) #psig
Psia=P+14.39 #psia
print(Psia)
T=np.array([40,40.40,59.2,59.3])
R_air=287 #J/kgK
rho=Psia*6.89476e3/(R_air * (T + 273.15)) #kg/m^3
print("Density of air at", P, "psig and", T, "C is", rho, "kg/m^3")
n2=2000
n1=4200
rho1=1.293
P1= 0.001 #hp
P1_W=P1*745.7 #W
P2=P1_W* (n2/n1)**3 * rho/rho1
print("Power required to drive the air at", n2, "rpm is", P2, "W")
deltaT=np.array([99.3-20.90,79.9-10.4,119.8-11.20,105.1-4.6])
print("Temperature increase (K):", deltaT)
work=P2*deltaT
print("Work done on air (J):", work)
cv=np.array([92.8, 56.1, 98.2, 72.6])
m_left=np.array([0.038, 0.062, 0.035, 0.052])
dTbydt=P2/(m_left*cv*1e3)
print("Rate of temperature increase (K/s):", dTbydt)
Q_added=np.array([66.5,40.6,100,108.6])
P_heater=Q_added*1e-3/deltaT
print("Power supplied to heater (W):", P_heater)
WproptoQh=work/(Q_added*1e3) * 100
print("Work done as percentage of heat added (%):", WproptoQh)

l_inch=11.25
l_m=l_inch*0.0254
print(l_m)
k=0.2
dT=np.array([39.9-25,14.1,28.7,19])
r2_inch=8
r2_m=r2_inch*0.0254
r1_inch=r2_inch-3/8
r1_m=r1_inch*0.0254
#ratio=natural log of (r2/r1)
ratio=math.log(r2_m/r1_m)
Q_dot=2*k*math.pi*l_m/ratio * dT
print(Q_dot)
dt=np.array([300.4 - 171, 360.6 -129, 391.6 - 166.9,504.2 - 189.6])
Q=Q_dot * dt
print(Q)
Q_lost=np.array([17.9e3, 43.3e3, 52.8e3, 97.1e3])
Q_p=Q_lost-Q
print("Net heat added to air (J):", Q_p)