from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
DASHBOARD_DIR = ROOT / "dashboard"
DASHBOARD_FILE = DASHBOARD_DIR / "index.html"


def pct(value: float) -> str:
    return f"{value:.2f}%"


def read_kpi(kpis: pd.DataFrame, name: str) -> float:
    return float(kpis.loc[kpis["kpi"].eq(name), "value"].iloc[0])


def build_rows(df: pd.DataFrame, columns: list[str]) -> str:
    rows = []
    for _, row in df.iterrows():
        cells = "".join(f"<td>{row[column]}</td>" for column in columns)
        rows.append(f"<tr>{cells}</tr>")
    return "\n".join(rows)


def main() -> None:
    DASHBOARD_DIR.mkdir(exist_ok=True)

    kpis = pd.read_csv(PROCESSED_DIR / "kpis.csv")
    departments = pd.read_csv(PROCESSED_DIR / "attrition_by_department.csv")
    overtime = pd.read_csv(PROCESSED_DIR / "attrition_by_overtime.csv")
    salary = pd.read_csv(PROCESSED_DIR / "attrition_by_salary_band.csv")
    segments = pd.read_csv(PROCESSED_DIR / "employee_segments.csv")

    total_employees = int(read_kpi(kpis, "Total Employees"))
    attrition_count = int(read_kpi(kpis, "Attrition Count"))
    attrition_rate = read_kpi(kpis, "Attrition Rate")
    retention_rate = read_kpi(kpis, "Retention Rate")
    avg_tenure = read_kpi(kpis, "Average Employee Tenure")
    overtime_attrition_rate = read_kpi(kpis, "Overtime Attrition Rate")

    top_department = departments.sort_values("attrition_rate", ascending=False).iloc[0]
    high_risk_segments = (
        segments[segments["employee_count"].ge(5)]
        .sort_values(["attrition_rate", "employee_count"], ascending=[False, False])
        .head(8)
        .copy()
    )

    segment_rows = build_rows(
        high_risk_segments[
            [
                "department",
                "job_role",
                "salary_band",
                "tenure_band",
                "over_time",
                "employee_count",
                "attrition_rate",
            ]
        ],
        [
            "department",
            "job_role",
            "salary_band",
            "tenure_band",
            "over_time",
            "employee_count",
            "attrition_rate",
        ],
    )

    department_rows = build_rows(
        departments.sort_values("attrition_rate", ascending=False)[
            ["department", "employee_count", "attrition_count", "retention_rate", "attrition_rate"]
        ],
        ["department", "employee_count", "attrition_count", "retention_rate", "attrition_rate"],
    )

    overtime_yes = overtime.set_index("over_time").loc["Yes", "attrition_rate"]
    overtime_no = overtime.set_index("over_time").loc["No", "attrition_rate"]
    low_salary = salary.set_index("salary_band").loc["Low", "attrition_rate"]
    high_salary = salary.set_index("salary_band").loc["High", "attrition_rate"]

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>HR Attrition and Retention Dashboard</title>
  <style>
    :root {{
      --ink: #1f2933;
      --muted: #64748b;
      --line: #d9e2ec;
      --panel: #ffffff;
      --page: #f6f8fb;
      --blue: #1f77b4;
      --red: #e15759;
      --green: #2f855a;
      --amber: #c27803;
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      color: var(--ink);
      background: var(--page);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.45;
    }}

    header {{
      background: #ffffff;
      border-bottom: 1px solid var(--line);
    }}

    .wrap {{
      width: min(1180px, calc(100% - 32px));
      margin: 0 auto;
    }}

    .topbar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
      padding: 22px 0;
    }}

    h1 {{
      margin: 0;
      font-size: 26px;
      line-height: 1.15;
      letter-spacing: 0;
    }}

    .subtitle {{
      margin: 6px 0 0;
      color: var(--muted);
      font-size: 14px;
    }}

    .badge {{
      display: inline-flex;
      align-items: center;
      min-height: 32px;
      padding: 6px 10px;
      border: 1px solid var(--line);
      border-radius: 6px;
      color: #334e68;
      background: #f8fafc;
      font-size: 13px;
      white-space: nowrap;
    }}

    main {{
      padding: 24px 0 38px;
    }}

    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 12px;
      margin-bottom: 18px;
    }}

    .kpi {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
      min-height: 104px;
    }}

    .kpi span {{
      display: block;
      color: var(--muted);
      font-size: 13px;
      margin-bottom: 10px;
    }}

    .kpi strong {{
      display: block;
      font-size: 28px;
      line-height: 1;
      letter-spacing: 0;
    }}

    .kpi small {{
      display: block;
      margin-top: 9px;
      color: var(--muted);
      font-size: 12px;
    }}

    .insights {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin-bottom: 18px;
    }}

    .insight {{
      background: var(--panel);
      border-left: 5px solid var(--blue);
      border-radius: 8px;
      padding: 14px 16px;
      border-top: 1px solid var(--line);
      border-right: 1px solid var(--line);
      border-bottom: 1px solid var(--line);
    }}

    .insight.risk {{
      border-left-color: var(--red);
    }}

    .insight.money {{
      border-left-color: var(--amber);
    }}

    .insight h2 {{
      margin: 0 0 8px;
      font-size: 15px;
      letter-spacing: 0;
    }}

    .insight p {{
      margin: 0;
      color: #334e68;
      font-size: 14px;
    }}

    .grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
      margin-bottom: 16px;
    }}

    .section {{
      margin-top: 16px;
    }}

    .panel {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
    }}

    .panel h2 {{
      margin: 0 0 12px;
      font-size: 17px;
      letter-spacing: 0;
    }}

    .chart {{
      display: block;
      width: 100%;
      height: auto;
      border: 1px solid #edf2f7;
      border-radius: 6px;
      background: #ffffff;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }}

    th,
    td {{
      padding: 10px 9px;
      border-bottom: 1px solid #e6edf5;
      text-align: left;
      vertical-align: top;
    }}

    th {{
      color: #334e68;
      background: #f8fafc;
      font-weight: 700;
      position: sticky;
      top: 0;
    }}

    .table-scroll {{
      max-height: 360px;
      overflow: auto;
      border: 1px solid #edf2f7;
      border-radius: 6px;
    }}

    .footer-note {{
      margin: 18px 0 0;
      color: var(--muted);
      font-size: 13px;
    }}

    @media (max-width: 980px) {{
      .kpi-grid {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }}

      .insights,
      .grid {{
        grid-template-columns: 1fr;
      }}

      .topbar {{
        align-items: flex-start;
        flex-direction: column;
      }}
    }}

    @media (max-width: 560px) {{
      .wrap {{
        width: min(100% - 20px, 1180px);
      }}

      .kpi-grid {{
        grid-template-columns: 1fr;
      }}

      h1 {{
        font-size: 22px;
      }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="wrap topbar">
      <div>
        <h1>HR Attrition and Retention Dashboard</h1>
        <p class="subtitle">IBM HR Analytics dataset | Python analysis preview for Power BI portfolio build</p>
      </div>
      <div class="badge">Generated from cleaned project data</div>
    </div>
  </header>

  <main class="wrap">
    <section class="kpi-grid" aria-label="KPI summary">
      <article class="kpi">
        <span>Total Employees</span>
        <strong>{total_employees:,}</strong>
        <small>Employee records analyzed</small>
      </article>
      <article class="kpi">
        <span>Attrition Count</span>
        <strong>{attrition_count}</strong>
        <small>Employees marked as attrited</small>
      </article>
      <article class="kpi">
        <span>Attrition Rate</span>
        <strong>{pct(attrition_rate)}</strong>
        <small>Overall attrition</small>
      </article>
      <article class="kpi">
        <span>Retention Rate</span>
        <strong>{pct(retention_rate)}</strong>
        <small>Employees retained</small>
      </article>
      <article class="kpi">
        <span>Average Tenure</span>
        <strong>{avg_tenure:.2f}</strong>
        <small>Years at company</small>
      </article>
    </section>

    <section class="insights" aria-label="Key insights">
      <article class="insight risk">
        <h2>Highest-Risk Department</h2>
        <p>{top_department["department"]} leads department attrition at {pct(float(top_department["attrition_rate"]))}.</p>
      </article>
      <article class="insight risk">
        <h2>Overtime Signal</h2>
        <p>Overtime employees attrite at {pct(overtime_attrition_rate)}, compared with {pct(float(overtime_no))} without overtime.</p>
      </article>
      <article class="insight money">
        <h2>Salary Impact</h2>
        <p>Low salary band attrition is {pct(float(low_salary))}, versus {pct(float(high_salary))} in the high salary band.</p>
      </article>
    </section>

    <section class="grid" aria-label="Core charts">
      <article class="panel">
        <h2>Attrition by Department</h2>
        <img class="chart" src="../assets/images/attrition_by_department.png" alt="Attrition rate by department">
      </article>
      <article class="panel">
        <h2>Overtime Impact</h2>
        <img class="chart" src="../assets/images/overtime_impact.png" alt="Attrition rate by overtime status">
      </article>
      <article class="panel">
        <h2>Salary Impact</h2>
        <img class="chart" src="../assets/images/salary_impact.png" alt="Attrition rate by salary band">
      </article>
      <article class="panel">
        <h2>Experience vs Attrition</h2>
        <img class="chart" src="../assets/images/experience_vs_attrition.png" alt="Attrition rate by experience band">
      </article>
    </section>

    <section class="grid section" aria-label="Additional analysis">
      <article class="panel">
        <h2>Job Satisfaction Trends</h2>
        <img class="chart" src="../assets/images/job_satisfaction_trends.png" alt="Attrition rate by job satisfaction">
      </article>
      <article class="panel">
        <h2>Department Retention Table</h2>
        <div class="table-scroll">
          <table>
            <thead>
              <tr>
                <th>Department</th>
                <th>Employees</th>
                <th>Attrition</th>
                <th>Retention %</th>
                <th>Attrition %</th>
              </tr>
            </thead>
            <tbody>
              {department_rows}
            </tbody>
          </table>
        </div>
      </article>
    </section>

    <section class="section panel" aria-label="High-risk segments">
      <h2>High-Risk Employee Segments</h2>
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th>Department</th>
              <th>Job Role</th>
              <th>Salary Band</th>
              <th>Tenure Band</th>
              <th>Overtime</th>
              <th>Employees</th>
              <th>Attrition %</th>
            </tr>
          </thead>
          <tbody>
            {segment_rows}
          </tbody>
        </table>
      </div>
    </section>

    <p class="footer-note">For the Power BI version, import <code>data/processed/powerbi_hr_attrition_model.csv</code>, apply the DAX measures in <code>powerbi/dax_measures.md</code>, and follow <code>powerbi/dashboard_build_guide.md</code>.</p>
  </main>
</body>
</html>
"""

    DASHBOARD_FILE.write_text(html, encoding="utf-8")
    print(f"Dashboard preview created: {DASHBOARD_FILE}")


if __name__ == "__main__":
    main()
