# HR Attrition Analysis - Executive Summary

## KPI Snapshot

| KPI | Result |
| --- | ---: |
| Total employees analyzed | 1,470 |
| Attrition rate | 16.12% |
| Average employee tenure | 7.01 years |
| Highest-risk department | Sales (20.63% attrition) |

## Key Insights

1. Overall attrition is **16.12%**, meaning roughly one in six employees in this dataset left the organization.
2. **Sales** has the highest department-level attrition rate at **20.63%**.
3. Employees working overtime attrite at **30.53%**, compared with **10.44%** for employees without overtime.
4. The lowest salary quartile has **29.27%** attrition, compared with **10.33%** in the highest salary quartile.
5. Employees with low job satisfaction have **22.84%** attrition, making engagement and manager follow-up important retention levers.

## Strongest Numeric Relationships With Attrition

| feature                 |   correlation_with_attrition |
|:------------------------|-----------------------------:|
| overtime_flag           |                       0.2461 |
| total_working_years     |                      -0.1711 |
| job_level               |                      -0.1691 |
| years_in_current_role   |                      -0.1605 |
| monthly_income          |                      -0.1598 |
| age                     |                      -0.1592 |
| years_with_curr_manager |                      -0.1562 |
| stock_option_level      |                      -0.1371 |

## HR Recommendations

- Build a targeted retention program for high-risk departments and job roles before broad company-wide interventions.
- Monitor overtime load weekly and flag employees with sustained overtime for manager review.
- Review compensation competitiveness for lower salary bands, especially where overtime and low satisfaction overlap.
- Add structured stay interviews for employees in their first three years, where early-tenure attrition risk is highest.
- Track job satisfaction and work-life balance as leading indicators, not only as annual survey metrics.
