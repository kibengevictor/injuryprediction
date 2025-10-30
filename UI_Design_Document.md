# 🏥 Hamstring Injury Prediction Web App - UI Design Document
## GNODE Model Deployment Interface (Consumer Version)

---

## 📊 **Executive Summary**

This document outlines the UI/UX design for a **consumer-facing** web application that deploys the **GNODE (Graph Neural ODE)** model for predicting hamstring injury risk. 

**CRITICAL REALITY CHECK:**
The original model uses technical features (EMG signals, molecular weight biomarkers) that **regular people cannot access**. This design presents **TWO DEPLOYMENT OPTIONS**:

### **Option A: Professional Medical Tool** 
- **Users**: Sports medicine clinics, physical therapy centers, athletic training facilities
- **Requirements**: EMG equipment + lab biomarker analysis
- **Use Case**: Clinical assessment tool

### **Option B: Consumer Self-Assessment (SIMPLIFIED - RECOMMENDED)** ✅
- **Users**: Athletes, fitness enthusiasts, general public
- **Requirements**: Observable symptoms + basic health questions
- **Use Case**: Early screening and risk awareness

**This document focuses on Option B** as it's the only realistic deployment for "regular people."

**Target Users**: Athletes, weekend warriors, gym-goers, sports enthusiasts (18-65 years)

---

## 🎯 **Required Input Features**

Based on the notebook analysis, the model requires **7 features** for prediction:

### **1. Biomarker Features (3 features)**
| Feature | Description | Input Type | Range/Options |
|---------|-------------|------------|---------------|
| `mw` | Molecular Weight (Daltons) | Numeric (float) | 0 - 1000+ Da |
| `tissue_sweat` | Sweat biomarker presence | Binary (0/1) | 0 = No, 1 = Yes |
| `tissue_urine` | Urine biomarker presence | Binary (0/1) | 0 = No, 1 = Yes |

*Note: `tissue_saliva` is the baseline (encoded as both tissue_sweat=0 and tissue_urine=0)*

### **2. Player Performance Features (4 features)**
| Feature | Description | Input Type | Typical Range |
|---------|-------------|------------|---------------|
| `rms_feat` | Root Mean Square (EMG signal strength) | Numeric (float) | 0.03 - 0.25 |
| `zero_crossings` | Signal zero-crossing frequency | Numeric (float) | 8 - 13 |
| `skewness` | Signal distribution skewness | Numeric (float) | -5 to 0 |
| `waveform_length` | Total waveform path length | Numeric (float) | 3 - 20 |

**Total Input Fields: 7**

---

## 🎨 **UI Design Structure**

### **Page Layout: Single-Page Application (SPA)**

```
┌─────────────────────────────────────────────────────────────┐
│                         HEADER                               │
│  🏃 Hamstring Injury Risk Prediction System (GNODE Model)   │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                    NAVIGATION TABS                           │
│   [📝 Input Data] [📊 Results] [📈 History] [ℹ️ About]      │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│                      MAIN CONTENT AREA                       │
│                    (Tab-dependent content)                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│  FOOTER: © 2025 | Model: GNODE v1.0 | Accuracy: 94.2%      │
└─────────────────────────────────────────────────────────────┘
```

---

## 📝 **TAB 1: Input Data Form**

### **Section A: Patient/Athlete Information**
```
┌─────────────────────────────────────────────────────────┐
│  👤 Athlete Information                                  │
├─────────────────────────────────────────────────────────┤
│  Name:        [________________________]                 │
│  ID/Number:   [____________]    Age: [___]  Sex: [M/F]  │
│  Sport:       [Dropdown: Soccer, Track, etc.]           │
│  Date:        [Calendar Picker: DD/MM/YYYY]             │
└─────────────────────────────────────────────────────────┘
```
*Non-model inputs - for record keeping only*

---

