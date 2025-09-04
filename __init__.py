# -*- coding: utf-8 -*-

from . import models
from . import wizard
from . import report

def post_init_hook(env):
    """Post-installation hook to set up initial data and configurations."""

    # Create default medication categories if they don't exist
    categories = [
        'Analgesics', 'Antibiotics', 'Antihistamines', 'Antihypertensives',
        'Diabetes Medications', 'Cardiovascular', 'Respiratory', 'Gastrointestinal'
    ]
    
    for category in categories:
        existing = env['clinic.medication.category'].search([('name', '=', category)])
        if not existing:
            env['clinic.medication.category'].create({'name': category})
    
    # Set up default vital signs reference ranges
    env['clinic.vital.signs.reference'].create_default_ranges()


def uninstall_hook(env):
    """Pre-uninstallation hook to clean up data."""

    # Archive all clinic-related records instead of deleting
    models_to_archive = [
        'clinic.patient',
        'clinic.vital.signs',
        'clinic.prescription',
        'clinic.medication'
    ]
    
    for model_name in models_to_archive:
        if model_name in env:
            records = env[model_name].search([])
            records.write({'active': False})





# from . import models
# from . import wizard
# from . import report

# def post_init_hook(env):
#     """Post-installation hook to set up initial data and configurations."""
#     from odoo import api, SUPERUSER_ID
    
#     env = api.Environment(cr, SUPERUSER_ID, {})
    
#     # Create default medication categories if they don't exist
#     categories = [
#         'Analgesics', 'Antibiotics', 'Antihistamines', 'Antihypertensives',
#         'Diabetes Medications', 'Cardiovascular', 'Respiratory', 'Gastrointestinal'
#     ]
    
#     for category in categories:
#         existing = env['clinic.medication.category'].search([('name', '=', category)])
#         if not existing:
#             env['clinic.medication.category'].create({'name': category})
    
#     # Set up default vital signs reference ranges
#     env['clinic.vital.signs.reference'].create_default_ranges()

# def uninstall_hook(cr, registry):
#     """Pre-uninstallation hook to clean up data."""
#     from odoo import api, SUPERUSER_ID
    
#     env = api.Environment(cr, SUPERUSER_ID, {})
    
#     # Archive all clinic-related records instead of deleting
#     models_to_archive = [
#         'clinic.patient',
#         'clinic.vital.signs',
#         'clinic.prescription',
#         'clinic.medication'
#     ]
    
#     for model_name in models_to_archive:
#         if model_name in env:
#             records = env[model_name].search([])
#             records.write({'active': False})

