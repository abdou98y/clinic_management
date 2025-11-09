from odoo import models, fields,api



class LabResult(models.Model):
    _name = 'clinic.lab.result'
    _description = 'Lab Result'
    _rec_name = 'test_name'
    
    
    patient_id = fields.Many2one('clinic.patient', string='Patient', required=True)
    date = fields.Date(string='Date', default=fields.Date.today)
    test_name = fields.Char(string='Test Name')
    result_file = fields.Binary(string='Result File', attachment=True)  # For PDF or any binary
    result_image = fields.Image(string='Result Image')  # Optional, for images only
    notes = fields.Text(string='Notes')

