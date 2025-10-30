# Hamstring Injury Risk Predictor - Frontend

A modern React-based web application for assessing hamstring injury risk using biomarker analysis and the GNODE AI model.

## 🚀 Features

- **Multi-Tissue Biomarker Input**: Collect data from saliva, sweat, and urine samples
- **Real-time Validation**: Instant feedback on biomarker values with normal range checking
- **Smart Analysis**: AI-powered risk assessment using Graph Neural ODE (GNODE) model
- **Clean UI**: User-friendly interface with step-by-step guidance
- **Actionable Results**: Clear risk scores with immediate, follow-up, and monitoring recommendations
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

## 📋 Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Backend API running (see backend setup instructions)

## 🛠️ Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file in the frontend directory:
```env
REACT_APP_API_URL=http://localhost:5000/api
```

4. Start the development server:
```bash
npm start
```

The application will open at `http://localhost:3000`

## 🏗️ Project Structure

```
frontend/
├── public/
│   └── index.html          # HTML template
├── src/
│   ├── components/         # React components
│   │   ├── BiomarkerInputForm.js     # Biomarker data entry form
│   │   ├── ProcessingScreen.js       # Loading/processing screen
│   │   └── ResultsDisplay.js         # Results visualization
│   ├── styles/             # CSS stylesheets
│   │   ├── App.css
│   │   ├── BiomarkerInputForm.css
│   │   ├── ProcessingScreen.css
│   │   ├── ResultsDisplay.css
│   │   └── index.css
│   ├── utils/              # Utility functions
│   │   └── api.js          # API communication
│   ├── App.js              # Main app component
│   └── index.js            # Entry point
├── package.json            # Dependencies
└── README.md              # This file
```

## 🎨 Components

### BiomarkerInputForm
- Collects biomarker values across three tissue types
- Real-time validation with normal range checking
- Visual feedback for valid/invalid inputs
- Organized sections for saliva, sweat, and urine biomarkers

### ProcessingScreen
- Animated loading state during prediction
- Step-by-step progress visualization
- Engaging user experience with progress bar

### ResultsDisplay
- Risk score visualization with color-coded severity
- Visual risk scale indicator
- Categorized recommendations (immediate, follow-up, monitoring)
- Action buttons for PDF download, email, history, and new assessment

## 📊 Biomarker Reference Ranges

### Saliva
- **Cortisol**: 0.1-15 μg/dL
- **Testosterone**: 10-200 pg/mL
- **IgA**: 10-500 μg/mL

### Sweat
- **Sodium**: 0.5-3.0 mmol/L
- **Lactate**: 0.5-4.0 mmol/L
- **Glucose**: 50-150 mg/dL

### Urine
- **Creatinine**: 20-400 mg/dL
- **Protein**: 0-20 mg/dL
- **pH**: 4.5-8.0

## 🔌 API Integration

The frontend communicates with the Flask backend via REST API:

**Endpoint**: `POST /api/predict`

**Request Format**:
```json
{
  "saliva": {
    "cortisol": 5.2,
    "testosterone": 85.0,
    "iga": 150.0
  },
  "sweat": {
    "sodium": 1.5,
    "lactate": 3.2,
    "glucose": 95.0
  },
  "urine": {
    "creatinine": 120.0,
    "protein": 5.0,
    "ph": 6.5
  }
}
```

**Response Format**:
```json
{
  "riskScore": 51,
  "riskLevel": "HIGH",
  "confidence": 87,
  "keyIndicators": "Elevated lactate levels detected...",
  "recommendations": {
    "immediate": [...],
    "followUp": [...],
    "monitoring": [...]
  }
}
```

## 🎯 Usage Flow

1. **Input**: User enters biomarker values from lab results
2. **Validation**: System validates inputs against normal ranges
3. **Processing**: Data sent to backend API for GNODE model prediction
4. **Results**: Risk score and recommendations displayed
5. **Actions**: User can download PDF, email results, or start new assessment

## 🚧 Development

### Available Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm eject` - Eject from Create React App (one-way operation)

### Environment Variables

Create `.env.local` for local development:
```env
REACT_APP_API_URL=http://localhost:5000/api
```

For production:
```env
REACT_APP_API_URL=https://your-production-api.com/api
```

## 🔐 Security Considerations

- All API calls use HTTPS in production
- Input validation on both frontend and backend
- No sensitive data stored in localStorage
- CORS properly configured for API access

## 🐛 Troubleshooting

### Common Issues

1. **"No response from server"**
   - Ensure backend is running on correct port
   - Check `REACT_APP_API_URL` in `.env`
   - Verify CORS settings in backend

2. **"Failed to get prediction"**
   - Check backend logs for errors
   - Verify biomarker data format
   - Ensure GNODE model is loaded

3. **Styling issues**
   - Clear browser cache
   - Check for CSS import errors
   - Verify all CSS files are in `styles/` directory

## 📱 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## 🔮 Future Enhancements

- [ ] PDF report generation
- [ ] Email results functionality
- [ ] Assessment history tracking
- [ ] User authentication
- [ ] Multi-language support
- [ ] Dark mode
- [ ] EMG data integration for professional users

## 📄 License

Copyright © 2025 Hamstring Injury Predictor

## 🤝 Contributing

This is a private project. For questions or issues, contact the development team.

## ⚠️ Medical Disclaimer

This tool provides risk assessment only and does not constitute medical advice. Always consult qualified healthcare professionals for diagnosis and treatment decisions.
