class RegionalDemographics:
    """
    Manages regional macroeconomic baselines, demand floors, 
    and price elasticity for multi-node telemetry ingestion.
    """
    def __init__(self, node_id: str = "default_node", D_baseline: float = 100.0, elasticity: float = 0.5):
        self.node_id = node_id
        self.D_baseline = D_baseline
        self.elasticity = elasticity

    def compute_critical_demand(self, floor_factor: float = 0.6) -> float:
        """Calculates localized critical demand threshold D_critical."""
        return self.D_baseline * floor_factor
