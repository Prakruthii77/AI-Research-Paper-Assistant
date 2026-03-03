from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def export_summary_to_pdf(result_text, output_path="summary_output.pdf"):
    pdf = canvas.Canvas(output_path, pagesize=letter)
    y = 750

    for line in result_text.split("\n"):
        pdf.drawString(40, y, line)
        y -= 20

        if y < 50:
            pdf.showPage()
            y = 750

    pdf.save()
    return output_path