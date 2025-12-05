from odoo import models, fields, api,_
import logging
from odoo.exceptions import UserError, ValidationError
_logger = logging.getLogger(__name__)



class Prescription(models.Model):
    _name = "medical.prescription"
    _description = "Prescription"

    name = fields.Char(  # Now computed
        string="Name",
        compute="_compute_name",
        store=True,  # Store for searching/sorting
        readonly=True,
    )

    treatment_line_ids = fields.One2many(
        'medical.prescription.line',
        'prescription_id',
        string="Treatments"
    )
    patient_id = fields.Many2one(
        'clinic.patient',
        store=True,
        string="Patient"
    )

    @api.depends('patient_id.name', 'create_date')  # Recompute if patient or create_date changes
    def _compute_name(self):
        for rec in self:
            if rec.patient_id and rec.create_date:
                date_str = rec.create_date.date().strftime('%Y-%m-%d')  # Date without time
                rec.name = f"{rec.patient_id.name} - Prescription - {date_str}"
            else:
                rec.name = "New Prescription"


    def name_get(self):
        result = []
        for rec in self:
            if rec.patient_id:
                name = f"{rec.patient_id.name} - Prescription"
            else:
                name = "New Prescription"
            result.append((rec.id, name))
        return result

    def action_print_prescription(self):
        self.ensure_one()

        if not self.patient_id or not self.patient_id.exists():
            raise UserError(_("Cannot print the prescription because no patient is assigned."))

        _logger.info("Printing prescription ID: %s | Patient: %s | Lines: %s",
                     self.id, self.patient_id.name, len(self.treatment_line_ids))

        return self.env.ref('clinic_management.report_medical_prescription').report_action(self)

    def open_auto_print(self):
        return {'type': 'ir.actions.act_url', 'target': 'new', 'url': f'/prescription/print/{self.id}'}