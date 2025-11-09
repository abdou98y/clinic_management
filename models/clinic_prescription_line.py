from odoo import models, fields, api

class PrescriptionLine(models.Model):
    _name = "medical.prescription.line"
    _description = "Prescription Line"

    prescription_id = fields.Many2one('medical.prescription', string="Prescription", ondelete="cascade")
    treatment_id = fields.Many2one('medical.treatment', string="Treatment")
    treatment_name = fields.Char(string="Treatment Name (if new)")
    usage_ar = fields.Text(related='treatment_id.usage_ar', string="Usage (Arabic)", readonly=False)

    @api.model
    def create(self, vals):
        """If treatment name typed doesn’t exist, create it."""
        if not vals.get('treatment_id') and vals.get('treatment_name'):
            name = vals['treatment_name'].strip()
            treatment = self.env['medical.treatment'].search([('name', '=', name)], limit=1)
            if not treatment:
                treatment = self.env['medical.treatment'].create({'name': name})
            vals['treatment_id'] = treatment.id
        return super().create(vals)


# # -*- coding: utf-8 -*-
# 
# from odoo import models, fields, api, _
# from odoo.exceptions import ValidationError
# 
# 
# class ClinicPrescriptionLine(models.Model):
#     _name = 'clinic.prescription.line'
#     _description = 'Prescription Medication Line'
#     _order = 'sequence, id'
# 
#     # Reference Fields
#     prescription_id = fields.Many2one(
#         'clinic.prescription',
#         string='Prescription',
#         required=True,
#         ondelete='cascade'
#     )
#     
#     medication_id = fields.Many2one(
#         'clinic.medication',
#         string='Medication',
#         required=True,
#         domain=[('active', '=', True)]
#     )
#     
#     sequence = fields.Integer(
#         string='Sequence',
#         default=10,
#         help="Display order of medications"
#     )
# 
#     # Dosing Instructions
#     strength_prescribed = fields.Char(
#         string='Strength',
#         required=True,
#         help="Prescribed strength (e.g., '500mg', '10mg/ml')"
#     )
#     
#     dosage_form_prescribed = fields.Char(
#         string='Dosage Form',
#         required=True,
#         help="Prescribed dosage form"
#     )
#     
#     dose_amount = fields.Char(
#         string='Dose Amount',
#         required=True,
#         help="Amount per dose (e.g., '1 tablet', '5ml', '2 capsules')"
#     )
#     
#     frequency = fields.Selection([
#         ('once_daily', 'Once Daily'),
#         ('bid', 'Twice Daily (BID)'),
#         ('tid', 'Three Times Daily (TID)'),
#         ('qid', 'Four Times Daily (QID)'),
#         ('q4h', 'Every 4 Hours'),
#         ('q6h', 'Every 6 Hours'),
#         ('q8h', 'Every 8 Hours'),
#         ('q12h', 'Every 12 Hours'),
#         ('prn', 'As Needed (PRN)'),
#         ('weekly', 'Weekly'),
#         ('monthly', 'Monthly'),
#         ('custom', 'Custom Frequency')
#     ], string='Frequency', required=True, default='once_daily')
#     
#     frequency_text = fields.Char(
#         string='Custom Frequency',
#         help="Custom frequency description when 'Custom Frequency' is selected"
#     )
#     
#     route = fields.Selection([
#         ('oral', 'Oral'),
#         ('iv', 'Intravenous (IV)'),
#         ('im', 'Intramuscular (IM)'),
#         ('sc', 'Subcutaneous (SC)'),
#         ('topical', 'Topical'),
#         ('inhalation', 'Inhalation'),
#         ('rectal', 'Rectal'),
#         ('sublingual', 'Sublingual'),
#         ('nasal', 'Nasal'),
#         ('ophthalmic', 'Ophthalmic'),
#         ('otic', 'Otic'),
#         ('transdermal', 'Transdermal')
#     ], string='Route of Administration', default='oral')
#     
#     duration = fields.Char(
#         string='Duration',
#         required=True,
#         help="Treatment duration (e.g., '7 days', '30 days', '3 months')"
#     )
#     
#     duration_days = fields.Integer(
#         string='Duration (Days)',
#         help="Duration in days for calculations"
#     )
# 
#     # Quantity and Refills
#     quantity_prescribed = fields.Float(
#         string='Quantity',
#         required=True,
#         digits=(10, 2),
#         help="Total quantity prescribed"
#     )
#     
#     quantity_unit = fields.Selection([
#         ('tablets', 'Tablets'),
#         ('capsules', 'Capsules'),
#         ('ml', 'Milliliters (ml)'),
#         ('grams', 'Grams'),
#         ('units', 'Units'),
#         ('patches', 'Patches'),
#         ('inhalers', 'Inhalers'),
#         ('bottles', 'Bottles'),
#         ('tubes', 'Tubes'),
#         ('vials', 'Vials')
#     ], string='Quantity Unit', default='tablets')
#     
#     days_supply = fields.Integer(
#         string='Days Supply',
#         help="Expected days supply based on dosing"
#     )
#     
#     refills_authorized = fields.Integer(
#         string='Refills Authorized',
#         default=0,
#         help="Number of refills allowed"
#     )
#     
#     generic_substitution_allowed = fields.Boolean(
#         string='Generic Substitution Allowed',
#         default=True,
#         help="Allow pharmacist to substitute generic equivalent"
#     )
# 
#     # Special Instructions
#     special_instructions = fields.Text(
#         string='Special Instructions',
#         help="Additional instructions (e.g., 'Take with food', 'Take at bedtime')"
#     )
#     
#     patient_counseling = fields.Text(
#         string='Patient Counseling Points',
#         help="Important patient education points"
#     )
#     
#     monitoring_required = fields.Text(
#         string='Monitoring Required',
#         help="Required monitoring (e.g., 'Monitor blood pressure', 'Check liver function')"
#     )
#     
#     stop_date = fields.Date(
#         string='Stop Date',
#         help="Date to discontinue medication"
#     )
# 
#     # Clinical Checks
#     allergy_checked = fields.Boolean(
#         string='Allergy Checked',
#         default=False,
#         help="Allergy interaction verified"
#     )
#     
#     drug_interaction_checked = fields.Boolean(
#         string='Drug Interaction Checked',
#         default=False,
#         help="Drug interactions verified"
#     )
#     
#     dose_range_checked = fields.Boolean(
#         string='Dose Range Checked',
#         default=False,
#         help="Dose within normal range verified"
#     )
#     
#     duplicate_therapy_checked = fields.Boolean(
#         string='Duplicate Therapy Checked',
#         default=False,
#         help="Duplicate therapy verified"
#     )
# 
#     # Computed Fields
#     calculated_quantity = fields.Float(
#         string='Calculated Quantity',
#         compute='_compute_calculated_quantity',
#         help="Calculated quantity based on dosing"
#     )
#     
#     total_cost = fields.Float(
#         string='Total Cost',
#         compute='_compute_total_cost',
#         digits=(10, 2),
#         help="Total cost based on medication price"
#     )
#     
#     is_controlled_substance = fields.Boolean(
#         string='Controlled Substance',
#         related='medication_id.controlled_substance',
#         readonly=True
#     )
#     
#     controlled_schedule = fields.Selection(
#         related='medication_id.controlled_schedule',
#         readonly=True
#     )
# 
#     @api.depends('dose_amount', 'frequency', 'duration_days')
#     def _compute_calculated_quantity(self):
#         """Calculate total quantity based on dosing regimen."""
#         for line in self:
#             if not line.duration_days:
#                 line.calculated_quantity = 0
#                 continue
#             
#             # Extract numeric dose amount (simplified)
#             try:
#                 dose_numeric = float(''.join(filter(str.isdigit, line.dose_amount or '0')))
#             except:
#                 dose_numeric = 1
#             
#             # Map frequency to daily doses
#             frequency_map = {
#                 'once_daily': 1,
#                 'bid': 2,
#                 'tid': 3,
#                 'qid': 4,
#                 'q4h': 6,
#                 'q6h': 4,
#                 'q8h': 3,
#                 'q12h': 2,
#                 'prn': 1,  # Assume once daily for PRN
#                 'weekly': 1/7,
#                 'monthly': 1/30,
#                 'custom': 1
#             }
#             
#             daily_doses = frequency_map.get(line.frequency, 1)
#             line.calculated_quantity = dose_numeric * daily_doses * line.duration_days
# 
#     @api.depends('quantity_prescribed', 'medication_id.cost_per_unit')
#     def _compute_total_cost(self):
#         """Calculate total cost of prescribed medication."""
#         for line in self:
#             if line.quantity_prescribed and line.medication_id.cost_per_unit:
#                 line.total_cost = line.quantity_prescribed * line.medication_id.cost_per_unit
#             else:
#                 line.total_cost = 0
# 
#     @api.onchange('medication_id')
#     def _onchange_medication_id(self):
#         """Auto-populate fields when medication is selected."""
#         if self.medication_id:
#             # Set strength and dosage form from medication
#             self.strength_prescribed = self.medication_id.strength
#             form_dict = dict(self.medication_id._fields['dosage_form'].selection)
#             self.dosage_form_prescribed = form_dict.get(self.medication_id.dosage_form, '')
#             
#             # Set route of administration
#             self.route = self.medication_id.route_of_administration
#             
#             # Set default dose amount based on dosage form
#             if self.medication_id.dosage_form in ['tablet', 'capsule']:
#                 self.dose_amount = '1 tablet' if self.medication_id.dosage_form == 'tablet' else '1 capsule'
#                 self.quantity_unit = 'tablets' if self.medication_id.dosage_form == 'tablet' else 'capsules'
#             elif self.medication_id.dosage_form == 'syrup':
#                 self.dose_amount = '5ml'
#                 self.quantity_unit = 'ml'
#             
#             # Set patient counseling from medication info
#             if self.medication_id.side_effects:
#                 self.patient_counseling = f"Common side effects: {self.medication_id.side_effects[:200]}..."
# 
#     @api.onchange('frequency')
#     def _onchange_frequency(self):
#         """Clear custom frequency text when standard frequency is selected."""
#         if self.frequency != 'custom':
#             self.frequency_text = ''
# 
#     @api.onchange('duration')
#     def _onchange_duration(self):
#         """Extract duration in days from duration text."""
#         if self.duration:
#             # Simple extraction of numeric days (e.g., "7 days" -> 7)
#             import re
#             match = re.search(r'(\d+)', self.duration)
#             if match:
#                 days = int(match.group(1))
#                 # Adjust for different time units
#                 if 'week' in self.duration.lower():
#                     days *= 7
#                 elif 'month' in self.duration.lower():
#                     days *= 30
#                 elif 'year' in self.duration.lower():
#                     days *= 365
#                 self.duration_days = days
# 
#     @api.constrains('quantity_prescribed')
#     def _check_quantity_prescribed(self):
#         """Validate prescribed quantity is positive."""
#         for line in self:
#             if line.quantity_prescribed <= 0:
#                 raise ValidationError(_('Prescribed quantity must be positive.'))
# 
#     @api.constrains('refills_authorized')
#     def _check_refills_authorized(self):
#         """Validate refills for controlled substances."""
#         for line in self:
#             if line.medication_id.controlled_substance:
#                 schedule = line.medication_id.controlled_schedule
#                 if schedule in ['I', 'II'] and line.refills_authorized > 0:
#                     raise ValidationError(
#                         _('Schedule I and II controlled substances cannot have refills.')
#                     )
#                 elif schedule in ['III', 'IV', 'V'] and line.refills_authorized > 5:
#                     raise ValidationError(
#                         _('Schedule III-V controlled substances are limited to 5 refills.')
#                     )
# 
#     @api.constrains('duration_days')
#     def _check_duration_days(self):
#         """Validate duration is reasonable."""
#         for line in self:
#             if line.duration_days and (line.duration_days < 1 or line.duration_days > 365):
#                 raise ValidationError(_('Duration must be between 1 and 365 days.'))
# 
#     def get_frequency_display(self):
#         """Get human-readable frequency display."""
#         self.ensure_one()
#         if self.frequency == 'custom' and self.frequency_text:
#             return self.frequency_text
#         else:
#             return dict(self._fields['frequency'].selection)[self.frequency]
# 
#     def get_dosing_instructions(self):
#         """Get complete dosing instructions for prescription."""
#         self.ensure_one()
#         
#         instructions = []
#         
#         # Basic dosing
#         instructions.append(f"Take {self.dose_amount}")
#         
#         # Frequency
#         freq_display = self.get_frequency_display()
#         instructions.append(freq_display.lower())
#         
#         # Route if not oral
#         if self.route != 'oral':
#             route_display = dict(self._fields['route'].selection)[self.route]
#             instructions.append(f"({route_display.lower()})")
#         
#         # Duration
#         if self.duration:
#             instructions.append(f"for {self.duration}")
#         
#         # Special instructions
#         if self.special_instructions:
#             instructions.append(f"- {self.special_instructions}")
#         
#         return ' '.join(instructions)
# 
#     def check_drug_interactions(self):
#         """Check for drug interactions with other medications in prescription."""
#         self.ensure_one()
#         
#         other_medications = self.prescription_id.prescription_line_ids.filtered(
#             lambda l: l.id != self.id
#         ).mapped('medication_id')
#         
#         if not other_medications:
#             return []
#         
#         return self.medication_id.get_drug_interactions(other_medications.ids)
# 
#     def check_allergy_contraindication(self):
#         """Check if medication is contraindicated due to patient allergies."""
#         self.ensure_one()
#         
#         patient_allergies = self.prescription_id.patient_id.allergies
#         return self.medication_id.check_allergy_contraindication(patient_allergies)
# 
#     def get_dosing_recommendations(self):
#         """Get dosing recommendations based on patient parameters."""
#         self.ensure_one()
#         
#         patient = self.prescription_id.patient_id
#         return self.medication_id.get_dosing_recommendations(
#             patient_age=patient.age,
#             patient_weight=self.prescription_id.patient_weight
#         )
# 
#     def perform_clinical_checks(self):
#         """Perform all clinical safety checks for this medication line."""
#         self.ensure_one()
#         
#         checks_performed = {
#             'allergy_check': False,
#             'interaction_check': False,
#             'dose_range_check': False,
#             'duplicate_therapy_check': False
#         }
#         
#         warnings = []
#         errors = []
#         
#         # Allergy check
#         if self.check_allergy_contraindication():
#             errors.append(f"Patient is allergic to {self.medication_id.name}")
#         checks_performed['allergy_check'] = True
#         
#         # Drug interaction check
#         interactions = self.check_drug_interactions()
#         for interaction in interactions:
#             warnings.append(
#                 f"Potential interaction between {self.medication_id.name} and {interaction['medication'].name}"
#             )
#         checks_performed['interaction_check'] = True
#         
#         # Dose range check (simplified)
#         dosing_recs = self.get_dosing_recommendations()
#         if dosing_recs.get('max_daily_dose'):
#             warnings.append(f"Maximum daily dose: {dosing_recs['max_daily_dose']}")
#         checks_performed['dose_range_check'] = True
#         
#         # Duplicate therapy check
#         same_class_meds = self.prescription_id.prescription_line_ids.filtered(
#             lambda l: l.id != self.id and l.medication_id.drug_class == self.medication_id.drug_class
#         )
#         if same_class_meds:
#             warnings.append(f"Duplicate therapy: Multiple {self.medication_id.drug_class} medications")
#         checks_performed['duplicate_therapy_check'] = True
#         
#         # Update check flags
#         self.write(checks_performed)
#         
#         return {
#             'errors': errors,
#             'warnings': warnings,
#             'checks_performed': checks_performed
#         }
# 
#     def name_get(self):
#         """Custom name display for prescription lines."""
#         result = []
#         for record in self:
#             name = f"{record.medication_id.name} {record.strength_prescribed}"
#             if record.dose_amount and record.frequency:
#                 freq_display = record.get_frequency_display()
#                 name += f" - {record.dose_amount} {freq_display}"
#             result.append((record.id, name))
#         return result
# 
