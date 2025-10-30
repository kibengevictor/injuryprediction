import React, { useState } from 'react';
import { FaTint, FaFlask } from 'react-icons/fa';
import UserDetailsModal from './UserDetailsModal';
import '../styles/BiomarkerInputForm.css';

const BiomarkerInputForm = ({ onSubmit }) => {
    const [isUserModalOpen, setIsUserModalOpen] = useState(false);
    const [formData, setFormData] = useState({
        saliva: {
            cortisol: '',
            testosterone: '',
            iga: ''
        },
        sweat: {
            sodium: '',
            lactate: '',
            glucose: ''
        },
        urine: {
            creatinine: '',
            protein: '',
            ph: ''
        }
    });

    const [errors, setErrors] = useState({});
    const [touched, setTouched] = useState({});

    // Normal ranges for validation
    const ranges = {
        saliva: {
            cortisol: { min: 0.1, max: 15, unit: 'μg/dL', normal: '0.1-15' },
            testosterone: { min: 10, max: 200, unit: 'pg/mL', normal: '10-200' },
            iga: { min: 10, max: 500, unit: 'μg/mL', normal: '10-500' }
        },
        sweat: {
            sodium: { min: 0.5, max: 3.0, unit: 'mmol/L', normal: '0.5-3.0' },
            lactate: { min: 0.5, max: 4.0, unit: 'mmol/L', normal: '0.5-4.0' },
            glucose: { min: 50, max: 150, unit: 'mg/dL', normal: '50-150' }
        },
        urine: {
            creatinine: { min: 20, max: 400, unit: 'mg/dL', normal: '20-400' },
            protein: { min: 0, max: 20, unit: 'mg/dL', normal: '0-20' },
            ph: { min: 4.5, max: 8.0, unit: 'pH', normal: '4.5-8.0' }
        }
    };

    const validateField = (tissue, biomarker, value) => {
        if (!value || value === '') return null;

        const numValue = parseFloat(value);
        if (isNaN(numValue)) return 'Invalid number';

        const range = ranges[tissue][biomarker];
        if (numValue < range.min || numValue > range.max) {
            return `Outside normal range (${range.normal} ${range.unit})`;
        }

        return null;
    };

    const handleInputChange = (tissue, biomarker, value) => {
        setFormData(prev => ({
            ...prev,
            [tissue]: {
                ...prev[tissue],
                [biomarker]: value
            }
        }));

        // Validate on change
        const error = validateField(tissue, biomarker, value);
        setErrors(prev => ({
            ...prev,
            [`${tissue}.${biomarker}`]: error
        }));
    };

    const handleBlur = (tissue, biomarker) => {
        setTouched(prev => ({
            ...prev,
            [`${tissue}.${biomarker}`]: true
        }));
    };

    const validateForm = () => {
        const newErrors = {};
        let hasAtLeastOneValue = false;

        Object.keys(formData).forEach(tissue => {
            Object.keys(formData[tissue]).forEach(biomarker => {
                const value = formData[tissue][biomarker];
                if (value && value !== '') {
                    hasAtLeastOneValue = true;
                    const error = validateField(tissue, biomarker, value);
                    if (error) {
                        newErrors[`${tissue}.${biomarker}`] = error;
                    }
                }
            });
        });

        if (!hasAtLeastOneValue) {
            newErrors.general = 'Please enter at least one biomarker value';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        // Mark all fields as touched
        const allTouched = {};
        Object.keys(formData).forEach(tissue => {
            Object.keys(formData[tissue]).forEach(biomarker => {
                allTouched[`${tissue}.${biomarker}`] = true;
            });
        });
        setTouched(allTouched);

        if (validateForm()) {
            // Open user details modal instead of direct submission
            setIsUserModalOpen(true);
        }
    };

    const handleUserDetailsSubmit = (userDetails) => {
        // Combine biomarker data with user details
        const completeData = {
            ...formData,
            userDetails
        };
        onSubmit(completeData);
        setIsUserModalOpen(false);
    };

    const renderBiomarkerInput = (tissue, biomarker, label) => {
        const value = formData[tissue][biomarker];
        const error = errors[`${tissue}.${biomarker}`];
        const isTouched = touched[`${tissue}.${biomarker}`];
        const range = ranges[tissue][biomarker];

        return (
            <div className="biomarker-input-group" key={`${tissue}-${biomarker}`}>
                <label htmlFor={`${tissue}-${biomarker}`}>
                    {label}
                    <span className="unit">({range.unit})</span>
                </label>
                <input
                    type="number"
                    id={`${tissue}-${biomarker}`}
                    step="0.01"
                    value={value}
                    onChange={(e) => handleInputChange(tissue, biomarker, e.target.value)}
                    onBlur={() => handleBlur(tissue, biomarker)}
                    placeholder={`Normal: ${range.normal}`}
                    className={isTouched && error ? 'input-error' : ''}
                />
                {isTouched && error && (
                    <span className="error-message">{error}</span>
                )}
                {isTouched && !error && value && (
                    <span className="success-message">✓ Valid</span>
                )}
            </div>
        );
    };

    return (
        <div className="biomarker-form-container">
            <UserDetailsModal
                isOpen={isUserModalOpen}
                onClose={() => setIsUserModalOpen(false)}
                onSubmit={handleUserDetailsSubmit}
            />

            <div className="form-header">
                <h2>Enter Your Biomarker Results</h2>
                <p>Input values from your laboratory test results for all three tissue types.</p>
            </div>

            <form onSubmit={handleSubmit} className="biomarker-form">
                {errors.general && (
                    <div className="general-error">{errors.general}</div>
                )}

                {/* Saliva Section */}
                <div className="tissue-section saliva-section">
                    <div className="section-header">
                        <FaTint className="tissue-icon" />
                        <h3>Saliva Biomarkers</h3>
                    </div>
                    <div className="biomarker-inputs">
                        {renderBiomarkerInput('saliva', 'cortisol', 'Cortisol')}
                        {renderBiomarkerInput('saliva', 'testosterone', 'Testosterone')}
                        {renderBiomarkerInput('saliva', 'iga', 'Immunoglobulin A (IgA)')}
                    </div>
                </div>

                {/* Sweat Section */}
                <div className="tissue-section sweat-section">
                    <div className="section-header">
                        <FaTint className="tissue-icon" />
                        <h3>Sweat Biomarkers</h3>
                    </div>
                    <div className="biomarker-inputs">
                        {renderBiomarkerInput('sweat', 'sodium', 'Sodium')}
                        {renderBiomarkerInput('sweat', 'lactate', 'Lactate')}
                        {renderBiomarkerInput('sweat', 'glucose', 'Glucose')}
                    </div>
                </div>

                {/* Urine Section */}
                <div className="tissue-section urine-section">
                    <div className="section-header">
                        <FaFlask className="tissue-icon" />
                        <h3>Urine Biomarkers</h3>
                    </div>
                    <div className="biomarker-inputs">
                        {renderBiomarkerInput('urine', 'creatinine', 'Creatinine')}
                        {renderBiomarkerInput('urine', 'protein', 'Protein')}
                        {renderBiomarkerInput('urine', 'ph', 'pH Level')}
                    </div>
                </div>

                <div className="form-actions">
                    <button type="submit" className="submit-button">
                        Analyze Risk
                    </button>
                </div>
            </form>

            <div className="form-footer">
                <div className="info-box">
                    <h4>💡 Tips for Accurate Assessment</h4>
                    <ul>
                        <li>Enter values exactly as shown on your lab results</li>
                        <li>Values outside normal ranges will trigger a warning but can still be submitted</li>
                        <li>For best results, provide data from all three tissue types</li>
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default BiomarkerInputForm;
