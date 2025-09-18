from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import csv
import importlib

# metrics 모듈의 후보 함수들 (있는 것만 사용)
CANDIDATES = [
    ("Mean", "mean"),
    ("Median", "median"),
    ("Min", "min_value"),
    ("Max", "max_value"),
    ("Std Dev (population)", "stdev"),
]


def read_values(csv_path: Path) -> list[float]:
    vals: list[float] = []
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if "value" not in (reader.fieldnames or []):
            # 스키마가 아니면 건너뜁니다.
            return []
        for row in reader:
            try:
                vals.append(float(row["value"]))
            except (TypeError, ValueError):
                # 숫자 변환 실패 행은 무시(학생 실습 편의)
                continue
    return vals


def find_csvs(data_dir: Path) -> list[Path]:
    return sorted(data_dir.glob("*.csv"))


def rows_for_values(metrics_mod, values: list[float]) -> str:
    if not values:
        return '<tr><td colspan="2">No valid numeric rows</td></tr>'
    rows = []
    for label, func_name in CANDIDATES:
        if hasattr(metrics_mod, func_name):
            fn = getattr(metrics_mod, func_name)
            try:
                val = fn(values)
                if val is None:
                    disp = "-"
                elif isinstance(val, float):
                    disp = f"{val:.4f}"
                else:
                    disp = str(val)
            except Exception as e:
                disp = f"ERROR: {e}"
            rows.append(f"<tr><th>{label}</th><td>{disp}</td></tr>")
    return "\n".join(rows)


def build_table_html(filename: str, body_rows_html: str) -> str:
    return f"""
    <div class=\"card\">
      <div class=\"filename\">{filename}</div>
      <table>
        <tbody>
          {body_rows_html}
        </tbody>
      </table>
    </div>
    """


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    data_dir = repo / "data"
    tpl_path = repo / "docs" / "index.template.html"
    out_dir = repo / "site"
    out_dir.mkdir(parents=True, exist_ok=True)

    # src.metrics 동적 임포트
    import sys
    sys.path.insert(0, str(repo))
    metrics_mod = importlib.import_module("src.metrics")

    tables_html_parts: list[str] = []
    for csv_path in find_csvs(data_dir):
        values = read_values(csv_path)
        body_rows = rows_for_values(metrics_mod, values)
        tables_html_parts.append(build_table_html(csv_path.name, body_rows))

    html = tpl_path.read_text(encoding="utf-8")
    html = html.replace("{{TABLES}}", "\n".join(tables_html_parts) if tables_html_parts else "<p>No CSV files found.</p>")

    updated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    html = html.replace("{{UPDATED_AT}}", updated_at)

    (out_dir / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
