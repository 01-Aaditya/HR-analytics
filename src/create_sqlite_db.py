from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
CLEAN_DATA = ROOT / "data" / "processed" / "hr_attrition_cleaned.csv"
DB_PATH = ROOT / "data" / "processed" / "hr_attrition.sqlite"


def main() -> None:
    if not CLEAN_DATA.exists():
        raise FileNotFoundError(
            "Run `python src/run_analysis.py` before creating the SQLite database."
        )

    df = pd.read_csv(CLEAN_DATA)
    with sqlite3.connect(DB_PATH) as connection:
        df.to_sql("hr_attrition", connection, if_exists="replace", index=False)

    print(f"SQLite database created at {DB_PATH}")
    print("Table: hr_attrition")


if __name__ == "__main__":
    main()
