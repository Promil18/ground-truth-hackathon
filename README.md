# Heart Disease Analysis Reporter

An automated reporting system that ingests heart disease data, generates AI-powered medical insights, and produces professional PDF reports with data visualizations.

## Features

- **Heart Disease Data Analysis**: Specialized processing for cardiovascular health datasets
- **Smart Data Processing**: Automatically detects and processes heart disease data schemas
- **AI-Powered Medical Analysis**: Uses OpenAI GPT-4o to generate comprehensive medical insights across 5 sections:
  - Executive Summary
  - Key Findings
  - Statistical Overview
  - Risk Factors Identified
  - Clinical Recommendations
- **Data Visualization**: Pie chart showing disease distribution across the complete dataset
- **Professional PDF Reports**: Creates well-formatted PDF reports with:
  - Wrapped headers for readability
  - Meaningful column names and mapped values (e.g., Male/Female, Heart Disease/No Disease)
  - Landscape orientation for wide datasets
  - Comprehensive AI-generated medical insights
  - Interactive data visualization
  - Top 20 patient records table

## Special Features for Heart Disease Dataset

The system includes enhanced formatting for the **Heart Disease Dataset**, automatically:
- Mapping categorical values (e.g., Sex: 0/1 → Female/Male)
- Renaming columns to descriptive names (e.g., `trestbps` → `Resting BP (mm Hg)`)
- Converting chest pain types to readable labels (e.g., `Typ. Angina`, `Atyp. Angina`)

## Installation

1. **Clone or download** this repository

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up OpenAI API Key**:
   - Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
   - Create a `.env` file in the project root directory
   - Add your API key to the `.env` file:
     ```
     OPENAI_API_KEY=your-api-key-here
     ```
   - The `.env` file is already included in the project and will be automatically loaded

## Usage

1. **Place your CSV file** in the `data/` directory (default: `Heart.csv`)

2. **Run the system**:
   ```bash
   python src/main.py
   ```

3. **Check the output**: The PDF report will be saved as `Heart_Disease_Analysis_Report.pdf`

## Project Structure

```
adtech_reporter/
├── data/
│   └── Heart.csv                # Heart disease dataset (UCI)
├── src/
│   ├── __init__.py
│   ├── main.py                  # Main entry point
│   ├── ingestion.py             # Data loading
│   ├── processing.py            # Data cleaning and transformation
│   ├── analysis.py              # AI insight generation (OpenAI)
│   └── reporting.py             # PDF report creation with charts
├── .env                         # Environment variables (API key)
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Dependencies

- **openai**: AI-powered medical insights
- **reportlab**: PDF generation
- **matplotlib**: Chart visualization
- **polars**: Fast data processing
- **python-dotenv**: Environment variable management

## Example Output

The system generates a comprehensive PDF report containing:

1. **Title Section**: "Heart Disease Analysis Report"
2. **Executive Summary**: AI-generated overview and primary insights
3. **Key Findings**: Important discoveries, patterns, and trends (4-5 bullet points)
4. **Statistical Overview**: Notable statistics about age, gender, cholesterol, blood pressure, etc. (4-5 bullet points)
5. **Risk Factors Identified**: Common risk factors and correlations (4-5 bullet points)
6. **Clinical Recommendations**: Professional recommendations for healthcare providers (4-5 bullet points)
7. **Data Visualization**: Pie chart showing disease distribution across all 303 patients
8. **Data Table**: Top 20 patient records with formatted, readable values




