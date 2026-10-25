import numpy as np
from scipy.integrate import solve_ivp
from kernel import MacroStateSpace, FirewallInvariants, AdaptiveController

def run_monte_carlo(n_runs=50):
    state = MacroStateSpace()
    firewall = FirewallInvariants()
    controller = AdaptiveController()
    t_eval = np.linspace(0, 100, 200)

    success_count = 0
    for i in range(n_runs):
        xi_noise = np.random.normal(0, 2.0, size=200)
        def system(t, y):
            idx = min(int(t / 100 * 200), 199)
            D, F, Delta_S, alpha, lambda_val = y
            P = state.compute_effective_price(Delta_S, alpha, D)
            dD_dt = state.demand_derivative(D, P, xi_noise[idx])
            dF_dt = state.fiscal_derivative(Delta_S, lambda_val, alpha, dD_dt)
            return [dD_dt, dF_dt, -lambda_val * max(Delta_S, 0.0), 0.0, 0.0]

        sol = solve_ivp(system, (0, 100), [100.0, 5.0, 5.0, 0.001, 0.05], t_eval=t_eval)
        if sol.status == 0:
            success_count += 1
            
    print(f"Monte Carlo stress test complete: {success_count}/{n_runs} runs stable.")

if __name__ == "__main__":
    run_monte_carlo()
