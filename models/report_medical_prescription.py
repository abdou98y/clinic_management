from odoo import models

class ReportMedicalPrescription(models.AbstractModel):
    _name = 'report.clinic_management.template_medical_prescription'
    _description = 'Medical Prescription Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['medical.prescription'].browse(docids)
        return {
            'doc': docs,  # This matches your template
        }
