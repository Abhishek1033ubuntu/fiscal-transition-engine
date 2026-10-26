import sys
import os
import json
import argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Ensure kernel is resolvable from root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from kernel import MacroStateSpace, FirewallInvariants, AdaptiveController

def run_scenario(config_path):
    if not os.path.exists(config_path):
        print(f"Error: Configuration file '{config_path}' not found.")
        return

    with open(config_path, "r") as f:
        cfg = json.load(f)

    print(f"\n==================================================")
    print(f" Executing Scenario: {cfg['scenario_name']}")
    print(f"==================================================")

    state = MacroStateSpace(
        gamma=cfg["gamma"], 
        D0=cfg["D0"], 
        P0=cfg["P0"], 
        P_unsubsidized=cfg["P_unsubsidized"], 
        epsilon_d=cfg["epsilon_d"]
    )
    firewall = FirewallInvariants(
        lambda_bounds=(0.0, cfg["lambda_max"]), 
        alpha_bounds=(0.0, cfg["alpha_max"]), 
        slew_max=cfg["slew_max"]
    )
    controller = AdaptiveController(w_D=1.0, w_F=1.0, beta1=0.001, beta2=0.0001)

    def ode_system(t, y):
        D, F, Delta_S, alpha, lambda_val = y
        shock = cfg["shock_val"] if cfg["shock_start"] <= t <= cfg["shock_end"] else 0.0
        P = state.compute_effective_price(Delta_S, alpha, D)
        dD_dt = state.demand_derivative(D, P, shock)
        dF_dt = state.fiscal_derivative(Delta_S, lambda_val, alpha, dD_dt)
        dDelta_S_dt = -lambda_val * max(Delta_S, 0.0)
        
        e_D, e_F = D - cfg["D0"], F - 0.0
        dlambda_raw, dalpha_raw = controller.compute_adaptations(
            e_D, e_F, Delta_S, D, P, state.P0, state.D0, state.gamma, state.epsilon_d, lambda_val, alpha
        )
        
        dlambda_dt = firewall.apply_slew_and_saturation(lambda_val, dlambda_raw, (firewall.lambda_min, firewall.lambda_max))
        dalpha_dt = firewall.apply_slew_and_saturation(alpha, dalpha_raw, (firewall.alpha_min, firewall.alpha_max))
        return [dD_dt, dF_dt, dDelta_S_dt, dalpha_dt, dlambda_dt]

    y0 = [cfg["D0"], cfg["F0"], cfg["Delta_S0"], cfg["alpha0"], cfg["lambda0"]]
    t_span = (0, cfg["t_max"])
    t_eval = np.linspace(0, cfg["t_max"], 1000)

    sol = solve_ivp(ode_system, t_span, y0, t_eval=t_eval, method='RK45')

    print(f"Solver Status: Success ({sol.nfev} function evaluations)")
    print(f"Final Aggregate Demand: {sol.y[0][-1]:.2f}")
    print(f"Final Net Deficit:     {sol.y[1][-1]:.2f}")
    print(f"Final Subsidy Delta:   {sol.y[2][-1]:.4f}")

    fig, axes = plt.subplots(3, 2, figsize=(11, 7))
    fig.suptitle(cfg["scenario_name"], fontsize=14, fontweight='bold')

    axes[0, 0].plot(sol.t, sol.y[0], 'b-'); axes[0, 0].set_title('Aggregate Demand D(t)'); axes[0, 0].grid(True)
    axes[0, 1].plot(sol.t, sol.y[1], 'g-'); axes[0, 1].set_title('Net Deficit F(t)'); axes[0, 1].grid(True)
    axes[1, 0].plot(sol.t, sol.y[2], 'm-'); axes[1, 0].set_title('Subsidy Remaining Delta_S(t)'); axes[1, 0].grid(True)
    axes[1, 1].plot(sol.t, sol.y[4], 'orange'); axes[1, 1].set_title('Decay Rate Lambda(t)'); axes[1, 1].grid(True)
    axes[2, 0].plot(sol.t, sol.y[3], 'purple'); axes[2, 0].set_title('Collection Rate Alpha(t)'); axes[2, 0].grid(True)
    
    shocks = [cfg["shock_val"] if cfg["shock_start"] <= ti <= cfg["shock_end"] else 0.0 for ti in sol.t]
    axes[2, 1].plot(sol.t, shocks, 'r-'); axes[2, 1].set_title('Exogenous Shock Profile'); axes[2, 1].grid(True)

    plt.tight_layout()
    output_png = f"scenario_{os.path.basename(config_path).replace('.json', '.png')}"
    plt.savefig(output_png)
    print(f"Saved plot output to: {output_png}")
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run fiscal transition engine scenario simulations.")
    parser.add_argument("--config", type=str, default="configs/energy_shock.json", help="Path to scenario JSON config file")
    args = parser.parse_args()
    run_scenario(args.config)
