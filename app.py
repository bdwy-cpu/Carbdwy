from flask import Flask, request, send_file, send_from_directory, jsonify
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfReader, PdfWriter
import io
import datetime
import os

app = Flask(__name__, static_folder='.', static_url_path='')

field_positions = {
    "policy_number": (100, 730),
    "license_number": (100, 710),
    "policy_holder_name": (100, 690),
    "id_number": (100, 670),
    "chassis_number": (100, 650),
    "vehicle_type": (100, 630),
    "manufacturer_model": (100, 610),
    "engine_volume": (100, 590),
    "manufacture_year": (100, 570),
    "passenger_count": (100, 550),
    "vehicle_class": (100, 530),
    "insurance_start": (100, 510),
    "insurance_end": (100, 490),
    "insurance_hour": (100, 470),
    "insurance_price": (100, 450)
}

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    data = request.json

    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=A4)

    for field, value in data.items():
        if field in field_positions:
            x, y = field_positions[field]
            c.drawString(x, y, str(value))
    c.save()
    packet.seek(0)

    overlay_pdf = PdfReader(packet)
    template_pdf = PdfReader("אסססססעד.pdf")
    writer = PdfWriter()

    base_page = template_pdf.pages[0]
    base_page.merge_page(overlay_pdf.pages[0])
    writer.add_page(base_page)

    output_stream = io.BytesIO()
    writer.write(output_stream)
    output_stream.seek(0)

    filename = f"insurance_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    return send_file(output_stream, as_attachment=True, download_name=filename, mimetype='application/pdf')

if __name__ == '__main__':
    app.run()
