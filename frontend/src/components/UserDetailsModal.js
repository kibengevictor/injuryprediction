import React, { useState } from 'react';
import '../styles/UserDetailsModal.css';

const UserDetailsModal = ({ isOpen, onClose, onSubmit }) => {
    const [formData, setFormData] = useState({
        name: '',
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

    const validate = () => {
        const newErrors = {};

        if (!formData.name.trim()) {
            newErrors.name = 'Name is required';
        } else if (formData.name.trim().length < 2) {
            newErrors.name = 'Name must be at least 2 characters';
        }

        if (!formData.sport.trim()) {
            newErrors.sport = 'Sport/Activity is required';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (validate()) {
            onSubmit({
                name: formData.name.trim(),
                sport: formData.sport.trim()
            });
            // Reset form
            setFormData({ name: '', sport: '' });
            setErrors({});
        }
    };

    const handleClose = () => {
        setFormData({ name: '', sport: '' });
        setErrors({});
        onClose();
    };

    if (!isOpen) return null;

    return (
        <div className="modal-overlay" onClick={handleClose}>
            <div className="modal-content user-details-modal" onClick={(e) => e.stopPropagation()}>
                <div className="modal-header">
                    <h2>👤 Your Information</h2>
                    <p>Please provide your details before starting the assessment</p>
                </div>

                <form onSubmit={handleSubmit} className="user-details-form">
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
                        <button type="button" className="btn-cancel" onClick={handleClose}>
                            Cancel
                        </button>
                        <button type="submit" className="btn-submit">
                            Continue to Analysis
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default UserDetailsModal;
