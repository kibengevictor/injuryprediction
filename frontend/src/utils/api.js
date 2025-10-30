import axios from 'axios';

// Base API URL - update this to match your backend
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

/**
 * Submit biomarker data for risk prediction
 * @param {Object} biomarkerData - Object containing saliva, sweat, and urine biomarker values
 * @returns {Promise} - API response with prediction results
 */
export const submitBiomarkerData = async (biomarkerData) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/predict`, biomarkerData, {
            headers: {
                'Content-Type': 'application/json',
            },
            timeout: 30000, // 30 second timeout
        });
        return response.data;
    } catch (error) {
        if (error.response) {
            // Server responded with error status
            throw new Error(error.response.data.error || 'Failed to get prediction from server');
        } else if (error.request) {
            // Request made but no response
            throw new Error('No response from server. Please check your connection.');
        } else {
            // Something else happened
            throw new Error('Failed to submit data: ' + error.message);
        }
    }
};

/**
 * Validate biomarker data before submission
 * @param {Object} biomarkerData - Biomarker data to validate
 * @returns {Object} - { isValid: boolean, errors: array }
 */
export const validateBiomarkerData = (biomarkerData) => {
    const errors = [];
    let hasData = false;

    const ranges = {
        saliva: {
            cortisol: { min: 0.1, max: 15, unit: 'μg/dL' },
            testosterone: { min: 10, max: 200, unit: 'pg/mL' },
            iga: { min: 10, max: 500, unit: 'μg/mL' }
        },
        sweat: {
            sodium: { min: 0.5, max: 3.0, unit: 'mmol/L' },
            lactate: { min: 0.5, max: 4.0, unit: 'mmol/L' },
            glucose: { min: 50, max: 150, unit: 'mg/dL' }
        },
        urine: {
            creatinine: { min: 20, max: 400, unit: 'mg/dL' },
            protein: { min: 0, max: 20, unit: 'mg/dL' },
            ph: { min: 4.5, max: 8.0, unit: 'pH' }
        }
    };

    // Check each tissue type
    Object.keys(biomarkerData).forEach(tissue => {
        Object.keys(biomarkerData[tissue]).forEach(biomarker => {
            const value = biomarkerData[tissue][biomarker];

            if (value && value !== '') {
                hasData = true;
                const numValue = parseFloat(value);

                if (isNaN(numValue)) {
                    errors.push(`${tissue}.${biomarker}: Invalid number`);
                } else {
                    const range = ranges[tissue][biomarker];
                    if (numValue < range.min || numValue > range.max) {
                        errors.push(
                            `${tissue}.${biomarker}: Value ${numValue} is outside normal range (${range.min}-${range.max} ${range.unit})`
                        );
                    }
                }
            }
        });
    });

    if (!hasData) {
        errors.push('Please enter at least one biomarker value');
    }

    return {
        isValid: errors.length === 0,
        errors
    };
};

/**
 * Format biomarker data for display
 * @param {Object} biomarkerData - Raw biomarker data
 * @returns {Array} - Formatted array of biomarker entries
 */
export const formatBiomarkerData = (biomarkerData) => {
    const formatted = [];

    const tissueLabels = {
        saliva: 'Saliva',
        sweat: 'Sweat',
        urine: 'Urine'
    };

    const biomarkerLabels = {
        cortisol: 'Cortisol',
        testosterone: 'Testosterone',
        iga: 'IgA',
        sodium: 'Sodium',
        lactate: 'Lactate',
        glucose: 'Glucose',
        creatinine: 'Creatinine',
        protein: 'Protein',
        ph: 'pH'
    };

    Object.keys(biomarkerData).forEach(tissue => {
        Object.keys(biomarkerData[tissue]).forEach(biomarker => {
            const value = biomarkerData[tissue][biomarker];
            if (value && value !== '') {
                formatted.push({
                    tissue: tissueLabels[tissue],
                    biomarker: biomarkerLabels[biomarker],
                    value: parseFloat(value)
                });
            }
        });
    });

    return formatted;
};

/**
 * Generate PDF report (placeholder - implement with jsPDF)
 * @param {Object} results - Prediction results
 * @param {Object} biomarkerData - Input biomarker data
 */
export const generatePDFReport = (results, biomarkerData) => {
    // TODO: Implement PDF generation using jsPDF
    console.log('Generating PDF report...', results, biomarkerData);
    alert('PDF generation coming soon!');
};

/**
 * Send results via email (placeholder)
 * @param {string} email - Recipient email
 * @param {Object} results - Prediction results
 */
export const emailResults = async (email, results) => {
    // TODO: Implement email functionality
    console.log('Sending email to:', email, results);
    alert('Email functionality coming soon!');
};

export default {
    submitBiomarkerData,
    validateBiomarkerData,
    formatBiomarkerData,
    generatePDFReport,
    emailResults
};
