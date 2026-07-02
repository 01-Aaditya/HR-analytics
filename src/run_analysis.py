from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
RAW_DATA = ROOT / "data" / "raw" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
PROCESSED_DIR = ROOT / "data" / "processed"
IMAGE_DIR = ROOT / "assets" / "images"
DOCS_DIR = ROOT / "docs"


SATISFACTION_MAP = {
    1: "Low",
    2: "Medium",
    3: "High",
    4: "Very High",
}

EDUCATION_MAP = {
    1: "Below College",
    2: "College",
    3: "Bachelor",
    4: "Master",
    5: "Doctor",
}

PERFORMANCE_MAP = {
    1: "Low",
    2: "Good",
    3: "Excellent",
    4: "Outstanding",
}

WORK_LIFE_MAP = {
    1: "Bad",
    2: "Good",
    3: "Better",
    4: "Best",
}


def snake_case(name: str) -> str:
    chars: list[str] = []
    for index, char in enumerate(name.strip().replace("\ufeff", "")):
        if char.isupper() and index > 0 and name[index - 1] != "_":
            chars.append("_")
        chars.append(char.lower())
    return "".join(chars).replace("__", "_")


def ensure_dirs() -> None:
    for directory in [PROCESSED_DIR, IMAGE_DIR, DOCS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)


def load_data() -> pd.DataFrame:
    df = pd.read_csv(RAW_DATA, encoding="utf-8-sig")
    df.columns = [snake_case(column) for column in df.columns]
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned = cleaned.drop_duplicates()

    constant_columns = [
        column for column in cleaned.columns if cleaned[column].nunique(dropna=False) == 1
    ]
    cleaned = cleaned.drop(columns=constant_columns)

    cleaned["attrition_flag"] = np.where(cleaned["attrition"].eq("Yes"), 1, 0)
    cleaned["retention_flag"] = 1 - cleaned["attrition_flag"]
    cleaned["overtime_flag"] = np.where(cleaned["over_time"].eq("Yes"), 1, 0)

    cleaned["education_label"] = cleaned["education"].map(EDUCATION_MAP)
    cleaned["environment_satisfaction_label"] = cleaned[
        "environment_satisfaction"
    ].map(SATISFACTION_MAP)
    cleaned["job_satisfaction_label"] = cleaned["job_satisfaction"].map(
        SATISFACTION_MAP
    )
    cleaned["relationship_satisfaction_label"] = cleaned[
        "relationship_satisfaction"
    ].map(SATISFACTION_MAP)
    cleaned["work_life_balance_label"] = cleaned["work_life_balance"].map(
        WORK_LIFE_MAP
    )
    cleaned["performance_rating_label"] = cleaned["performance_rating"].map(
        PERFORMANCE_MAP
    )

    cleaned["salary_band"] = pd.qcut(
        cleaned["monthly_income"],
        q=4,
        labels=["Low", "Lower-Mid", "Upper-Mid", "High"],
    )
    cleaned["tenure_band"] = pd.cut(
        cleaned["years_at_company"],
        bins=[-1, 1, 3, 7, 15, 50],
        labels=["0-1 Years", "2-3 Years", "4-7 Years", "8-15 Years", "16+ Years"],
    )
    cleaned["experience_band"] = pd.cut(
        cleaned["total_working_years"],
        bins=[-1, 2, 5, 10, 20, 50],
        labels=["0-2 Years", "3-5 Years", "6-10 Years", "11-20 Years", "21+ Years"],
    )
    cleaned["age_band"] = pd.cut(
        cleaned["age"],
        bins=[17, 25, 35, 45, 55, 70],
        labels=["18-25", "26-35", "36-45", "46-55", "56+"],
    )

    cleaned["salary_to_level_ratio"] = (
        cleaned["monthly_income"] / cleaned["job_level"]
    ).round(2)
    cleaned["tenure_share_of_experience"] = np.where(
        cleaned["total_working_years"].gt(0),
        cleaned["years_at_company"] / cleaned["total_working_years"],
        0,
    ).round(3)

    return cleaned


