# File: clinic_management/controllers/auto_print.py
from odoo import http
from odoo.http import request
import base64

class PrescriptionPrintController(http.Controller):

    @http.route('/prescription/print/<int:doc_id>', type='http', auth='user', csrf=False)
    def prescription_auto_print(self, doc_id, **kw):
        report = request.env.ref('clinic_management.report_medical_prescription')

        pdf_content = report._render_qweb_pdf(
            report_ref='clinic_management.report_medical_prescription',
            res_ids=[doc_id]
        )[0]

        pdf_base64 = base64.b64encode(pdf_content).decode()

        # DO NOT USE f-string HERE
        html = (
            "<!DOCTYPE html>"
            "<html>"
            "<head>"
            "<meta charset='utf-8'/>"
            "<title>طباعة الروشتة</title>"
            "<style>"
            "body, html { margin:0; padding:0; height:100vh; overflow:hidden; }"
            "iframe { border:none; width:100%; height:100%; }"
            "</style>"
            "</head>"
            "<body>"
            "<iframe src='data:application/pdf;base64," + pdf_base64 + "'></iframe>"
            "</body>"
            "</html>"
        )

        return request.make_response(html, headers=[('Content-Type', 'text/html')])
