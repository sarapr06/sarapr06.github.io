import numpy as np

def levin_solver(t_data, a, b, V0=1.0, N=40):
    """
    Solve dV/dt = a*V*log(b/V) using a Levin-type Chebyshev collocation method.
    Returns V(t) interpolated to match t_data.
    """
    # Chebyshev nodes and differentiation matrix
    T = t_data[-1]
    k = np.arange(0, N+1)
    x = np.cos(np.pi * k / N)
    t_nodes = 0.5 * T * (1 - x)

    # Differentiation matrix
    c = np.ones(N+1)
    c[0] = c[-1] = 2
    c = c * ((-1) ** k)
    X = np.tile(x, (N+1, 1))
    dX = X - X.T + np.eye(N+1)
    D = (c[:, None] / c[None, :]) / (dX + np.eye(N+1))
    D -= np.diag(np.sum(D, axis=1))
    D = (2 / T) * D  # rescale to [0, T]

    # Newton iteration to solve D@V = a*V*log(b/V)
    V = np.linspace(V0, b, N+1)
    for i in range(40):
        V = np.clip(V, 1e-6, 0.999*b)
        F = D @ V - a * V * np.log(b / V)
        if not np.all(np.isfinite(F)) or np.linalg.norm(F) < 1e-8:
            break
        J = D - a * np.diag(np.log(b / V) - 1)
        try:
            delta = np.linalg.solve(J, -F)
        except np.linalg.LinAlgError:
            # stabilize singular Jacobian
            delta = np.linalg.solve(J + 1e-6*np.eye(J.shape[0]), -F)
        V += 0.3 * delta

    V[0] = V0

    # Interpolate solution to experimental time points
    V_interp = np.interp(t_data, t_nodes, V)
    return V_interp
from scipy.optimize import curve_fit

# Replace with your own data

time_data_1 = np.array([1, 2, 44, 56])         # your experimental time points
tumor_volume_data_1 = np.array([16751.0, 6799.0, 5.0, 3597.0]) # your measured tumor sizes

t2=np.array([0, 3, 21, 37, 40, 47]) #weeks 
tum2= np.array([16887.0, 4857.0, 0.0, 5928.0, 32.0, 28080.0]) #mm^3

time_data=t2
tumor_volume_data=tum2
def model_to_fit(t, a, b):
    return levin_solver(t, a, b, V0=tumor_volume_data[0])

# Initial guesses
p0 = [0.02, 10000.0]

popt, pcov = curve_fit(
    model_to_fit, time_data, tumor_volume_data,
    p0=[0.02, 1000.0],
    bounds=([0.0001, 10], [0.1, 1e5])
)

a_fit, b_fit = popt
print(f"Fitted parameters: a = {a_fit:.4f}, b = {b_fit:.2f}")

import matplotlib.pyplot as plt

V_fit = model_to_fit(time_data, a_fit, b_fit)

plt.scatter(time_data, tumor_volume_data, label="Experimental Data")
plt.plot(time_data, V_fit, 'r-', label="Levin Collocation Fit")
plt.xlabel("Time (days)")
plt.ylabel("Tumor Volume (mm³)")
plt.legend()
plt.show()

