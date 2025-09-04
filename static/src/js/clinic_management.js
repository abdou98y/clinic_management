/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

// Clinic Management Dashboard Widget
class ClinicDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            patientCount: 0,
            todayVisits: 0,
            pendingPrescriptions: 0,
            criticalVitals: 0,
        });

        onWillStart(async () => {
            await this.loadDashboardData();
        });
    }

    async loadDashboardData() {
        try {
            // Load patient count
            const patientCount = await this.orm.searchCount("clinic.patient", [["active", "=", true]]);
            
            // Load today's visits
            const today = new Date().toISOString().split('T')[0];
            const todayVisits = await this.orm.searchCount("clinic.vital.signs", [
                ["visit_datetime", ">=", today + " 00:00:00"],
                ["visit_datetime", "<=", today + " 23:59:59"]
            ]);
            
            // Load pending prescriptions
            const pendingPrescriptions = await this.orm.searchCount("clinic.prescription", [
                ["state", "=", "draft"]
            ]);
            
            // Load critical vitals (high BP, fever, low O2)
            const criticalVitals = await this.orm.searchCount("clinic.vital.signs", [
                "|", "|",
                ["bp_category", "in", ["stage2", "crisis"]],
                ["temperature", ">", 38.5],
                ["oxygen_saturation", "<", 90]
            ]);

            this.state.patientCount = patientCount;
            this.state.todayVisits = todayVisits;
            this.state.pendingPrescriptions = pendingPrescriptions;
            this.state.criticalVitals = criticalVitals;
        } catch (error) {
            console.error("Error loading dashboard data:", error);
        }
    }
}

ClinicDashboard.template = "clinic_management.Dashboard";

// BMI Calculator Utility
class BMICalculator {
    static calculate(weight, height) {
        if (!weight || !height || weight <= 0 || height <= 0) {
            return null;
        }
        
        // Convert height from cm to meters if needed
        const heightInMeters = height > 3 ? height / 100 : height;
        const bmi = weight / (heightInMeters * heightInMeters);
        
        return Math.round(bmi * 10) / 10; // Round to 1 decimal place
    }
    
    static getCategory(bmi) {
        if (!bmi) return null;
        
        if (bmi < 18.5) return 'underweight';
        if (bmi < 25) return 'normal';
        if (bmi < 30) return 'overweight';
        if (bmi < 35) return 'obese_class1';
        if (bmi < 40) return 'obese_class2';
        return 'obese_class3';
    }
    
    static getCategoryLabel(category) {
        const labels = {
            'underweight': 'Underweight',
            'normal': 'Normal Weight',
            'overweight': 'Overweight',
            'obese_class1': 'Obese Class I',
            'obese_class2': 'Obese Class II',
            'obese_class3': 'Obese Class III'
        };
        return labels[category] || '';
    }
}

// Blood Pressure Categorization
class BloodPressureAnalyzer {
    static categorize(systolic, diastolic) {
        if (!systolic || !diastolic) return null;
        
        // Hypertensive Crisis
        if (systolic >= 180 || diastolic >= 120) return 'crisis';
        
        // Stage 2 Hypertension
        if (systolic >= 140 || diastolic >= 90) return 'stage2';
        
        // Stage 1 Hypertension
        if (systolic >= 130 || diastolic >= 80) return 'stage1';
        
        // Elevated
        if (systolic >= 120 && diastolic < 80) return 'elevated';
        
        // Normal
        if (systolic < 120 && diastolic < 80) return 'normal';
        
        return 'unknown';
    }
    
    static getCategoryLabel(category) {
        const labels = {
            'normal': 'Normal',
            'elevated': 'Elevated',
            'stage1': 'Stage 1 Hypertension',
            'stage2': 'Stage 2 Hypertension',
            'crisis': 'Hypertensive Crisis'
        };
        return labels[category] || '';
    }
    
    static getCategoryColor(category) {
        const colors = {
            'normal': '#28a745',
            'elevated': '#ffc107',
            'stage1': '#fd7e14',
            'stage2': '#dc3545',
            'crisis': '#721c24'
        };
        return colors[category] || '#6c757d';
    }
}

// Vital Signs Form Enhancement
class VitalSignsFormController extends Component {
    setup() {
        this.state = useState({
            weight: 0,
            height: 0,
            systolic: 0,
            diastolic: 0,
            bmi: null,
            bmiCategory: null,
            bpCategory: null
        });
    }
    
    onWeightChange(weight) {
        this.state.weight = weight;
        this.updateBMI();
    }
    
    onHeightChange(height) {
        this.state.height = height;
        this.updateBMI();
    }
    
    onBloodPressureChange(systolic, diastolic) {
        this.state.systolic = systolic;
        this.state.diastolic = diastolic;
        this.updateBloodPressureCategory();
    }
    
    updateBMI() {
        const bmi = BMICalculator.calculate(this.state.weight, this.state.height);
        this.state.bmi = bmi;
        this.state.bmiCategory = BMICalculator.getCategory(bmi);
    }
    
    updateBloodPressureCategory() {
        const category = BloodPressureAnalyzer.categorize(this.state.systolic, this.state.diastolic);
        this.state.bpCategory = category;
    }
}

