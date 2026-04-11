import csv
import json
from io import StringIO, BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def export_to_csv(analysis_data: dict) -> str:
    """Export analysis results to CSV format."""
    output = StringIO()
    writer = csv.writer(output)
    
    writer.writerow(["Resume Analysis Results"])
    writer.writerow([])
    

    writer.writerow(["Extracted Information"])
    data = analysis_data.get("data", {})
    if not data.get("error"):
        for key, value in data.items():
            if isinstance(value, list):
                writer.writerow([key, ", ".join(str(v) for v in value)])
            else:
                writer.writerow([key, value])
    else:
        writer.writerow(["Status", "Unable to extract information"])
    
    writer.writerow([])
    
    writer.writerow(["ATS Score & Benchmarking"])
    writer.writerow(["Score", analysis_data.get("score", "N/A")])
    writer.writerow(["Rating", analysis_data.get("rating", "N/A")])
    writer.writerow(["Percentile", analysis_data.get("percentile", "N/A")])
    writer.writerow(["Industry Average", analysis_data.get("industry_average", "N/A")])
    writer.writerow(["Comparison", analysis_data.get("comparison", "N/A")])
    
    writer.writerow([])
    

    skill_gaps = analysis_data.get("skill_gaps", {})
    if skill_gaps and not skill_gaps.get("error"):
        writer.writerow(["Skill Gap Analysis"])
        writer.writerow(["Present Skills", ", ".join(skill_gaps.get("present_skills", []))])
        writer.writerow(["Required Skills", ", ".join(skill_gaps.get("required_skills", []))])
        writer.writerow(["Missing Skills", ", ".join(skill_gaps.get("missing_skills", []))])
        writer.writerow([])
    

    feedback = analysis_data.get("feedback", [])
    if feedback:
        writer.writerow(["Improvement Suggestions"])
        for i, suggestion in enumerate(feedback, 1):
            writer.writerow([f"Suggestion {i}", suggestion])
    
    return output.getvalue()

def export_to_pdf(analysis_data: dict) -> bytes:
    """Export analysis results to PDF format."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=30
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2d5aa8'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    
    story.append(Paragraph("Resume Analysis Report", title_style))
    story.append(Spacer(1, 0.2 * inch))
    
   
    story.append(Paragraph("ATS Score & Benchmarking", heading_style))
    score_data = [
        ["Metric", "Value"],
        ["Score", f"{analysis_data.get('score', 'N/A')}"],
        ["Rating", analysis_data.get("rating", "N/A")],
        ["Percentile", f"{analysis_data.get('percentile', 'N/A')}th"],
        ["Industry Average", f"{analysis_data.get('industry_average', 'N/A')}%"],
        ["Comparison", analysis_data.get("comparison", "N/A")]
    ]
    
    table = Table(score_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2d5aa8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(table)
    story.append(Spacer(1, 0.3 * inch))
    
 
    story.append(Paragraph("Extracted Information", heading_style))
    data = analysis_data.get("data", {})
    if data and not data.get("error"):
        data_rows = [["Field", "Value"]]
        for key, value in data.items():
            if isinstance(value, list):
                data_rows.append([key, ", ".join(str(v) for v in value)])
            else:
                data_rows.append([key, str(value)])
        
        table = Table(data_rows)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2d5aa8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
    else:
        story.append(Paragraph("Unable to extract information at this time.", styles['Normal']))
    
    story.append(Spacer(1, 0.3 * inch))
    

    skill_gaps = analysis_data.get("skill_gaps", {})
    if skill_gaps and not skill_gaps.get("error"):
        story.append(Paragraph("Skill Gap Analysis", heading_style))
        skill_text = f"""
        <b>Present Skills:</b> {', '.join(skill_gaps.get('present_skills', []))}<br/>
        <b>Required Skills:</b> {', '.join(skill_gaps.get('required_skills', [])[:10])}<br/>
        <b>Missing Skills:</b> {', '.join(skill_gaps.get('missing_skills', []))}
        """
        story.append(Paragraph(skill_text, styles['Normal']))
        story.append(Spacer(1, 0.3 * inch))
    
    
    feedback = analysis_data.get("feedback", [])
    if feedback:
        story.append(Paragraph("Improvement Suggestions", heading_style))
        for i, suggestion in enumerate(feedback, 1):
            story.append(Paragraph(f"<b>{i}.</b> {suggestion}", styles['Normal']))
            story.append(Spacer(1, 0.1 * inch))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
