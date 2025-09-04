# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ClinicVitalSignsReference(models.Model):
    _name = 'clinic.vital.signs.reference'
    _description = 'Vital Signs Reference Ranges'
    _order = 'age_min, age_max'

    name = fields.Char(
        string='Reference Name',
        required=True,
        help="Name for this reference range set"
    )
    
    # Age Range
    age_min = fields.Integer(
        string='Minimum Age (years)',
        default=0,
        help="Minimum age for this reference range"
    )
    
    age_max = fields.Integer(
        string='Maximum Age (years)',
        default=150,
        help="Maximum age for this reference range"
    )
    
    gender = fields.Selection([
        ('all', 'All Genders'),
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender', default='all')

    # Blood Pressure Ranges
    systolic_bp_min = fields.Integer(
        string='Systolic BP Min (mmHg)',
        help="Minimum normal systolic blood pressure"
    )
    systolic_bp_max = fields.Integer(
        string='Systolic BP Max (mmHg)',
        help="Maximum normal systolic blood pressure"
    )
    diastolic_bp_min = fields.Integer(
        string='Diastolic BP Min (mmHg)',
        help="Minimum normal diastolic blood pressure"
    )
    diastolic_bp_max = fields.Integer(
        string='Diastolic BP Max (mmHg)',
        help="Maximum normal diastolic blood pressure"
    )

    # Heart Rate Ranges
    heart_rate_min = fields.Integer(
        string='Heart Rate Min (bpm)',
        help="Minimum normal heart rate"
    )
    heart_rate_max = fields.Integer(
        string='Heart Rate Max (bpm)',
        help="Maximum normal heart rate"
    )

    # Temperature Ranges
    temperature_min = fields.Float(
        string='Temperature Min (°C)',
        digits=(4, 1),
        help="Minimum normal body temperature"
    )
    temperature_max = fields.Float(
        string='Temperature Max (°C)',
        digits=(4, 1),
        help="Maximum normal body temperature"
    )

    # Respiratory Rate Ranges
    respiratory_rate_min = fields.Integer(
        string='Respiratory Rate Min (/min)',
        help="Minimum normal respiratory rate"
    )
    respiratory_rate_max = fields.Integer(
        string='Respiratory Rate Max (/min)',
        help="Maximum normal respiratory rate"
    )

    # Oxygen Saturation Ranges
    oxygen_saturation_min = fields.Float(
        string='SpO₂ Min (%)',
        digits=(5, 1),
        help="Minimum normal oxygen saturation"
    )
    oxygen_saturation_max = fields.Float(
        string='SpO₂ Max (%)',
        digits=(5, 1),
        help="Maximum normal oxygen saturation"
    )

    # BMI Ranges (for adults)
    bmi_underweight_max = fields.Float(
        string='BMI Underweight Max',
        digits=(4, 1),
        default=18.5
    )
    bmi_normal_max = fields.Float(
        string='BMI Normal Max',
        digits=(4, 1),
        default=24.9
    )
    bmi_overweight_max = fields.Float(
        string='BMI Overweight Max',
        digits=(4, 1),
        default=29.9
    )

    active = fields.Boolean(
        string='Active',
        default=True
    )
    
    notes = fields.Text(
        string='Notes',
        help="Additional notes about these reference ranges"
    )

    @api.model
    def create_default_ranges(self):
        """Create default reference ranges for different age groups."""
        default_ranges = [
            {
                'name': 'Adult (18-65 years)',
                'age_min': 18,
                'age_max': 65,
                'gender': 'all',
                'systolic_bp_min': 90,
                'systolic_bp_max': 120,
                'diastolic_bp_min': 60,
                'diastolic_bp_max': 80,
                'heart_rate_min': 60,
                'heart_rate_max': 100,
                'temperature_min': 36.1,
                'temperature_max': 37.2,
                'respiratory_rate_min': 12,
                'respiratory_rate_max': 20,
                'oxygen_saturation_min': 95.0,
                'oxygen_saturation_max': 100.0,
            },
            {
                'name': 'Elderly (65+ years)',
                'age_min': 65,
                'age_max': 150,
                'gender': 'all',
                'systolic_bp_min': 90,
                'systolic_bp_max': 140,
                'diastolic_bp_min': 60,
                'diastolic_bp_max': 90,
                'heart_rate_min': 60,
                'heart_rate_max': 100,
                'temperature_min': 36.0,
                'temperature_max': 37.2,
                'respiratory_rate_min': 12,
                'respiratory_rate_max': 25,
                'oxygen_saturation_min': 95.0,
                'oxygen_saturation_max': 100.0,
            },
            {
                'name': 'Adolescent (13-17 years)',
                'age_min': 13,
                'age_max': 17,
                'gender': 'all',
                'systolic_bp_min': 90,
                'systolic_bp_max': 120,
                'diastolic_bp_min': 60,
                'diastolic_bp_max': 80,
                'heart_rate_min': 60,
                'heart_rate_max': 100,
                'temperature_min': 36.1,
                'temperature_max': 37.2,
                'respiratory_rate_min': 12,
                'respiratory_rate_max': 20,
                'oxygen_saturation_min': 95.0,
                'oxygen_saturation_max': 100.0,
            },
            {
                'name': 'Child (6-12 years)',
                'age_min': 6,
                'age_max': 12,
                'gender': 'all',
                'systolic_bp_min': 80,
                'systolic_bp_max': 110,
                'diastolic_bp_min': 50,
                'diastolic_bp_max': 70,
                'heart_rate_min': 70,
                'heart_rate_max': 120,
                'temperature_min': 36.1,
                'temperature_max': 37.2,
                'respiratory_rate_min': 15,
                'respiratory_rate_max': 25,
                'oxygen_saturation_min': 95.0,
                'oxygen_saturation_max': 100.0,
            },
            {
                'name': 'Preschool (3-5 years)',
                'age_min': 3,
                'age_max': 5,
                'gender': 'all',
                'systolic_bp_min': 75,
                'systolic_bp_max': 105,
                'diastolic_bp_min': 45,
                'diastolic_bp_max': 65,
                'heart_rate_min': 80,
                'heart_rate_max': 130,
                'temperature_min': 36.1,
                'temperature_max': 37.2,
                'respiratory_rate_min': 20,
                'respiratory_rate_max': 30,
                'oxygen_saturation_min': 95.0,
                'oxygen_saturation_max': 100.0,
            },
            {
                'name': 'Toddler (1-2 years)',
                'age_min': 1,
                'age_max': 2,
                'gender': 'all',
                'systolic_bp_min': 70,
                'systolic_bp_max': 100,
                'diastolic_bp_min': 40,
                'diastolic_bp_max': 60,
                'heart_rate_min': 90,
                'heart_rate_max': 150,
                'temperature_min': 36.1,
                'temperature_max': 37.2,
                'respiratory_rate_min': 25,
                'respiratory_rate_max': 35,
                'oxygen_saturation_min': 95.0,
                'oxygen_saturation_max': 100.0,
            },
            {
                'name': 'Infant (0-12 months)',
                'age_min': 0,
                'age_max': 0,
                'gender': 'all',
                'systolic_bp_min': 65,
                'systolic_bp_max': 90,
                'diastolic_bp_min': 35,
                'diastolic_bp_max': 55,
                'heart_rate_min': 100,
                'heart_rate_max': 160,
                'temperature_min': 36.1,
                'temperature_max': 37.2,
                'respiratory_rate_min': 30,
                'respiratory_rate_max': 50,
                'oxygen_saturation_min': 95.0,
                'oxygen_saturation_max': 100.0,
            }
        ]
        
        for range_data in default_ranges:
            existing = self.search([
                ('name', '=', range_data['name']),
                ('age_min', '=', range_data['age_min']),
                ('age_max', '=', range_data['age_max'])
            ])
            if not existing:
                self.create(range_data)

    @api.model
    def get_reference_range(self, age, gender='all'):
        """Get appropriate reference range for given age and gender."""
        domain = [
            ('active', '=', True),
            ('age_min', '<=', age),
            ('age_max', '>=', age),
            '|',
            ('gender', '=', 'all'),
            ('gender', '=', gender)
        ]
        
        # Prefer gender-specific ranges over general ones
        ranges = self.search(domain, order='gender desc, age_min desc')
        return ranges[:1] if ranges else self.browse()

    def check_vital_signs(self, vital_signs_record):
        """Check if vital signs are within normal ranges."""
        self.ensure_one()
        results = {
            'normal': [],
            'abnormal': [],
            'warnings': []
        }
        
        # Check blood pressure
        if vital_signs_record.systolic_bp and vital_signs_record.diastolic_bp:
            if (self.systolic_bp_min <= vital_signs_record.systolic_bp <= self.systolic_bp_max and
                self.diastolic_bp_min <= vital_signs_record.diastolic_bp <= self.diastolic_bp_max):
                results['normal'].append('Blood Pressure')
            else:
                results['abnormal'].append(
                    f"Blood Pressure: {vital_signs_record.systolic_bp}/{vital_signs_record.diastolic_bp} "
                    f"(Normal: {self.systolic_bp_min}-{self.systolic_bp_max}/{self.diastolic_bp_min}-{self.diastolic_bp_max})"
                )
        
        # Check heart rate
        if vital_signs_record.heart_rate:
            if self.heart_rate_min <= vital_signs_record.heart_rate <= self.heart_rate_max:
                results['normal'].append('Heart Rate')
            else:
                results['abnormal'].append(
                    f"Heart Rate: {vital_signs_record.heart_rate} bpm "
                    f"(Normal: {self.heart_rate_min}-{self.heart_rate_max})"
                )
        
        # Check temperature
        if vital_signs_record.temperature:
            if self.temperature_min <= vital_signs_record.temperature <= self.temperature_max:
                results['normal'].append('Temperature')
            else:
                results['abnormal'].append(
                    f"Temperature: {vital_signs_record.temperature}°C "
                    f"(Normal: {self.temperature_min}-{self.temperature_max})"
                )
        
        # Check respiratory rate
        if vital_signs_record.respiratory_rate:
            if self.respiratory_rate_min <= vital_signs_record.respiratory_rate <= self.respiratory_rate_max:
                results['normal'].append('Respiratory Rate')
            else:
                results['abnormal'].append(
                    f"Respiratory Rate: {vital_signs_record.respiratory_rate}/min "
                    f"(Normal: {self.respiratory_rate_min}-{self.respiratory_rate_max})"
                )
        
        # Check oxygen saturation
        if vital_signs_record.oxygen_saturation:
            if self.oxygen_saturation_min <= vital_signs_record.oxygen_saturation <= self.oxygen_saturation_max:
                results['normal'].append('Oxygen Saturation')
            else:
                results['abnormal'].append(
                    f"SpO₂: {vital_signs_record.oxygen_saturation}% "
                    f"(Normal: {self.oxygen_saturation_min}-{self.oxygen_saturation_max})"
                )
        
        return results

    def name_get(self):
        """Display name with age range and gender."""
        result = []
        for record in self:
            name = record.name
            if record.age_min == record.age_max:
                age_range = f"{record.age_min} years"
            else:
                age_range = f"{record.age_min}-{record.age_max} years"
            
            if record.gender != 'all':
                gender_display = dict(record._fields['gender'].selection)[record.gender]
                name += f" ({gender_display}, {age_range})"
            else:
                name += f" ({age_range})"
            
            result.append((record.id, name))
        return result

