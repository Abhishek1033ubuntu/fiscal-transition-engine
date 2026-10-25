import numpy as np

class AdaptiveController:
    """
    Gradient descent adaptive controller (MIT Rule) for dynamic tuning of
    subsidy decay (lambda) and micro-collection (alpha).
    """
    def __init__(self, w_D=1.0, w_F=1.0, beta1=0.001, beta2=0.0001, 
                 kappa_lambda=0.01, kappa_alpha=0.01, lambda_0=0.05):
        self.w_D = w_D
        self.w_F = w_F
        self.beta1 = beta1
        self.beta2 = beta2
        self.kappa_lambda = kappa_lambda
        self.kappa_alpha = kappa_alpha
        self.lambda_0 = lambda_0

    def compute_adaptations(self, e_D, e_F, Delta_S, V, P, P0, D0, gamma, epsilon_d, lambda_val, alpha):
        """Calculates unconstrained dlambda/dt and dalpha/dt signals."""
        dP_term = (P / P0) ** (-epsilon_d - 1.0)
        dDdot_dlambda = gamma * D0 * epsilon_d * dP_term * (1.0 / P0) * max(Delta_S, 0.0)
        dDdot_dalpha = -gamma * D0 * epsilon_d * dP_term * (1.0 / P0) * V

        dlambda_raw = self.beta1 * (self.w_F * e_F * Delta_S + self.w_D * e_D * dDdot_dlambda) - self.kappa_lambda * (lambda_val - self.lambda_0)
        dalpha_raw = self.beta2 * (self.w_F * e_F * V + self.w_D * e_D * dDdot_dalpha) - self.kappa_alpha * alpha

        return dlambda_raw, dalpha_raw