def summarize_group(
    df: pd.DataFrame, group_cols: str | list[str], table_name: str
) -> pd.DataFrame:
    grouped = (
        df.groupby(group_cols, observed=True)
        .agg(
            employee_count=("employee_number", "count"),
            attrition_count=("attrition_flag", "sum"),
            retained_count=("retention_flag", "sum"),
            attrition_rate=("attrition_flag", "mean"),
            retention_rate=("retention_flag", "mean"),
            avg_monthly_income=("monthly_income", "mean"),
            avg_tenure=("years_at_company", "mean"),
            avg_total_experience=("total_working_years", "mean"),
        )
        .reset_index()
    )
    grouped["attrition_rate"] = (grouped["attrition_rate"] * 100).round(2)
    grouped["retention_rate"] = (grouped["retention_rate"] * 100).round(2)
    grouped["avg_monthly_income"] = grouped["avg_monthly_income"].round(2)
    grouped["avg_tenure"] = grouped["avg_tenure"].round(2)
    grouped["avg_total_experience"] = grouped["avg_total_experience"].round(2)
    grouped.to_csv(PROCESSED_DIR / f"{table_name}.csv", index=False)
    return grouped


def create_kpis(df: pd.DataFrame) -> pd.DataFrame:
    total_employees = len(df)
    attrition_count = int(df["attrition_flag"].sum())
    retained_count = int(df["retention_flag"].sum())
    kpis = pd.DataFrame(
        [
            ["Total Employees", total_employees, "employees"],
            ["Attrition Count", attrition_count, "employees"],
            ["Retained Employees", retained_count, "employees"],
            ["Attrition Rate", round(attrition_count / total_employees * 100, 2), "%"],
            ["Retention Rate", round(retained_count / total_employees * 100, 2), "%"],
            ["Average Employee Tenure", round(df["years_at_company"].mean(), 2), "years"],
            ["Average Monthly Income", round(df["monthly_income"].mean(), 2), "currency"],
            ["Overtime Attrition Rate", round(df.loc[df["over_time"].eq("Yes"), "attrition_flag"].mean() * 100, 2), "%"],
        ],
        columns=["kpi", "value", "unit"],
    )
    kpis.to_csv(PROCESSED_DIR / "kpis.csv", index=False)
    return kpis


def create_correlation_table(df: pd.DataFrame) -> pd.DataFrame:
    numeric_df = df.select_dtypes(include=["number"]).copy()
    leakage_columns = ["retention_flag"]
    numeric_df = numeric_df.drop(columns=leakage_columns, errors="ignore")
    correlations = (
        numeric_df.corr(numeric_only=True)["attrition_flag"]
        .drop("attrition_flag")
        .sort_values(key=lambda values: values.abs(), ascending=False)
        .reset_index()
    )
    correlations.columns = ["feature", "correlation_with_attrition"]
    correlations["correlation_with_attrition"] = correlations[
        "correlation_with_attrition"
    ].round(4)
    correlations.to_csv(PROCESSED_DIR / "feature_correlations.csv", index=False)
    return correlations


def save_bar_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    filename: str,
    hue: str | None = None,
    order: list[str] | None = None,
) -> None:
    plt.figure(figsize=(9, 5.2))
    if hue is None:
        sns.barplot(
            data=data,
            x=x,
            y=y,
            hue=x,
            order=order,
            palette="Set2",
            legend=False,
        )
    else:
        sns.barplot(data=data, x=x, y=y, hue=hue, order=order, palette="Set2")
    plt.title(title, fontsize=14, weight="bold")
    plt.ylabel("Attrition Rate (%)")
    plt.xlabel("")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(IMAGE_DIR / filename, dpi=180)
    plt.close()


def create_visuals(tables: dict[str, pd.DataFrame]) -> None:
    save_bar_chart(
        tables["department"],
        "department",
        "attrition_rate",
        "Attrition Rate by Department",
        "attrition_by_department.png",
    )
    save_bar_chart(
        tables["salary"],
        "salary_band",
        "attrition_rate",
        "Salary Impact on Attrition",
        "salary_impact.png",
        order=["Low", "Lower-Mid", "Upper-Mid", "High"],
    )
    save_bar_chart(
        tables["overtime"],
        "over_time",
        "attrition_rate",
        "Overtime Impact on Attrition",
        "overtime_impact.png",
    )
    save_bar_chart(
        tables["job_satisfaction"],
        "job_satisfaction_label",
        "attrition_rate",
        "Job Satisfaction and Attrition",
        "job_satisfaction_trends.png",
        order=["Low", "Medium", "High", "Very High"],
    )
    save_bar_chart(
        tables["experience"],
        "experience_band",
        "attrition_rate",
        "Experience vs Attrition",
        "experience_vs_attrition.png",
        order=["0-2 Years", "3-5 Years", "6-10 Years", "11-20 Years", "21+ Years"],
    )


