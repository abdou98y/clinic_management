# -*- coding: utf-8 -*-
{
    'name': 'Custom Clinic Management System - AY',
    'version': '19.0.1.0.0',
    'category': 'Healthcare',
    'summary': 'Comprehensive clinic management system for patient care, vital signs, and prescriptions',
    'description': "built for Odoo 19 Community Edition",
    'author': 'Abdelrhman younes',
    'website': 'https://github.com/abdou98y/clinic_management',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'web',
        'portal',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',
        # Reports
        'report/clinic_patient_report.xml',
        'report/report_medical_prescription.xml',
        'report/report_medical_prescription_action.xml',
        # Data
        'data/clinic_sequence.xml',
        # Views
        'views/clinic_patient_views.xml',
        'views/clinic_vital_signs_views.xml',
        'views/lap_result.xml',
        'views/clinic_menu.xml',
        'views/patient_complaint.xml',
        'views/prescription.xml',
        # Wizards
    ],
    'assets': {
        'web.assets_backend': [
            'clinic_management/static/src/js/patient_autosave.js',
        ],
        'web.report_assets_common': [
                'clinic_management/static/src/scss/fonts.scss',
            ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'external_dependencies': {
        'python': ['reportlab', 'qrcode'],
    },
}

