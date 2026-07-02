# Methodology

## 1. Data Cleaning

- Loaded the IBM HR attrition CSV with UTF-8 BOM handling.
- Standardized column names to snake_case.
- Removed duplicate rows.
- Removed constant columns that do not support analysis.
- Created binary flags for attrition, retention, and overtime.
- Added readable labels for satisfaction, education, work-life balance, and performance rating fields.

## 2. Feature Engineering

- Created salary quartiles: Low, Lower-Mid, Upper-Mid, High.
- Created tenure bands using `years_at_company`.
- Created experience bands using `total_working_years`.
- Created age bands for demographic slicing.
- Created `salary_to_level_ratio` and `tenure_share_of_experience` for additional analysis.

## 3. KPI Development

The project calculates:

- Total employees
- Attrition count
- Retained employee count
- Attrition rate
- Retention rate
- Average employee tenure
- Average monthly income
- Overtime attrition rate

## 4. Segmentation

Employees are segmented by:

- Department
- Job role
- Salary band
- Tenure band
- Overtime status

This allows HR teams to move from broad attrition reporting to targeted retention planning.

## 5. Analysis Areas

- Department-level attrition and retention
- Salary impact on attrition
- Overtime impact on attrition
- Job satisfaction trends
- Experience and tenure risk patterns
- Numeric feature correlations with attrition
