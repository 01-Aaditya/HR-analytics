# Power BI Dashboard Build Guide

## Data Source

Load this file:

`data/processed/powerbi_hr_attrition_model.csv`

Use `hr_attrition` as the table name.

## Theme

Import `powerbi/hr_attrition_theme.json`.

## Page 1: Executive Overview

Purpose: give HR leaders a fast view of attrition scale and priority areas.

Recommended visuals:

- KPI cards: Total Employees, Attrition Count, Attrition Rate, Retention Rate, Average Employee Tenure.
- Clustered bar chart: Attrition Rate by Department.
- Clustered bar chart: Attrition Rate by Overtime.
- Bar chart: Attrition Rate by Salary Band.
- Slicers: Department, Job Role, Gender, Salary Band, Tenure Band, Over Time.

Layout:

- Top row: KPI cards.
- Middle left: Department attrition.
- Middle right: Overtime impact.
- Bottom: Salary band attrition and filter slicers.

## Page 2: Attrition Drivers

Purpose: explain which factors are associated with attrition.

Recommended visuals:

- Bar chart: Attrition Rate by Job Satisfaction Label.
- Bar chart: Attrition Rate by Experience Band.
- Bar chart: Attrition Rate by Tenure Band.
- Scatter plot: Monthly Income vs Total Working Years, colored by Attrition.
- Matrix: Department by Salary Band with Attrition Rate.

## Page 3: Employee Segmentation

Purpose: help HR identify retention intervention groups.

Recommended visuals:

- Matrix: Department, Job Role, Salary Band, Tenure Band, Over Time.
- Conditional formatting: Attrition Rate.
- Table: Employee Number, Department, Job Role, Salary Band, Tenure Band, Job Satisfaction Label, Work Life Balance Label, Over Time.
- Slicers for department, job role, overtime, satisfaction, and salary band.

## Design Notes

- Use percent formatting for attrition and retention measures.
- Sort salary bands manually: Low, Lower-Mid, Upper-Mid, High.
- Sort satisfaction labels manually: Low, Medium, High, Very High.
- Keep the dashboard focused on business decisions: where attrition is happening, why it may be happening, and what HR should do next.

## Suggested Dashboard Title

HR Attrition and Retention Dashboard
