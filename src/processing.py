import polars as pl

def clean_data(df: pl.DataFrame) -> pl.DataFrame:
    """
    Cleans the dataframe by handling nulls and ensuring correct types.
    """
    df = df.fill_null(0)
    
    if "Date" in df.columns:
        try:
            df = df.with_columns(pl.col("Date").str.to_date())
        except Exception:
            pass 

    return df

def aggregate_metrics(df: pl.DataFrame) -> pl.DataFrame:
    """
    Aggregates metrics.
    If AdTech columns are present, calculates AdTech KPIs.
    Otherwise, returns a summary of the dataset.
    """
    adtech_cols = ["Campaign_ID", "Impressions", "Clicks", "Spend", "Conversions"]
    if all(col in df.columns for col in adtech_cols):
        agg_df = df.group_by("Campaign_ID").agg([
            pl.col("Impressions").sum(),
            pl.col("Clicks").sum(),
            pl.col("Spend").sum(),
            pl.col("Conversions").sum()
        ])
        
        agg_df = agg_df.with_columns([
            (pl.col("Clicks") / pl.col("Impressions") * 100).alias("CTR"),
            (pl.col("Spend") / pl.col("Impressions") * 1000).alias("CPM"),
            (pl.col("Spend") / pl.col("Conversions")).alias("CPA")
        ])
        
        agg_df = agg_df.with_columns([
            pl.col("CTR").fill_nan(0).fill_null(0),
            pl.col("CPM").fill_nan(0).fill_null(0),
            pl.col("CPA").fill_nan(0).fill_null(0),
        ])
        return agg_df
    else:
        heart_disease_cols = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"]
        
        current_cols = [c.lower() for c in df.columns]
        if all(c in current_cols for c in heart_disease_cols):
            print("Heart Disease dataset detected. Applying meaningful names and value mappings...")
            
            df = df.with_columns(
                pl.when(pl.col("sex") == 1).then(pl.lit("Male"))
                .when(pl.col("sex") == 0).then(pl.lit("Female"))
                .otherwise(pl.col("sex").cast(pl.Utf8)).alias("sex")
            )
            
            df = df.with_columns(
                pl.when(pl.col("target") == 1).then(pl.lit("Heart Disease"))
                .when(pl.col("target") == 0).then(pl.lit("No Disease"))
                .otherwise(pl.col("target").cast(pl.Utf8)).alias("target")
            )
            
            df = df.with_columns(
                pl.when(pl.col("cp") == 0).then(pl.lit("Typ. Angina"))
                .when(pl.col("cp") == 1).then(pl.lit("Atyp. Angina"))
                .when(pl.col("cp") == 2).then(pl.lit("Non-anginal"))
                .when(pl.col("cp") == 3).then(pl.lit("Asymptomatic"))
                .otherwise(pl.col("cp").cast(pl.Utf8)).alias("cp")
            )
            
            df = df.with_columns(
                pl.when(pl.col("fbs") == 1).then(pl.lit("True"))
                .when(pl.col("fbs") == 0).then(pl.lit("False"))
                .otherwise(pl.col("fbs").cast(pl.Utf8)).alias("fbs")
            )
            
            df = df.with_columns(
                pl.when(pl.col("exang") == 1).then(pl.lit("Yes"))
                .when(pl.col("exang") == 0).then(pl.lit("No"))
                .otherwise(pl.col("exang").cast(pl.Utf8)).alias("exang")
            )

            df = df.rename({
                "age": "Age",
                "sex": "Sex",
                "cp": "Chest Pain Type",
                "trestbps": "Resting BP (mm Hg)",
                "chol": "Cholesterol (mg/dl)",
                "fbs": "Fasting BS > 120",
                "restecg": "Resting ECG",
                "thalach": "Max Heart Rate",
                "exang": "Exercise Angina",
                "oldpeak": "ST Depression",
                "slope": "ST Slope",
                "ca": "Major Vessels (0-3)",
                "thal": "Thalassemia",
                "target": "Diagnosis"
            })
            
        print("Generic dataset detected. Returning top 20 rows.")
        return df.head(20)
