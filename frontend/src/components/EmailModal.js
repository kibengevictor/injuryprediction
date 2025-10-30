import React, { useState } from 'react';
import '../styles/EmailModal.css';

const EmailModal = ({ isOpen, onClose, onSubmit }) => {
    const [formData, setFormData] = useState({
        email: '',
        recipientName: ''
    });

    const [errors, setErrors] = useState({});
    const [isSending, setIsSending] = useState(false);

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

    const validateEmail = (email) => {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    };

    const validateForm = () => {
        const newErrors = {};

        if (!formData.email.trim()) {
            newErrors.email = 'Email address is required';
        } else if (!validateEmail(formData.email)) {
            newErrors.email = 'Please enter a valid email address';
        }

        if (!formData.recipientName.trim()) {
            newErrors.recipientName = 'Recipient name is required';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (validateForm()) {
            setIsSending(true);
            try {
                await onSubmit(formData);
                // Reset form on success
                setFormData({ email: '', recipientName: '' });
                setErrors({});
            } catch (error) {
                setErrors({ submit: 'Failed to send email. Please try again.' });
            } finally {
                setIsSending(false);
            }
        }
    };

    const handleCancel = () => {
        setFormData({ email: '', recipientName: '' });
        setErrors({});
        onClose();
    };

    if (!isOpen) return null;

    return (
        <div className="modal-overlay" onClick={handleCancel}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <div className="modal-header">
                    <h2>📧 Email Results</h2>
                    <p>Send your assessment report via email</p>
                </div>

                <form onSubmit={handleSubmit} className="modal-form">
                    <div className="form-group">
                        <label htmlFor="recipientName">Recipient Name *</label>
                        <input
                            type="text"
                            id="recipientName"
                            name="recipientName"
                            value={formData.recipientName}
                            onChange={handleChange}
                            placeholder="Enter recipient's name"
                            className={errors.recipientName ? 'error' : ''}
                            disabled={isSending}
                        />
                        {errors.recipientName && <span className="error-message">{errors.recipientName}</span>}
                    </div>

                    <div className="form-group">
                        <label htmlFor="email">Email Address *</label>
                        <input
                            type="email"
                            id="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            placeholder="example@email.com"
                            className={errors.email ? 'error' : ''}
                            disabled={isSending}
                        />
                        {errors.email && <span className="error-message">{errors.email}</span>}
                    </div>

                    {errors.submit && (
                        <div className="error-message submit-error">{errors.submit}</div>
                    )}

                    <div className="modal-actions">
                        <button type="button" className="btn-cancel" onClick={handleCancel} disabled={isSending}>
                            Cancel
                        </button>
                        <button type="submit" className="btn-submit" disabled={isSending}>
                            {isSending ? '📤 Sending...' : '📧 Send Email'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default EmailModal;
