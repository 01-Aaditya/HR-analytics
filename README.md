# HR Analytics: Employee Attrition and Retention Analysis

## Business Problem

Employee attrition increases hiring cost, disrupts team continuity, and can signal deeper issues in workload, compensation, manager relationships, or career growth. This project analyzes employee attrition using the IBM HR Analytics Employee Attrition dataset to identify factors affecting retention and recommend practical actions for HR teams.

## Project Objectives

- Clean and prepare HR employee data for analysis.
- Build retention KPIs: attrition rate, average tenure, and department-wise retention.
- Analyze attrition by department, salary band, overtime, job satisfaction, and experience.
- Segment employees by department, role, tenure, salary band, and overtime status.
- Provide SQL queries for common HR business questions.
- Prepare a Power BI-ready data model, DAX measures, dashboard plan, and theme.
- Package the project for GitHub and LinkedIn portfolio presentation.

## Dataset

This project uses the IBM HR Analytics Employee Attrition & Performance dataset, a fictional employee dataset created by IBM data scientists and commonly distributed through Kaggle.

- Rows: 1,470 employees
- Raw columns: 35
- Target field: `Attrition`
- Source reference: https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset
- Local raw file: `data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv`

## Key Results

| Metric | Value |
| --- | ---: |
| Total employees | 1,470 |
| Attrition rate | 16.12% |
| Retention rate | 83.88% |
| Average employee tenure | 7.01 years |
| Highest attrition department | Sales, 20.63% |
| Overtime attrition rate | 30.53% |

## High-Impact Insights

- Sales has the highest department-level attrition rate at 20.63%.
- Employees working overtime attrite at 30.53%, almost three times the 10.44% rate for employees without overtime.
- Employees in the lowest salary quartile attrite at 29.27%, compared with 10.33% in the highest salary quartile.
- Low job satisfaction is associated with higher attrition at 22.84%.
- Early-career and lower-tenure employees show elevated risk, making onboarding and stay interviews important retention levers.

## Repository Structure

```text
hr-analytics-employee-attrition/
├── assets/images/                  # Generated analysis visuals
├── dashboard/                      # Static HTML dashboard preview
├── data/raw/                       # Original dataset
├── data/processed/                 # Cleaned data, KPI tables, segment outputs, SQLite DB
├── docs/                           # Project documentation and portfolio content
├── notebooks/                      # Notebook workflow notes
├── powerbi/                        # Dashboard guide, DAX measures, Power BI theme
├── sql/                            # Schema and HR business questions
├── src/                            # Reproducible Python scripts
├── .gitignore
├── README.md
└── requirements.txt
```

## How to Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/run_analysis.py
python src/create_sqlite_db.py
python src/build_dashboard_preview.py
```

## Outputs

- Cleaned dataset: `data/processed/hr_attrition_cleaned.csv`
- Power BI model CSV: `data/processed/powerbi_hr_attrition_model.csv`
- SQLite database: `data/processed/hr_attrition.sqlite`
- KPI table: `data/processed/kpis.csv`
- Employee segmentation table: `data/processed/employee_segments.csv`
- Executive summary: `docs/executive_summary.md`
- SQL queries: `sql/business_questions.sql`
- Power BI build guide: `powerbi/dashboard_build_guide.md`
- HTML dashboard preview: `dashboard/index.html` (open directly in a browser)

## Dashboard Preview Assets

Generated visuals are available in `assets/images/`:

- Attrition by department
- Salary impact
- Overtime impact
- Job satisfaction trends
- Experience vs attrition

## Recommended HR Actions

- Prioritize Sales retention initiatives and investigate role-specific workload drivers.
- Introduce overtime monitoring and manager intervention for sustained overtime.
- Review compensation competitiveness for lower salary bands.
- Use stay interviews for employees in their first three years.
- Track job satisfaction and work-life balance as operational retention signals.
