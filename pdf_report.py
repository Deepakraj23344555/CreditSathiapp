from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

def generate_pdf_report(score, inputs, components):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Header
    c.setFont("Helvetica-Bold", 24)
    c.setFillColorRGB(0.04, 0.12, 0.22) # Navy
    c.drawString(50, 730, "CreditSaathi - Investor Grade Report")
    
    # Content
    c.setFont("Helvetica", 14)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.drawString(50, 680, f"Business Name: {inputs.get('name', 'N/A')}")
    c.drawString(50, 650, f"Turnover: Rs. {inputs.get('turnover', 0):,}")
    
    # Score
    c.setFont("Helvetica-Bold", 40)
    c.setFillColorRGB(0.08, 0.72, 0.65) # Teal
    c.drawString(50, 580, f"CRS Score: {score}/850")
    
    # Factors
    c.setFont("Helvetica-Bold", 16)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(50, 510, "Factor Breakdown:")
    
    y = 480
    c.setFont("Helvetica", 12)
    for k, v in components.items():
        c.drawString(50, y, f"- {k}: {v}% Performance")
        y -= 20
        
    c.drawString(50, y-40, "Generated securely by CreditSaathi AI Engine.")
    
    c.save()
    buffer.seek(0)
    return buffer
