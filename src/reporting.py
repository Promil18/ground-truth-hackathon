from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import inch
import polars as pl
import re
import matplotlib.pyplot as plt
import os

def create_diagnosis_chart(df: pl.DataFrame) -> str:
    """Creates a pie chart showing heart disease distribution."""

    diagnosis_col = None
    if 'Diagnosis' in df.columns:
        diagnosis_col = 'Diagnosis'
    elif 'target' in df.columns:
        diagnosis_col = 'target'
        df = df.with_columns(
            pl.when(pl.col("target") == 1).then(pl.lit("Heart Disease"))
            .when(pl.col("target") == 0).then(pl.lit("No Disease"))
            .otherwise(pl.col("target").cast(pl.Utf8)).alias("diagnosis_display")
        )
        diagnosis_col = 'diagnosis_display'
    else:
        print("Warning: Neither 'Diagnosis' nor 'target' column found.")
        return None

    diagnosis_counts = df.group_by(diagnosis_col).agg(pl.count()).sort(diagnosis_col)
    labels = diagnosis_counts[diagnosis_col].to_list()
    sizes = diagnosis_counts['count'].to_list()
    
    fig, ax = plt.subplots(figsize=(7, 5))
    colors_list = ['#4ECDC4', '#FF6B6B']  
    
    wedges, texts, autotexts = ax.pie(
        sizes, 
        labels=labels, 
        autopct='%1.1f%%',
        startangle=90,
        colors=colors_list,
        textprops={'fontsize': 12, 'weight': 'bold'}
    )
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(14)
        autotext.set_weight('bold')
    
    ax.axis('equal')
    plt.title('Heart Disease Distribution in Dataset\n(Total Patients: {})'.format(sum(sizes)), 
              fontsize=14, weight='bold', pad=20)
    
    chart_path = 'diagnosis_distribution.png'
    plt.savefig(chart_path, bbox_inches='tight', dpi=150, facecolor='white')
    plt.close()
    
    return chart_path


def format_markdown(text):
    """
    Converts basic markdown to ReportLab XML tags.
    Handles bold (**text**), bullet points, and removes markdown headers.
    """
    if not text:
        return ""
    
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    

    text = re.sub(r'^\s*#{1,6}\s*$', '', text, flags=re.MULTILINE)
    
    text = re.sub(r'^##\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^#\s+', '', text, flags=re.MULTILINE)
    
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    
    text = re.sub(r'^-\s+', '• ', text, flags=re.MULTILINE)
    
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    
    text = text.replace('\n', '<br/>')
    
    return text


def create_pdf_report(data: pl.DataFrame, insights: str, output_path: str = "output_report.pdf", full_data: pl.DataFrame = None):
    """
    Creates a professional PDF report with the data and insights using ReportLab.
    Automatically switches to Landscape if data is wide.
    
    Args:
        data: Aggregated/processed data for the table
        insights: AI-generated insights (string or dict)
        output_path: Path to save the PDF
        full_data: Full dataset for chart generation (optional)
    """
    num_cols = len(data.columns)
    if num_cols > 8:
        page_size = landscape(letter)
        page_width, page_height = landscape(letter)
    else:
        page_size = letter
        page_width, page_height = letter

    left_margin = 36
    right_margin = 36
    top_margin = 72
    bottom_margin = 36
    
    doc = SimpleDocTemplate(
        output_path, 
        pagesize=page_size,
        rightMargin=right_margin, leftMargin=left_margin,
        topMargin=top_margin, bottomMargin=bottom_margin
    )
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.HexColor("#2C3E50")
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=18,
        spaceBefore=20,
        spaceAfter=12,
        textColor=colors.HexColor("#34495E"),
        borderColor=colors.HexColor("#BDC3C7"),
        borderPadding=5,
        borderWidth=0,
        borderBottomWidth=1
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        leading=16,  
        spaceAfter=10,
        alignment=TA_LEFT, 
        leftIndent=0,
        bulletIndent=10
    )

    # Title
    elements.append(Paragraph("Heart Disease Analysis Report", title_style))
    elements.append(Paragraph("Automated Insights & Performance Metrics", styles['Normal']))
    elements.append(Spacer(1, 30))

  
    elements.append(Paragraph("Executive Summary", heading_style))
    
 
    if isinstance(insights, dict):

        exec_summary = insights.get("executive_summary", "")
        formatted_summary = format_markdown(exec_summary)
        elements.append(Paragraph(formatted_summary, body_style))
        elements.append(Spacer(1, 12))
        

        if insights.get("key_findings"):
            elements.append(Paragraph("Key Findings", heading_style))
            formatted_findings = format_markdown(insights["key_findings"])
            elements.append(Paragraph(formatted_findings, body_style))
            elements.append(Spacer(1, 12))
        

        if insights.get("statistical_overview"):
            elements.append(Paragraph("Statistical Overview", heading_style))
            formatted_stats = format_markdown(insights["statistical_overview"])
            elements.append(Paragraph(formatted_stats, body_style))
            elements.append(Spacer(1, 12))
    
        if insights.get("risk_factors"):
            elements.append(Paragraph("Risk Factors Identified", heading_style))
            formatted_risks = format_markdown(insights["risk_factors"])
            elements.append(Paragraph(formatted_risks, body_style))
            elements.append(Spacer(1, 12))
       
        if insights.get("recommendations"):
            elements.append(Paragraph("Clinical Recommendations", heading_style))
            formatted_recs = format_markdown(insights["recommendations"])
            elements.append(Paragraph(formatted_recs, body_style))
            elements.append(Spacer(1, 12))
    else:
        formatted_insights = format_markdown(insights)
        elements.append(Paragraph(formatted_insights, body_style))
        elements.append(Spacer(1, 20))

    if full_data is not None:
        try:
            chart_path = create_diagnosis_chart(full_data)
            if chart_path and os.path.exists(chart_path):
                elements.append(Paragraph("Heart Disease Distribution", heading_style))
                elements.append(Spacer(1, 12))
                img = Image(chart_path, width=5*inch, height=3.75*inch)
                elements.append(img)
                elements.append(Spacer(1, 12))
        except Exception as e:
            print(f"Warning: Could not generate chart: {e}")
    
    elements.append(Paragraph("Key Data Metrics (Top 20 Samples)", heading_style))
    elements.append(Spacer(1, 12))


    available_width = page_width - left_margin - right_margin
    col_width = available_width / num_cols
    

    font_size = 10
    if num_cols > 10:
        font_size = 8
    if num_cols > 15:
        font_size = 6
        
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontSize=font_size,
        alignment=TA_CENTER,
        textColor=colors.black,
        fontName='Helvetica-Bold'
    )
    
    header_row = [Paragraph(col, header_style) for col in data.columns]
    
    table_data = [header_row]
    for row in data.iter_rows():
        formatted_row = []
        for item in row:
            if isinstance(item, float):
                formatted_row.append(f"{item:.2f}")
            else:
                formatted_row.append(str(item))
        table_data.append(formatted_row)

    t = Table(table_data, colWidths=[col_width] * num_cols, repeatRows=1)
    
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        # FONTNAME/FONTSIZE for headers is handled by ParagraphStyle
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (1, 0), (-1, -1), [colors.whitesmoke, colors.white]),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), font_size),
    ]))
    elements.append(t)
    
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("AI Reporter", ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.gray, alignment=TA_CENTER)))

    doc.build(elements)
    print(f"PDF Report saved to {output_path}")
    return output_path
