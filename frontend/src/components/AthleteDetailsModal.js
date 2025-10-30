import React, { useState } from 'react';
import '../styles/AthleteDetailsModal.css';

const AthleteDetailsModal = ({ isOpen, onClose, onSubmit }) => {
    const [formData, setFormData] = useState({
        name: '',
        age: '',
        sport: ''
    });

    const [errors, setErrors] = useState({});

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
        // Clear error when user starts typing
        if (errors[name]) {
            setErrors(prev => ({
                ...prev,
                [name]: ''
            }));
        }
    };

    const validateForm = () => {
        const newErrors = {};

        if (!formData.name.trim()) {
            newErrors.name = 'Name is required';
        }

        if (!formData.age.trim()) {
            newErrors.age = 'Age is required';
        } else if (isNaN(formData.age) || parseInt(formData.age) < 1 || parseInt(formData.age) > 120) {
            newErrors.age = 'Please enter a valid age (1-120)';
        }

        if (!formData.sport.trim()) {
            newErrors.sport = 'Sport/Activity is required';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (validateForm()) {
            onSubmit(formData);
            // Reset form
            setFormData({ name: '', age: '', sport: '' });
            setErrors({});
        }
    };

    const handleCancel = () => {
        setFormData({ name: '', age: '', sport: '' });
        setErrors({});
        onClose();
    };

    if (!isOpen) return null;

    return (
        <div className="modal-overlay" onClick={handleCancel}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <div className="modal-header">
                    <h2>📋 Athlete Information</h2>
                    <p>Please provide your details for the PDF report</p>
                </div>

                <form onSubmit={handleSubmit} className="modal-form">
                    <div className="form-group">
                        <label htmlFor="name">Full Name *</label>
                        <input
                            type="text"
                            id="name"
                            name="name"
                            value={formData.name}
                            onChange={handleChange}
                            placeholder="Enter your full name"
                            className={errors.name ? 'error' : ''}
                        />
                        {errors.name && <span className="error-message">{errors.name}</span>}
                    </div>

                    <div className="form-group">
                        <label htmlFor="age">Age *</label>
                        <input
                            type="number"
                            id="age"
                            name="age"
                            value={formData.age}
                            onChange={handleChange}
                            placeholder="Enter your age"
                            min="1"
                            max="120"
                            className={errors.age ? 'error' : ''}
                        />
                        {errors.age && <span className="error-message">{errors.age}</span>}
                    </div>

                    <div className="form-group">
                        <label htmlFor="sport">Sport/Activity *</label>
                        <input
                            type="text"
                            id="sport"
                            name="sport"
                            value={formData.sport}
                            onChange={handleChange}
                            placeholder="e.g., Soccer, Running, Basketball"
                            className={errors.sport ? 'error' : ''}
                        />
                        {errors.sport && <span className="error-message">{errors.sport}</span>}
                    </div>

                    <div className="modal-actions">
                        <button type="button" className="btn-cancel" onClick={handleCancel}>
                            Cancel
                        </button>
                        <button type="submit" className="btn-submit">
                            Generate PDF
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default AthleteDetailsModal;
