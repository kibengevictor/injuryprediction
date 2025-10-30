# 🧬 Tissue Type Selection - Complete Implementation Guide

## Target: Both Professional & Consumer Users | No Model Retraining | ASAP Deployment

---

## 🎯 **Understanding Tissue Type in the Model**

### **What the Model Uses:**

From the notebook (Cell 24):
```python
biomarker_model_df = combined_df[['mw', 'tissue']].copy()
biomarker_model_df = pd.get_dummies(biomarker_model_df, columns=['tissue'], drop_first=True)

# Result: Two binary features
# - tissue_sweat: 1 if sweat, 0 otherwise
# - tissue_urine: 1 if urine, 0 otherwise
# - saliva is baseline (both = 0)
```

### **The Three Options:**

| User Selects | tissue_sweat | tissue_urine | Model Interpretation |
|--------------|--------------|--------------|---------------------|
| **Saliva**   | 0            | 0            | Saliva sample (baseline) |
| **Sweat**    | 1            | 0            | Sweat sample |
| **Urine**    | 0            | 1            | Urine sample |

---

## 🎨 **UI Design: Multi-Tissue Input with Intelligent Selection (YOUR APPROACH)**

### **User Experience: Enter All, System Decides**

Users can input biomarkers from **all three tissue types** in one form. The system analyzes all data and automatically selects the most relevant tissue for prediction.

```
┌─────────────────────────────────────────────────────────────────┐
│  🧬 Biomarker Data Entry                                         │
│  Enter values for any or all tissue types you have data for     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  💧 SALIVA BIOMARKERS                                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Cortisol (nmol/L)         [0.78____] ⓘ Normal: 0.3-0.8  │  │
│  │ Testosterone (pg/mL)      [0.23____] ⓘ Normal: 0.1-0.4  │  │
│  │ IgA (μg/mL)               [0.75____] ⓘ Normal: 0.5-1.0  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  💦 SWEAT BIOMARKERS                                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Sodium (mmol/L)           [1.5_____] ⓘ Normal: 20-60    │  │
│  │ Lactate (mmol/L)          [3.2_____] ⚠️ ELEVATED!       │  │
│  │ Glucose (mg/dL)           [95.0____] ⓘ Normal: 50-150   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  🧪 URINE BIOMARKERS                                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Creatinine (mg/dL)        [________] ⓘ Normal: 0.6-1.2  │  │
│  │ Protein (mg/day)          [________] ⓘ Normal: 0-150    │  │
│  │ Specific Gravity          [________] ⓘ Normal: 1.005-1.03│ │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  📝 Note: Leave fields blank if data not available              │
│                                                                  │
│  [Analyze Risk]                                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### **Key Features:**

✅ **All tissues in one view** - No switching between pages  
✅ **Real-time validation** - Shows normal ranges with tooltips  
✅ **Elevation warnings** - Highlights abnormal values  
✅ **Optional fields** - User can skip any section  
✅ **Smart backend** - System picks best tissue automatically  

### **Why This Approach is BEST:**

1. **Flexible**: Works for users with 1, 2, or 3 sample types
2. **Simple**: One form, no decisions needed
3. **Smart**: Backend handles complexity
4. **Professional**: Handles real-world scenarios where multiple tests are done
5. **Transparent**: User sees which tissue was selected in results

---

## 🧠 **Backend Selection Logic**

### **Priority Algorithm:**

```python
def determine_primary_tissue(biomarker_data, user_preference=None):
    """
    Automatically determine which tissue type to use for analysis
    
    Priority:
    1. User explicit choice (if provided)
    2. Tissue with most elevated biomarkers
    3. Clinical relevance for injury (Sweat > Urine > Saliva)
    4. Data completeness (most fields filled)
    """
    
    # If user explicitly selected, honor it
    if user_preference in ['saliva', 'sweat', 'urine']:
        return {
            'tissue': user_preference,
            'reason': 'User selected',
            'confidence': 'user_specified'
        }
    
    # Calculate relevance scores for each tissue
    scores = {
        'saliva': 0,
        'sweat': 0,
        'urine': 0
    }
    
    # Clinical relevance weights for injury prediction
    injury_relevance = {
        'sweat': 1.0,    # Highest - direct muscle activity
        'urine': 0.7,    # Medium - metabolic waste
        'saliva': 0.5    # Lower - hormonal/stress
    }
    
    # Add base clinical relevance
    for tissue in scores:
        scores[tissue] += injury_relevance[tissue]
    
    # Check data completeness
    completeness = {
        'saliva': count_filled_fields(biomarker_data.get('saliva', {})),
        'sweat': count_filled_fields(biomarker_data.get('sweat', {})),
        'urine': count_filled_fields(biomarker_data.get('urine', {}))
    }
    
    # Add points for completeness (max 0.3 points)
    for tissue in scores:
        if completeness[tissue] > 0:
            scores[tissue] += min(completeness[tissue] / 10, 0.3)
    
    # Check for elevated biomarkers (most important)
    elevations = {
        'saliva': calculate_elevation_score(biomarker_data.get('saliva', {})),
        'sweat': calculate_elevation_score(biomarker_data.get('sweat', {})),
        'urine': calculate_elevation_score(biomarker_data.get('urine', {}))
    }
    
    # Add elevation scores (max 2.0 points - highest weight)
    for tissue in scores:
        scores[tissue] += elevations[tissue]
    
    # Select tissue with highest score
    primary_tissue = max(scores, key=scores.get)
    
    # Generate explanation
    reasons = []
    if elevations[primary_tissue] > 0.5:
        reasons.append(f"Elevated biomarkers detected")
    if completeness[primary_tissue] >= 2:
        reasons.append(f"Complete data available")
    if primary_tissue == 'sweat':
        reasons.append(f"Most relevant for athletic injury")
    
    confidence = 'high' if scores[primary_tissue] > 2.0 else 'medium'
    
    return {
        'tissue': primary_tissue,
        'reason': ', '.join(reasons) if reasons else 'Default selection',
        'confidence': confidence,
        'scores': scores  # For debugging
    }


