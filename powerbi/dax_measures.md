# Power BI DAX Measures

Import `data/processed/powerbi_hr_attrition_model.csv` into Power BI and name the table `hr_attrition`.

```DAX
Total Employees =
COUNTROWS(hr_attrition)
```

```DAX
Attrition Count =
CALCULATE(
    [Total Employees],
    hr_attrition[attrition] = "Yes"
)
```

```DAX
Retained Employees =
CALCULATE(
    [Total Employees],
    hr_attrition[attrition] = "No"
)
```

```DAX
Attrition Rate =
DIVIDE([Attrition Count], [Total Employees])
```

```DAX
Retention Rate =
DIVIDE([Retained Employees], [Total Employees])
```

```DAX
Average Employee Tenure =
AVERAGE(hr_attrition[years_at_company])
```

```DAX
Average Monthly Income =
AVERAGE(hr_attrition[monthly_income])
```

```DAX
Overtime Attrition Rate =
CALCULATE(
    [Attrition Rate],
    hr_attrition[over_time] = "Yes"
)
```

```DAX
Non-Overtime Attrition Rate =
CALCULATE(
    [Attrition Rate],
    hr_attrition[over_time] = "No"
)
```

```DAX
Department Retention Rate =
[Retention Rate]
```

```DAX
Attrition Risk Employees =
CALCULATE(
    [Total Employees],
    hr_attrition[attrition] = "No",
    hr_attrition[over_time] = "Yes"
)
```

Format `Attrition Rate`, `Retention Rate`, `Overtime Attrition Rate`, `Non-Overtime Attrition Rate`, and `Department Retention Rate` as percentages.
