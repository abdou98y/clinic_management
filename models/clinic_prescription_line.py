from odoo import models, fields, api
import html

class PrescriptionLine(models.Model):
    _name = "medical.prescription.line"
    _description = "Prescription Line"

    prescription_id = fields.Many2one('medical.prescription', string="Prescription", ondelete="cascade")
    treatment_id = fields.Many2one('medical.treatment', string="Treatment")
    treatment_name = fields.Char(string="Treatment Name (if new)")
    usage_ar = fields.Text(related='treatment_id.usage_ar', string="Usage (Arabic)", readonly=False)
    usage_ar_html = fields.Text(string="Usage (HTML)", compute='_compute_usage_html')

    @api.depends('usage_ar')
    def _compute_usage_html(self):
        for line in self:
            line.usage_ar_html = html.escape(line.usage_ar or '')