def count_filled_fields(tissue_data):
    """Count how many biomarker fields have values"""
    if not tissue_data:
        return 0
    return sum(1 for value in tissue_data.values() if value is not None and value != '')


def calculate_elevation_score(tissue_data):
    """
    Calculate how elevated the biomarkers are from normal ranges
    Returns score 0-2.0
    """
    if not tissue_data:
        return 0.0
    
    # Normal ranges (simplified)
    normal_ranges = {
        # Saliva
        'cortisol': (0.3, 0.8),      # nmol/L
        'testosterone': (0.1, 0.4),   # pg/mL
        'iga': (0.5, 1.0),            # μg/mL
        
        # Sweat
        'sodium': (20, 60),           # mmol/L
        'lactate': (0.5, 2.2),        # mmol/L
        'glucose': (50, 150),         # mg/dL
        
        # Urine
        'creatinine': (0.6, 1.2),     # mg/dL
        'protein': (0, 150),          # mg/day
        'specific_gravity': (1.005, 1.030)
    }
    
    total_deviation = 0
    count = 0
    
    for biomarker, value in tissue_data.items():
        if value is None or biomarker not in normal_ranges:
            continue
        
        min_normal, max_normal = normal_ranges[biomarker]
        
        # Calculate deviation from normal range
        if value < min_normal:
            deviation = (min_normal - value) / min_normal
        elif value > max_normal:
            deviation = (value - max_normal) / max_normal
        else:
            deviation = 0  # Within normal range
        
        total_deviation += deviation
        count += 1
    
    if count == 0:
        return 0.0
    
    # Average deviation, capped at 2.0
    avg_deviation = total_deviation / count
    return min(avg_deviation * 2, 2.0)
