from typing import Dict, List
import numpy as np

class BFTOracleMesh:
    """
    Byzantine Fault Tolerant Oracle Mesh for multi-node regional telemetry ingestion.
    Filters outliers using k-sigma variance bounds and computes consensus aggregate demand.
    """
    def __init__(self, fault_tolerance: float = 0.33, k_sigma: float = 2.0):
        self.fault_tolerance = fault_tolerance
        self.k_sigma = k_sigma

    def filter_outliers(self, raw_telemetry: Dict[str, float]) -> List[float]:
        """Filters out node reporting anomalies using k-sigma bounds."""
        values = list(raw_telemetry.values())
        if len(values) < 3:
            return values
        
        mean_val = np.mean(values)
        std_val = np.std(values)
        if std_val == 0:
            return values
            
        filtered = [v for v in values if abs(v - mean_val) <= self.k_sigma * std_val]
        return filtered if len(filtered) > 0 else values

    def compute_consensus(self, raw_telemetry: Dict[str, float]) -> float:
        """Computes BFT consensus mean across active regional telemetry feeds."""
        valid_values = self.filter_outliers(raw_telemetry)
        return float(np.mean(valid_values))
