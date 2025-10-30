import React, { useEffect, useState } from 'react';
import '../styles/ProcessingScreen.css';

const ProcessingScreen = () => {
    const [currentStep, setCurrentStep] = useState(0);

    const steps = [
        { text: 'Validating biomarker data...', duration: 500 },
        { text: 'Analyzing tissue profiles...', duration: 800 },
        { text: 'Processing neural network inputs...', duration: 1000 },
        { text: 'Running GNODE prediction model...', duration: 700 },
        { text: 'Generating risk assessment...', duration: 500 }
    ];

    useEffect(() => {
        const timer = setTimeout(() => {
            if (currentStep < steps.length - 1) {
                setCurrentStep(prev => prev + 1);
            }
        }, steps[currentStep].duration);

        return () => clearTimeout(timer);
    }, [currentStep, steps]);

    return (
        <div className="processing-screen">
            <div className="processing-container">
                <div className="spinner-container">
                    <div className="spinner"></div>
                    <div className="pulse-ring"></div>
                </div>

                <h2>Analyzing Your Data</h2>
                <p className="processing-subtitle">
                    Our AI model is evaluating your biomarkers to assess hamstring injury risk
                </p>

                <div className="progress-steps">
                    {steps.map((step, index) => (
                        <div
                            key={index}
                            className={`step ${index <= currentStep ? 'active' : ''} ${index < currentStep ? 'completed' : ''}`}
                        >
                            <div className="step-indicator">
                                {index < currentStep ? '✓' : index + 1}
                            </div>
                            <div className="step-text">{step.text}</div>
                        </div>
                    ))}
                </div>

                <div className="progress-bar">
                    <div
                        className="progress-fill"
                        style={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
                    ></div>
                </div>

                <p className="processing-note">
                    This usually takes 3-5 seconds
                </p>
            </div>
        </div>
    );
};

export default ProcessingScreen;
