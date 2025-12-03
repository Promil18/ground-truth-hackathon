import os
import polars as pl
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def configure_openai():
    """Checks for OpenAI API key."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Warning: OPENAI_API_KEY not found in environment variables. AI insights will be disabled.")
        return None
    return OpenAI(api_key=api_key)

def generate_narrative(df: pl.DataFrame) -> dict:
    """
    Generates a comprehensive narrative analysis of the data using OpenAI GPT-4o.
    Returns a dictionary with multiple analysis sections.
    """
    client = configure_openai()
    if not client:
        return {
            "executive_summary": "AI Insights unavailable (Missing API Key).",
            "key_findings": "",
            "statistical_overview": "",
            "risk_factors": "",
            "recommendations": ""
        }

    # Convert dataframe to string for context
    data_str = df.write_csv(separator=",")
    
    prompt = f"""
    You are an expert Medical Data Analyst specializing in cardiovascular health. Analyze the following Heart Disease dataset:
    
    {data_str}
    
    Provide a comprehensive analysis in the following sections:
    
    1. **EXECUTIVE SUMMARY** (3-4 sentences): Overview of the dataset and primary insights.
    
    2. **KEY FINDINGS** (4-5 bullet points): Most important discoveries, patterns, and trends in the data.
    
    3. **STATISTICAL OVERVIEW** (4-5 bullet points): Notable statistics about age distribution, gender distribution, cholesterol levels, blood pressure, heart rate, etc.
    
    4. **RISK FACTORS IDENTIFIED** (4-5 bullet points): Common risk factors observed in patients with heart disease, correlations between variables.
    
    5. **CLINICAL RECOMMENDATIONS** (4-5 bullet points): Professional recommendations based on the data for healthcare providers or further analysis needed.
    
    Format your response EXACTLY as follows, with clear section headers:
    
    ## EXECUTIVE SUMMARY
    [Your summary here]
    
    ## KEY FINDINGS
    - [Finding 1]
    - [Finding 2]
    ...
    
    ## STATISTICAL OVERVIEW
    - [Stat 1]
    - [Stat 2]
    ...
    
    ## RISK FACTORS IDENTIFIED
    - [Risk factor 1]
    - [Risk factor 2]
    ...
    
    ## CLINICAL RECOMMENDATIONS
    - [Recommendation 1]
    - [Recommendation 2]
    ...
    
    Keep the analysis professional, data-driven, and clinically relevant.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a medical data analysis expert specializing in cardiovascular health."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        # Parse the response into sections
        full_text = response.choices[0].message.content
        
        # Simple parsing - split by section headers
        sections = {
            "executive_summary": extract_section(full_text, "EXECUTIVE SUMMARY", "KEY FINDINGS"),
            "key_findings": extract_section(full_text, "KEY FINDINGS", "STATISTICAL OVERVIEW"),
            "statistical_overview": extract_section(full_text, "STATISTICAL OVERVIEW", "RISK FACTORS"),
            "risk_factors": extract_section(full_text, "RISK FACTORS", "CLINICAL RECOMMENDATIONS"),
            "recommendations": extract_section(full_text, "CLINICAL RECOMMENDATIONS", None)
        }
        
        return sections
        
    except Exception as e:
        return {
            "executive_summary": f"Error generating insights: {e}",
            "key_findings": "",
            "statistical_overview": "",
            "risk_factors": "",
            "recommendations": ""
        }

def extract_section(text: str, start_marker: str, end_marker: str = None) -> str:
    """Extract a section from the AI response text between markers."""
    try:
        start_idx = text.find(start_marker)
        if start_idx == -1:
            return ""
        
        start_idx = text.find("\n", start_idx) + 1
        
        if end_marker:
            end_idx = text.find(end_marker, start_idx)
            if end_idx == -1:
                return text[start_idx:].strip()
            return text[start_idx:end_idx].strip()
        else:
            return text[start_idx:].strip()
    except Exception:
        return ""
