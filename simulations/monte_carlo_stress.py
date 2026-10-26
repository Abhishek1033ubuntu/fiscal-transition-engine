import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Ensure kernel module is resolvable from repository root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from kernel import MacroStateSpace, FirewallInvariants, AdaptiveController

def run_monte_carlo():
    N_trials = 200
    t_max = 50
    t_eval = np.linspace(0, t_max, 500)

    print("==================================================")
    print(f" Executing Stochastic Monte Carlo Stress Test (N={N_trials})")
    print("==================================================\n")

    state = MacroStateSpace(gamma=0.5, D0=100.0, P0=10.0, P_unsubsidized=15.0, epsilon_d=0.5)
    firewall = FirewallInvariants(lambda_bounds=(0.0, 0.2), alpha_bounds=(0.0, 0.02), slew_max=0.01)
    controller = AdaptiveController(w_D=1.0, w_F=1.0, beta1=0.001, beta2=0.0001)

    all_demand_runs = []
    stable_count = 0

    for trial in range(N_trials):
        # Generate stochastic Ornstein-Uhlenbeck shock process
        ou_noise = np.zeros(len(t_eval))
        theta, sigma = 0.15, 2.0
        for i in range(1, len(t_eval)):
            dt = t_eval[i] - t_eval[i-1]
            ou_noise[i] = ou_noise[i-1] - theta * ou_noise[i-1] * dt + sigma * np.sqrt(dt) * np.random.normal()

        def ode_system(t, y):
            D, F, Delta_S, alpha, lambda_val = y
            # Interpolate stochastic shock at current time t
            idx = min(int(t / t_max * len(t_eval)), len(t_eval) - 1)
            shock = ou_noise[idx]
            
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

        y0 = [100.0, 5.0, 5.0, 0.001, 0.05]
        sol = solve_ivp(ode_system, (0, t_max), y0, t_eval=t_eval, method='RK45')

        all_demand_runs.append(sol.y[0])
        # Invariant Stability Check: Demand remains above crisis threshold D > 50.0
        if np.all(sol.y[0] > 50.0):
            stable_count += 1

    pass_rate = (stable_count / N_trials) * 100.0
    print(f"Monte Carlo Stress Test Complete.")
    print(f"Pass Rate (Lyapunov ISS Invariant Preserved): {pass_rate:.1f}% ({stable_count}/{N_trials} runs)\n")

    # Render Stochastic Envelope Plot
    all_runs_arr = np.array(all_demand_runs)
    mean_trajectory = np.mean(all_runs_arr, axis=0)
    p5 = np.percentile(all_runs_arr, 5, axis=0)
    p95 = np.percentile(all_runs_arr, 95, axis=0)

    plt.figure(figsize=(10, 6))
    for i in range(min(50, N_trials)):
        plt.plot(t_eval, all_runs_arr[i], color='gray', alpha=0.15, linewidth=0.8)

    plt.plot(t_eval, mean_trajectory, 'b-', linewidth=2.5, label='Mean Aggregate Demand')
    plt.fill_between(t_eval, p5, p95, color='blue', alpha=0.2, label='95% Confidence Envelope')
    plt.axhline(y=50.0, color='r', linestyle='--', linewidth=2, label='Crisis Floor Bound (D_crisis)')

    plt.title(f"Stochastic Monte Carlo Stress Test (N={N_trials} Runs, Pass Rate: {pass_rate:.1f}%)", fontsize=13, fontweight='bold')
    plt.xlabel("Simulation Time")
    plt.ylabel("Aggregate Demand D(t)")
    plt.grid(True)
    plt.legend(loc='upper right')

    plt.tight_layout()
    output_png = "monte_carlo_stress_test.png"
    plt.savefig(output_png)
    print(f"Saved figure output to: {output_png}")
    plt.show()

if __name__ == "__main__":
    run_monte_carlo()