### **Section B: Biomarker Data** 🧬
```
┌─────────────────────────────────────────────────────────┐
│  🧬 Biomarker Measurements                               │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Molecular Weight (mw):                                 │
│  ┌────────────────────────────────────────────┐         │
│  │ [_____________] Da                         │ ⓘ       │
│  └────────────────────────────────────────────┘         │
│  Range: 0-1000+ Daltons                                 │
│                                                          │
│  Tissue Source:                                         │
│  ○ Saliva    ○ Sweat    ○ Urine                        │
│  (Select ONE - determines tissue_sweat/tissue_urine)    │
│                                                          │
│  ───────────────────────────────────────────────        │
│  OR Load from CSV: [Choose File] [Upload]              │
└─────────────────────────────────────────────────────────┘
```

**Interactive Elements:**
- **ⓘ Tooltip**: "Molecular weight of detected metabolite biomarker (typical: 50-500 Da)"
- **Validation**: 
  - MW must be > 0
  - One tissue type must be selected
- **CSV Upload Option**: Allow batch predictions with CSV containing `mw,tissue` columns

---

### **Section C: EMG Signal Features** 📊
```
┌─────────────────────────────────────────────────────────┐
│  📊 Electromyography (EMG) Signal Analysis               │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  RMS Feature (rms_feat):                                │
│  ┌────────────────────────────────────────────┐         │
│  │ [_____________]                            │ ⓘ       │
│  └────────────────────────────────────────────┘         │
│  Typical Range: 0.03 - 0.25                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━         │
│  Slider: [●────────────────────────────────]            │
│                                                          │
│  Zero Crossings (zero_crossings):                       │
│  ┌────────────────────────────────────────────┐         │
│  │ [_____________]                            │ ⓘ       │
│  └────────────────────────────────────────────┘         │
│  Typical Range: 8 - 13                                  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━         │
│  Slider: [──────●──────────────────────────]            │
│                                                          │
│  Skewness (skewness):                                   │
│  ┌────────────────────────────────────────────┐         │
│  │ [_____________]                            │ ⓘ       │
│  └────────────────────────────────────────────┘         │
│  Typical Range: -5 to 0                                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━         │
│  Slider: [────────────────────●────────────]            │
│                                                          │
│  Waveform Length (waveform_length):                     │
│  ┌────────────────────────────────────────────┐         │
│  │ [_____________]                            │ ⓘ       │
│  └────────────────────────────────────────────┘         │
│  Typical Range: 3 - 20                                  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━         │
│  Slider: [──────────●──────────────────────]            │
│                                                          │
│  ───────────────────────────────────────────────        │
│  OR Upload EMG File: [Choose File] [Process]           │
│  Supported: .csv, .txt (with signal data)               │
└─────────────────────────────────────────────────────────┘
```

**Interactive Elements:**
- **Dual Input**: Text field + slider for better UX
- **ⓘ Tooltips**:
  - RMS: "Root Mean Square - measures signal strength/amplitude"
  - Zero Crossings: "Number of times signal crosses zero - indicates frequency"
  - Skewness: "Signal asymmetry - negative values common in muscle fatigue"
  - Waveform Length: "Total path length of signal - measures complexity"
- **Real-time Validation**: Show visual feedback (green checkmark/red X)
- **Auto-calculation Option**: Upload raw EMG signal, auto-compute features

---

### **Section D: Action Buttons**
```
┌─────────────────────────────────────────────────────────┐
│                                                          │
│  [📋 Load Sample Data] [🔄 Reset Form] [🎯 Predict]    │
│                                                          │
│  Note: All 7 features are required for prediction       │
└─────────────────────────────────────────────────────────┘
```

**Button Functions:**
- **Load Sample**: Populate with example values (healthy vs. injury-prone profiles)
- **Reset**: Clear all fields
- **Predict**: Validate inputs → Call API → Navigate to Results tab

---

## 📊 **TAB 2: Prediction Results**

