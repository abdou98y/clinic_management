from odoo import models, fields, api

class Treatment(models.Model):
    _name = "medical.treatment"
    _description = "Treatment"

    name = fields.Char(string="Treatment (English)", required=True, translate=True)
    usage_ar = fields.Text(string="Usage (Arabic)", translate=True)

    _sql_constraints = [
        ('unique_treatment_name', 'unique(name)', 'This treatment already exists!')
    ]



# # -*- coding: utf-8 -*-
#
# from odoo import models, fields, api, _
# from odoo.exceptions import ValidationError
#
#
# class ClinicMedication(models.Model):
#     _name = 'clinic.medication'
#     _description = 'Medication Database'
#     _order = 'name'
#     _rec_name = 'display_name'
#     _sql_constraints = [
#         ('name_strength_form_unique',
#          'UNIQUE(name, strength, dosage_form)',
#          'Medication with same name, strength and form already exists!')
#     ]
#
#     # Basic Drug Information
#     name = fields.Char(
#         string='Generic Name',
#         required=True,
#         help="Generic medication name (INN)"
#     )
#     brand_names = fields.Text(
#         string='Brand Names',
#         help="Commercial brand names (comma-separated)"
#     )
#     generic_name = fields.Char(
#         string='International Name',
#         help="International nonproprietary name (INN)"
#     )
#
#     # Drug Classification
#     drug_class = fields.Selection([
#         ('analgesic', 'Analgesics'),
#         ('antibiotic', 'Antibiotics'),
#         ('antihistamine', 'Antihistamines'),
#         ('antihypertensive', 'Antihypertensives'),
#         ('diabetes', 'Diabetes Medications'),
#         ('cardiovascular', 'Cardiovascular'),
#         ('respiratory', 'Respiratory'),
#         ('gastrointestinal', 'Gastrointestinal'),
#         ('neurological', 'Neurological'),
#         ('psychiatric', 'Psychiatric'),
#         ('dermatological', 'Dermatological'),
#         ('hormonal', 'Hormonal'),
#         ('immunological', 'Immunological'),
#         ('oncological', 'Oncological'),
#         ('other', 'Other')
#     ], string='Drug Class', required=True)
#
#     category_id = fields.Many2one(
#         'clinic.medication.category',
#         string='Category',
#         help="Medication category for organization"
#     )
#
#     controlled_substance = fields.Boolean(
#         string='Controlled Substance',
#         help="DEA controlled substance flag"
#     )
#     controlled_schedule = fields.Selection([
#         ('I', 'Schedule I'),
#         ('II', 'Schedule II'),
#         ('III', 'Schedule III'),
#         ('IV', 'Schedule IV'),
#         ('V', 'Schedule V')
#     ], string='Controlled Schedule')
#
#     # Pharmaceutical Details
#     dosage_form = fields.Selection([
#         ('tablet', 'Tablet'),
#         ('capsule', 'Capsule'),
#         ('syrup', 'Syrup/Liquid'),
#         ('injection', 'Injection'),
#         ('cream', 'Cream/Ointment'),
#         ('drops', 'Drops'),
#         ('inhaler', 'Inhaler'),
#         ('patch', 'Patch'),
#         ('suppository', 'Suppository'),
#         ('powder', 'Powder'),
#         ('gel', 'Gel'),
#         ('spray', 'Spray')
#     ], string='Dosage Form', required=True)
#
#     strength = fields.Char(
#         string='Strength',
#         required=True,
#         help="Drug strength (e.g., '500mg', '10mg/ml')"
#     )
#
#     unit_of_measure = fields.Selection([
#         ('mg', 'Milligrams (mg)'),
#         ('g', 'Grams (g)'),
#         ('ml', 'Milliliters (ml)'),
#         ('units', 'Units'),
#         ('iu', 'International Units (IU)'),
#         ('mcg', 'Micrograms (mcg)'),
#         ('meq', 'Milliequivalents (mEq)'),
#         ('percent', 'Percentage (%)'),
#         ('ratio', 'Ratio')
#     ], string='Unit of Measure', default='mg')
#
#     route_of_administration = fields.Selection([
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
#     manufacturer = fields.Char(string='Manufacturer')
#     ndc_number = fields.Char(
#         string='NDC Number',
#         help="National Drug Code"
#     )
#     lot_number = fields.Char(
#         string='Lot Number',
#         help="Batch/lot identification"
#     )
#
#     # Clinical Information
#     indications = fields.Text(
#         string='Indications',
#         help="Approved medical uses and conditions treated"
#     )
#     contraindications = fields.Text(
#         string='Contraindications',
#         help="Conditions where drug should not be used"
#     )
#     side_effects = fields.Text(
#         string='Side Effects',
#         help="Common and serious adverse effects"
#     )
#     drug_interactions = fields.Text(
#         string='Drug Interactions',
#         help="Known drug-drug interactions"
#     )
#
#     pregnancy_category = fields.Selection([
#         ('A', 'Category A - Safe'),
#         ('B', 'Category B - Probably Safe'),
#         ('C', 'Category C - Risk Cannot be Ruled Out'),
#         ('D', 'Category D - Positive Evidence of Risk'),
#         ('X', 'Category X - Contraindicated')
#     ], string='Pregnancy Category')
#
#     pediatric_use = fields.Boolean(
#         string='Safe for Pediatric Use',
#         default=True
#     )
#     geriatric_considerations = fields.Text(
#         string='Geriatric Considerations',
#         help="Special considerations for elderly patients"
#     )
#
#     # Prescribing Information
#     usual_adult_dose = fields.Text(
#         string='Usual Adult Dose',
#         help="Standard adult dosing recommendations"
#     )
#     usual_pediatric_dose = fields.Text(
#         string='Usual Pediatric Dose',
#         help="Standard pediatric dosing recommendations"
#     )
#     maximum_daily_dose = fields.Text(
#         string='Maximum Daily Dose',
#         help="Maximum safe daily dose"
#     )
#     renal_adjustment = fields.Text(
#         string='Renal Dose Adjustment',
#         help="Dose adjustment for kidney disease"
#     )
#     hepatic_adjustment = fields.Text(
#         string='Hepatic Dose Adjustment',
#         help="Dose adjustment for liver disease"
#     )
#
#     # Inventory and Cost Information
#     active = fields.Boolean(
#         string='Active',
#         default=True,
#         help="Active medication flag"
#     )
#     cost_per_unit = fields.Float(
#         string='Cost per Unit',
#         digits=(10, 4),
#         help="Unit cost for inventory management"
#     )
#     preferred_generic = fields.Boolean(
#         string='Preferred Generic',
#         help="Preferred generic option"
#     )
#     formulary_status = fields.Selection([
#         ('on_formulary', 'On Formulary'),
#         ('off_formulary', 'Off Formulary'),
#         ('restricted', 'Restricted'),
#         ('prior_auth', 'Prior Authorization Required')
#     ], string='Formulary Status', default='on_formulary')
#
#     # Additional Information
#     storage_requirements = fields.Text(
#         string='Storage Requirements',
#         help="Special storage conditions (temperature, light, etc.)"
#     )
#     expiration_monitoring = fields.Boolean(
#         string='Monitor Expiration',
#         help="Track expiration dates for this medication"
#     )
#
#     # System Fields
#     company_id = fields.Many2one(
#         'res.company',
#         string='Company',
#         default=lambda self: self.env.company,
#         required=True
#     )
#
#     # Computed Fields
#     display_name = fields.Char(
#         string='Display Name',
#         compute='_compute_display_name',
#         store=True
#     )
#
#     prescription_count = fields.Integer(
#         string='Prescription Count',
#         compute='_compute_prescription_count'
#     )
#
#     @api.depends('name', 'strength', 'dosage_form')
#     def _compute_display_name(self):
#         """Compute display name with name, strength, and form."""
#         for record in self:
#             if record.name:
#                 parts = record.name
#             else:
#                 parts = ""
#             if record.strength:
#                 parts +"-"+ record.strength
#             if record.dosage_form:
#                 parts + record.dosage_form
#             record.display_name = parts
#
#     def _compute_prescription_count(self):
#         """Count prescriptions using this medication."""
#         for record in self:
#             record.prescription_count = self.env['clinic.prescription.line'].search_count([
#                 ('medication_id', '=', record.id)
#             ])
#
#     @api.constrains('controlled_substance', 'controlled_schedule')
#     def _check_controlled_substance(self):
#         """Validate controlled substance schedule."""
#         for record in self:
#             if record.controlled_substance and not record.controlled_schedule:
#                 raise ValidationError(_('Controlled substances must have a schedule assigned.'))
#             if not record.controlled_substance and record.controlled_schedule:
#                 raise ValidationError(_('Only controlled substances can have a schedule assigned.'))
#
#     @api.constrains('cost_per_unit')
#     def _check_cost_per_unit(self):
#         """Validate cost per unit is positive."""
#         for record in self:
#             if record.cost_per_unit and record.cost_per_unit < 0:
#                 raise ValidationError(_('Cost per unit must be positive.'))
#
#     @api.onchange('controlled_substance')
#     def _onchange_controlled_substance(self):
#         """Clear controlled schedule when not a controlled substance."""
#         if not self.controlled_substance:
#             self.controlled_schedule = False
#
#     def name_get(self):
#         """Custom name display with strength and form."""
#         result = []
#         for record in self:
#             name = record.name
#             if record.strength:
#                 name += f" {record.strength}"
#             if record.dosage_form:
#                 form_label = dict(record._fields['dosage_form'].selection)[record.dosage_form]
#                 name += f" ({form_label})"
#             result.append((record.id, name))
#         return result
#
#     @api.model
#     def name_search(self, name='', args=None, operator='ilike', limit=100):
#         """Enhanced search by name, brand names, or generic name."""
#         args = args or []
#         domain = []
#
#         if name:
#             domain = [
#                 '|', '|', '|',
#                 ('name', operator, name),
#                 ('generic_name', operator, name),
#                 ('brand_names', operator, name),
#                 ('display_name', operator, name)
#             ]
#
#         medications = self.search(domain + args, limit=limit)
#         return medications.name_get()
#
#     def get_drug_interactions(self, other_medication_ids):
#         """Check for drug interactions with other medications."""
#         self.ensure_one()
#         interactions = []
#
#         if not self.drug_interactions:
#             return interactions
#
#         other_medications = self.browse(other_medication_ids)
#         interaction_text = self.drug_interactions.lower()
#
#         for med in other_medications:
#             # Simple keyword matching - in real implementation, use drug interaction database
#             if med.name.lower() in interaction_text or \
#                (med.drug_class and med.drug_class in interaction_text):
#                 interactions.append({
#                     'medication': med,
#                     'interaction': self.drug_interactions,
#                     'severity': 'moderate'  # Would be determined by interaction database
#                 })
#
#         return interactions
#
#     def check_allergy_contraindication(self, patient_allergies):
#         """Check if medication is contraindicated due to patient allergies."""
#         self.ensure_one()
#
#         if not patient_allergies:
#             return False
#
#         allergy_text = patient_allergies.lower()
#         medication_terms = [
#             self.name.lower(),
#             self.generic_name.lower() if self.generic_name else '',
#             self.drug_class.lower() if self.drug_class else ''
#         ]
#
#         # Check brand names
#         if self.brand_names:
#             brand_list = [brand.strip().lower() for brand in self.brand_names.split(',')]
#             medication_terms.extend(brand_list)
#
#         for term in medication_terms:
#             if term and term in allergy_text:
#                 return True
#
#         return False
#
#     def get_dosing_recommendations(self, patient_age=None, patient_weight=None, indication=None):
#         """Get dosing recommendations based on patient parameters."""
#         self.ensure_one()
#         recommendations = {}
#
#         # Age-based dosing
#         if patient_age is not None:
#             if patient_age < 18 and self.usual_pediatric_dose:
#                 recommendations['pediatric_dose'] = self.usual_pediatric_dose
#             elif patient_age >= 18 and self.usual_adult_dose:
#                 recommendations['adult_dose'] = self.usual_adult_dose
#
#             if patient_age >= 65 and self.geriatric_considerations:
#                 recommendations['geriatric_notes'] = self.geriatric_considerations
#
#         # Maximum dose warning
#         if self.maximum_daily_dose:
#             recommendations['max_daily_dose'] = self.maximum_daily_dose
#
#         # Special considerations
#         if self.renal_adjustment:
#             recommendations['renal_adjustment'] = self.renal_adjustment
#         if self.hepatic_adjustment:
#             recommendations['hepatic_adjustment'] = self.hepatic_adjustment
#
#         return recommendations
#
#     def action_view_prescriptions(self):
#         """View prescriptions using this medication."""
#         self.ensure_one()
#         return {
#             'name': _('Prescriptions'),
#             'type': 'ir.actions.act_window',
#             'res_model': 'clinic.prescription.line',
#             'view_mode': 'list,form',
#             'domain': [('medication_id', '=', self.id)],
#             'context': {'default_medication_id': self.id},
#             'target': 'current',
#         }
#
#     @api.model
#     def get_controlled_substances(self):
#         """Get all controlled substances for monitoring."""
#         return self.search([('controlled_substance', '=', True)])
#
#     @api.model
#     def get_medications_by_class(self, drug_class):
#         """Get medications by therapeutic class."""
#         return self.search([('drug_class', '=', drug_class), ('active', '=', True)])
#
#     @api.model
#     def search_medications_for_condition(self, condition_keywords):
#         """Search medications by indication keywords."""
#         domain = [
#             ('active', '=', True),
#             ('indications', 'ilike', condition_keywords)
#         ]
#         return self.search(domain)
#
#     def toggle_active(self):
#         """Toggle active status of medication."""
#         for record in self:
#             record.active = not record.active
#
#     def duplicate_medication(self):
#         """Create a copy of the medication with different strength."""
#         self.ensure_one()
#         return {
#             'name': _('Duplicate Medication'),
#             'type': 'ir.actions.act_window',
#             'res_model': 'clinic.medication',
#             'view_mode': 'form',
#             'context': {
#                 'default_name': self.name,
#                 'default_generic_name': self.generic_name,
#                 'default_drug_class': self.drug_class,
#                 'default_dosage_form': self.dosage_form,
#                 'default_route_of_administration': self.route_of_administration,
#                 'default_manufacturer': self.manufacturer,
#             },
#             'target': 'new',
#         }
#
