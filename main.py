import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from config import gains, time_span, t_eval, x_d, xdot_d
from functions.dynamics import tracker
from functions.metrics import compute_metrics
from functions.plotting import plot

def main():
    # ICs
    IC_PD = [0.0, 0.0]          # x(0), v(0)      
    IC_PID = [0.0, 0.0, 0.0]    # x(0), v(0), I(0) 

    solutions = []
    rows = []

    #Solve
    for name, K in gains:
        y0 = IC_PID if K["ki"] != 0 else IC_PD
        sol = solve_ivp(tracker, t_span=time_span, y0=y0, t_eval=t_eval, args=(K,))
        solutions.append((name, K, sol))

    for name, K, sol in solutions:
        rows.append(compute_metrics(sol, x_d, K, name))

    df = pd.DataFrame(rows).sort_values(by="IAE", ascending=True)

    pd.set_option("display.max_columns", None)

    pd.set_option("display.width", 1000)

    pd.set_option("display.float_format", "{:.2f}".format)

    print(df)

    # Save results
    df.to_csv("Results/results.csv", index=False)
    df.to_csv("results.csv", index=False)        # optional duplicate at root

    #plots
    plot(solutions, x_d, xdot_d)
    save_table_as_image(df)
    
def save_table_as_image(df, path="Results/metrics_table.jpg",title="Controller Performance Comparison"):
    # 1) Make a copy and round floats to avoid long strings
    df_show = df.copy()
    df_show = df_show.round(4)

    # 2) Convert to strings (consistent formatting)
    df_show = df_show.astype(str)

    # 3) Dynamic figure width based on number of columns
    ncols = df_show.shape[1]
    fig_w = max(12, 1.2 * ncols)
    # scale width with columns
    fig_h = max(3, 0.6 * len(df_show) + 1)

    fig, ax = plt.subplots(figsize=(fig_w,fig_h))
    ax.axis('off')

    table = ax.table(
        cellText=df_show.values,
        colLabels=df_show.columns,
        loc='center',
        cellLoc='center',
        colLoc='center'
    )

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.0,1.4)

    # Auto-adjust colunn widths (this is the key part)
    try:

        table.auto_set_column_width(col=list(range(ncols)))
    except Exception:
        pass

    ax.set_title(title, fontsize=14, pad=15)
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)

if __name__ == "__main__":
    main()