### **Main Result Display**
```
┌─────────────────────────────────────────────────────────┐
│  🎯 PREDICTION RESULT                                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│        ┌─────────────────────────────────┐              │
│        │                                 │              │
│        │   RISK STATUS:  ⚠️ HIGH RISK   │              │
│        │                                 │              │
│        │   Injury Probability: 87.4%    │              │
│        │                                 │              │
│        └─────────────────────────────────┘              │
│                                                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  Risk Level Progress Bar:                               │
│  🟢 Low (0-33%)  🟡 Moderate (34-66%)  🔴 High (67-100%) │
│  ████████████████████████████████████░░░░░░░░           │
│                                      └─ 87.4%           │
└─────────────────────────────────────────────────────────┘
```

**Color Coding:**
- 🟢 **Low Risk** (0-33%): Green background, "Proceed with normal training"
- 🟡 **Moderate Risk** (34-66%): Yellow background, "Monitor closely, reduce intensity"
- 🔴 **High Risk** (67-100%): Red background, "URGENT: Medical evaluation recommended"

---

### **Detailed Breakdown**
```
┌─────────────────────────────────────────────────────────┐
│  📈 Confidence Metrics                                   │
├─────────────────────────────────────────────────────────┤
│  Model Confidence:    ████████████░░░░░  92.1%          │
│  ROC-AUC Score:       0.94                              │
│  Precision:           0.91                              │
│  F1 Score:            0.93                              │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  🔍 Feature Importance (SHAP Analysis)                   │
├─────────────────────────────────────────────────────────┤
│  Top Contributing Factors:                              │
│                                                          │
│  1. RMS Feature      ████████████████░░  85.2%          │
│  2. Skewness         ██████████████░░░░  72.3%          │
│  3. Waveform Length  ████████████░░░░░░  64.1%          │
│  4. Molecular Weight ████████░░░░░░░░░░  45.7%          │
│  5. Zero Crossings   ██████░░░░░░░░░░░░  32.4%          │
│                                                          │
│  [View Detailed SHAP Plot] [Download Report]           │
└─────────────────────────────────────────────────────────┘
```

---

### **Clinical Recommendations**
```
┌─────────────────────────────────────────────────────────┐
│  💊 Recommended Actions                                  │
├─────────────────────────────────────────────────────────┤
│  Based on HIGH RISK prediction:                         │
│                                                          │
│  ✅ IMMEDIATE:                                          │
│     • Schedule medical evaluation within 48 hours       │
│     • Suspend high-intensity training                   │
│     • Apply ice + compression if symptoms present       │
│                                                          │
│  📋 SHORT-TERM (1-2 weeks):                             │
│     • Physiotherapy assessment                          │
│     • Modified training program                         │
│     • Re-test EMG signals weekly                        │
│                                                          │
│  🔬 MONITORING:                                          │
│     • Repeat biomarker analysis in 7 days              │
│     • Track pain levels (0-10 scale)                    │
│     • Document range of motion changes                  │
│                                                          │
│  [📄 Print Care Plan] [📧 Email to Physician]           │
└─────────────────────────────────────────────────────────┘
```

---

### **Download Options**
```
┌─────────────────────────────────────────────────────────┐
│  💾 Export Results                                       │
├─────────────────────────────────────────────────────────┤
│  [📄 PDF Report] [📊 Excel Data] [📋 JSON API Response] │
└─────────────────────────────────────────────────────────┘
```

---

## 📈 **TAB 3: Prediction History**

