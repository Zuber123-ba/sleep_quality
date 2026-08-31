import os
from datetime import datetime
from fpdf import FPDF

def generate_pdf(user_data, label, recommendations):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    REPORT_DIR = os.path.join(BASE_DIR, "reports")
    os.makedirs(REPORT_DIR, exist_ok=True)

    filename = f"sleep_report_{int(datetime.now().timestamp())}.pdf"
    filepath = os.path.join(REPORT_DIR, filename)

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Sleep Quality Report", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Sleep Quality: {label}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "User Inputs:", ln=True)

    pdf.set_font("Arial", size=11)
    for k, v in user_data.items():
        pdf.cell(0, 8, f"{k}: {v}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Recommendations:", ln=True)

    pdf.set_font("Arial", size=11)
    for r in recommendations:
        pdf.multi_cell(0, 8, f"- {r}")

    pdf.output(filepath)
    return filename
