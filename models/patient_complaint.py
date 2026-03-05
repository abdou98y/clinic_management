from odoo import models, fields, api

class MainComplaint(models.Model):
    _name = "main.complaint"
    _description = "Main Complaint"
    _rec_name = 'description'
    date = fields.Datetime(string="Date", default=fields.Datetime.now)
    description = fields.Text(string="Details")

    patient_id = fields.Many2one("clinic.patient", string="Patient", required=True)
    vital_signs_ids = fields.One2many(
        'clinic.vital.signs',
        'main_complaint_id',
        string="Vital Signs"
    )
    @api.depends('description', 'date')
    def _compute_display_name(self):
        """Compute display name for main complaint record."""
        for rec in self:
            name = rec.description or (rec.date.strftime('%Y-%m-%d') if rec.date else _("New Complaint"))
            if len(name) > 53:
                name = name[:50] + '...'
            rec.display_name = name

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        patient_id = self.env.context.get('default_patient_id')
        if patient_id:
            defaults['patient_id'] = patient_id
        return defaults

