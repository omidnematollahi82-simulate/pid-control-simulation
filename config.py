import numpy as np

#System Parameters
m = 1.0        # kg
k = 4.0        # N/m
c = 0.8        # N*s/m

#Controller gains (base values)
kp = 25.0
kd = 10.0
ki = 5.0

#Desired Reference
x_d = 1.0
xdot_d = 0.0

#Controller configurations
gains = [
    ("P",{"kp":kp , "kd":0.0 , "ki":0.0}),
    ("PD",{"kp":kp , "kd":kd , "ki":0.0}),
    ("PID",{"kp":kp , "kd":kd , "ki":ki}),
    ]

#Simulation time
time_span = (0.0,20.0)
t_eval = np.linspace(time_span[0],time_span[1],4000)