```
┌─────────────────────────────────────────────────────────┐
│  📅 Prediction History & Trend Analysis                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Filters: Athlete [Dropdown] | Date Range [___-___]    │
│                                                          │
│  ┌─────────────────────────────────────────────────┐    │
│  │ Date       | Name    | Risk   | Prob   | Status │    │
│  ├─────────────────────────────────────────────────┤    │
│  │ 2025-10-29 | John D  | 🔴 High | 87.4%  | [View]│    │
│  │ 2025-10-22 | John D  | 🟡 Mod  | 54.2%  | [View]│    │
│  │ 2025-10-15 | John D  | 🟢 Low  | 21.3%  | [View]│    │
│  │ 2025-10-29 | Sarah M | 🟢 Low  | 18.9%  | [View]│    │
│  └─────────────────────────────────────────────────┘    │
│                                                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                          │
│  Risk Trend Graph (Last 30 Days):                       │
│  100% ┤                                    ●             │
│   75% ┤                          ●                       │
│   50% ┤               ●                                  │
│   25% ┤      ●                                           │
│    0% └──────────────────────────────────────────►      │
│       Oct 1      Oct 8      Oct 15     Oct 22   Oct 29  │
│                                                          │
│  [📥 Export History] [📊 Generate Report]               │
└─────────────────────────────────────────────────────────┘
```

---

## ℹ️ **TAB 4: About / Model Info**

```
┌─────────────────────────────────────────────────────────┐
│  ℹ️ About This System                                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  🧠 Model Architecture: GNODE (Graph Neural ODE)        │
│  📊 Training Dataset:   120,000 samples (balanced)      │
│  🎯 Model Accuracy:     94.2%                           │
│  📅 Last Updated:       October 2025                    │
│                                                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                          │
│  📚 How It Works:                                        │
│  This system combines EMG signal features with          │
│  biomarker data to predict hamstring injury risk        │
│  using Graph Neural Ordinary Differential Equations.    │
│                                                          │
│  The model analyzes relationships between:              │
│  • Muscle electrical activity patterns                  │
│  • Metabolite biomarkers (saliva, sweat, urine)        │
│  • Signal morphology characteristics                    │
│                                                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                          │
│  🔬 Scientific References:                              │
│  • SSD-HIP Dataset (120K samples, 17 features)         │
│  • HMDB Biomarker Database                             │
│  • Graph Neural ODE Framework (torchdiffeq)            │
│                                                          │
│  ⚠️ Disclaimer:                                         │
│  This tool is for screening purposes only and should    │
│  not replace professional medical diagnosis. Always     │
│  consult with qualified healthcare professionals.       │
│                                                          │
│  [📖 User Guide] [🔗 Documentation] [📧 Contact Us]     │
└─────────────────────────────────────────────────────────┘
```

---

## 🎨 **Visual Design Specifications**

### **Color Palette**
```
Primary Colors:
├─ Primary Blue:     #2C5F8D (Navigation, headers)
├─ Accent Green:     #28A745 (Low risk, success states)
├─ Warning Orange:   #FFC107 (Moderate risk)
├─ Danger Red:       #DC3545 (High risk, errors)
└─ Neutral Gray:     #6C757D (Secondary text)

Background:
├─ Main BG:          #F8F9FA (Light gray)
├─ Card BG:          #FFFFFF (Pure white)
└─ Input Focus:      #E3F2FD (Light blue)
```

### **Typography**
```
Headings:   'Inter', sans-serif, 600 weight
Body Text:  'Roboto', sans-serif, 400 weight
Monospace:  'Fira Code', monospace (for data values)

Sizes:
├─ H1 (Page Title):      32px
├─ H2 (Section):         24px
├─ H3 (Subsection):      18px
├─ Body:                 16px
└─ Small/Caption:        14px
```

### **Responsive Breakpoints**
```
Desktop:  > 1200px  (Full 3-column layout)
Tablet:   768-1199px (2-column layout)
Mobile:   < 768px   (Single column, stacked)
```

---

## 🔧 **Technical Requirements**

### **Input Validation Rules**
| Field | Validation | Error Message |
|-------|-----------|---------------|
| `mw` | > 0, numeric | "Molecular weight must be a positive number" |
| `tissue_*` | Exactly ONE selected | "Please select one tissue type" |
| `rms_feat` | 0.03 - 0.25 | "RMS value out of typical range (warning only)" |
| `zero_crossings` | 8 - 13 | "Zero crossings out of typical range" |
| `skewness` | -5 to 0 | "Skewness out of typical range" |
| `waveform_length` | 3 - 20 | "Waveform length out of typical range" |

