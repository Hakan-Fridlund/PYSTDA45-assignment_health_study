# Health Study – Statistical Analysis in Python

## Overview

This project is an individual data analysis assignment for the course PYSTDA45, Data Science programme based on a simulated health study dataset. The goal is to investigate relationships between demographic characteristics, health measurements, lifestyle factors, and disease prevalence using Python.

The analysis is performed using Python and presented in Jupyter Notebooks, combining statistical calculations, simulations, hypothesis testing, data visualization, and object-oriented programming.  
The report text is written in Swedish.  
The project is divided into two parts, each developed and submitted through a separate Git branch.  

## Dataset

The project uses `health_study_dataset.csv`, a simulated dataset with 800 study participants.

| **Column** | **Description** | **Unit / Values** |
|---|---|---|
| `age` | Age | Years |
| `sex` | Biological sex | M / F |
| `height` | Height | cm |
| `weight` | Weight | kg |
| `systolic_bp` | Systolic blood pressure | mmHg |
| `cholesterol` | Cholesterol level | mmol/L |
| `smoker` | Smoking status | Yes / No |
| `disease` | Disease status | 0 / 1 |

## Project Parts

### Part 1 – Basic Analysis and Statistics

**Branch:** `del1`

The first part focuses on exploratory data analysis and fundamental statistical methods.

Topics covered:

- **Descriptive Statistics** – Calculating mean, median, minimum, and maximum for selected health measurements.
- **Data Visualization** – Exploring distributions and relationships using histograms, boxplots, and bar charts.
- **Statistical Simulation** – Simulating disease prevalence using NumPy and comparing simulated results with the observed dataset.
- **Confidence Intervals** – Estimating the population mean of systolic blood pressure using statistical methods.
- **Hypothesis Testing** – Investigating whether smokers have a higher mean systolic blood pressure than non-smokers.

Additional advanced analysis:

- Comparing confidence intervals calculated using two different methods.
- Simulating statistical power to investigate the reliability of the hypothesis test.
- Justifying statistical methods using documentation and relevant references.

#### Key findings (Part 1)

