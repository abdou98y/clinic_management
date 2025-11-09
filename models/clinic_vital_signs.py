# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class ClinicVitalSigns(models.Model):
    _name = 'clinic.vital.signs'
    _description = 'Patient Vital Signs Recording'
    _order = 'visit_datetime desc'
    _rec_name = 'display_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Reference Fields
    patient_id = fields.Many2one(
        'clinic.patient',
        string='Patient',
        required=True,
        ondelete='cascade',
        tracking=True
    )
    visit_datetime = fields.Datetime(
        string='Visit Date & Time',
        required=True,
        default=fields.Datetime.now,
        tracking=True
    )
    recorded_by = fields.Many2one(
        'res.users',
        string='Recorded By',
        default=lambda self: self.env.user,
        required=True,
        tracking=True
    )
    visit_type = fields.Selection([
        ('regular', 'Regular Visit'),
        ('emergency', 'Emergency'),
        ('followup', 'Follow-up'),
        ('consultation', 'Consultation'),
        ('screening', 'Health Screening')
    ], string='Visit Type', default='regular', required=True)

    # Vital Signs Measurements
    systolic_bp = fields.Integer(
        string='Systolic BP (mmHg)',
        help="Systolic blood pressure (60-300 mmHg range)"
    )
    diastolic_bp = fields.Integer(
        string='Diastolic BP (mmHg)',
        help="Diastolic blood pressure (30-200 mmHg range)"
    )
    blood_pressure_display = fields.Char(
        string='Blood Pressure',
        compute='_compute_blood_pressure_display',
        store=True
    )
    bp_category = fields.Selection([
        ('normal', 'Normal'),
        ('elevated', 'Elevated'),
        ('stage1', 'Stage 1 Hypertension'),
        ('stage2', 'Stage 2 Hypertension'),
        ('crisis', 'Hypertensive Crisis')
    ], string='BP Category', compute='_compute_bp_category', store=True)

    heart_rate = fields.Integer(
        string='Heart Rate (bpm)',
        help="Heart rate in beats per minute (30-200 bpm range)"
    )
    heart_rhythm = fields.Selection([
        ('regular', 'Regular'),
        ('irregular', 'Irregular'),
        ('tachycardia', 'Tachycardia'),
        ('bradycardia', 'Bradycardia')
    ], string='Heart Rhythm', default='regular')

    temperature = fields.Float(
        string='Temperature (°C)',
        digits=(4, 1),
        help="Body temperature in Celsius (30.0-45.0°C range)"
    )
    temperature_method = fields.Selection([
        ('oral', 'Oral'),
        ('rectal', 'Rectal'),
        ('axillary', 'Axillary'),
        ('tympanic', 'Tympanic'),
        ('temporal', 'Temporal')
    ], string='Temperature Method', default='oral')
    temperature_fahrenheit = fields.Float(
        string='Temperature (°F)',
        compute='_compute_temperature_fahrenheit',
        digits=(4, 1)
    )

    respiratory_rate = fields.Integer(
        string='Respiratory Rate (breaths/min)',
        help="Breaths per minute (5-60 range)"
    )
    
    oxygen_saturation = fields.Float(
        string='SpO₂ (%)',
        digits=(5, 1),
        help="Oxygen saturation percentage (70.0-100.0% range)"
    )
    oxygen_support = fields.Boolean(
        string='On Oxygen Support',
        help="Whether patient is receiving supplemental oxygen"
    )
    oxygen_flow_rate = fields.Float(
        string='O₂ Flow Rate (L/min)',
        digits=(4, 1),
        help="Oxygen flow rate if on supplemental oxygen"
    )

    # Anthropometric Measurements
    weight = fields.Float(
        string='Weight (kg)',
        digits=(5, 1),
        help="Weight in kilograms (0.5-500.0 kg range)"
    )
    height = fields.Float(
        string='Height (cm)',
        digits=(5, 1),
        help="Height in centimeters (30.0-250.0 cm range)"
    )
    mother_height = fields.Float(
        string='Mother Height (cm)',
        digits=(5, 1),
        help="Height in centimeters (30.0-250.0 cm range)"
    )
    father_height = fields.Float(
        string='Father Height (cm)',
        digits=(5, 1),
        help="Height in centimeters (30.0-250.0 cm range)"
    )
    bmi = fields.Float(
        string='BMI',
        compute='_compute_bmi',
        store=True,
        digits=(4, 1),
        help="Body Mass Index calculation"
    )
    bmi_category = fields.Selection([
        ('underweight', 'Underweight (<18.5)'),
        ('normal', 'Normal (18.5-24.9)'),
        ('overweight', 'Overweight (25.0-29.9)'),
        ('obese_class1', 'Obese Class I (30.0-34.9)'),
        ('obese_class2', 'Obese Class II (35.0-39.9)'),
        ('obese_class3', 'Obese Class III (≥40.0)')
    ], string='BMI Category', compute='_compute_bmi_category', store=True)

    head_circumference = fields.Float(
        string='Head Circumference (cm)',
        digits=(4, 1),
        help="For pediatric patients"
    )
    waist_circumference = fields.Float(
        string='Waist Circumference (cm)',
        digits=(4, 1),
        help="Waist measurement for metabolic assessment"
    )

    # Clinical Assessment
    pain_scale = fields.Selection([
        ('0', '0 - No Pain'),
        ('1', '1 - Minimal'),
        ('2', '2 - Mild'),
        ('3', '3 - Uncomfortable'),
        ('4', '4 - Moderate'),
        ('5', '5 - Distracting'),
        ('6', '6 - Distressing'),
        ('7', '7 - Unmanageable'),
        ('8', '8 - Intense'),
        ('9', '9 - Severe'),
        ('10', '10 - Unable to Move')
    ], string='Pain Scale (0-10)')

    consciousness_level = fields.Selection([
        ('alert', 'Alert'),
        ('drowsy', 'Drowsy'),
        ('confused', 'Confused'),
        ('unconscious', 'Unconscious')
    ], string='Consciousness Level', default='alert')

    mobility_status = fields.Selection([
        ('independent', 'Independent'),
        ('assisted', 'Assisted'),
        ('wheelchair', 'Wheelchair'),
        ('bedbound', 'Bedbound')
    ], string='Mobility Status', default='independent')

    skin_condition = fields.Selection([
        ('normal', 'Normal'),
        ('dry', 'Dry'),
        ('moist', 'Moist'),
        ('diaphoretic', 'Diaphoretic'),
        ('cyanotic', 'Cyanotic'),
        ('jaundiced', 'Jaundiced'),
        ('pale', 'Pale')
    ], string='Skin Condition', default='normal')

    # Clinical Notes
    chief_complaint = fields.Text(
        string='Chief Complaint',
        help="Primary reason for visit"
    )
    history_present_illness = fields.Text(
        string='History of Present Illness',
        help="Current illness history and symptoms"
    )
    physical_examination = fields.Text(
        string='Physical Examination',
        help="Physical examination findings"
    )
    diagnosis = fields.Text(
        string='Diagnosis/Assessment',
        help="Clinical diagnosis or impression"
    )
    assessment_plan = fields.Text(
        string='Assessment & Plan',
        help="Clinical assessment and treatment plan"
    )
    doctor_remarks = fields.Text(
        string='Doctor Remarks',
        help="Additional physician notes and observations"
    )
    follow_up_instructions = fields.Text(
        string='Follow-up Instructions',
        help="Patient follow-up and care instructions"
    )

    # System Fields
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True
    )

    # Display Fields
    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True
    )

    main_complaint_id = fields.Many2one(
        "main.complaint",
        string="Main Complaint",
        ondelete="restrict",
        required=True,
        default=lambda self: self.env['main.complaint'].search([], order="id desc", limit=1).id
    )

    display_main_complaint = fields.Char(
        string="Main Complaint Display",
        compute='_compute_display_main_complaint'
    )


    @api.depends('main_complaint_id', 'visit_datetime', 'chief_complaint')
    def _compute_display_main_complaint(self):
        for rec in self:
            if rec.main_complaint_id:
                rec.display_main_complaint = rec.main_complaint_id.name_get()[0][1]
            else:
                date_str = (rec.visit_datetime or fields.Datetime.now()).strftime('%Y-%m-%d')
                desc = rec.chief_complaint or ''
                rec.display_main_complaint = f"{date_str} - {desc[:50]}" if desc else date_str

    @api.depends('patient_id', 'visit_datetime')
    def _compute_display_name(self):
        """Compute display name for vital signs record."""
        for record in self:
            if record.patient_id and record.visit_datetime:
                date_str = record.visit_datetime.strftime('%Y-%m-%d %H:%M')
                record.display_name = f"{record.patient_id.name} - {date_str}"
            else:
                record.display_name = _('New Vital Signs')

    @api.depends('systolic_bp', 'diastolic_bp')
    def _compute_blood_pressure_display(self):
        """Compute blood pressure display string."""
        for record in self:
            if record.systolic_bp and record.diastolic_bp:
                record.blood_pressure_display = f"{record.systolic_bp}/{record.diastolic_bp}"
            else:
                record.blood_pressure_display = ""

    @api.depends('systolic_bp', 'diastolic_bp')
    def _compute_bp_category(self):
        """Compute blood pressure category based on AHA guidelines."""
        for record in self:
            if not record.systolic_bp or not record.diastolic_bp:
                record.bp_category = False
                continue
            
            systolic = record.systolic_bp
            diastolic = record.diastolic_bp
            
            if systolic >= 180 or diastolic >= 120:
                record.bp_category = 'crisis'
            elif systolic >= 140 or diastolic >= 90:
                record.bp_category = 'stage2'
            elif systolic >= 130 or diastolic >= 80:
                record.bp_category = 'stage1'
            elif systolic >= 120 and diastolic < 80:
                record.bp_category = 'elevated'
            else:
                record.bp_category = 'normal'

    @api.depends('temperature')
    def _compute_temperature_fahrenheit(self):
        """Convert Celsius to Fahrenheit."""
        for record in self:
            if record.temperature:
                record.temperature_fahrenheit = (record.temperature * 9/5) + 32
            else:
                record.temperature_fahrenheit = 0

    @api.depends('weight', 'height')
    def _compute_bmi(self):
        """Compute Body Mass Index."""
        for record in self:
            if record.weight and record.height and record.height > 0:
                height_m = record.height / 100  # Convert cm to meters
                record.bmi = record.weight / (height_m ** 2)
            else:
                record.bmi = 0

    @api.depends('bmi')
    def _compute_bmi_category(self):
        """Compute BMI category classification."""
        for record in self:
            if not record.bmi:
                record.bmi_category = False
                continue
            
            bmi = record.bmi
            if bmi < 18.5:
                record.bmi_category = 'underweight'
            elif bmi < 25:
                record.bmi_category = 'normal'
            elif bmi < 30:
                record.bmi_category = 'overweight'
            elif bmi < 35:
                record.bmi_category = 'obese_class1'
            elif bmi < 40:
                record.bmi_category = 'obese_class2'
            else:
                record.bmi_category = 'obese_class3'

    @api.constrains('systolic_bp', 'diastolic_bp')
    def _check_blood_pressure(self):
        """Validate blood pressure values."""
        for record in self:
            if record.systolic_bp and (record.systolic_bp < 60 or record.systolic_bp > 300):
                raise ValidationError(_('Systolic blood pressure must be between 60 and 300 mmHg.'))
            if record.diastolic_bp and (record.diastolic_bp < 30 or record.diastolic_bp > 200):
                raise ValidationError(_('Diastolic blood pressure must be between 30 and 200 mmHg.'))
            if record.systolic_bp and record.diastolic_bp and record.systolic_bp <= record.diastolic_bp:
                raise ValidationError(_('Systolic blood pressure must be higher than diastolic blood pressure.'))

    @api.constrains('heart_rate')
    def _check_heart_rate(self):
        """Validate heart rate values."""
        for record in self:
            if record.heart_rate and (record.heart_rate < 30 or record.heart_rate > 200):
                raise ValidationError(_('Heart rate must be between 30 and 200 bpm.'))

    @api.constrains('temperature')
    def _check_temperature(self):
        """Validate temperature values."""
        for record in self:
            if record.temperature and (record.temperature < 30.0 or record.temperature > 45.0):
                raise ValidationError(_('Temperature must be between 30.0 and 45.0°C.'))

    @api.constrains('respiratory_rate')
    def _check_respiratory_rate(self):
        """Validate respiratory rate values."""
        for record in self:
            if record.respiratory_rate and (record.respiratory_rate < 5 or record.respiratory_rate > 60):
                raise ValidationError(_('Respiratory rate must be between 5 and 60 breaths per minute.'))

    @api.constrains('oxygen_saturation')
    def _check_oxygen_saturation(self):
        """Validate oxygen saturation values."""
        for record in self:
            if record.oxygen_saturation and (record.oxygen_saturation < 70.0 or record.oxygen_saturation > 100.0):
                raise ValidationError(_('Oxygen saturation must be between 70.0 and 100.0%.'))

    @api.constrains('weight')
    def _check_weight(self):
        """Validate weight values."""
        for record in self:
            if record.weight and (record.weight < 0.5 or record.weight > 500.0):
                raise ValidationError(_('Weight must be between 0.5 and 500.0 kg.'))

    @api.constrains('height')
    def _check_height(self):
        """Validate height values."""
        for record in self:
            if record.height and (record.height < 30.0 or record.height > 250.0):
                raise ValidationError(_('Height must be between 30.0 and 250.0 cm.'))

    @api.constrains('visit_datetime')
    def _check_visit_datetime(self):
        """Validate visit datetime is not in the future."""
        for record in self:
            if record.visit_datetime and record.visit_datetime > fields.Datetime.now():
                raise ValidationError(_('Visit date and time cannot be in the future.'))

    @api.onchange('oxygen_support')
    def _onchange_oxygen_support(self):
        """Clear oxygen flow rate when not on oxygen support."""
        if not self.oxygen_support:
            self.oxygen_flow_rate = 0

    def get_vital_signs_summary(self):
        """Get a summary of vital signs for reports."""
        self.ensure_one()
        summary = []
        
        if self.blood_pressure_display:
            summary.append(f"BP: {self.blood_pressure_display} mmHg")
        if self.heart_rate:
            summary.append(f"HR: {self.heart_rate} bpm")
        if self.temperature:
            summary.append(f"Temp: {self.temperature}°C")
        if self.respiratory_rate:
            summary.append(f"RR: {self.respiratory_rate}/min")
        if self.oxygen_saturation:
            summary.append(f"SpO₂: {self.oxygen_saturation}%")
        if self.weight:
            summary.append(f"Weight: {self.weight} kg")
        if self.bmi:
            summary.append(f"BMI: {self.bmi}")
        
        return " | ".join(summary)

    def get_abnormal_values(self):
        """Identify abnormal vital signs values."""
        self.ensure_one()
        abnormal = []
        
        # Check blood pressure
        if self.bp_category in ['stage1', 'stage2', 'crisis']:
            abnormal.append(f"Blood Pressure: {self.blood_pressure_display} ({dict(self._fields['bp_category'].selection)[self.bp_category]})")
        
        # Check heart rate
        if self.heart_rate:
            if self.heart_rate < 60:
                abnormal.append(f"Heart Rate: {self.heart_rate} bpm (Bradycardia)")
            elif self.heart_rate > 100:
                abnormal.append(f"Heart Rate: {self.heart_rate} bpm (Tachycardia)")
        
        # Check temperature
        if self.temperature:
            if self.temperature > 37.5:
                abnormal.append(f"Temperature: {self.temperature}°C (Fever)")
            elif self.temperature < 36.0:
                abnormal.append(f"Temperature: {self.temperature}°C (Hypothermia)")
        
        # Check oxygen saturation
        if self.oxygen_saturation and self.oxygen_saturation < 95.0:
            abnormal.append(f"SpO₂: {self.oxygen_saturation}% (Low)")
        
        # Check BMI
        if self.bmi_category in ['underweight', 'obese_class1', 'obese_class2', 'obese_class3']:
            abnormal.append(f"BMI: {self.bmi} ({dict(self._fields['bmi_category'].selection)[self.bmi_category]})")
        
        return abnormal

    @api.model
    def get_patients_with_abnormal_vitals(self, days=7):
        """Get patients with abnormal vital signs in the last N days."""
        cutoff_date = fields.Datetime.now() - timedelta(days=days)
        
        # Find records with abnormal values
        abnormal_records = self.search([
            ('visit_datetime', '>=', cutoff_date),
            '|', '|', '|', '|',
            ('bp_category', 'in', ['stage1', 'stage2', 'crisis']),
            ('temperature', '>', 37.5),
            ('temperature', '<', 36.0),
            ('oxygen_saturation', '<', 95.0),
            ('heart_rate', '<', 60),
            ('heart_rate', '>', 100)
        ])
        
        return abnormal_records.mapped('patient_id')

    def action_create_prescription(self):
        """Create prescription based on this vital signs record."""
        self.ensure_one()
        return {
            'name': _('Create Prescription'),
            'type': 'ir.actions.act_window',
            'res_model': 'clinic.prescription',
            'view_mode': 'form',
            'context': {
                'default_patient_id': self.patient_id.id,
                'default_vital_signs_id': self.id,
            },
            'target': 'new',
        }

    @api.model
    def create(self, vals):
        rec = super().create(vals)
        if rec.patient_id:
            rec.patient_id._on_related_changed()
        return rec

    def write(self, vals):
        res = super().write(vals)
        for rec in self:
            if rec.patient_id:
                rec.patient_id._on_related_changed()
        return res

    def unlink(self):
        patients = self.mapped("patient_id")
        res = super().unlink()
        patients._on_related_changed()
        return res