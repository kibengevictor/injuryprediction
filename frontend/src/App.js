import React, { useState } from 'react';
import BiomarkerInputForm from './components/BiomarkerInputForm';
import ProcessingScreen from './components/ProcessingScreen';
import ResultsDisplay from './components/ResultsDisplay';
import './styles/App.css';

function App() {
    const [currentStep, setCurrentStep] = useState('input'); // 'input', 'processing', 'results'
    const [biomarkerData, setBiomarkerData] = useState(null);
    const [predictionResults, setPredictionResults] = useState(null);
    const [userDetails, setUserDetails] = useState(null);

    const handleSubmit = async (data) => {
        // Extract user details and biomarker data
        const { userDetails: userInfo, ...biomarkers } = data;
        setUserDetails(userInfo);
        setBiomarkerData(biomarkers);
        setCurrentStep('processing');

        try {
            // Call the real API
            const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001/api';
            const response = await fetch(`${API_URL}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(biomarkers)
            });

            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }

            const results = await response.json();
            setPredictionResults(results);
            setCurrentStep('results');
        } catch (error) {
            console.error('Prediction failed:', error);
            // Show error to user
            setPredictionResults({
                error: true,
                message: 'Failed to connect to prediction service. Please try again.',
                riskScore: 0,
                riskLevel: 'ERROR',
                confidence: 0,
                keyIndicators: 'Unable to analyze biomarkers at this time.',
                recommendations: {
                    immediate: ['Please check your connection and try again'],
                    followUp: [],
                    monitoring: []
                }
            });
            setCurrentStep('results');
        }
    };

    const handleNewAssessment = () => {
        setCurrentStep('input');
        setBiomarkerData(null);
        setPredictionResults(null);
    };

    return (
        <div className="app">
            <header className="app-header">
                <div className="header-content">
                    <h1>🏃 Hamstring Injury Risk Predictor</h1>
                    <p>AI-powered assessment using biomarker analysis</p>
                </div>
            </header>

            <main className="app-main">
                {currentStep === 'input' && (
                    <BiomarkerInputForm onSubmit={handleSubmit} />
                )}

                {currentStep === 'processing' && (
                    <ProcessingScreen />
                )}

                {currentStep === 'results' && predictionResults && (
                    <ResultsDisplay
                        results={predictionResults}
                        userDetails={userDetails}
                        onNewAssessment={handleNewAssessment}
                    />
                )}
            </main>

            <footer className="app-footer">
                <p>© 2025 Hamstring Injury Predictor | Powered by GNODE AI</p>
            </footer>
        </div>
    );
}

export default App;
