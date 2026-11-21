import os
import json
import copy

# Override with the GEMINI_MODEL environment variable or the --model option
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")


def generate_report(eda_summary: dict, model: str = DEFAULT_MODEL) -> str:
    """
    Sends EDA summary to Gemini API and returns a professional
    narrative report with business insights.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "❌ GEMINI_API_KEY not set.\n"
            "Get your free key at: https://aistudio.google.com/app/apikey\n"
            "Then run: export GEMINI_API_KEY='your_key_here'"
        )

    from google import genai  # imported here so --eda-only works without the SDK

    client = genai.Client(api_key=api_key)

    # Reduce summary size to stay within free tier token limits
    light_summary = copy.deepcopy(eda_summary)
    if "numeric_stats" in light_summary:
        for col, stats in light_summary["numeric_stats"].items():
            light_summary["numeric_stats"][col] = {
                k: v for k, v in stats.items()
                if k in ["mean", "std", "min", "max", "50%"]
            }
    # Limit top_5 in categorical to top 3
    if "categorical_stats" in light_summary:
        for col in light_summary["categorical_stats"]:
            if "top_5" in light_summary["categorical_stats"][col]:
                top = light_summary["categorical_stats"][col]["top_5"]
                light_summary["categorical_stats"][col]["top_5"] = dict(
                    list(top.items())[:3]
                )

    prompt = f"""
You are a senior data analyst writing a professional business intelligence report.

Below is a structured EDA (Exploratory Data Analysis) summary of a dataset.
Your task is to generate a clear, insightful, and professional report in Markdown format.

## EDA Summary:
{json.dumps(light_summary, indent=2, default=str)}

## Report Requirements:
1. Start with an **Executive Summary** (3-4 sentences overview of the dataset)
2. **Dataset Overview** — describe what the data contains, size, structure
3. **Data Quality Assessment** — missing values, duplicates, outliers
4. **Key Statistical Findings** — highlight the most relevant numeric stats
5. **Categorical Insights** — patterns in categorical variables
6. **Correlation Analysis** — explain any notable relationships between variables
7. **Business Insights & Recommendations** — at least 3 actionable insights based on the data
8. **Suggested Next Steps** — what analysis or ML models would be appropriate

## Style Guidelines:
- Write in professional English
- Use clear section headers with ## and ###
- Use bullet points for lists
- Bold **key terms and metrics**
- Be specific — reference actual column names and numbers from the summary
- Avoid generic filler text; every sentence should add value
- End with a brief conclusion paragraph

Generate the full report now:
"""

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )
    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")
    return response.text
