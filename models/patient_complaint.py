from odoo import models, fields, api

class MainComplaint(models.Model):
    _name = "main.complaint"
    _description = "Main Complaint"

    date = fields.Datetime(string="Date", default=fields.Datetime.now)
    description = fields.Text(string="Details")

    patient_id = fields.Many2one("clinic.patient", string="Patient", required=True)
    vital_signs_ids = fields.One2many(
        'clinic.vital.signs',
        'main_complaint_id',
        string="Vital Signs"
    )
    def name_get(self):
        result = []
        for rec in self:
            name = rec.description or rec.date.strftime('%Y-%m-%d')
            if len(name) > 53:
                name = name[:50] + '...'
            result.append((rec.id, name))
        return result

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        patient_id = self.env.context.get('default_patient_id')
        if patient_id:
            defaults['patient_id'] = patient_id
        return defaults




# from odoo import models, fields, api
#
# class MainComplaint(models.Model):
#     _name = "main.complaint"
#     _description = "Main Complaint"
#
#     date = fields.Datetime(string="Date", default=fields.Datetime.now)
#     description = fields.Text(string="Details")
#
#     patient_id = fields.Many2one("clinic.patient", string="Patient", required=True)
#     vital_signs_ids = fields.One2many(
#         'clinic.vital.signs',
#         'main_complaint_id',
#         string="Vital Signs"
#     )
#     def name_get(self):
#         result = []
#         for rec in self:
#             name = f"{rec.date.strftime('%Y-%m-%d')} - {rec.description[:50]}" if rec.description else rec.date.strftime(
#                 '%Y-%m-%d')
#             result.append((rec.id, name))
#         return result
#
#     @api.model
#     def default_get(self, fields_list):
#         defaults = super().default_get(fields_list)
#         patient_id = self.env.context.get('default_patient_id')
#         if patient_id:
#             defaults['patient_id'] = patient_id
#         return defaults