# AI Data Analyst — Automated EDA Report Generator

A Python tool that performs **Exploratory Data Analysis (EDA)** on any CSV dataset and uses **Google Gemini AI** to generate a professional, narrative business intelligence report automatically.

---

## 🎯 What it does

1. Loads any CSV dataset
2. Automatically analyzes: shape, types, missing values, duplicates, outliers, correlations, class balance
3. Sends the structured summary to **Gemini 1.5 Flash**
4. Receives a professional Markdown report with business insights and recommendations
5. Saves the report as `report_output.md`

---

## 🧠 Why this matters

Manual EDA is repetitive. This tool accelerates the first step of any data project — turning raw data into actionable narratives in seconds. Ideal for business analysts, data engineers, and BI teams who need fast, documented insights.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.8+ | Core language |
| pandas | Data loading and analysis |
| numpy | Numeric operations |
| Google Gemini API | AI report generation |

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/samuel-salazarC/ai-data-analyst.git
cd ai-data-analyst
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get your free Gemini API key

1. Go to [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key

### 4. Set your API key as environment variable

```bash
export GEMINI_API_KEY="your_api_key_here"
```

On Windows:
```cmd
set GEMINI_API_KEY=your_api_key_here
```

---

## 🚀 Usage

```bash
# With default dataset
python main.py

# With your own dataset
python main.py path/to/your/data.csv
```

### Example output

```
🔍 Loading dataset: data/cybersecurity_intrusion_data.csv
============================================================
📊 Dataset shape: 10000 rows × 14 columns
🔎 Missing values: No missing values found
🔎 Duplicate rows: 0
🎯 Target column detected: 'attack_detected'
✅ EDA complete

🤖 Generating AI-powered report with Gemini...

✅ Report saved to: report_output.md
```

The generated report includes:
- Executive Summary
- Dataset Overview
- Data Quality Assessment
- Key Statistical Findings
- Categorical Insights
- Correlation Analysis
- Business Insights & Recommendations
- Suggested Next Steps

---

## 📁 Project Structure

```
ai-data-analyst/
├── main.py              # Entry point — orchestrates EDA + report generation
├── eda.py               # EDA module — analyzes the dataset automatically
├── report_generator.py  # Gemini API integration — generates narrative report
├── requirements.txt     # Python dependencies
├── data/                # Place your CSV datasets here
└── report_output.md     # Generated report (created on run)
```

---

## 🔒 Security

- API key is loaded from environment variables — **never hardcoded**
- No sensitive data is committed to the repository
- `.gitignore` excludes all generated outputs and credentials

---

## 📌 Use Cases

- Rapid dataset profiling for BI teams
- First-pass analysis before building ML models
- Automated documentation of data quality
- Onboarding new datasets in data pipelines

---

## 👤 Author

**Samuel Salazar** — Data Science Engineering Student  
[GitHub](https://github.com/samuel-salazarC)
