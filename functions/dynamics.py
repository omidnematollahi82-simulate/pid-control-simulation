from config import m,c,k,x_d

def tracker(t,x,K):
    """
    Mass-spring-damper with P/PD/PID tracking controller.

    state:
      P/PD: x = [position,velocity]
      PID:  x = [position,velocity,integral_error]

      Control law(implemented in the dynamics form):
            u(t) = Kp*(x_d - x) - Kd*x_dot + Ki*I
    """
    x1 = x[0]    #position
    x2 = x[1]    #velocity

    e = x_d - x1
    
    #integral state (PID only)
    if len(x)== 2:
        I = 0
    elif len(x)==3:
        I = x[2]
        didt = e

    dx1dt = x2
    dx2dt = (-(c + K["kd"]) * x2 - (k + K["kp"]) * x1 + K["ki"] * I + K["kp"] * x_d) / m

    #Return derivatives
    if len(x) == 2:
        return [dx1dt, dx2dt]
    else:
        return [dx1dt, dx2dt, didt]