**Note**: Range validations should show warnings but not block submission (to handle edge cases).

---

### **API Endpoint Structure**
```json
POST /api/predict
Content-Type: application/json

Request Body:
{
  "patient_info": {
    "name": "John Doe",
    "id": "ATH-001",
    "age": 25,
    "sport": "Soccer"
  },
  "features": {
    "mw": 250.5,
    "tissue_sweat": 1,
    "tissue_urine": 0,
    "rms_feat": 0.127982,
    "zero_crossings": 10.0,
    "skewness": -3.163882,
    "waveform_length": 11.168069
  }
}

Response:
{
  "status": "success",
  "prediction": {
    "class": 1,
    "probability": 0.874,
    "risk_level": "HIGH",
    "confidence": 0.921
  },
  "feature_importance": {
    "rms_feat": 0.852,
    "skewness": 0.723,
    "waveform_length": 0.641,
    "mw": 0.457,
    "zero_crossings": 0.324
  },
  "recommendations": [
    "Schedule medical evaluation within 48 hours",
    "Suspend high-intensity training"
  ],
  "timestamp": "2025-10-29T10:30:00Z",
  "model_version": "GNODE-v1.0"
}
```

---

## 📱 **Additional Features**

### **Nice-to-Have Enhancements**
1. **Batch Upload**: CSV with multiple athletes
2. **Comparison Mode**: Side-by-side comparison of 2+ predictions
3. **Mobile App**: iOS/Android native apps
4. **Email Alerts**: Auto-notify when risk exceeds threshold
5. **Integration**: Export to EHR systems (HL7 FHIR)
6. **Multi-language**: Support for Spanish, French, etc.
7. **Dark Mode**: Toggle for low-light environments
8. **Voice Input**: Dictate values hands-free
9. **Dashboard Analytics**: Team-wide risk overview
10. **Automated Reporting**: Weekly summary emails

---

## 🔐 **Security & Compliance**

### **Data Privacy**
- **HIPAA Compliance**: Encrypt PHI at rest and in transit
- **User Authentication**: Multi-factor authentication (MFA)
- **Role-Based Access**: Admin, Physician, Trainer roles
- **Audit Logging**: Track all predictions and data access
- **Data Retention**: Auto-delete after configurable period (default: 7 years)

### **Security Measures**
- HTTPS/TLS 1.3 encryption
- Rate limiting (10 requests/minute per user)
- Input sanitization (prevent XSS/SQL injection)
- CORS policies for API endpoints
- Regular security audits

---

## ✅ **Success Metrics**

### **User Experience KPIs**
- Time to complete prediction: < 3 minutes
- Form completion rate: > 90%
- User satisfaction: > 4.5/5 stars
- Error rate: < 2%

### **Technical KPIs**
- API response time: < 500ms
- Uptime: > 99.9%
- Mobile responsiveness: 100% compatible
- Accessibility: WCAG 2.1 AA compliance

---

## 📋 **Next Steps**

1. ✅ **Review this UI design** with stakeholders
2. 🎨 Create high-fidelity mockups (Figma/Adobe XD)
3. 🧪 Build interactive prototype
4. 💻 Develop backend API (Flask/FastAPI)
5. 🎨 Develop frontend (React/Vue.js)
6. 🧪 User testing with sports medicine professionals
7. 🚀 Deploy to production

---

## 📞 **Contact & Collaboration**

Ready to proceed with implementation? Let's:
1. Finalize the UI mockups
2. Set up the development environment
3. Build the backend API
4. Create the frontend interface
5. Integrate the GNODE model
6. Test and deploy!

---

*Document Version: 1.0*  
*Last Updated: October 29, 2025*  
*Created for: GNODE Hamstring Injury Prediction System*
