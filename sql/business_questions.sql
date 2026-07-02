-- HR Analytics Business Questions
-- Run against data/processed/hr_attrition.sqlite after:
-- python src/run_analysis.py
-- python src/create_sqlite_db.py

-- 1. What is the overall attrition rate?
SELECT
    COUNT(*) AS total_employees,
    SUM(attrition_flag) AS attrition_count,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_attrition;

-- 2. What is the average employee tenure?
SELECT
    ROUND(AVG(years_at_company), 2) AS avg_employee_tenure_years
FROM hr_attrition;

-- 3. What is the department-wise retention rate?
SELECT
    department,
    COUNT(*) AS total_employees,
    SUM(retention_flag) AS retained_employees,
    ROUND(100.0 * SUM(retention_flag) / COUNT(*), 2) AS retention_rate_pct
FROM hr_attrition
GROUP BY department
ORDER BY retention_rate_pct DESC;

-- 4. Which departments have the highest attrition rate?
SELECT
    department,
    COUNT(*) AS total_employees,
    SUM(attrition_flag) AS attrition_count,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_attrition
GROUP BY department
ORDER BY attrition_rate_pct DESC;

-- 5. How does overtime affect attrition?
SELECT
    over_time,
    COUNT(*) AS total_employees,
    SUM(attrition_flag) AS attrition_count,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_attrition
GROUP BY over_time
ORDER BY attrition_rate_pct DESC;

-- 6. How does salary band affect attrition?
SELECT
    salary_band,
    COUNT(*) AS total_employees,
    ROUND(AVG(monthly_income), 2) AS avg_monthly_income,
    SUM(attrition_flag) AS attrition_count,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_attrition
GROUP BY salary_band
ORDER BY attrition_rate_pct DESC;

-- 7. Which job roles have the highest attrition rate?
SELECT
    job_role,
    COUNT(*) AS total_employees,
    SUM(attrition_flag) AS attrition_count,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_attrition
GROUP BY job_role
HAVING COUNT(*) >= 20
ORDER BY attrition_rate_pct DESC;

-- 8. How does job satisfaction relate to attrition?
SELECT
    job_satisfaction_label,
    COUNT(*) AS total_employees,
    SUM(attrition_flag) AS attrition_count,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_attrition
GROUP BY job_satisfaction_label
ORDER BY MIN(job_satisfaction);

-- 9. What is attrition by total experience band?
SELECT
    experience_band,
    COUNT(*) AS total_employees,
    SUM(attrition_flag) AS attrition_count,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_attrition
GROUP BY experience_band
ORDER BY MIN(total_working_years);

-- 10. What is attrition by tenure band?
SELECT
    tenure_band,
    COUNT(*) AS total_employees,
    SUM(attrition_flag) AS attrition_count,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_attrition
GROUP BY tenure_band
ORDER BY MIN(years_at_company);

-- 11. Which employee segments combine high attrition and meaningful population size?
SELECT
    department,
    job_role,
    salary_band,
    tenure_band,
    over_time,
    COUNT(*) AS total_employees,
    SUM(attrition_flag) AS attrition_count,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_attrition
GROUP BY department, job_role, salary_band, tenure_band, over_time
HAVING COUNT(*) >= 5
ORDER BY attrition_rate_pct DESC, total_employees DESC
LIMIT 20;

-- 12. Does distance from home show elevated attrition?
SELECT
    CASE
        WHEN distance_from_home <= 5 THEN '0-5'
        WHEN distance_from_home <= 10 THEN '6-10'
        WHEN distance_from_home <= 20 THEN '11-20'
        ELSE '21+'
    END AS distance_band,
    COUNT(*) AS total_employees,
    SUM(attrition_flag) AS attrition_count,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_attrition
GROUP BY distance_band
ORDER BY MIN(distance_from_home);

-- 13. Are employees with fewer promotions more likely to leave?
SELECT
    CASE
        WHEN years_since_last_promotion = 0 THEN 'Promoted this year'
        WHEN years_since_last_promotion BETWEEN 1 AND 2 THEN '1-2 years'
        WHEN years_since_last_promotion BETWEEN 3 AND 5 THEN '3-5 years'
        ELSE '6+ years'
    END AS promotion_recency,
    COUNT(*) AS total_employees,
    SUM(attrition_flag) AS attrition_count,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_attrition
GROUP BY promotion_recency
ORDER BY MIN(years_since_last_promotion);

-- 14. What is attrition by work-life balance?
SELECT
    work_life_balance_label,
    COUNT(*) AS total_employees,
    SUM(attrition_flag) AS attrition_count,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_attrition
GROUP BY work_life_balance_label
ORDER BY MIN(work_life_balance);

-- 15. Which active employees should HR prioritize for retention outreach?
SELECT
    employee_number,
    department,
    job_role,
    salary_band,
    tenure_band,
    job_satisfaction_label,
    work_life_balance_label,
    over_time,
    monthly_income,
    years_at_company,
    total_working_years
FROM hr_attrition
WHERE attrition = 'No'
  AND (
      over_time = 'Yes'
      OR salary_band = 'Low'
      OR job_satisfaction_label IN ('Low', 'Medium')
      OR tenure_band IN ('0-1 Years', '2-3 Years')
  )
ORDER BY
    CASE WHEN over_time = 'Yes' THEN 1 ELSE 0 END DESC,
    CASE WHEN salary_band = 'Low' THEN 1 ELSE 0 END DESC,
    years_at_company ASC,
    monthly_income ASC
LIMIT 50;
