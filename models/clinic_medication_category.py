# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ClinicMedicationCategory(models.Model):
    _name = 'clinic.medication.category'
    _description = 'Medication Category'
    _order = 'name'
    _parent_store = True

    name = fields.Char(
        string='Category Name',
        required=True,
        translate=True
    )
    
    parent_id = fields.Many2one(
        'clinic.medication.category',
        string='Parent Category',
        ondelete='cascade'
    )
    
    child_ids = fields.One2many(
        'clinic.medication.category',
        'parent_id',
        string='Child Categories'
    )
    
    parent_path = fields.Char(index=True)
    
    description = fields.Text(
        string='Description',
        help="Category description and usage guidelines"
    )
    
    active = fields.Boolean(
        string='Active',
        default=True
    )
    
    medication_count = fields.Integer(
        string='Medication Count',
        compute='_compute_medication_count'
    )
    

    @api.depends('name')
    def _compute_medication_count(self):
        """Count medications in this category."""
        for record in self:
            record.medication_count = self.env['clinic.medication'].search_count([
                ('category_id', '=', record.id)
            ])

    @api.constrains('parent_id')
    def _check_parent_recursion(self):
        """Prevent recursive parent relationships."""
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive categories.'))

    def name_get(self):
        """Display full category path."""
        result = []
        for record in self:
            names = []
            current = record
            while current:
                names.append(current.name)
                current = current.parent_id
            result.append((record.id, ' / '.join(reversed(names))))
        return result

