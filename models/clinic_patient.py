# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import date, datetime
import re


class ClinicPatient(models.Model):
    _name = 'clinic.patient'
    _description = 'Patient Information Management'
    _order = 'name'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _sql_constraints = [
        ('patient_id_unique', 'UNIQUE(patient_id)', 'Patient ID must be unique!'),
        ('phone_format', 'CHECK(phone ~ \'^[0-9+\\-\\s\\(\\)]*$\')', 'Invalid phone number format!'),
        ('email_format', 'CHECK(email ~* \'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$\' OR email IS NULL)', 'Invalid email format!')
    ]

    # Personal Information Fields
    name = fields.Char(
        string='Full Name', 
        required=True, 
        tracking=True,
        help="Patient's full legal name"
    )
    patient_id = fields.Char(
        string='Patient ID', 
        required=True, 
        copy=False, 
        readonly=True,
        default=lambda self: _('New'),
        tracking=True,
        help="Unique patient identifier"
    )
    date_of_birth = fields.Date(
        string='Date of Birth',
        tracking=True,
        help="Patient's birth date for age calculation"
    )
    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        store=True,
        help="Automatically calculated from date of birth"
    )
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender', required=True, tracking=True)
    
    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
        ('other', 'Other')
    ], string='Marital Status')
    
    occupation = fields.Char(
        string='Occupation',
        help="Patient's occupation for occupational health considerations"
    )
    
    # Emergency Contact Information
    emergency_contact_name = fields.Char(
        string='Emergency Contact Name',
        tracking=True
    )
    emergency_contact_phone = fields.Char(
        string='Emergency Contact Phone',
        tracking=True
    )
    emergency_contact_relationship = fields.Char(
        string='Relationship to Patient'
    )

    # Contact Information Fields
    phone = fields.Char(
        string='Phone Number',
        tracking=True
    )
    mobile = fields.Char(
        string='Mobile Number',
        tracking=True
    )
    email = fields.Char(
        string='Email Address',
        tracking=True
    )
    street = fields.Char(string='Street Address')
    street2 = fields.Char(string='Street Address 2')
    city = fields.Char(string='City')
    state_id = fields.Many2one(
        'res.country.state',
        string='State/Province'
    )
    zip = fields.Char(string='ZIP/Postal Code')
    country_id = fields.Many2one(
        'res.country',
        string='Country',
        default=lambda self: self.env.company.country_id
    )

    # Medical History Fields
    blood_group = fields.Selection([
        ('a_positive', 'A+'),
        ('a_negative', 'A-'),
        ('b_positive', 'B+'),
        ('b_negative', 'B-'),
        ('ab_positive', 'AB+'),
        ('ab_negative', 'AB-'),
        ('o_positive', 'O+'),
        ('o_negative', 'O-')
    ], string='Blood Group', tracking=True)
    
    allergies = fields.Text(
        string='Known Allergies',
        tracking=True,
        help="List all known allergies with severity and reaction details"
    )
    chronic_conditions = fields.Text(
        string='Chronic Conditions',
        tracking=True,
        help="Ongoing medical conditions requiring management"
    )
    past_treatments = fields.Text(
        string='Past Treatments',
        tracking=True,
        help="Previous treatments, surgeries, and hospitalizations"
    )
    current_medications = fields.Text(
        string='Current Medications',
        help="Current medication regimen from other providers"
    )
    family_history = fields.Text(
        string='Family Medical History',
        help="Relevant family medical history"
    )
    social_history = fields.Text(
        string='Social History',
        help="Smoking, alcohol, drug use, and lifestyle factors"
    )

    # System Fields
    active = fields.Boolean(
        string='Active',
        default=True,
        help="Uncheck to archive the patient record"
    )
    notes = fields.Text(
        string='General Notes',
        help="Additional notes and observations"
    )
    image = fields.Binary(
        string='Patient Photo',
        help="Patient photograph for identification"
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True
    )

    # Relationship Fields
    vital_signs_ids = fields.One2many(
        'clinic.vital.signs',
        'patient_id',
        string='Vital Signs Records'
    )
    prescription_ids = fields.One2many(
        'clinic.prescription',
        'patient_id',
        string='Prescriptions'
    )

    # Computed Fields
    vital_signs_count = fields.Integer(
        string='Vital Signs Count',
        compute='_compute_vital_signs_count'
    )
    prescription_count = fields.Integer(
        string='Prescription Count',
        compute='_compute_prescription_count'
    )
    last_visit_date = fields.Datetime(
        string='Last Visit',
        compute='_compute_last_visit_date'
    )
    
    #lap  result  relation field
    lab_result_ids = fields.One2many('clinic.lab.result', 'patient_id', string='Lab Results')

    @api.depends('date_of_birth')
    def _compute_age(self):
        """Compute patient age from date of birth."""
        for record in self:
            if record.date_of_birth:
                today = date.today()
                birth_date = record.date_of_birth
                record.age = today.year - birth_date.year - (
                    (today.month, today.day) < (birth_date.month, birth_date.day)
                )
            else:
                record.age = 0

    @api.depends('vital_signs_ids')
    def _compute_vital_signs_count(self):
        """Count vital signs records for the patient."""
        for record in self:
            record.vital_signs_count = len(record.vital_signs_ids)

    @api.depends('prescription_ids')
    def _compute_prescription_count(self):
        """Count prescriptions for the patient."""
        for record in self:
            record.prescription_count = len(record.prescription_ids)

    @api.depends('vital_signs_ids.visit_datetime')
    def _compute_last_visit_date(self):
        """Compute the last visit date from vital signs records."""
        for record in self:
            if record.vital_signs_ids:
                record.last_visit_date = max(record.vital_signs_ids.mapped('visit_datetime'))
            else:
                record.last_visit_date = False

    @api.model
    def create(self, vals):
        """Override create to generate patient ID sequence."""
        if vals.get('patient_id', _('New')) == _('New'):
            vals['patient_id'] = self.env['ir.sequence'].next_by_code('clinic.patient') or _('New')
        return super().create(vals)

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        """Validate date of birth is not in the future."""
        for record in self:
            if record.date_of_birth and record.date_of_birth > date.today():
                raise ValidationError(_('Date of birth cannot be in the future.'))

    @api.constrains('age')
    def _check_age(self):
        """Validate age is within reasonable range."""
        for record in self:
            if record.age and (record.age < 0 or record.age > 150):
                raise ValidationError(_('Age must be between 0 and 150 years.'))

    @api.constrains('phone', 'mobile')
    def _check_phone_format(self):
        """Validate phone number format."""
        phone_pattern = re.compile(r'^[0-9+\-\s\(\)]*$')
        for record in self:
            if record.phone and not phone_pattern.match(record.phone):
                raise ValidationError(_('Invalid phone number format.'))
            if record.mobile and not phone_pattern.match(record.mobile):
                raise ValidationError(_('Invalid mobile number format.'))

    @api.constrains('email')
    def _check_email_format(self):
        """Validate email format."""
        email_pattern = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
        for record in self:
            if record.email and not email_pattern.match(record.email):
                raise ValidationError(_('Invalid email format.'))

    def name_get(self):
        """Custom name display including patient ID."""
        result = []
        for record in self:
            name = f"[{record.patient_id}] {record.name}"
            if record.age:
                name += f" ({record.age}y)"
            result.append((record.id, name))
        return result

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        """Enhanced search by name, patient ID, or phone."""
        args = args or []
        domain = []
        
        if name:
            domain = [
                '|', '|', '|',
                ('name', operator, name),
                ('patient_id', operator, name),
                ('phone', operator, name),
                ('mobile', operator, name)
            ]
        
        patients = self.search(domain + args, limit=limit)
        return patients.name_get()

    def action_view_vital_signs(self):
        """Action to view patient's vital signs records."""
        self.ensure_one()
        return {
            'name': _('Vital Signs'),
            'type': 'ir.actions.act_window',
            'res_model': 'clinic.vital.signs',
            'view_mode': 'list,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
            'target': 'current',
        }

    def action_view_prescriptions(self):
        """Action to view patient's prescriptions."""
        self.ensure_one()
        return {
            'name': _('Prescriptions'),
            'type': 'ir.actions.act_window',
            'res_model': 'clinic.prescription',
            'view_mode': 'list,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
            'target': 'current',
        }

    def action_create_vital_signs(self):
        """Action to create new vital signs record for patient."""
        self.ensure_one()
        return {
            'name': _('Record Vital Signs'),
            'type': 'ir.actions.act_window',
            'res_model': 'clinic.vital.signs',
            'view_mode': 'form',
            'context': {'default_patient_id': self.id},
            'target': 'new',
        }

    def action_create_prescription(self):
        """Action to create new prescription for patient."""
        self.ensure_one()
        return {
            'name': _('Create Prescription'),
            'type': 'ir.actions.act_window',
            'res_model': 'clinic.prescription',
            'view_mode': 'form',
            'context': {'default_patient_id': self.id},
            'target': 'new',
        }

    def get_latest_vital_signs(self):
        """Get the most recent vital signs record for the patient."""
        self.ensure_one()
        return self.vital_signs_ids.sorted('visit_datetime', reverse=True)[:1]

    def get_active_prescriptions(self):
        """Get active prescriptions for the patient."""
        self.ensure_one()
        return self.prescription_ids.filtered(
            lambda p: p.state in ['confirmed', 'dispensed'] and 
            p.prescription_date >= fields.Datetime.now() - fields.Datetime.timedelta(days=90)
        )

    def check_drug_allergies(self, medication_id):
        """Check if patient has allergies to the specified medication."""
        self.ensure_one()
        if not self.allergies or not medication_id:
            return False
        
        medication = self.env['clinic.medication'].browse(medication_id)
        allergy_text = self.allergies.lower()
        
        # Check against medication name and common allergy terms
        medication_terms = [
            medication.name.lower(),
            medication.generic_name.lower() if medication.generic_name else '',
            medication.drug_class.lower() if medication.drug_class else ''
        ]
        
        for term in medication_terms:
            if term and term in allergy_text:
                return True
        
        return False

    @api.model
    def get_patients_needing_followup(self):
        """Get patients who need follow-up based on last visit date."""
        cutoff_date = fields.Datetime.now() - fields.Datetime.timedelta(days=90)
        return self.search([
            ('active', '=', True),
            ('last_visit_date', '<', cutoff_date),
            ('chronic_conditions', '!=', False)
        ])

    def archive_patient(self):
        """Archive patient record with confirmation."""
        self.ensure_one()
        if self.vital_signs_count > 0 or self.prescription_count > 0:
            raise UserError(_(
                'Cannot archive patient with existing vital signs or prescriptions. '
                'Please review and handle existing records first.'
            ))
        self.active = False
        self.message_post(body=_('Patient record archived.'))

    def unarchive_patient(self):
        """Unarchive patient record."""
        self.ensure_one()
        self.active = True
        self.message_post(body=_('Patient record reactivated.'))