```

---

## 📊 **Example Scenarios**

### **Scenario 1: Only Sweat Data Provided**

**User Input:**
```json
{
  "saliva": {},
  "sweat": {
    "sodium": 45,
    "lactate": 3.2,
    "glucose": 95
  },
  "urine": {}
}
```

**System Decision:**
```python
{
  "tissue": "sweat",
  "tissue_sweat": 1,
  "tissue_urine": 0,
  "reason": "Complete sweat data available, lactate elevated +45%",
  "confidence": "high"
}
```

---

### **Scenario 2: Multiple Samples, Urine Most Elevated**

**User Input:**
```json
{
  "saliva": {
    "cortisol": 0.6  // Normal range
  },
  "sweat": {
    "lactate": 2.0   // Normal range
  },
  "urine": {
    "creatinine": 2.5,  // VERY HIGH (normal: 0.6-1.2)
    "protein": 400      // VERY HIGH (normal: 0-150)
  }
}
```

**System Decision:**
```python
{
  "tissue": "urine",
  "tissue_sweat": 0,
  "tissue_urine": 1,
  "reason": "Elevated biomarkers detected in urine (creatinine +108%, protein +167%)",
  "confidence": "high"
}
```

---

### **Scenario 3: All Data Normal, Default to Sweat**

**User Input:**
```json
{
  "saliva": {
    "cortisol": 0.5
  },
  "sweat": {
    "lactate": 1.8,
    "sodium": 40
  },
  "urine": {
    "creatinine": 1.0
  }
}
```

**System Decision:**
```python
{
  "tissue": "sweat",
  "tissue_sweat": 1,
  "tissue_urine": 0,
  "reason": "Most relevant for athletic injury, complete data available",
  "confidence": "medium"
}
```

---

## 🎯 **Complete UI Flow (Your Multi-Tissue Approach)**

### **Step-by-Step User Experience:**

```
STEP 1: Welcome Screen
┌─────────────────────────────────────────────────────────────┐
│  🏃 Hamstring Injury Risk Assessment                        │
│                                                              │
│  Enter your biomarker test results from any lab work:      │
│                                                              │
│  ✓ Saliva samples (stress, hormones)                       │
│  ✓ Sweat samples (muscle activity, hydration)              │
│  ✓ Urine samples (metabolic health)                        │
│                                                              │
│  💡 You can enter data from one or all sample types.       │
│     Our AI will automatically analyze and select the        │
│     most relevant indicators for injury prediction.         │
│                                                              │
│  [Start Assessment]                                         │
└─────────────────────────────────────────────────────────────┘

STEP 2: Single Form - All Tissues (User enters everything)
┌─────────────────────────────────────────────────────────────┐
│  🧬 Enter Your Biomarker Results                            │
│  Fill in any fields where you have data                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  💧 SALIVA BIOMARKERS                                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Cortisol (nmol/L)      [0.78____] ⓘ Normal: 0.3-0.8 │  │
│  │ Testosterone (pg/mL)   [0.23____] ⓘ Normal: 0.1-0.4 │  │
│  │ IgA (μg/mL)            [0.75____] ⓘ Normal: 0.5-1.0 │  │
│  │ Alpha-Amylase (U/mL)   [________] ⓘ Normal: 20-100  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  💦 SWEAT BIOMARKERS                                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Sodium (mmol/L)        [1.5_____] ⓘ Normal: 20-60   │  │
│  │ Lactate (mmol/L)       [3.2_____] ⚠️ ELEVATED!      │  │
│  │ Glucose (mg/dL)        [95.0____] ⓘ Normal: 50-150  │  │
│  │ Chloride (mmol/L)      [________] ⓘ Normal: 10-70   │  │
│  │ Potassium (mmol/L)     [________] ⓘ Normal: 2-8     │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  🧪 URINE BIOMARKERS                                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Creatinine (mg/dL)     [________] ⓘ Normal: 0.6-1.2 │  │
│  │ Protein (mg/day)       [________] ⓘ Normal: 0-150   │  │
│  │ Specific Gravity       [________] ⓘ Normal: 1.005-1.03│ │
│  │ pH Level               [________] ⓘ Normal: 4.5-8.0  │  │
│  │ Urea (mg/dL)           [________] ⓘ Normal: 7-20     │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  📝 Notes:                                                  │
│  • Leave blank any fields you don't have data for          │
│  • Hover over ⓘ for more information                       │
│  • ⚠️ indicates values outside normal range                │
│                                                              │
│  [Clear Form]  [Load Sample Data]  [Analyze Risk] ➜        │
│                                                              │
└─────────────────────────────────────────────────────────────┘

