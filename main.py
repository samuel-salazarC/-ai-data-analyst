import argparse
import json
import os
import sys

from eda import run_eda
from report_generator import DEFAULT_MODEL, generate_report

DEFAULT_DATASET = os.path.join("data", "netflix_titles.csv")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run automatic EDA on a CSV file and generate a narrative report with Gemini."
    )
    parser.add_argument(
        "dataset",
        nargs="?",
        default=DEFAULT_DATASET,
        help=f"Path to the CSV file (default: {DEFAULT_DATASET})",
    )
    parser.add_argument(
        "-o", "--output",
        default="report_output.md",
        help="Where to save the generated report (default: report_output.md)",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Gemini model to use (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--eda-only",
        action="store_true",
        help="Skip the AI report and save the EDA summary as eda_summary.json (no API key needed)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if not os.path.exists(args.dataset):
        print(f"❌ Dataset not found at: {args.dataset}")
        print("Usage: python main.py <path_to_csv>")
        sys.exit(1)

    print(f"🔍 Loading dataset: {args.dataset}")
    print("=" * 60)

    eda_summary = run_eda(args.dataset)

    if args.eda_only:
        output_path = "eda_summary.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(eda_summary, f, indent=2, default=str, ensure_ascii=False)
        print(f"\n✅ EDA summary saved to: {output_path}")
        return

    print(f"\n🤖 Generating AI-powered report with Gemini ({args.model})...")
    try:
        report = generate_report(eda_summary, model=args.model)
    except EnvironmentError as error:
        print(error)
        sys.exit(1)
    except Exception as error:
        print(f"❌ Gemini request failed: {error}")
        print("Check your API key, the model name (--model) and your quota.")
        sys.exit(1)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n✅ Report saved to: {args.output}")
    print("\n" + "=" * 60)
    print(report)


if __name__ == "__main__":
    main()