- Age correlates with both systolic blood pressure (r ≈ 0.61) and cholesterol (r ≈ 0.49).
- 95 % confidence interval for mean systolic blood pressure: approx. 148.3–150.1 mmHg. The normal approximation and bootstrap give nearly identical results.
- No significant difference in mean systolic blood pressure between smokers and non-smokers (Welch's t-test, p ≈ 0.65).
- The power simulation shows low power for detecting the observed difference (about 0.5 mmHg), even at large sample sizes.
- Disease is more common among smokers than non-smokers in the dataset (8.9 % vs 4.8 %). This is tested statistically in Part 2 (logistic regression).


### Part 2 – Advanced Analysis and Pipeline

**Branch:** `del2`

The second part builds on the first by introducing a more structured and reusable approach to data analysis.

Topics covered:

- **Code Structure** – Analysis code is refactored into reusable modules in `src/`:
  - `data_utils.py` – data loading, cleaning and validation
  - `metrics.py` – statistical calculations, regression and simulations
  - `viz.py` – visualizations
- **Object-Oriented Programming** – The `HealthAnalyzer` class (`health_analyzer.py`) is the single interface to the three modules. The notebook runs all analyses and plots through it, and the colour palette is selected when the class is created.
- **Linear Algebra in Practice** – Regression coefficients are estimated with matrix algebra (OLS via scikit-learn and Statsmodels). Correlation matrices (Pearson, Spearman, Kendall) and variance inflation factors (VIF) are based on the same matrix methods.
- **Regression Analysis** – Multiple linear regression for systolic blood pressure and logistic regression for disease status.
- **Extended Analysis and Visualization** – Correlation analysis with binary variables, regression lines with bootstrap confidence bands, boxplots with swarm plots by disease status, and a power simulation extended to larger sample sizes.
- **Documentation** – Type hints and docstrings in the code, and Markdown explanations, methodological justifications and references in the notebook.

Additional advanced analysis:

- A comprehensive analysis class (`HealthAnalyzer`) wrapping the data, metrics and visualization modules.
- Multiple linear regression with regression diagnostics (Q-Q plot, residual plot, VIF) and logistic regression with odds ratios and ROC/AUC.
- Further justification of methodological choices with references to relevant documentation.

#### Key findings (Part 2)

- **Multiple linear regression** (systolic blood pressure ~ age, cholesterol, BMI, smoking, sex): age, BMI and sex have statistically significant positive associations with systolic blood pressure (coefficients 0.52, 0.34 and 2.42 mmHg), while cholesterol and smoking do not. The model explains about 39.8 % of the variation (R² = 0.398). VIF values (1.01–1.50) show no problematic multicollinearity, and the residual diagnostics support the model assumptions reasonably well.
- **Logistic regression** (disease status): smoking is the only statistically significant predictor (odds ratio ≈ 2.0, p = 0.026). The model's ability to separate people with and without disease is limited (AUC = 0.631, calculated on the training data), and the dataset contains only 47 disease cases.
- **Extended power simulation:** for the observed difference of about 0.47 mmHg between smokers and non-smokers, the power first exceeds 80 % at roughly 35,000 observations.
- **Recommendations:** collect data with more disease cases, include more relevant variables (for example physical activity, diet, stress and medication use), and evaluate the logistic model on separate test data.

## Technologies and Libraries

- **Python 3.14.7** – Main programming language.
- **Pandas** – Data manipulation and analysis.
- **NumPy** – Numerical computing and statistical simulations.
- **Matplotlib & Seaborn** – Data visualization.
- **SciPy** – Statistical methods and hypothesis testing.
- **Statsmodels** – Regression models, regression diagnostics and VIF.
- **scikit-learn** – Linear regression and ROC/AUC.
- **Jupyter Notebook** – Interactive analysis and documentation.

## Visualization Standards

All charts and visualizations follow my [Data Visualization Policy](https://github.com/Hakan-Fridlund/PYSTDA45-assignment_health_study/blob/del1/visualization_policy.md), with a focus on accessibility, inclusivity, readability, and scientific integrity.

The default palette is Okabe-Ito. Alternative palettes (`glasbey_20` and `okabe_ito_tritanopi`) can be selected in Part 2 by changing the `palette` argument when creating `HealthAnalyzer`.

## Repository Structure

```text
PYSTDA45-assignment_health_study/
│
├── data/
│   └── health_study_dataset.csv
│
├── images/
│   └── okabe_ito_palette.png
│
├── notebooks/
│   ├── health_study_part1.ipynb
│   └── health_study_part2.ipynb
│
├── src/
│   ├── __init__.py
│   ├── health_analyzer.py
│   ├── data_utils.py
│   ├── metrics.py
│   └── viz.py
│
├── README.md
├── requirements.txt
└── visualization_policy.md
```

## Getting Started

### Prerequisites

- Python 3.14.7
- Git
- Jupyter Notebook or Visual Studio Code with the Jupyter extension

### Installation

**1. Clone the repository:**

```bash
git clone https://github.com/Hakan-Fridlund/PYSTDA45-assignment_health_study.git
```

**2. Navigate to the project directory:**

```bash
cd PYSTDA45-assignment_health_study
```

**3. Create a virtual environment:**

```bash
python -m venv .venv
```

**4. Activate the virtual environment:**

Choose the command for your operating system and terminal.

Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

Windows (Git Bash):

```bash
source .venv/Scripts/activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

**5. Install the required dependencies:**

```bash
python -m pip install -r requirements.txt
```

### Running the Notebooks

Switch to the desired branch:

Part 1:

```bash
git checkout del1
```

Part 2:

```bash
git checkout del2
```

Open the desired .ipynb file in the notebooks directory in Visual Studio Code.  

Ensure that the Python and Jupyter extensions are installed and select the appropriate Python interpreter and kernel before running the notebook.  


## Reproducibility

Random seeds are used in simulations to ensure reproducibility and consistent results across runs.

All analysis, code, visualizations, and explanations are documented directly in the Jupyter Notebooks.

## Author

Håkan Fridlund

Individual course assignment – Health Study Analysis.
