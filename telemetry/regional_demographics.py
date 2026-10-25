class RegionalDemographics:
    """Calculates dynamic regional demand floors D_critical based on local wages and CPI."""
    @staticmethod
    def compute_regional_floor(D0_regional, wage_regional, wage_national, cpi_regional, cpi_national, theta=0.6):
        wage_ratio = (wage_regional / wage_national) ** theta
        cpi_ratio = cpi_national / cpi_regional
        return D0_regional * wage_ratio * cpi_ratio
