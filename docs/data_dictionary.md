# Data Dictionary

The cleaned model uses snake_case column names and adds analysis-friendly features.

| Column | Description |
| --- | --- |
| age | Employee age |
| attrition | Whether the employee left the organization: Yes or No |
| business_travel | Business travel frequency |
| daily_rate | Daily pay rate proxy |
| department | Employee department |
| distance_from_home | Distance between employee home and workplace |
| education | Encoded education level |
| education_field | Employee education field |
| employee_number | Unique employee identifier |
| environment_satisfaction | Encoded environment satisfaction score |
| gender | Employee gender |
| hourly_rate | Hourly pay rate proxy |
| job_involvement | Encoded job involvement score |
| job_level | Employee job level |
| job_role | Employee job role |
| job_satisfaction | Encoded job satisfaction score |
| marital_status | Employee marital status |
| monthly_income | Monthly income |
| monthly_rate | Monthly pay rate proxy |
| num_companies_worked | Number of prior companies worked |
| over_time | Whether the employee works overtime |
| percent_salary_hike | Most recent salary hike percentage |
| performance_rating | Encoded performance rating |
| relationship_satisfaction | Encoded relationship satisfaction score |
| stock_option_level | Stock option level |
| total_working_years | Total years of work experience |
| training_times_last_year | Number of trainings attended last year |
| work_life_balance | Encoded work-life balance score |
| years_at_company | Years at current company |
| years_in_current_role | Years in current role |
| years_since_last_promotion | Years since last promotion |
| years_with_curr_manager | Years with current manager |
| attrition_flag | 1 if attrition is Yes, otherwise 0 |
| retention_flag | 1 if attrition is No, otherwise 0 |
| overtime_flag | 1 if overtime is Yes, otherwise 0 |
| salary_band | Quartile-based salary band |
| tenure_band | Years-at-company segment |
| experience_band | Total-working-years segment |
| age_band | Age segment |
| salary_to_level_ratio | Monthly income divided by job level |
| tenure_share_of_experience | Years at company divided by total working years |

Constant columns from the raw file were removed during cleaning: `employee_count`, `over18`, and `standard_hours`.
