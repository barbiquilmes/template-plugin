import csv
import os
import statistics

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("csv-tools")


@mcp.tool()
def describe_csv_file(path: str) -> dict:
    """Describe a CSV file with case_id and usd_amount columns.

    Returns row count, list of case_ids, and usd_amount statistics
    (total, min, max, mean).
    """
    if not os.path.exists(path):
        return {"error": f"File not found: {path}"}

    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        return {"error": "CSV file is empty"}

    columns = list(rows[0].keys())
    missing = {"case_id", "usd_amount"} - set(columns)
    if missing:
        return {"error": f"Missing required columns: {sorted(missing)}. Found: {columns}"}

    try:
        amounts = [float(r["usd_amount"]) for r in rows]
    except ValueError as e:
        return {"error": f"Invalid usd_amount value: {e}"}

    return {
        "row_count": len(rows),
        "columns": columns,
        "case_ids": [r["case_id"] for r in rows],
        "usd_amount": {
            "total": round(sum(amounts), 2),
            "min": round(min(amounts), 2),
            "max": round(max(amounts), 2),
            "mean": round(statistics.mean(amounts), 2),
        },
    }


if __name__ == "__main__":
    mcp.run()
