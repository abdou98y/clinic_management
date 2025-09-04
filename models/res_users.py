# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re


class ResUsers(models.Model):
    _inherit = 'res.users'

    # Healthcare Provider Information
    is_healthcare_provider = fields.Boolean(
        string='Healthcare Provider',
        default=False,
        help="Check if this user is a healthcare provider"
    )
    
    provider_type = fields.Selection([
        ('physician', 'Physician'),
        ('nurse', 'Nurse'),
        ('medical_assistant', 'Medical Assistant'),
        ('pharmacist', 'Pharmacist'),
        ('therapist', 'Therapist'),
        ('technician', 'Technician'),
        ('other', 'Other')
    ], string='Provider Type')
    
    # Professional Credentials
    clinic_license_number = fields.Char(
        string='Medical License Number',
        help="State medical license number"
    )
    
    clinic_license_state = fields.Many2one(
        'res.country.state',
        string='License State',
        help="State where medical license was issued"
    )
    
    clinic_license_expiry = fields.Date(
        string='License Expiry Date',
        help="Medical license expiration date"
    )
    
    clinic_dea_number = fields.Char(
        string='DEA Registration Number',
        help="Drug Enforcement Administration registration number"
    )
    
    clinic_dea_expiry = fields.Date(
        string='DEA Expiry Date',
        help="DEA registration expiration date"
    )
    
    clinic_npi_number = fields.Char(
        string='NPI Number',
        help="National Provider Identifier number"
    )
    
    # Specialties and Certifications
    clinic_specialty = fields.Selection([
        ('family_medicine', 'Family Medicine'),
        ('internal_medicine', 'Internal Medicine'),
        ('pediatrics', 'Pediatrics'),
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('emergency_medicine', 'Emergency Medicine'),
        ('endocrinology', 'Endocrinology'),
        ('gastroenterology', 'Gastroenterology'),
        ('neurology', 'Neurology'),
        ('oncology', 'Oncology'),
        ('orthopedics', 'Orthopedics'),
        ('psychiatry', 'Psychiatry'),
        ('radiology', 'Radiology'),
        ('surgery', 'Surgery'),
        ('urology', 'Urology'),
        ('other', 'Other')
    ], string='Medical Specialty')
    
    clinic_board_certifications = fields.Text(
        string='Board Certifications',
        help="List of board certifications"
    )
    
    clinic_education = fields.Text(
        string='Medical Education',
        help="Medical school and residency information"
    )
    
    # Practice Information
    clinic_years_experience = fields.Integer(
        string='Years of Experience',
        help="Years of clinical experience"
    )
    
    clinic_languages = fields.Char(
        string='Languages Spoken',
        help="Languages spoken with patients"
    )
    
    clinic_hospital_affiliations = fields.Text(
        string='Hospital Affiliations',
        help="Affiliated hospitals and medical centers"
    )


