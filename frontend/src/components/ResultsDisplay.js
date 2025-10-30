import React, { useState, useEffect } from 'react';
import { FaDownload, FaEnvelope, FaRedo, FaChartLine } from 'react-icons/fa';
import jsPDF from 'jspdf';
import AthleteDetailsModal from './AthleteDetailsModal';
import EmailModal from './EmailModal';
import HistoryModal from './HistoryModal';
import '../styles/ResultsDisplay.css';

const ResultsDisplay = ({ results, userDetails, onNewAssessment }) => {
    const { riskScore, riskLevel, confidence, keyIndicators, recommendations } = results;
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isEmailModalOpen, setIsEmailModalOpen] = useState(false);
    const [isSuccessModalOpen, setIsSuccessModalOpen] = useState(false);
    const [successEmail, setSuccessEmail] = useState('');
    const [isHistoryModalOpen, setIsHistoryModalOpen] = useState(false);

    // Save assessment to history when component mounts
    useEffect(() => {
        saveToHistory();
    }, []);

    const saveToHistory = () => {
        try {
            const assessment = {
                id: Date.now().toString(),
                timestamp: new Date().toISOString(),
                userDetails: {
                    name: userDetails?.name || 'Unknown',
                    sport: userDetails?.sport || 'Not specified'
                },
                results: {
                    riskScore,
                    riskLevel,
                    confidence,
                    keyIndicators,
                    recommendations
                },
                biomarkers: {
                    primaryTissue: keyIndicators.split(',')[0]?.trim() || 'N/A'
                }
            };

            // Get existing history
            const savedHistory = localStorage.getItem('assessmentHistory');
            const history = savedHistory ? JSON.parse(savedHistory) : [];

            // Add new assessment to the beginning
            history.unshift(assessment);

            // Keep only the last 50 assessments
            const trimmedHistory = history.slice(0, 50);

            // Save back to localStorage
            localStorage.setItem('assessmentHistory', JSON.stringify(trimmedHistory));
        } catch (error) {
            console.error('Error saving to history:', error);
        }
    };

    const handleSelectAssessment = (assessment) => {
        // This could be enhanced to show the selected assessment
        // For now, we'll just close the modal
        console.log('Selected assessment:', assessment);
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

    const generatePDF = (athleteDetails) => {
        const { name, age, sport } = athleteDetails;

        const doc = new jsPDF();
        const pageWidth = doc.internal.pageSize.getWidth();
        const margin = 20;
        let yPos = 20;

        // Title
        doc.setFontSize(20);
        doc.setTextColor(44, 62, 80);
        doc.text('Hamstring Injury Risk Assessment Report', pageWidth / 2, yPos, { align: 'center' });

        yPos += 15;
        doc.setFontSize(10);
        doc.setTextColor(100, 100, 100);
        doc.text(`Generated: ${new Date().toLocaleString()}`, pageWidth / 2, yPos, { align: 'center' });

        yPos += 15;

        // Athlete Information Section
        doc.setFontSize(16);
        doc.setTextColor(44, 62, 80);
        doc.text('Athlete Information', margin, yPos);
        yPos += 10;

        doc.setFontSize(12);
        doc.setTextColor(0, 0, 0);
        doc.text(`Name: ${name}`, margin, yPos);
        yPos += 7;
        doc.text(`Age: ${age}`, margin, yPos);
        yPos += 7;
        doc.text(`Sport/Activity: ${sport}`, margin, yPos);
        yPos += 15;

        // Risk Score Section
        doc.setFontSize(16);
        doc.setTextColor(44, 62, 80);
        doc.text('Risk Assessment', margin, yPos);
        yPos += 10;

        doc.setFontSize(12);
        doc.setTextColor(0, 0, 0);
        doc.text(`Risk Score: ${riskScore}%`, margin, yPos);
        yPos += 7;
        doc.text(`Risk Level: ${riskLevel}`, margin, yPos);
        yPos += 7;
        doc.text(`Model Confidence: ${confidence}%`, margin, yPos);
        yPos += 15;

        // Key Indicators
        doc.setFontSize(16);
        doc.setTextColor(44, 62, 80);
        doc.text('Key Indicators', margin, yPos);
        yPos += 10;

        doc.setFontSize(11);
        doc.setTextColor(0, 0, 0);
        const splitIndicators = doc.splitTextToSize(keyIndicators, pageWidth - 2 * margin);
        doc.text(splitIndicators, margin, yPos);
        yPos += splitIndicators.length * 7 + 10;

        // Recommendations
        doc.setFontSize(16);
        doc.setTextColor(44, 62, 80);
        doc.text('Recommendations', margin, yPos);
        yPos += 10;

        // Immediate Actions
        doc.setFontSize(13);
        doc.setTextColor(239, 68, 68);
        doc.text('IMMEDIATE ACTIONS:', margin, yPos);
        yPos += 8;

        doc.setFontSize(10);
        doc.setTextColor(0, 0, 0);
        recommendations.immediate.forEach((item, index) => {
            const splitText = doc.splitTextToSize(`${index + 1}. ${item}`, pageWidth - 2 * margin - 5);
            doc.text(splitText, margin + 5, yPos);
            yPos += splitText.length * 5 + 2;
        });
        yPos += 5;

        // Check if we need a new page
        if (yPos > 250) {
            doc.addPage();
            yPos = 20;
        }

        // Follow-up Actions
        doc.setFontSize(13);
        doc.setTextColor(245, 158, 11);
        doc.text('FOLLOW-UP (Within 3-5 Days):', margin, yPos);
        yPos += 8;

        doc.setFontSize(10);
        doc.setTextColor(0, 0, 0);
        recommendations.followUp.forEach((item, index) => {
            const splitText = doc.splitTextToSize(`${index + 1}. ${item}`, pageWidth - 2 * margin - 5);
            doc.text(splitText, margin + 5, yPos);
            yPos += splitText.length * 5 + 2;

            if (yPos > 270) {
                doc.addPage();
                yPos = 20;
            }
        });
        yPos += 5;

        // Monitoring
        doc.setFontSize(13);
        doc.setTextColor(34, 197, 94);
        doc.text('ONGOING MONITORING:', margin, yPos);
        yPos += 8;

        doc.setFontSize(10);
        doc.setTextColor(0, 0, 0);
        recommendations.monitoring.forEach((item, index) => {
            const splitText = doc.splitTextToSize(`${index + 1}. ${item}`, pageWidth - 2 * margin - 5);
            doc.text(splitText, margin + 5, yPos);
            yPos += splitText.length * 5 + 2;

            if (yPos > 270) {
                doc.addPage();
                yPos = 20;
            }
        });

        // Footer
        const pageCount = doc.internal.getNumberOfPages();
        for (let i = 1; i <= pageCount; i++) {
            doc.setPage(i);
            doc.setFontSize(9);
            doc.setTextColor(150, 150, 150);
            doc.text(
                `Page ${i} of ${pageCount} | Hamstring Injury Risk Predictor | Powered by GNODE AI`,
                pageWidth / 2,
                doc.internal.pageSize.getHeight() - 10,
                { align: 'center' }
            );
        }

        // Save the PDF with athlete name
        const fileName = `Hamstring_Report_${name.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.pdf`;
        doc.save(fileName);

        // Close modal
        setIsModalOpen(false);
    };

    const handleDownloadPDF = () => {
        setIsModalOpen(true);
    };

    const handleEmailResults = async (emailData) => {
        try {
            const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001/api';

            const payload = {
                email: emailData.email,
                recipientName: emailData.recipientName,
                results: {
                    riskScore,
                    riskLevel,
                    confidence,
                    keyIndicators,
                    recommendations
                }
            };

            const response = await fetch(`${API_URL}/email-results`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                throw new Error('Failed to send email');
            }

            const data = await response.json();

            // Show success message in modal
            setSuccessEmail(emailData.email);
            setIsSuccessModalOpen(true);

            // Close email input modal
            setIsEmailModalOpen(false);
        } catch (error) {
            console.error('Email error:', error);
            throw error; // Re-throw to show error in modal
        }
    };

    const handleEmailButtonClick = () => {
        setIsEmailModalOpen(true);
    };

    const handleViewHistory = () => {
        setIsHistoryModalOpen(true);
    };

    return (
        <div className="results-container">
            <AthleteDetailsModal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                onSubmit={generatePDF}
            />

            <EmailModal
                isOpen={isEmailModalOpen}
                onClose={() => setIsEmailModalOpen(false)}
                onSubmit={handleEmailResults}
            />

            <HistoryModal
                isOpen={isHistoryModalOpen}
                onClose={() => setIsHistoryModalOpen(false)}
                onSelectAssessment={handleSelectAssessment}
            />

            {/* Success Modal */}
            {isSuccessModalOpen && (
                <div className="modal-overlay" onClick={() => setIsSuccessModalOpen(false)}>
                    <div className="modal-content success-modal" onClick={(e) => e.stopPropagation()}>
                        <div className="success-icon">✅</div>
                        <h2>Email Sent Successfully!</h2>
                        <p className="success-message">
                            Your assessment report has been sent to:
                        </p>
                        <p className="success-email">{successEmail}</p>
                        <button
                            className="modal-btn success-btn"
                            onClick={() => setIsSuccessModalOpen(false)}
                        >
                            OK
                        </button>
                    </div>
                </div>
            )}

            <div className="results-card">
                <div className="results-header">
                    <h2>🎯 Injury Risk Assessment Results</h2>
                </div>

                {/* Risk Score Display */}
                <div className="risk-score-section">
                    <div className="risk-score-circle" style={{ borderColor: getRiskColor(riskScore) }}>
                        <div className="score-value">{riskScore}%</div>
                        <div className="score-label">RISK SCORE</div>
                    </div>

                    <div className="risk-level" style={{ color: getRiskColor(riskScore) }}>
                        {getRiskEmoji(riskLevel)} {riskLevel} RISK
                    </div>
                </div>

                {/* Risk Scale */}
                <div className="risk-scale">
                    <div className="scale-bar">
                        <div
                            className="scale-indicator"
                            style={{
                                left: `${riskScore}%`,
                                backgroundColor: getRiskColor(riskScore)
                            }}
                        ></div>
                        <div className="scale-fill" style={{ width: `${riskScore}%`, backgroundColor: getRiskColor(riskScore) }}></div>
                    </div>
                    <div className="scale-labels">
                        <span>Low</span>
                        <span>Moderate</span>
                        <span>High</span>
                        <span>Critical</span>
                    </div>
                </div>

                <hr className="divider" />

                {/* Key Indicators */}
                <div className="key-indicators-section">
                    <h3>📊 Key Indicators</h3>
                    <p className="indicators-text">{keyIndicators}</p>
                    <div className="confidence-badge">
                        Model Confidence: <strong>{confidence}%</strong>
                    </div>
                </div>

                <hr className="divider" />

                {/* Recommendations */}
                <div className="recommendations-section">
                    <h3>💊 Recommendations</h3>

                    <div className="recommendation-group immediate">
                        <h4>⚠️ IMMEDIATE ACTIONS:</h4>
                        <ul>
                            {recommendations.immediate.map((item, index) => (
                                <li key={index}>{item}</li>
                            ))}
                        </ul>
                    </div>

                    <div className="recommendation-group followup">
                        <h4>📅 FOLLOW-UP (Within 3-5 Days):</h4>
                        <ul>
                            {recommendations.followUp.map((item, index) => (
                                <li key={index}>{item}</li>
                            ))}
                        </ul>
                    </div>

                    <div className="recommendation-group monitoring">
                        <h4>📈 ONGOING MONITORING:</h4>
                        <ul>
                            {recommendations.monitoring.map((item, index) => (
                                <li key={index}>{item}</li>
                            ))}
                        </ul>
                    </div>
                </div>

                <hr className="divider" />

                {/* Action Buttons */}
                <div className="action-buttons">
                    <button className="action-btn primary" onClick={handleDownloadPDF}>
                        <FaDownload /> Download PDF Report
                    </button>
                    <button className="action-btn secondary" onClick={handleEmailButtonClick}>
                        <FaEnvelope /> Email Results
                    </button>
                    <button className="action-btn secondary" onClick={onNewAssessment}>
                        <FaRedo /> New Assessment
                    </button>
                    <button className="action-btn secondary" onClick={handleViewHistory}>
                        <FaChartLine /> View History
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ResultsDisplay;
