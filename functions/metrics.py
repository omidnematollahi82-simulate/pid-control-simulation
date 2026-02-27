import numpy as np

def compute_metrics (solutions,x_d,K,name):
    x = solutions.y[0]
    v = solutions.y[1]
    t = solutions.t
    
    # PID integral term if it exists
    if solutions.y.shape[0] == 3:
        I = solutions.y[2]
    else:
        I = 0.0

    e = x_d - x
    e_dot = -v   # because x_d is constant

    # Controller effort: u(t) = Kp*e + Kd*e_dot + Ki*I
    ut = K["kp"] * e + K["kd"] * e_dot + K["ki"] * I

    # Overshoot %
    x_peak = np.max(x)
    OS =  ((x_peak - x_d) / x_d) * 100.0

    #Settling time (2% band)
    tol = 0.02   
    upper = x_d * (1.0 + tol)
    lower = x_d * (1.0 - tol)

    t_settle = np.nan
    for i in range(len(x)):
        if np.all((x[i:] >= lower) & (x[i:] <= upper)):
            t_settle = t[i]    
            break              # IMPORTANT : first time it stays in the band

    # Peak time (time of maximum x)
    t_peak = t[np.argmax(x)]

    # IAE / ISE
    IAE = np.trapezoid(np.abs(e), t)
    ISE = np.trapezoid(e**2, t)

    #Steady-State error (average of last 10%)
    e_ss = float(np.mean(e[int(0.9 * len(e)):]))

    # Effort stats
    u_max = float(np.max(ut))
    u_min = float(np.min(ut))
    u_ss = float(np.mean(ut[int(0.9 * len(ut)):]))

    #Effort energy 
    J_u = np.trapezoid(ut**2, t)

    return {
        "Controller": str(name),
        "kp": K["kp"],
        "ki": K["ki"],
        "kd": K["kd"],
        "OS%": float(OS),
        "t_settle": float(t_settle) if not np.isnan(t_settle) else np.nan,
        "T_peak": float(t_peak),
        "e_ss": e_ss,
        "u_max": u_max,
        "u_min": u_min,
        "u_ss": u_ss,
        "J_u": float(J_u),
        "IAE": float(IAE),
        "ISE": float(ISE),
        }