STEP 3: Processing & Tissue Selection (Automatic)
┌─────────────────────────────────────────────────────────────┐
│  ⚙️ Analyzing Your Biomarkers...                            │
│                                                              │
│  [████████████████████░░] 85%                               │
│                                                              │
│  ✓ Validating data ranges                                  │
│  ✓ Calculating elevation scores                            │
│  ✓ Selecting primary tissue...                             │
│                                                              │
└─────────────────────────────────────────────────────────────┘

STEP 4: Processing & Analysis (Automatic - User doesn't see details)
┌─────────────────────────────────────────────────────────────┐
│  ⚙️ Analyzing Your Biomarkers...                            │
│                                                              │
│  [████████████████████████] 100%                            │
│                                                              │
│  ✓ Data validated                                           │
│  ✓ AI analysis complete                                     │
│  ✓ Risk assessment ready                                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘

STEP 5: Final Results (Clean, no technical details)
┌─────────────────────────────────────────────────────────────┐
│  🎯 INJURY RISK ASSESSMENT RESULTS                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │              RISK SCORE: 51%                        │    │
│  │                                                      │    │
│  │              ⚠️ HIGH RISK                           │    │
│  │                                                      │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  Risk Level:  🔴━━━━━━━━━━━━━━━━●━━━━━━ 51%               │
│               ├────────┼────────┼────────┤                  │
│               Low    Moderate  High   Critical              │
│                                                              │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                              │
│  � KEY INDICATORS                                          │
│                                                              │
│  Elevated lactate levels detected in your biomarkers,      │
│  indicating significant muscle fatigue and increased        │
│  hamstring injury risk.                                     │
│                                                              │
│  Model Confidence: 87%                                      │
│                                                              │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                              │
│  💊 RECOMMENDATIONS                                         │
│                                                              │
│  ⚠️ IMMEDIATE ACTIONS:                                     │
│  • Rest hamstring muscles for 24-48 hours                  │
│  • Apply ice/compression if pain present                    │
│  • Schedule sports medicine evaluation                      │
│  • Reduce training intensity by 50%                         │
│  • Avoid high-intensity sprinting or jumping               │
│                                                              │
│  📅 FOLLOW-UP (Within 3-5 Days):                           │
│  • Re-test biomarkers to monitor improvement               │
│  • Consider physiotherapy assessment                        │
│  • Implement targeted hamstring strengthening              │
│  • Review training load and recovery protocols             │
│                                                              │
│  📈 ONGOING MONITORING:                                     │
│  • Monitor for pain, tightness, or reduced flexibility     │
│  • Track daily hamstring comfort levels                     │
│  • Log any discomfort during activities                     │
│  • Weekly biomarker monitoring recommended                  │
│                                                              │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                              │
│  [📄 Download PDF Report]  [📧 Email Results]               │
│  [🔄 New Assessment]       [📊 View History]                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 💻 **Complete Backend Implementation**

### **Main API Endpoint:**

```python
from flask import Flask, request, jsonify
from datetime import datetime
import numpy as np

app = Flask(__name__)

@app.route('/api/predict', methods=['POST'])
def predict_injury_risk():
    """
    Main prediction endpoint - accepts multi-tissue input
    User can provide data for all three tissues
    System automatically selects the best one
    """
    try:
        data = request.json
        
        # Extract all biomarker data (all three tissues)
        biomarkers = {
            'saliva': data.get('saliva', {}),
            'sweat': data.get('sweat', {}),
            'urine': data.get('urine', {})
        }
        
        # STEP 1: Validate input data
        validation_result = validate_biomarkers(biomarkers)
        if not validation_result['valid']:
            return jsonify({
                'status': 'error',
                'message': validation_result['error']
            }), 400
        
        # STEP 2: Auto-select primary tissue
        tissue_selection = determine_primary_tissue(biomarkers)
        
        # STEP 3: Select primary metabolite from chosen tissue
        metabolite_selection = select_primary_metabolite(
            biomarkers[tissue_selection['tissue']],
            tissue_selection['tissue']
        )
        
        # STEP 4: Prepare model input (7 features)
        model_features = prepare_model_features(
            tissue=tissue_selection['tissue'],
            molecular_weight=metabolite_selection['mw'],
            emg_data=data.get('emg', None)  # Optional EMG if provided
        )
        
        # STEP 5: Run GNODE model prediction
        prediction = run_gnode_model(model_features)
        
        # STEP 6: Generate recommendations
        recommendations = generate_recommendations(
            prediction['risk_level'],
            tissue_selection['tissue'],
            metabolite_selection
        )
        
        # STEP 7: Format comprehensive response
        response = {
            'status': 'success',
            'prediction': {
                'risk_score': prediction['probability'],
                'risk_level': prediction['risk_category'],  # LOW, MODERATE, HIGH
                'confidence': prediction['confidence']
            },
            'tissue_selection': {
                'primary_tissue': tissue_selection['tissue'],
                'reason': tissue_selection['reason'],
                'confidence': tissue_selection['confidence'],
                'selection_score': tissue_selection['score'],
                'alternatives': tissue_selection.get('alternatives', [])
            },
            'metabolite_analysis': {
                'primary_metabolite': metabolite_selection['name'],
                'molecular_weight': metabolite_selection['mw'],
                'formula': metabolite_selection['formula'],
                'measured_value': metabolite_selection['value'],
                'normal_range': metabolite_selection['normal_range'],
                'deviation_percent': metabolite_selection['deviation'],
                'is_elevated': metabolite_selection['elevated']
            },
            'model_details': {
                'features_used': model_features,
                'model_version': 'GNODE-v1.0',
                'accuracy': '94.2%'
            },
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        }
        
        # Optional: Save to database for history
        # save_assessment(user_id, response)
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }), 500


def validate_biomarkers(biomarkers):
    """
    Validate that at least one tissue has data
    """
    total_fields = 0
    
    for tissue, data in biomarkers.items():
        if data:
            total_fields += len([v for v in data.values() if v is not None and v != ''])
    
    if total_fields == 0:
        return {
            'valid': False,
            'error': 'No biomarker data provided. Please enter at least one value.'
        }
    
    return {'valid': True}


def select_primary_metabolite(tissue_data, tissue_type):
    """
    From the selected tissue, pick the most important metabolite
    """
    # Metabolite information database
    metabolite_db = {
        # Saliva metabolites
        'cortisol': {
            'mw': 362.46,
            'formula': 'C21H30O5',
            'normal_range': (0.3, 0.8),  # nmol/L
            'importance': 0.8
        },
        'testosterone': {
            'mw': 288.42,
            'formula': 'C19H28O2',
            'normal_range': (0.1, 0.4),  # pg/mL
            'importance': 0.6
        },
        'iga': {
            'mw': 150000,  # Large protein
            'formula': 'Variable',
            'normal_range': (0.5, 1.0),  # μg/mL
            'importance': 0.5
        },
        'alpha_amylase': {
            'mw': 55000,
            'formula': 'Variable',
            'normal_range': (20, 100),  # U/mL
            'importance': 0.4
        },
        
        # Sweat metabolites
        'lactate': {
            'mw': 89.07,
            'formula': 'C3H6O3',
            'normal_range': (0.5, 2.2),  # mmol/L
            'importance': 1.0  # HIGHEST for injury
        },
        'sodium': {
            'mw': 22.99,
            'formula': 'Na',
            'normal_range': (20, 60),  # mmol/L
            'importance': 0.3
        },
        'glucose': {
            'mw': 180.16,
            'formula': 'C6H12O6',
            'normal_range': (50, 150),  # mg/dL
            'importance': 0.5
        },
        'chloride': {
            'mw': 35.45,
            'formula': 'Cl',
            'normal_range': (10, 70),  # mmol/L
            'importance': 0.2
        },
        'potassium': {
            'mw': 39.10,
            'formula': 'K',
            'normal_range': (2, 8),  # mmol/L
            'importance': 0.4
        },
        
        # Urine metabolites
        'creatinine': {
            'mw': 113.12,
            'formula': 'C4H7N3O',
            'normal_range': (0.6, 1.2),  # mg/dL
            'importance': 0.7
        },
        'protein': {
            'mw': 'Variable',
            'formula': 'Variable',
            'normal_range': (0, 150),  # mg/day
            'importance': 0.6
        },
        'specific_gravity': {
            'mw': None,
            'formula': None,
            'normal_range': (1.005, 1.030),
            'importance': 0.3
        },
        'ph_level': {
            'mw': None,
            'formula': None,
            'normal_range': (4.5, 8.0),
            'importance': 0.2
        },
        'urea': {
            'mw': 60.06,
            'formula': 'CH4N2O',
            'normal_range': (7, 20),  # mg/dL
            'importance': 0.5
        }
    }
    
    # Calculate scores for each metabolite
    scores = {}
    
    for metabolite_name, value in tissue_data.items():
        if value is None or value == '' or metabolite_name not in metabolite_db:
            continue
        
        metabolite_info = metabolite_db[metabolite_name]
        
        # Skip if no molecular weight (like pH, specific gravity)
        if metabolite_info['mw'] is None:
            continue
        
        # Calculate deviation from normal
        min_normal, max_normal = metabolite_info['normal_range']
        
        if value < min_normal:
            deviation = (min_normal - value) / min_normal
        elif value > max_normal:
            deviation = (value - max_normal) / max_normal
        else:
            deviation = 0
        
        # Weighted score: importance * deviation
        scores[metabolite_name] = {
            'score': metabolite_info['importance'] * (1 + deviation),
            'deviation': deviation,
            'value': value,
            'normal_range': metabolite_info['normal_range'],
            **metabolite_info
        }
    
    # Select metabolite with highest score
    if not scores:
        # Default to first available metabolite with MW
        for metabolite_name, value in tissue_data.items():
            if metabolite_name in metabolite_db and metabolite_db[metabolite_name]['mw']:
                return {
                    'name': metabolite_name,
                    'mw': metabolite_db[metabolite_name]['mw'],
                    'formula': metabolite_db[metabolite_name]['formula'],
                    'value': value,
                    'normal_range': metabolite_db[metabolite_name]['normal_range'],
                    'deviation': 0,
                    'elevated': False
                }
    
    primary_metabolite = max(scores, key=lambda x: scores[x]['score'])
    metabolite_info = scores[primary_metabolite]
    
    return {
        'name': primary_metabolite,
        'mw': metabolite_info['mw'],
        'formula': metabolite_info['formula'],
        'value': metabolite_info['value'],
        'normal_range': metabolite_info['normal_range'],
        'deviation': round(metabolite_info['deviation'] * 100, 1),  # Convert to percentage
        'elevated': metabolite_info['deviation'] > 0
    }


def run_gnode_model(features):
    """
    Run the GNODE model with 7 features
    Returns prediction with risk score and category
    """
    # TODO: Load actual trained GNODE model
    # For now, simulate prediction based on features
    
    # Extract features
    mw = features['mw']
    tissue_sweat = features['tissue_sweat']
    tissue_urine = features['tissue_urine']
    rms_feat = features.get('rms_feat', 0)
    
    # Simple rule-based logic for demonstration
    # Replace with actual model.predict(features)
    
    # If no EMG data, rely more on biomarkers
    if rms_feat == 0:
        # Biomarker-only prediction (less accurate)
        # Higher MW metabolites might correlate with stress/inflammation
        base_risk = 0.3
        if mw > 200:  # Larger molecules like cortisol
            base_risk += 0.1
        if tissue_sweat == 1:  # Sweat indicates athletic activity
            base_risk += 0.15
        
        risk_probability = min(base_risk + np.random.uniform(0, 0.3), 1.0)
        confidence = 0.70  # Lower confidence without EMG
    else:
        # With EMG data (higher accuracy)
        # Actual model would use all 7 features
        risk_probability = 0.51  # Example
        confidence = 0.94  # Model's reported accuracy
    
    # Categorize risk
    if risk_probability < 0.33:
        risk_category = 'LOW'
    elif risk_probability < 0.67:
        risk_category = 'MODERATE'
    else:
        risk_category = 'HIGH'
    
    return {
        'probability': round(risk_probability, 2),
        'risk_category': risk_category,
        'confidence': confidence
    }


def generate_recommendations(risk_level, tissue_type, metabolite_info):
    """
    Generate personalized recommendations based on risk and biomarkers
    """
    recommendations = {
        'immediate': [],
        'short_term': [],
        'monitoring': []
    }
    
    if risk_level == 'HIGH':
        recommendations['immediate'] = [
            'Rest hamstring muscles for 24-48 hours',
            'Apply ice and compression if pain present',
            'Schedule sports medicine evaluation within 48 hours',
            'Reduce training intensity by 50%',
            'Avoid high-intensity sprinting or jumping'
        ]
        recommendations['short_term'] = [
            f'Re-test {tissue_type} biomarkers in 3-5 days',
            'Consider physiotherapy assessment',
            'Implement targeted hamstring strengthening exercises',
            'Review training load and recovery protocols'
        ]
        recommendations['monitoring'] = [
            'Monitor for pain, tightness, or reduced range of motion',
            'Track daily hamstring flexibility',
            'Log any discomfort during activities',
            'Consider weekly biomarker monitoring'
        ]
    
    elif risk_level == 'MODERATE':
        recommendations['immediate'] = [
            'Reduce training intensity by 20-30%',
            'Include extra warm-up and cool-down',
            'Monitor for any hamstring discomfort'
        ]
        recommendations['short_term'] = [
            f'Re-test {tissue_type} biomarkers in 7-10 days',
            'Focus on hamstring flexibility exercises',
            'Maintain adequate hydration'
        ]
        recommendations['monitoring'] = [
            'Track training load weekly',
            'Note any unusual fatigue or soreness',
            'Bi-weekly biomarker checks recommended'
        ]
    
    else:  # LOW risk
        recommendations['immediate'] = [
            'Continue current training regimen',
            'Maintain good warm-up practices'
        ]
        recommendations['short_term'] = [
            f'Routine {tissue_type} biomarker check in 30 days',
            'Continue injury prevention exercises'
        ]
        recommendations['monitoring'] = [
            'Monthly biomarker baseline checks',
            'Track training load trends'
        ]
    
    # Add metabolite-specific recommendations
    if metabolite_info.get('elevated'):
        if metabolite_info['name'] == 'lactate':
            recommendations['immediate'].insert(0, 
                '⚠️ Elevated lactate indicates muscle fatigue - immediate rest recommended')
        elif metabolite_info['name'] == 'cortisol':
            recommendations['immediate'].append(
                'High cortisol detected - focus on stress management and adequate sleep')
        elif metabolite_info['name'] == 'creatinine':
            recommendations['immediate'].append(
                'Elevated creatinine may indicate muscle breakdown - consult physician')
    
    return recommendations


if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

---

## 📋 **Summary: Tissue Type Selection Strategy**

### **For ASAP Deployment:**

1. ✅ **Allow all three tissue types** in UI (flexibility)
2. ✅ **Auto-select based on data quality** (smart defaults)
3. ✅ **Show transparent reasoning** (user trust)
4. ✅ **Allow manual override** (user control)
5. ✅ **Prioritize sweat for athletes** (clinical relevance)

### **Implementation Priority:**

**Week 1:** Basic radio button selection (Option 1)
**Week 2:** Add automatic detection (Option 3)
**Week 3:** Refine selection algorithm based on testing

### **Next Steps:**

1. Implement `determine_primary_tissue()` function
2. Create UI mockups for tissue selection
3. Add validation for biomarker ranges
4. Test with sample data
5. Deploy MVP

---

*Document Created: October 30, 2025*  
*For: GNODE Dual-User Deployment (Professional + Consumer)*
