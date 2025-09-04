# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta


class ClinicPrescription(models.Model):
    _name = 'clinic.prescription'
    _description = 'Medical Prescription'
    _order = 'prescription_date desc'
    _rec_name = 'prescription_number'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Header Information
    prescription_number = fields.Char(
        string='Prescription Number',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
        tracking=True
    )
    
    patient_id = fields.Many2one(
        'clinic.patient',
        string='Patient',
        required=True,
        ondelete='cascade',
        tracking=True
    )
    
    vital_signs_id = fields.Many2one(
        'clinic.vital.signs',
        string='Related Vital Signs',
        help="Vital signs record associated with this prescription"
    )
    
    prescription_date = fields.Datetime(
        string='Prescription Date',
        required=True,
        default=fields.Datetime.now,
        tracking=True
    )
    
    prescriber_id = fields.Many2one(
        'res.users',
        string='Prescriber',
        required=True,
        default=lambda self: self.env.user,
        tracking=True,
        domain=[('groups_id', 'in', [lambda self: self.env.ref('clinic_management.group_clinic_physician').id])]
    )
    
    prescriber_license = fields.Char(
        string='Medical License Number',
        related='prescriber_id.clinic_license_number',
        readonly=True
    )
    
    prescriber_dea = fields.Char(
        string='DEA Registration',
        related='prescriber_id.clinic_dea_number',
        readonly=True
    )

    # Clinical Context
    diagnosis_codes = fields.Text(
        string='Diagnosis Codes (ICD-10)',
        help="ICD-10 diagnosis codes for this prescription"
    )
    
    clinical_indication = fields.Text(
        string='Clinical Indication',
        help="Medical reason for prescription"
    )
    
    patient_weight = fields.Float(
        string='Patient Weight (kg)',
        digits=(5, 1),
        help="Patient weight at time of prescription for dosing calculations"
    )
    
    allergies_noted = fields.Text(
        string='Allergies Considered',
        help="Patient allergies reviewed and considered"
    )
    
    pregnancy_status = fields.Selection([
        ('na', 'Not Applicable'),
        ('not_pregnant', 'Not Pregnant'),
        ('pregnant', 'Pregnant'),
        ('breastfeeding', 'Breastfeeding'),
        ('unknown', 'Unknown')
    ], string='Pregnancy Status', default='na')

    # Prescription Details
    prescription_line_ids = fields.One2many(
        'clinic.prescription.line',
        'prescription_id',
        string='Prescribed Medications',
        copy=True
    )
    
    total_medications = fields.Integer(
        string='Total Medications',
        compute='_compute_total_medications',
        store=True
    )
    
    controlled_substances = fields.Boolean(
        string='Contains Controlled Substances',
        compute='_compute_controlled_substances',
        store=True
    )
    
    generic_substitution = fields.Boolean(
        string='Allow Generic Substitution',
        default=True,
        help="Allow pharmacist to substitute generic equivalents"
    )

    # Status and Workflow
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('dispensed', 'Dispensed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    
    dispensing_pharmacy = fields.Char(
        string='Dispensing Pharmacy',
        help="Pharmacy where prescription was filled"
    )
    
    dispensed_date = fields.Datetime(
        string='Dispensed Date',
        help="Date prescription was filled"
    )
    
    refills_remaining = fields.Integer(
        string='Refills Remaining',
        compute='_compute_refills_remaining'
    )

    # Legal and Compliance
    electronic_signature = fields.Text(
        string='Electronic Signature',
        help="Digital signature data"
    )
    
    signature_timestamp = fields.Datetime(
        string='Signature Timestamp',
        help="When prescription was electronically signed"
    )
    
    printed = fields.Boolean(
        string='Printed',
        default=False,
        help="Whether prescription was printed"
    )
    
    transmitted = fields.Boolean(
        string='Transmitted Electronically',
        default=False,
        help="Whether sent electronically to pharmacy"
    )

    # System Fields
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True
    )

    # Additional Information
    special_instructions = fields.Text(
        string='Special Instructions',
        help="Additional instructions for patient or pharmacist"
    )
    
    follow_up_date = fields.Date(
        string='Follow-up Date',
        help="Recommended follow-up date"
    )
    
    notes = fields.Text(
        string='Internal Notes',
        help="Internal notes not printed on prescription"
    )

    @api.depends('prescription_line_ids')
    def _compute_total_medications(self):
        """Count total medications in prescription."""
        for record in self:
            record.total_medications = len(record.prescription_line_ids)

    @api.depends('prescription_line_ids.medication_id.controlled_substance')
    def _compute_controlled_substances(self):
        """Check if prescription contains controlled substances."""
        for record in self:
            record.controlled_substances = any(
                line.medication_id.controlled_substance 
                for line in record.prescription_line_ids
            )

    @api.depends('prescription_line_ids.refills_authorized')
    def _compute_refills_remaining(self):
        """Compute total refills remaining across all medications."""
        for record in self:
            if record.prescription_line_ids:
                record.refills_remaining = sum(
                    line.refills_authorized for line in record.prescription_line_ids
                )
            else:
                record.refills_remaining = 0

    @api.model
    def create(self, vals):
        """Override create to generate prescription number."""
        if vals.get('prescription_number', _('New')) == _('New'):
            vals['prescription_number'] = self.env['ir.sequence'].next_by_code('clinic.prescription') or _('New')
        
        # Auto-populate patient weight from latest vital signs
        if vals.get('patient_id') and not vals.get('patient_weight'):
            patient = self.env['clinic.patient'].browse(vals['patient_id'])
            latest_vitals = patient.get_latest_vital_signs()
            if latest_vitals and latest_vitals.weight:
                vals['patient_weight'] = latest_vitals.weight
        
        return super().create(vals)

    @api.constrains('prescription_date')
    def _check_prescription_date(self):
        """Validate prescription date is not in the future."""
        for record in self:
            if record.prescription_date and record.prescription_date > fields.Datetime.now():
                raise ValidationError(_('Prescription date cannot be in the future.'))

    @api.constrains('patient_weight')
    def _check_patient_weight(self):
        """Validate patient weight is reasonable."""
        for record in self:
            if record.patient_weight and (record.patient_weight < 0.5 or record.patient_weight > 500):
                raise ValidationError(_('Patient weight must be between 0.5 and 500 kg.'))

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        """Auto-populate patient information when patient is selected."""
        if self.patient_id:
            # Get latest vital signs
            latest_vitals = self.patient_id.get_latest_vital_signs()
            if latest_vitals:
                self.vital_signs_id = latest_vitals.id
                if latest_vitals.weight:
                    self.patient_weight = latest_vitals.weight
            
            # Set allergies noted
            if self.patient_id.allergies:
                self.allergies_noted = self.patient_id.allergies
            
            # Set pregnancy status based on gender and age
            if self.patient_id.gender == 'female' and self.patient_id.age and 12 <= self.patient_id.age <= 55:
                self.pregnancy_status = 'unknown'
            else:
                self.pregnancy_status = 'na'

    def action_confirm(self):
        """Confirm the prescription."""
        self.ensure_one()
        
        if not self.prescription_line_ids:
            raise UserError(_('Cannot confirm prescription without medications.'))
        
        # Perform clinical checks
        self._perform_clinical_checks()
        
        # Sign prescription electronically
        self.electronic_signature = f"Electronically signed by {self.prescriber_id.name}"
        self.signature_timestamp = fields.Datetime.now()
        
        self.state = 'confirmed'
        self.message_post(body=_('Prescription confirmed and electronically signed.'))

    def action_cancel(self):
        """Cancel the prescription."""
        self.ensure_one()
        
        if self.state == 'dispensed':
            raise UserError(_('Cannot cancel a dispensed prescription.'))
        
        self.state = 'cancelled'
        self.message_post(body=_('Prescription cancelled.'))

    def action_mark_dispensed(self):
        """Mark prescription as dispensed."""
        self.ensure_one()
        
        if self.state != 'confirmed':
            raise UserError(_('Only confirmed prescriptions can be marked as dispensed.'))
        
        self.state = 'dispensed'
        self.dispensed_date = fields.Datetime.now()
        self.message_post(body=_('Prescription marked as dispensed.'))

    def action_print_prescription(self):
        """Print prescription report."""
        self.ensure_one()
        
        if self.state == 'draft':
            raise UserError(_('Cannot print draft prescription. Please confirm first.'))
        
        self.printed = True
        
        return self.env.ref('clinic_management.action_report_prescription').report_action(self)

    def action_transmit_electronically(self):
        """Transmit prescription electronically to pharmacy."""
        self.ensure_one()
        
        if self.state != 'confirmed':
            raise UserError(_('Only confirmed prescriptions can be transmitted.'))
        
        # In real implementation, integrate with e-prescribing system
        self.transmitted = True
        self.message_post(body=_('Prescription transmitted electronically to pharmacy.'))

    def _perform_clinical_checks(self):
        """Perform clinical safety checks before confirming prescription."""
        self.ensure_one()
        
        warnings = []
        errors = []
        
        # Check for drug allergies
        if self.patient_id.allergies:
            for line in self.prescription_line_ids:
                if line.medication_id.check_allergy_contraindication(self.patient_id.allergies):
                    errors.append(
                        f"ALLERGY ALERT: Patient is allergic to {line.medication_id.name}"
                    )
        
        # Check for drug interactions
        medication_ids = self.prescription_line_ids.mapped('medication_id.id')
        for line in self.prescription_line_ids:
            other_meds = [mid for mid in medication_ids if mid != line.medication_id.id]
            interactions = line.medication_id.get_drug_interactions(other_meds)
            for interaction in interactions:
                warnings.append(
                    f"INTERACTION: {line.medication_id.name} may interact with {interaction['medication'].name}"
                )
        
        # Check controlled substance prescribing
        for line in self.prescription_line_ids:
            if line.medication_id.controlled_substance:
                if not self.prescriber_dea:
                    errors.append(
                        f"DEA registration required to prescribe {line.medication_id.name}"
                    )
                
                # Check refill limits for controlled substances
                schedule = line.medication_id.controlled_schedule
                if schedule in ['I', 'II'] and line.refills_authorized > 0:
                    errors.append(
                        f"Schedule {schedule} controlled substances cannot have refills"
                    )
                elif schedule in ['III', 'IV', 'V'] and line.refills_authorized > 5:
                    errors.append(
                        f"Schedule {schedule} controlled substances limited to 5 refills"
                    )
        
        # Check pregnancy contraindications
        if self.pregnancy_status == 'pregnant':
            for line in self.prescription_line_ids:
                if line.medication_id.pregnancy_category == 'X':
                    errors.append(
                        f"PREGNANCY ALERT: {line.medication_id.name} is contraindicated in pregnancy"
                    )
                elif line.medication_id.pregnancy_category in ['D']:
                    warnings.append(
                        f"PREGNANCY WARNING: {line.medication_id.name} may pose risks in pregnancy"
                    )
        
        # Raise errors if any critical issues found
        if errors:
            raise UserError(_('Cannot confirm prescription due to safety concerns:\\n\\n') + '\\n'.join(errors))
        
        # Log warnings
        if warnings:
            warning_msg = _('Clinical warnings for this prescription:\\n\\n') + '\\n'.join(warnings)
            self.message_post(body=warning_msg, message_type='comment')

    def get_prescription_summary(self):
        """Get prescription summary for reports."""
        self.ensure_one()
        
        summary = {
            'patient_name': self.patient_id.name,
            'patient_id': self.patient_id.patient_id,
            'patient_age': self.patient_id.age,
            'prescription_number': self.prescription_number,
            'prescription_date': self.prescription_date,
            'prescriber_name': self.prescriber_id.name,
            'total_medications': self.total_medications,
            'controlled_substances': self.controlled_substances,
            'medications': []
        }
        
        for line in self.prescription_line_ids:
            med_info = {
                'name': line.medication_id.name,
                'strength': line.strength_prescribed,
                'form': line.dosage_form_prescribed,
                'dose': line.dose_amount,
                'frequency': line.get_frequency_display(),
                'duration': line.duration,
                'quantity': line.quantity_prescribed,
                'refills': line.refills_authorized,
                'instructions': line.special_instructions
            }
            summary['medications'].append(med_info)
        
        return summary

    @api.model
    def get_prescriptions_needing_review(self):
        """Get prescriptions that need clinical review."""
        return self.search([
            ('state', '=', 'draft'),
            ('create_date', '<', fields.Datetime.now() - timedelta(hours=24))
        ])

    @api.model
    def get_controlled_substance_prescriptions(self, date_from=None, date_to=None):
        """Get controlled substance prescriptions for monitoring."""
        domain = [('controlled_substances', '=', True)]
        
        if date_from:
            domain.append(('prescription_date', '>=', date_from))
        if date_to:
            domain.append(('prescription_date', '<=', date_to))
        
        return self.search(domain)

    def duplicate_prescription(self):
        """Create a copy of the prescription for refill."""
        self.ensure_one()
        
        # Check if refills are available
        if not any(line.refills_authorized > 0 for line in self.prescription_line_ids):
            raise UserError(_('No refills available for this prescription.'))
        
        # Create new prescription
        new_prescription = self.copy({
            'prescription_number': _('New'),
            'prescription_date': fields.Datetime.now(),
            'state': 'draft',
            'printed': False,
            'transmitted': False,
            'dispensed_date': False,
            'electronic_signature': False,
            'signature_timestamp': False
        })
        
        # Reduce refills for original prescription lines
        for line in self.prescription_line_ids:
            if line.refills_authorized > 0:
                line.refills_authorized -= 1
        
        return {
            'name': _('Refill Prescription'),
            'type': 'ir.actions.act_window',
            'res_model': 'clinic.prescription',
            'res_id': new_prescription.id,
            'view_mode': 'form',
            'target': 'current',
        }