def create_executive_summary(
    df: pd.DataFrame,
    kpis: pd.DataFrame,
    tables: dict[str, pd.DataFrame],
    correlations: pd.DataFrame,
) -> None:
    attrition_rate = kpis.loc[kpis["kpi"].eq("Attrition Rate"), "value"].iloc[0]
    avg_tenure = kpis.loc[kpis["kpi"].eq("Average Employee Tenure"), "value"].iloc[0]
    top_department = tables["department"].sort_values("attrition_rate", ascending=False).iloc[0]
    overtime_rates = tables["overtime"].set_index("over_time")["attrition_rate"]
    salary_low = tables["salary"].set_index("salary_band").loc["Low", "attrition_rate"]
    salary_high = tables["salary"].set_index("salary_band").loc["High", "attrition_rate"]
    satisfaction_low = tables["job_satisfaction"].set_index("job_satisfaction_label").loc[
        "Low", "attrition_rate"
    ]
    top_corr = correlations.head(8).to_markdown(index=False)

    summary = f"""# HR Attrition Analysis - Executive Summary

## KPI Snapshot

| KPI | Result |
| --- | ---: |
| Total employees analyzed | {len(df):,} |
| Attrition rate | {attrition_rate:.2f}% |
| Average employee tenure | {avg_tenure:.2f} years |
| Highest-risk department | {top_department['department']} ({top_department['attrition_rate']:.2f}% attrition) |

## Key Insights

1. Overall attrition is **{attrition_rate:.2f}%**, meaning roughly one in six employees in this dataset left the organization.
2. **{top_department['department']}** has the highest department-level attrition rate at **{top_department['attrition_rate']:.2f}%**.
3. Employees working overtime attrite at **{overtime_rates.get('Yes', 0):.2f}%**, compared with **{overtime_rates.get('No', 0):.2f}%** for employees without overtime.
4. The lowest salary quartile has **{salary_low:.2f}%** attrition, compared with **{salary_high:.2f}%** in the highest salary quartile.
5. Employees with low job satisfaction have **{satisfaction_low:.2f}%** attrition, making engagement and manager follow-up important retention levers.

## Strongest Numeric Relationships With Attrition

{top_corr}

## HR Recommendations

- Build a targeted retention program for high-risk departments and job roles before broad company-wide interventions.
- Monitor overtime load weekly and flag employees with sustained overtime for manager review.
- Review compensation competitiveness for lower salary bands, especially where overtime and low satisfaction overlap.
- Add structured stay interviews for employees in their first three years, where early-tenure attrition risk is highest.
- Track job satisfaction and work-life balance as leading indicators, not only as annual survey metrics.
"""
    (DOCS_DIR / "executive_summary.md").write_text(summary, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    raw = load_data()
    cleaned = clean_data(raw)

    cleaned.to_csv(PROCESSED_DIR / "hr_attrition_cleaned.csv", index=False)
    cleaned.to_csv(PROCESSED_DIR / "powerbi_hr_attrition_model.csv", index=False)

    kpis = create_kpis(cleaned)
    tables = {
        "department": summarize_group(cleaned, "department", "attrition_by_department"),
        "salary": summarize_group(cleaned, "salary_band", "attrition_by_salary_band"),
        "overtime": summarize_group(cleaned, "over_time", "attrition_by_overtime"),
        "job_satisfaction": summarize_group(
            cleaned, "job_satisfaction_label", "attrition_by_job_satisfaction"
        ),
        "experience": summarize_group(
            cleaned, "experience_band", "attrition_by_experience_band"
        ),
        "segments": summarize_group(
            cleaned,
            ["department", "job_role", "salary_band", "tenure_band", "over_time"],
            "employee_segments",
        ),
    }
    correlations = create_correlation_table(cleaned)
    create_visuals(tables)
    create_executive_summary(cleaned, kpis, tables, correlations)

    print("HR attrition analysis complete.")
    print(f"Cleaned data: {PROCESSED_DIR / 'hr_attrition_cleaned.csv'}")
    print(f"Power BI model: {PROCESSED_DIR / 'powerbi_hr_attrition_model.csv'}")
    print(f"Executive summary: {DOCS_DIR / 'executive_summary.md'}")


if __name__ == "__main__":
    main()
