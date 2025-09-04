# -*- coding: utf-8 -*-
{
    'name': 'Clinic Management System',
    'version': '18.0.1.0.0',
    'category': 'Healthcare',
    'summary': 'Comprehensive clinic management system for patient care, vital signs, and prescriptions',
    'description': """
Clinic Management System
========================

A comprehensive healthcare management solution built for Odoo 18 Community Edition.

Key Features:
* Patient Profile Management with medical history
* Vital Signs Recording with automatic BMI calculation
* Medication Database with drug interaction checking
* Prescription Management with printable reports
* Security and access controls for healthcare data
* HIPAA compliance features and audit trails

This module provides healthcare facilities with a complete solution for managing
patient care workflows from registration through diagnosis and treatment.
    """,
    'author': 'Manus AI',
    'website': 'https://github.com/manus-ai/clinic-management',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'web',
        'portal',
    ],
    'data': [
        # Security
        'security/clinic_security.xml',
        'security/ir.model.access.csv',
        
        # Data
        'data/clinic_sequence.xml',
        'data/clinic_medication_data.xml',
        # 'data/clinic_vital_signs_reference.xml',
        
        # Views
        'views/clinic_patient_views.xml',
        'views/clinic_vital_signs_views.xml',
        'views/clinic_medication_views.xml',
        'views/clinic_prescription_views.xml',
        'views/lap_result.xml',
        'views/clinic_menu.xml',
        
        # Reports
        'report/clinic_prescription_report.xml',
        'report/clinic_patient_report.xml',
        
        # Wizards
        # 'wizard/clinic_prescription_wizard_views.xml',
    ],
    'demo': [
        'data/clinic_demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'clinic_management/static/src/css/clinic_management.css',
            'clinic_management/static/src/js/clinic_management.js',
        ],
        'web.assets_frontend': [
            'clinic_management/static/src/css/clinic_portal.css',
        ],
    },
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'external_dependencies': {
        'python': ['reportlab', 'qrcode'],
    },
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
}

