# Dashboard Preview

Open `dashboard/index.html` in a browser to view the portfolio dashboard preview.

This is a static browser preview generated from the same processed outputs used for Power BI:

- `data/processed/kpis.csv`
- `data/processed/attrition_by_department.csv`
- `data/processed/attrition_by_overtime.csv`
- `data/processed/attrition_by_salary_band.csv`
- `data/processed/employee_segments.csv`
- `assets/images/*.png`

Regenerate it with:

```bash
python src/build_dashboard_preview.py
```

For the actual Power BI report, import `data/processed/powerbi_hr_attrition_model.csv` and follow `powerbi/dashboard_build_guide.md`.
