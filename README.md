# Health Study – Statistical Analysis in Python

## Overview

This project is an individual data analysis assignment based on a health study dataset. The goal is to investigate relationships between demographic characteristics, health measurements, lifestyle factors, and disease prevalence using Python.

The analysis is performed using Python and presented in Jupyter Notebooks, combining statistical calculations, simulations, hypothesis testing, data visualization, and object-oriented programming.

The project is divided into two parts, each developed and submitted through a separate Git branch.

## Dataset

The project uses `health_study_dataset.csv`, containing health-related information about study participants.

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

### Part 2 – Advanced Analysis and Pipeline

**Branch:** `del2`

The second part builds on the first by introducing a more structured and reusable approach to data analysis.

Topics covered:

- **Code Structure** – Refactoring notebook code into reusable functions and modules.
- **Object-Oriented Programming** – Implementing at least one class to handle statistical analysis or visualizations.
- **Linear Algebra in Practice** – Applying matrix- and vector-based methods using NumPy or scikit-learn.
- **Regression Analysis / PCA** – Exploring relationships and patterns within the dataset.
- **Extended Analysis and Visualization** – Adding further analysis to gain deeper insights into the health data.
- **Documentation** – Using docstrings and Markdown explanations to document the code and analytical decisions.

Additional advanced analysis:

- Developing a more comprehensive analysis class.
- Applying multiple regression or another advanced analytical method.
- Providing further justification of methodological choices and referencing relevant documentation.

## Technologies and Libraries

- **Python 3.14.7** – Main programming language.
- **Pandas** – Data manipulation and analysis.
- **NumPy** – Numerical computing and statistical simulations.
- **Matplotlib & Seaborn** – Data visualization.
- **SciPy** – Statistical methods and hypothesis testing.
- **Jupyter Notebook** – Interactive analysis and documentation.

## Visualization Standards

All charts and visualizations follow my [Data Visualization Policy](https://github.com/Hakan-Fridlund/PYSTDA45-assignment_health_study/blob/del1/visualization_policy.md), with a focus on accessibility, inclusivity, readability, and scientific integrity.

## Repository Structure

```text
health-study/
│
├── data/
│   └── health_study_dataset.csv
│
├── notebooks/
│   ├── health_study_part1.ipynb
│   └── health_study_part2.ipynb
│
├── src/
│   ├── __init__.py
│   └── health_analyzer.py
│
├── tests/
│   └── ...
│
├── README.md
└── requirements.txt
```

*Note: The structure may evolve as the project develops.*

## Getting Started

### Prerequisites

- Python 3.14.7
- Git
- Jupyter Notebook or Visual Studio Code with the Jupyter extension

### Installation

**1. Clone the repository:**

```bash
git clone <repository-url>
```

**2. Navigate to the project directory:**

```bash
cd health-study
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

Start Jupyter Notebook:

```bash
jupyter notebook
```

Run the notebook cells sequentially to reproduce the analysis, statistical calculations, simulations, and visualizations.

## Reproducibility

Random seeds are used in simulations to ensure reproducibility and consistent results across runs.

All analysis, code, visualizations, and explanations are documented directly in the Jupyter Notebooks.

## Author

Håkan Fridlund

Individual course assignment – Health Study Analysis.
