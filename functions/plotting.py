import matplotlib.pyplot as plt

def plot(solutions, x_d, xdot_d):
    # 1) Tracking response
    plt.figure(figsize=(14, 6))
    for name, K, sol in solutions:
        t = sol.t
        x = sol.y[0]
        plt.plot(t, x, linewidth=2.0, label=str(name))
        plt.title("Tracking Response for Different Controllers")
        plt.xlabel("Time (s)")
        plt.ylabel("x(t)")
        plt.axhline(y=x_d, linestyle="dashed", alpha=0.4, color="gray")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
    plt.savefig("Results/tracking_response.jpg", dpi=300)

    # 2) Tracking error
    plt.figure(figsize=(14, 6))
    for name, K, sol in solutions:
        t = sol.t
        x = sol.y[0]
        e = x_d - x
        plt.plot(t, e, linewidth=2.0, label=str(name))
        plt.title("Tracking Error e(t)")
        plt.xlabel("Time (s)")
        plt.ylabel("e(t)")
        plt.axhline(y=0.0, linestyle="dashed" ,color="green", alpha=0.4)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
    plt.savefig("Results/error_plot.jpg", dpi=300)

    # 3) Control effort
    plt.figure(figsize=(14, 6))
    for name, K, sol in solutions:
        t = sol.t
        x = sol.y[0]
        v = sol.y[1]

        e = x_d - x
        edot = xdot_d - v    # usually -v

        u = K["kp"] * e + K["kd"] * edot

        # Add integral term if it exists
        if sol.y.shape[0] == 3 and K["ki"] != 0:
            u = u + K["ki"] * sol.y[2]
        plt.plot(t, u, linewidth=2.0, label = str(name))
        plt.title("Controller Effort u(t)")
        plt.xlabel("Time (s)")
        plt.ylabel("u(t)")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
    plt.savefig("Results/control_effort.jpg", dpi=300)

    plt.show()