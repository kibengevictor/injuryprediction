import React, { useState, useEffect } from 'react';
import '../styles/HistoryModal.css';

const HistoryModal = ({ isOpen, onClose, onSelectAssessment }) => {
    const [history, setHistory] = useState([]);
    const [selectedId, setSelectedId] = useState(null);

    useEffect(() => {
        if (isOpen) {
            loadHistory();
        }
    }, [isOpen]);

    const loadHistory = () => {
        try {
            const savedHistory = localStorage.getItem('assessmentHistory');
            if (savedHistory) {
                const parsed = JSON.parse(savedHistory);
                // Sort by date, newest first
                parsed.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
                setHistory(parsed);
            } else {
                setHistory([]);
            }
        } catch (error) {
            console.error('Error loading history:', error);
            setHistory([]);
        }
    };

    const handleDelete = (id, e) => {
        e.stopPropagation();
        if (window.confirm('Are you sure you want to delete this assessment?')) {
            try {
                const updatedHistory = history.filter(item => item.id !== id);
                localStorage.setItem('assessmentHistory', JSON.stringify(updatedHistory));
                setHistory(updatedHistory);
                if (selectedId === id) {
                    setSelectedId(null);
                }
            } catch (error) {
                console.error('Error deleting assessment:', error);
            }
        }
    };

    const handleClearAll = () => {
        if (window.confirm('Are you sure you want to clear all history? This cannot be undone.')) {
            try {
                localStorage.removeItem('assessmentHistory');
                setHistory([]);
                setSelectedId(null);
            } catch (error) {
                console.error('Error clearing history:', error);
            }
        }
    };

    const handleView = (assessment) => {
        onSelectAssessment(assessment);
        onClose();
    };

    const formatDate = (timestamp) => {
        const date = new Date(timestamp);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    const getRiskColor = (score) => {
        if (score < 25) return '#22c55e';
        if (score < 50) return '#f59e0b';
        if (score < 75) return '#ef4444';
        return '#dc2626';
    };

    const getRiskEmoji = (level) => {
        switch (level) {
            case 'LOW': return '✅';
            case 'MODERATE': return '⚠️';
            case 'HIGH': return '🔴';
            case 'CRITICAL': return '🚨';
            default: return '⚠️';
        }
    };

    if (!isOpen) return null;

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content history-modal" onClick={(e) => e.stopPropagation()}>
                <div className="modal-header">
                    <h2>📊 Assessment History</h2>
                    <p>View your previous hamstring injury risk assessments</p>
                </div>

                {history.length === 0 ? (
                    <div className="empty-history">
                        <div className="empty-icon">📋</div>
                        <h3>No Assessment History</h3>
                        <p>Your completed assessments will appear here.</p>
                    </div>
                ) : (
                    <>
                        <div className="history-list">
                            {history.map((item) => (
                                <div
                                    key={item.id}
                                    className={`history-item ${selectedId === item.id ? 'selected' : ''}`}
                                    onClick={() => setSelectedId(item.id)}
                                >
                                    <div className="history-item-header">
                                        <div className="history-risk-badge" style={{ background: getRiskColor(item.results.riskScore) }}>
                                            <span className="risk-emoji">{getRiskEmoji(item.results.riskLevel)}</span>
                                            <span className="risk-score">{item.results.riskScore}%</span>
                                        </div>
                                        <div className="history-info">
                                            <div className="history-name">{item.userDetails?.name || 'Unknown'}</div>
                                            <div className="history-risk-level">{item.results.riskLevel} Risk</div>
                                            <div className="history-date">{formatDate(item.timestamp)}</div>
                                        </div>
                                    </div>

                                    <div className="history-details">
                                        <div className="detail-item">
                                            <span className="detail-label">Sport:</span>
                                            <span className="detail-value">{item.userDetails?.sport || 'N/A'}</span>
                                        </div>
                                        <div className="detail-item">
                                            <span className="detail-label">Primary Tissue:</span>
                                            <span className="detail-value">{item.biomarkers.primaryTissue || 'N/A'}</span>
                                        </div>
                                        <div className="detail-item">
                                            <span className="detail-label">Confidence:</span>
                                            <span className="detail-value">{item.results.confidence}%</span>
                                        </div>
                                    </div>

                                    <div className="history-item-actions">
                                        <button
                                            className="btn-view"
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                handleView(item);
                                            }}
                                        >
                                            View Details
                                        </button>
                                        <button
                                            className="btn-delete"
                                            onClick={(e) => handleDelete(item.id, e)}
                                        >
                                            🗑️
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>

                        <div className="history-footer">
                            <button className="btn-clear-all" onClick={handleClearAll}>
                                Clear All History
                            </button>
                        </div>
                    </>
                )}

                <div className="modal-actions">
                    <button className="btn-close" onClick={onClose}>
                        Close
                    </button>
                </div>
            </div>
        </div>
    );
};

export default HistoryModal;
