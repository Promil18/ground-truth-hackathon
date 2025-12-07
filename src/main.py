import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from ingestion import load_csv
from processing import clean_data, aggregate_metrics
from analysis import generate_narrative
from reporting import create_pdf_report

def main():
    print("Starting AdTech Reporting System...")
    

    data_path = os.path.join("data", "Heart.csv")
    output_path = "Heart_Disease_Analysis_Report.pdf"
    
    print(f"Loading data from {data_path}...")
    try:
        df = load_csv(data_path)
    except Exception as e:
        print(f"Failed to load data: {e}")
        return

    print("Processing data...")
    df_clean = clean_data(df)
    df_agg = aggregate_metrics(df_clean)
    print("Aggregated Data:")
    print(df_agg)

    print("Generating AI insights...")
    insights = generate_narrative(df_agg)
    print("Insights generated.")
    print(insights)

    print("Creating PDF report...")
    create_pdf_report(df_agg, insights, output_path, full_data=df_clean)
    print("Done!")

if __name__ == "__main__":
    main()
