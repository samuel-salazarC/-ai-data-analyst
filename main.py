import os
import sys
from eda import run_eda
from report_generator import generate_report

def main():
    # Default dataset path - can be passed as argument
    dataset_path = sys.argv[1] if len(sys.argv) > 1 else "netflix_titles.csv"

    if not os.path.exists(dataset_path):
        print(f"❌ Dataset not found at: {dataset_path}")
        print("Usage: python main.py <path_to_csv>")
        sys.exit(1)

    print(f"🔍 Loading dataset: {dataset_path}")
    print("=" * 60)

    # Run EDA
    eda_summary = run_eda(dataset_path)

    # Generate AI report
    print("\n🤖 Generating AI-powered report with Gemini...")
    report = generate_report(eda_summary)

    # Save report
    output_path = "report_output.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n✅ Report saved to: {output_path}")
    print("\n" + "=" * 60)
    print(report)

if __name__ == "__main__":
    main()
