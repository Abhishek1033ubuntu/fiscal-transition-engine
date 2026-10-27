# Fiscal Transition Engine — Complete User & Developer Execution Guide

Welcome to the `fiscal-transition-engine`. This guide provides step-by-step instructions for setting up your environment, running native simulations, executing pre-configured policy scenarios, and viewing plot outputs across different operating systems.

---

## 1. Prerequisites & Environment Setup

### System Requirements
* **Python**: Version 3.9 or higher.
* **Core Libraries**: `numpy`, `scipy`, `matplotlib`.

### Step-by-Step Installation
1. Clone or extract the repository onto your machine.
2. Open your terminal (Ubuntu CLI, macOS Terminal, or Windows PowerShell) and navigate to the project root:
   ```bash
   cd fiscal-transition-engine

```

3. git clone [https://github.com/Abhishek1033ubuntu/fiscal-transition-engine.git](https://github.com/Abhishek1033ubuntu/fiscal-transition-engine.git)
cd fiscal-transition-engine
pip install -e .

4 . Install dependencies:
```bash
pip install -r requirements.txt

```


4. Install the repository in editable mode so Python links `kernel` and `telemetry` packages globally:
```bash
# Ubuntu / Linux CLI / macOS:
python3 -m pip install -e .

# Windows PowerShell:
py -m pip install -e .

```



---

## 2. Running Simulations & Viewing Graphics

### Command Line Syntax

To prevent Python import errors (`ModuleNotFoundError: No module named 'kernel'`), always run scripts as modules using the `-m` flag from the repository root directory.

#### A. Native ODE Trajectory Simulation

Solves the continuous 5-state macroeconomic ODE system and renders the 6-panel trajectory dashboard.

* **Ubuntu / Linux CLI:**
```bash
python3 -m simulations.scipy_trajectory

```


* **Windows PowerShell:**
```powershell
py -m simulations.scipy_trajectory

```


* **Output:** Generates terminal telemetry log, opens an interactive plot window, and saves `scipy_macro_bounded_simulation.png` in your active folder.

#### B. Pre-Configured Policy Scenario Runner

Executes real-world economic scenarios using JSON parameter profiles.

* **Energy Shock Mitigation:**
```bash
py -m simulations.scenario_runner --config configs/energy_shock.json

```


* **Sovereign Debt Recovery:**
```bash
py -m simulations.scenario_runner --config configs/high_debt_recovery.json

```


* **Poverty Protection:**
```bash
py -m simulations.scenario_runner --config configs/poverty_protection.json

```


* **Rapid Expansion:**
```bash
py -m simulations.scenario_runner --config configs/rapid_expansion.json

```


* **Output:** Prints final state values ($D, F, \Delta S$) at $T_{\text{max}}$ and saves scenario-specific PNG files (e.g., `scenario_energy_shock.png`).

#### C. 30-Day Multi-Region Telemetry Dry Run

Simulates daily telemetry ingestion across Urban, Rural, and Industrial nodes.

```bash
py -m simulations.sandbox_30day_dryrun

```

#### D. Stochastic Monte Carlo Stress Test

Executes $N=200$ stochastic iterations with Ornstein-Uhlenbeck noise and Poisson jump shocks to verify Lyapunov Input-to-State Stability (ISS).

```bash
py -m simulations.monte_carlo_stress

```

---

## 3. Understanding Plot & Graphical Displays

Different execution environments handle Matplotlib graphics in specific ways:

* **Google Colab / Jupyter Notebooks:** Graphs automatically render inline under the executed code cell.
* **IDE Environments (VS Code, PyCharm):** Figures automatically open inside the IDE's dedicated "Plots" pane.
* **Headless Terminals / Ubuntu CLI / PowerShell:**
* All scripts automatically write graphical outputs directly to `.png` files in the root folder.
* To open image files directly from PowerShell:
```powershell
Invoke-Item scipy_macro_bounded_simulation.png

```


* To open image files from Ubuntu CLI (with Desktop GUI):
```bash
xdg-open scipy_macro_bounded_simulation.png

```





---

## 4. Custom Experimentation

You can test custom economic parameters by duplicating any JSON file in `configs/`:

```bash
cp configs/energy_shock.json configs/my_custom_scenario.json

```

Edit `configs/my_custom_scenario.json` to modify elasticity (`epsilon_d`), demand shock intensity (`shock_val`), or slew-rate bounds (`slew_max`), then execute:

```bash
py -m simulations.scenario_runner --config configs/my_custom_scenario.json

```

---

## 5. Troubleshooting Common Issues

| Issue / Error | Cause | Solution |
| --- | --- | --- |
| `ModuleNotFoundError: No module named 'kernel'` | Script executed directly inside `simulations/` folder instead of root. | Run from root using `py -m simulations.scipy_trajectory`. |
| `pip: command not found` (Windows) | Python binary path missing from system PATH. | Use the built-in launcher: `py -m pip install -r requirements.txt`. |
| Graph window closes instantly | Terminal shell lacks interactive event loop. | View the saved `.png` file directly in your folder via File Explorer. |