// Drug Interaction Checker (placeholder for future implementation)
class DrugInteractionChecker {
    static async checkInteractions(medications) {
        // This would integrate with a drug interaction database
        // For now, return a placeholder
        return {
            hasInteractions: false,
            interactions: [],
            warnings: []
        };
    }
    
    static async checkAllergies(patientId, medicationId) {
        // Check patient allergies against medication
        return {
            hasAllergy: false,
            allergyType: null,
            severity: null
        };
    }
}

// Prescription Validation
class PrescriptionValidator {
    static validateDosage(medication, dose, frequency, patientAge, patientWeight) {
        const warnings = [];
        
        // Basic validation rules (would be expanded with real clinical data)
        if (patientAge < 18 && !medication.pediatric_use) {
            warnings.push("This medication is not approved for pediatric use");
        }
        
        if (patientAge > 65) {
            warnings.push("Consider dose adjustment for geriatric patient");
        }
        
        return {
            isValid: warnings.length === 0,
            warnings: warnings
        };
    }
    
    static validateControlledSubstance(medication, prescriber) {
        if (medication.controlled_substance && !prescriber.clinic_dea_number) {
            return {
                isValid: false,
                error: "DEA number required for controlled substances"
            };
        }
        
        return { isValid: true };
    }
}

// Utility Functions
const ClinicUtils = {
    formatBloodPressure: (systolic, diastolic) => {
        if (!systolic || !diastolic) return '';
        return `${systolic}/${diastolic}`;
    },
    
    formatTemperature: (celsius) => {
        if (!celsius) return '';
        const fahrenheit = (celsius * 9/5) + 32;
        return `${celsius}°C (${fahrenheit.toFixed(1)}°F)`;
    },
    
    formatBMI: (bmi) => {
        if (!bmi) return '';
        return `${bmi} kg/m²`;
    },
    
    getAgeFromBirthDate: (birthDate) => {
        if (!birthDate) return null;
        const today = new Date();
        const birth = new Date(birthDate);
        let age = today.getFullYear() - birth.getFullYear();
        const monthDiff = today.getMonth() - birth.getMonth();
        
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
            age--;
        }
        
        return age;
    },
    
    highlightAbnormalValues: (element, value, normalRange) => {
        if (!element || !value || !normalRange) return;
        
        const isAbnormal = value < normalRange.min || value > normalRange.max;
        
        if (isAbnormal) {
            element.classList.add('clinic_abnormal_value');
            element.style.backgroundColor = '#fff3cd';
            element.style.borderLeft = '4px solid #ffc107';
        } else {
            element.classList.remove('clinic_abnormal_value');
            element.style.backgroundColor = '';
            element.style.borderLeft = '';
        }
    }
};

// Export utilities for use in other modules
export {
    ClinicDashboard,
    BMICalculator,
    BloodPressureAnalyzer,
    VitalSignsFormController,
    DrugInteractionChecker,
    PrescriptionValidator,
    ClinicUtils
};

// Register dashboard widget
registry.category("dashboard").add("clinic_dashboard", ClinicDashboard);

// Initialize clinic management enhancements when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Add real-time BMI calculation to vital signs forms
    const weightInputs = document.querySelectorAll('input[name="weight"]');
    const heightInputs = document.querySelectorAll('input[name="height"]');
    
    function updateBMIDisplay() {
        const weight = parseFloat(document.querySelector('input[name="weight"]')?.value);
        const height = parseFloat(document.querySelector('input[name="height"]')?.value);
        const bmiDisplay = document.querySelector('.bmi_display');
        
        if (weight && height && bmiDisplay) {
            const bmi = BMICalculator.calculate(weight, height);
            const category = BMICalculator.getCategory(bmi);
            const categoryLabel = BMICalculator.getCategoryLabel(category);
            
            bmiDisplay.innerHTML = `BMI: ${bmi} (${categoryLabel})`;
            bmiDisplay.className = `bmi_display bmi_${category}`;
        }
    }
    
    weightInputs.forEach(input => {
        input.addEventListener('input', updateBMIDisplay);
    });
    
    heightInputs.forEach(input => {
        input.addEventListener('input', updateBMIDisplay);
    });
    
    // Add blood pressure categorization
    const systolicInputs = document.querySelectorAll('input[name="systolic_bp"]');
    const diastolicInputs = document.querySelectorAll('input[name="diastolic_bp"]');
    
    function updateBPDisplay() {
        const systolic = parseFloat(document.querySelector('input[name="systolic_bp"]')?.value);
        const diastolic = parseFloat(document.querySelector('input[name="diastolic_bp"]')?.value);
        const bpDisplay = document.querySelector('.bp_category_display');
        
        if (systolic && diastolic && bpDisplay) {
            const category = BloodPressureAnalyzer.categorize(systolic, diastolic);
            const categoryLabel = BloodPressureAnalyzer.getCategoryLabel(category);
            const categoryColor = BloodPressureAnalyzer.getCategoryColor(category);
            
            bpDisplay.innerHTML = categoryLabel;
            bpDisplay.style.color = categoryColor;
            bpDisplay.className = `bp_category_display bp_${category}`;
        }
    }
    
    systolicInputs.forEach(input => {
        input.addEventListener('input', updateBPDisplay);
    });
    
    diastolicInputs.forEach(input => {
        input.addEventListener('input', updateBPDisplay);
    });
});

console.log('Clinic Management System JavaScript loaded successfully');

