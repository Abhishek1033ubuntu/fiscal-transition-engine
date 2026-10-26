import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Ensure kernel is resolvable from root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from kernel import MacroStateSpace, FirewallInvariants, AdaptiveController

def run_simulation():
    # 1. Initialize State Space and Control Objects
    state = MacroStateSpace(gamma=0.5, D0=100.0, P0=10.0, P_unsubsidized=15.0, epsilon_d=0.5)
    firewall = FirewallInvariants(lambda_bounds=(0.0, 0.2), alpha_bounds=(0.0, 0.02), slew_max=0.01)
    controller = AdaptiveController(w_D=1.0, w_F=1.0, beta1=0.001, beta2=0.0001)

    # 2. Define ODE System Dynamics
    def macro_system_ode(t, y):
        D, F, Delta_S, alpha, lambda_val = y
        shock = -10.0 if 30 <= t <= 50 else 0.0
        P = state.compute_effective_price(Delta_S, alpha, D)
        dD_dt = state.demand_derivative(D, P, shock)
        dF_dt = state.fiscal_derivative(Delta_S, lambda_val, alpha, dD_dt)
        dDelta_S_dt = -lambda_val * max(Delta_S, 0.0)
        
        e_D, e_F = D - 100.0, F - 0.0
        dlambda_raw, dalpha_raw = controller.compute_adaptations(
            e_D, e_F, Delta_S, D, P, state.P0, state.D0, state.gamma, state.epsilon_d, lambda_val, alpha
        )
        dlambda_dt = firewall.apply_slew_and_saturation(lambda_val, dlambda_raw, (firewall.lambda_min, firewall.lambda_max))
        dalpha_dt = firewall.apply_slew_and_saturation(alpha, dalpha_raw, (firewall.alpha_min, firewall.alpha_max))
        return [dD_dt, dF_dt, dDelta_S_dt, dalpha_dt, dlambda_dt]

    # 3. Execute Solver Across 1000 Time Steps
    y0 = [100.0, 5.0, 5.0, 0.001, 0.05]
    t_eval = np.linspace(0, 100, 1000)
    sol = solve_ivp(macro_system_ode, (0, 100), y0, t_eval=t_eval, method='RK45')

    print(f"SciPy trajectory run finished successfully. Solved shape: {sol.y.shape}")

    # 4. Generate and Render 6-Panel Trajectory Plot Dashboard
    fig, axes = plt.subplots(3, 2, figsize=(11, 7))
    fig.suptitle("Native Macroeconomic Bounded Trajectory Simulation", fontsize=14, fontweight='bold')

    axes[0, 0].plot(sol.t, sol.y[0], 'b-', label='Demand D(t)'); axes[0, 0].set_title('Aggregate Demand'); axes[0, 0].grid(True)
    axes[0, 1].plot(sol.t, sol.y[1], 'g-', label='Deficit F(t)'); axes[0, 1].set_title('Net Fiscal Deficit'); axes[0, 1].grid(True)
    axes[1, 0].plot(sol.t, sol.y[2], 'm-', label='Subsidy'); axes[1, 0].set_title('Subsidy Remaining Delta_S(t)'); axes[1, 0].grid(True)
    axes[1, 1].plot(sol.t, sol.y[4], 'orange', label='Lambda'); axes[1, 1].set_title('Decay Rate Lambda(t)'); axes[1, 1].grid(True)
    axes[2, 0].plot(sol.t, sol.y[3], 'purple', label='Alpha'); axes[2, 0].set_title('Collection Rate Alpha(t)'); axes[2, 0].grid(True)
    
    shocks = [-10.0 if 30 <= ti <= 50 else 0.0 for ti in sol.t]
    axes[2, 1].plot(sol.t, shocks, 'r-', label='Shock'); axes[2, 1].set_title('Exogenous Demand Shock'); axes[2, 1].grid(True)

    plt.tight_layout()
    output_png = "scipy_macro_bounded_simulation.png"
    plt.savefig(output_png)
    print(f"Saved figure output to: {output_png}")
    plt.show()

if __name__ == "__main__":
    run_simulation()
