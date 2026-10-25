import numpy as np

class BFTOracleMesh:
    """
    Simulates a Byzantine Fault Tolerant Multi-Node Data Consensus Network.
    Filters out outlier streams exceeding k-sigma variance bounds.
    """
    def __init__(self, k_sigma=2.5):
        self.k_sigma = k_sigma

    def filter_telemetry(self, raw_node_inputs):
        """Filters manipulated inputs and returns robust median value."""
        inputs = np.array(raw_node_inputs)
        median = np.median(inputs)
        std = np.std(inputs)
        
        if std == 0:
            return median
            
        valid_mask = np.abs(inputs - median) <= (self.k_sigma * std)
        filtered = inputs[valid_mask]
        return float(np.mean(filtered))
