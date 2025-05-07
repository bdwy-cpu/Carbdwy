
from flask import Flask, request, send_file, send_from_directory
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfReader, PdfWriter
import io
import datetime
import os

app = Flask(__name__, static_folder='.', static_url_path='')

field_positions = {'insurance_start': (270, 253), 'insurance_end': (140, 253), 'issue_time': (330, 92), 'issue_date': (270, 92), 'insurance_price': (460, 108)}

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    data = request.json

    now = datetime.datetime.now()
    issue_date = data.get("issue_date") or now.strftime("%d/%m/%Y")
    issue_time = data.get("issue_time") or now.strftime("%H:%M")
    data["issue_date"] = issue_date
    data["issue_time"] = issue_time

    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=A4)

    for field, value in data.items():
        if field in field_positions:
            x, y = field_positions[field]
            c.drawString(x, y, str(value))
    c.save()
    packet.seek(0)

    overlay_pdf = PdfReader(packet)
    template_path = os.path.join(os.path.dirname(__file__), "template.pdf")
    template_pdf = PdfReader(template_path)
    writer = PdfWriter()

    base_page = template_pdf.pages[0]
    base_page.merge_page(overlay_pdf.pages[0])
    writer.add_page(base_page)

    output_stream = io.BytesIO()
    writer.write(output_stream)
    output_stream.seek(0)

    filename = f"insurance_{now.strftime('%Y%m%d_%H%M%S')}.pdf"
    return send_file(output_stream, as_attachment=True, download_name=filename, mimetype='application/pdf')

if __name__ == '__main__':
    app.run()
