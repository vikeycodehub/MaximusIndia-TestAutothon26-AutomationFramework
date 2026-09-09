"""Build a complete Gajab testcase status report from CSV matrices and JUnit XML.

The report deliberately distinguishes automated results from checks that need
an inbox, payment-provider state, Android device, visual baseline, or manual
security review.
"""
from __future__ import annotations

import csv
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "framework" / "data"
REPORT_DIR = ROOT / "reports"
AUTOMATED_IDS = {
    "GJ-MAN-001", "GJ-MAN-005", "GJ-MAN-007", "GJ-MAN-008", "GJ-MAN-010",
    "GJ-MAN-011", "GJ-MAN-012", "GJ-MAN-013", "GJ-MAN-014", "GJ-MAN-040",
}


def load_cases() -> list[dict[str, str]]:
    cases: list[dict[str, str]] = []
    seen: set[str] = set()
    for path in (DATA_DIR / "gajab_manual_test_cases.csv", DATA_DIR / "gajab_extended_manual_test_cases.csv"):
        if not path.exists():
            continue
        with path.open(encoding="utf-8", newline="") as stream:
            for row in csv.DictReader(stream):
                case_id = (row.get("Test Case ID") or "").strip()
                if case_id and case_id not in seen:
                    row["Test Case ID"] = case_id
                    row["Source"] = path.name
                    cases.append(row)
                    seen.add(case_id)
    return cases


def junit_statuses(junit_path: Path) -> dict[str, str]:
    if not junit_path.exists():
        return {}
    statuses: dict[str, str] = {}
    root = ET.parse(junit_path).getroot()
    for testcase in root.iter("testcase"):
        name = testcase.get("name", "")
        for case_id in AUTOMATED_IDS:
            if case_id in name:
                if testcase.find("failure") is not None or testcase.find("error") is not None:
                    statuses[case_id] = "FAIL"
                elif testcase.find("skipped") is not None:
                    statuses[case_id] = "BLOCKED"
                else:
                    statuses[case_id] = "PASS"
    return statuses


def main() -> int:
    junit_path = Path(sys.argv[1]) if len(sys.argv) > 1 else REPORT_DIR / "gajab-junit.xml"
    cases = load_cases()
    observed = junit_statuses(junit_path)
    report_rows: list[dict[str, str]] = []
    for case in cases:
        case_id = case["Test Case ID"]
        status = observed.get(case_id, "NOT_RUN" if case_id in AUTOMATED_IDS else "MANUAL_REQUIRED")
        report_rows.append({
            "Test Case ID": case_id,
            "Area": case.get("Area", ""),
            "Priority": case.get("Priority", ""),
            "Test Case": case.get("Test Case", ""),
            "Automation Status": status,
            "Source": case.get("Source", ""),
        })

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = REPORT_DIR / "gajab-testcase-status.csv"
    json_path = REPORT_DIR / "gajab-testcase-status.json"
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(report_rows[0]) if report_rows else ["Test Case ID"])
        writer.writeheader()
        writer.writerows(report_rows)
    json_path.write_text(json.dumps(report_rows, indent=2), encoding="utf-8")

    counts: dict[str, int] = {}
    for row in report_rows:
        counts[row["Automation Status"]] = counts.get(row["Automation Status"], 0) + 1
    print(json.dumps({"total": len(report_rows), "counts": counts, "csv": str(csv_path), "json": str(json_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
