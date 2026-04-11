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

def export_template_to_csv(template_data: dict) -> str:
    """Export template to CSV format."""
    output = StringIO()
    writer = csv.writer(output)
    
    writer.writerow(["Resume Template Generator - Export"])
    writer.writerow(["Generated:", template_data.get("timestamp", "N/A")])
    writer.writerow([])
    
    writer.writerow(["PROFESSIONAL SUMMARY"])
    writer.writerow([template_data.get("summary", "")])
    writer.writerow([])
    
    writer.writerow(["KEY RESUME SECTIONS"])
    sections = template_data.get("sections", [])
    for section in sections:
        writer.writerow([section])
    writer.writerow([])
    
    writer.writerow(["SUGGESTED ACHIEVEMENT BULLETS"])
    bullets = template_data.get("bullets", [])
    for i, bullet in enumerate(bullets, 1):
        writer.writerow([f"Bullet {i}", bullet])
    writer.writerow([])
    
    writer.writerow(["RECOMMENDED SKILLS"])
    skills = template_data.get("recommended_skills", [])
    for skill in skills:
        writer.writerow([skill])
    writer.writerow([])
    
    writer.writerow(["COVER LETTER OPENING"])
    writer.writerow([template_data.get("cover_letter", "")])
    
    return output.getvalue()

def export_template_to_pdf(template_data: dict) -> bytes:
    """Export template to PDF format."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=20,
        spaceBefore=12
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#764ba2'),
        spaceAfter=10,
        spaceBefore=10,
        borderPadding=5
    )
    
    story.append(Paragraph("Resume Template - Ready to Customize", title_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # Professional Summary
    story.append(Paragraph("Professional Summary", heading_style))
    summary = template_data.get("summary", "")
    story.append(Paragraph(summary if summary else "Add your professional summary here.", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))
    
    # Key Sections
    story.append(Paragraph("Key Resume Sections", heading_style))
    sections = template_data.get("sections", [])
    for section in sections:
        story.append(Paragraph(f"• {section}", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))
    
    # Achievement Bullets
    story.append(Paragraph("Suggested Achievement Bullets", heading_style))
    bullets = template_data.get("bullets", [])
    for bullet in bullets:
        story.append(Paragraph(f"✓ {bullet}", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))
    
    # Recommended Skills
    story.append(Paragraph("Recommended Skills", heading_style))
    skills = template_data.get("recommended_skills", [])
    skills_text = ", ".join(skills) if skills else "N/A"
    story.append(Paragraph(skills_text, styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))
    
    # Cover Letter Opening
    story.append(Paragraph("Cover Letter Opening", heading_style))
    cover_letter = template_data.get("cover_letter", "")
    story.append(Paragraph(cover_letter if cover_letter else "Add your cover letter here.", styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
