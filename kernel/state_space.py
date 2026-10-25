import numpy as np

class MacroStateSpace:
    """
    Non-linear continuous state-space engine for macro-demand, consumer price,
    and net fiscal outflow trajectories.
    """
    def __init__(self, gamma=0.5, D0=100.0, P0=10.0, P_unsubsidized=15.0, epsilon_d=0.5):
        self.gamma = gamma
        self.D0 = D0
        self.P0 = P0
        self.P_unsubsidized = P_unsubsidized
        self.epsilon_d = epsilon_d

    def compute_effective_price(self, Delta_S, alpha, D):
        """Calculates P(t) = P_unsubsidized - Delta_S(t) + C(t)"""
        C = alpha * max(D, 1.0)
        return max(self.P_unsubsidized - max(Delta_S, 0.0) + C, 1.0)

    def demand_derivative(self, D, P, shock=0.0):
        """dD/dt = -gamma * (D - D_eq) + xi(t)"""
        D_eq = self.D0 * ((P / self.P0) ** (-self.epsilon_d))
        return -self.gamma * (D - D_eq) + shock

    def fiscal_derivative(self, Delta_S, lambda_val, alpha, dD_dt):
        """dF/dt = d(Delta_S)/dt - dC/dt"""
        dDelta_S_dt = -lambda_val * max(Delta_S, 0.0)
        dC_dt = alpha * dD_dt
        return dDelta_S_dt - dC_dt
