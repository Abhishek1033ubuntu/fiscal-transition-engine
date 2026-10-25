!pip install scipy numpy matplotlib
!git clone https://github.com/Abhishek1033ubuntu/fiscal-transition-engine.git
%cd fiscal-transition-engine

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from kernel import MacroStateSpace, FirewallInvariants, AdaptiveController

def run_simulation():
    state = MacroStateSpace()
    firewall = FirewallInvariants()
    controller = AdaptiveController()

    def ode_system(t, y):
        D, F, Delta_S, alpha, lambda_val = y
        shock = -10.0 if 30 <= t <= 50 else 0.0
        
        P = state.compute_effective_price(Delta_S, alpha, D)
        dD_dt = state.demand_derivative(D, P, shock)
        dF_dt = state.fiscal_derivative(Delta_S, lambda_val, alpha, dD_dt)
        
        e_D, e_F = D - 100.0, F - 0.0
        dlambda_raw, dalpha_raw = controller.compute_adaptations(
            e_D, e_F, Delta_S, D, P, state.P0, state.D0, state.gamma, state.epsilon_d, lambda_val, alpha
        )
        
        dlambda_dt = firewall.apply_slew_and_saturation(lambda_val, dlambda_raw, (firewall.lambda_min, firewall.lambda_max))
        dalpha_dt = firewall.apply_slew_and_saturation(alpha, dalpha_raw, (firewall.alpha_min, firewall.alpha_max))
        
        return [dD_dt, dF_dt, -lambda_val * max(Delta_S, 0.0), dalpha_dt, dlambda_dt]

    y0 = [100.0, 5.0, 5.0, 0.001, 0.05]
    sol = solve_ivp(ode_system, (0, 100), y0, t_eval=np.linspace(0, 100, 1000), method='RK45')
    print("SciPy trajectory run finished successfully. Solved shape:", sol.y.shape)

if __name__ == "__main__":
    run_simulation()
