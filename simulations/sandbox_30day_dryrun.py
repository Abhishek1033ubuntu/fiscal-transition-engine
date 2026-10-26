import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Ensure kernel and telemetry modules are resolvable from repository root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from telemetry.regional_demographics import RegionalDemographics
from telemetry.bft_oracle_mesh import BFTOracleMesh
from kernel.firewall_invariants import FirewallInvariants

def run_30day_dryrun():
    print("==================================================")
    print(" Starting 30-Day Multi-Region Telemetry Dry Run")
    print("==================================================\n")

    # 1. Initialize Regional Nodes & Consensus Mesh
    regions = {
        "Urban_Central": RegionalDemographics(node_id="Urban_Central", D_baseline=150.0, elasticity=0.4),
        "Rural_West": RegionalDemographics(node_id="Rural_West", D_baseline=60.0, elasticity=0.8),
        "Industrial_East": RegionalDemographics(node_id="Industrial_East", D_baseline=200.0, elasticity=0.3),
    }

    mesh = BFTOracleMesh(fault_tolerance=0.33)
    firewall = FirewallInvariants(lambda_bounds=(0.0, 0.2), alpha_bounds=(0.0, 0.02), slew_max=0.01)

    days = 30
    history = {node_id: [] for node_id in regions}
    aggregate_demand_hist = []
    firewall_status_hist = []

    # 2. Daily Telemetry Ingestion Loop
    for day in range(1, days + 1):
        daily_reports = {}
        # Simulate a regional shock on Day 12 to Day 18 in Rural_West
        for node_id, region in regions.items():
            shock = -25.0 if (node_id == "Rural_West" and 12 <= day <= 18) else 0.0
            noise = np.random.normal(0, 1.5)
            D_current = max(10.0, region.D_baseline + shock + noise)
            daily_reports[node_id] = D_current
            history[node_id].append(D_current)

        # Process telemetry consensus
        consensus_demand = mesh.compute_consensus(daily_reports)
        aggregate_demand_hist.append(consensus_demand)

        # Evaluate safety floor invariant
        critical_floor = 80.0
        floor_triggered = consensus_demand < critical_floor
        firewall_status_hist.append(1 if floor_triggered else 0)

        status_str = "FROZEN (Safety Floor Active)" if floor_triggered else "NORMAL"
        print(f"Day [{day:02d}/30] | Consensus Demand: {consensus_demand:6.2f} | Firewall Status: {status_str}")

    print("\n30-Day Telemetry Simulation Completed Successfully.")

    # 3. Render and Save Telemetry Dashboard
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    fig.suptitle("30-Day Multi-Region Telemetry & Firewall Invariant Log", fontsize=14, fontweight='bold')

    time_axis = list(range(1, days + 1))
    for node_id, values in history.items():
        ax1.plot(time_axis, values, label=f"Node: {node_id}", linestyle='--')
    ax1.plot(time_axis, aggregate_demand_hist, 'k-', linewidth=2.5, label='BFT Consensus Aggregate')
    ax1.axhline(y=80.0, color='r', linestyle=':', label='Critical Demand Floor (D_min)')
    ax1.set_ylabel("Demand Level")
    ax1.set_title("Regional Telemetry Ingestion vs Consensus")
    ax1.grid(True)
    ax1.legend(loc='upper right')

    ax2.step(time_axis, firewall_status_hist, where='post', color='red', linewidth=2)
    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(['Normal Operating', 'Firewall Freeze Active'])
    ax2.set_xlabel("Operational Days")
    ax2.set_ylabel("Firewall State")
    ax2.set_title("Safety Floor Invariant Status")
    ax2.grid(True)

    plt.tight_layout()
    output_png = "sandbox_30day_dryrun.png"
    plt.savefig(output_png)
    print(f"Saved plot output to: {output_png}")
    plt.show()

if __name__ == "__main__":
    run_30day_dryrun()
