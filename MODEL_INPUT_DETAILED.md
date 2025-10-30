# 🔬 Understanding GNODE Model Input Requirements

## What the Model ACTUALLY Expects - Deep Dive

---

## 📊 **The Model's Input Structure**

From the notebook analysis (Cell 24 & Cell 29), the GNODE model expects **7 features**:

```python
selected_features = [
    'mw',              # Feature 1: Molecular Weight (float)
    'tissue_sweat',    # Feature 2: Binary flag (0 or 1)
    'tissue_urine',    # Feature 3: Binary flag (0 or 1)
    'rms_feat',        # Feature 4: EMG signal
    'zero_crossings',  # Feature 5: EMG signal
    'skewness',        # Feature 6: EMG signal
    'waveform_length'  # Feature 7: EMG signal
]
```

Let's break down the **biomarker features** (features 1-3):

---

## 🧬 **Feature 1: Molecular Weight (mw)**

### **What It Is:**
- A **single numeric value** representing the molecular weight of ONE metabolite
- Measured in Daltons (Da)
- Range: Typically 50-500 Da for small metabolites

### **Example Values:**
```python
mw = 89.07    # Lactate (C3H6O3)
mw = 113.12   # Creatinine (C4H7N3O)
mw = 180.16   # Glucose (C6H12O6)
mw = 362.46   # Cortisol (C21H30O5)
```

### **The Problem for Your UI:**

Your UI collects **MULTIPLE biomarkers**:
```
Saliva:
  - Cortisol: 0.78 nmol/L    (MW: 362.46 Da)
  - Testosterone: 0.23 pg/mL (MW: 288.42 Da)
  - IgA: 0.75 μg/mL          (MW: ~150,000 Da - antibody)

Sweat:
  - Sodium: 1.5 mmol/L       (MW: 22.99 Da)
  - Lactate: 3.2 mmol/L      (MW: 89.07 Da)
  - Glucose: 2.2 mg/dL       (MW: 180.16 Da)

Urine:
  - Creatinine: ??? mg/dL    (MW: 113.12 Da)
  - Specific Gravity: ???    (not a metabolite)
  - pH Level: ???            (not a metabolite)
```

**But the model expects ONE single `mw` value!**

---

### **Which Molecular Weight Should You Use?**

The notebook doesn't specify! Here are the options:

#### **Option A: Use the "Most Important" Metabolite**
```python
def select_primary_metabolite(biomarkers):
    """
    Choose which metabolite to report based on clinical significance
    """
    # Priority order for injury prediction:
    if biomarkers['lactate'] > LACTATE_THRESHOLD:
        return {
            'mw': 89.07,  # Lactate
            'tissue': 'sweat'
        }
    elif biomarkers['creatine_kinase'] > CK_THRESHOLD:
        return {
            'mw': 113.12,  # Creatinine (proxy for muscle damage)
            'tissue': 'urine'
        }
    elif biomarkers['cortisol'] > CORTISOL_THRESHOLD:
        return {
            'mw': 362.46,  # Cortisol
            'tissue': 'saliva'
        }
    else:
        # Default to lactate
        return {
            'mw': 89.07,
            'tissue': 'sweat'
        }
```

#### **Option B: Use the Most Elevated Metabolite**
```python
def select_most_elevated(biomarkers):
    """
    Calculate which biomarker is most outside normal range
    """
    deviations = {
        'lactate': (biomarkers['lactate'] - 2.2) / 2.2,  # % above normal
        'cortisol': (biomarkers['cortisol'] - 0.5) / 0.5,
        'glucose': (biomarkers['glucose'] - 95) / 95,
    }
    
    most_elevated = max(deviations, key=deviations.get)
    
    metabolite_map = {
        'lactate': {'mw': 89.07, 'tissue': 'sweat'},
        'cortisol': {'mw': 362.46, 'tissue': 'saliva'},
        'glucose': {'mw': 180.16, 'tissue': 'sweat'}
    }
    
    return metabolite_map[most_elevated]
```

#### **Option C: Use Average/Weighted Combination**
```python
def calculate_weighted_mw(biomarkers):
    """
    Create a composite molecular weight based on all biomarkers
    """
    # Weight by clinical importance for injury
    weights = {
        'lactate': 0.40,    # 40% - muscle fatigue indicator
        'cortisol': 0.25,   # 25% - stress/recovery
        'glucose': 0.20,    # 20% - energy availability
        'creatinine': 0.15  # 15% - kidney function/muscle breakdown
    }
    
    mw_values = {
        'lactate': 89.07,
        'cortisol': 362.46,
        'glucose': 180.16,
        'creatinine': 113.12
    }
    
    # Weighted average
    weighted_mw = sum(weights[m] * mw_values[m] for m in weights)
    # Result: ~176.5 Da
    
    return weighted_mw
```

#### **Option D: Always Use Lactate (Simplest)**
```python
def use_lactate_default():
    """
    Lactate is the most relevant for muscle injury prediction
    """
    return {
        'mw': 89.07,  # Lactate molecular weight
        'tissue': 'sweat'  # Lactate is typically measured in sweat
    }
```

---

## 🧪 **Features 2 & 3: Tissue Type Encoding**

### **How Tissue Type Works:**

The model uses **one-hot encoding** with **drop_first=True**:

```python
# Original data
tissue = 'saliva'  # OR 'sweat' OR 'urine'

# After one-hot encoding (drop_first=True means 'saliva' is the baseline)
pd.get_dummies(['saliva', 'sweat', 'urine'], drop_first=True)
```

**Result:**
| Original | tissue_sweat | tissue_urine | Meaning |
|----------|--------------|--------------|---------|
| saliva   | 0            | 0            | Baseline (reference category) |
| sweat    | 1            | 0            | Sweat sample |
| urine    | 0            | 1            | Urine sample |

### **The Problem for Your UI:**

Your UI has **THREE separate forms**:
- Page 1: Saliva biomarkers (Cortisol, Testosterone, IgA)
- Page 2: Urine biomarkers (Creatinine, Specific Gravity, pH)
- Page 3: Sweat biomarkers (Sodium, Lactate, Glucose)

**But the model expects ONE tissue type selection!**

---

### **Which Tissue Should You Report?**

#### **Option A: Report Whichever Form Has Data**
```python
def determine_tissue_type(form_data):
    """
    Use whichever sample type the user provided
    """
    if form_data['sweat']['lactate'] is not None:
        return {'tissue_sweat': 1, 'tissue_urine': 0}
    elif form_data['urine']['creatinine'] is not None:
        return {'tissue_sweat': 0, 'tissue_urine': 1}
    elif form_data['saliva']['cortisol'] is not None:
        return {'tissue_sweat': 0, 'tissue_urine': 0}  # saliva is baseline
```

#### **Option B: Use Priority Ranking**
```python
def prioritize_tissue():
    """
    Sweat is most relevant for sports injury
    """
    # Priority: Sweat > Urine > Saliva
    if has_sweat_data():
        return {'tissue_sweat': 1, 'tissue_urine': 0}
    elif has_urine_data():
        return {'tissue_sweat': 0, 'tissue_urine': 1}
    else:
        return {'tissue_sweat': 0, 'tissue_urine': 0}
```

#### **Option C: Let User Select at the End**
```python
# After all three forms are filled, ask:
"Which sample should we analyze for injury risk?"
○ Sweat (recommended for athletes)
○ Urine (comprehensive metabolic view)
○ Saliva (stress & hormonal indicators)
```

---

## 💡 **Complete Example: Converting Your UI Data to Model Input**

### **Your UI Collects:**
```python
user_input = {
    'saliva': {
        'cortisol': 0.78,      # nmol/L
        'testosterone': 0.23,  # pg/mL
        'iga': 0.75           # μg/mL
    },
    'sweat': {
        'sodium': 1.5,    # mmol/L
        'lactate': 3.2,   # mmol/L (ELEVATED!)
        'glucose': 2.2    # mg/dL
    },
    'urine': {
        'creatinine': None,  # Not provided
        'specific_gravity': None,
        'ph_level': None
    }
}
```

### **Conversion Strategy:**

```python
def convert_to_model_format(user_input):
    """
    Convert multi-biomarker UI input to GNODE model format
    """
    
    # STEP 1: Identify which metabolite to use
    # Since sweat lactate is elevated (3.2 > normal 2.2), use lactate
    if user_input['sweat']['lactate'] > 2.2:
        mw = 89.07  # Lactate molecular weight
        tissue_sweat = 1
        tissue_urine = 0
        metabolite_used = "Lactate (elevated in sweat)"
    
    # STEP 2: Prepare model features
    model_input = {
        # Biomarker features
        'mw': mw,                    # 89.07
        'tissue_sweat': tissue_sweat,  # 1
        'tissue_urine': tissue_urine,  # 0
        
        # EMG features (set to 0 since we don't have them)
        'rms_feat': 0,
        'zero_crossings': 0,
        'skewness': 0,
        'waveform_length': 0
    }
    
    return model_input, metabolite_used

# Result:
# model_input = {
#     'mw': 89.07,
#     'tissue_sweat': 1,
#     'tissue_urine': 0,
#     'rms_feat': 0,
#     'zero_crossings': 0,
#     'skewness': 0,
#     'waveform_length': 0
# }
# metabolite_used = "Lactate (elevated in sweat)"
```

---

## 🎯 **Recommended Implementation**

### **Backend API Function:**

```python
def prepare_biomarker_features(ui_data):
    """
    Master function to convert UI biomarkers to model input
    
    Args:
        ui_data: dict with 'saliva', 'sweat', 'urine' sections
    
    Returns:
        dict: 7 features ready for GNODE model
    """
    
    # Define clinical importance weights
    injury_relevance = {
        'lactate': 0.45,      # Muscle fatigue - HIGHEST priority
        'cortisol': 0.25,     # Stress/recovery
        'glucose': 0.15,      # Energy
        'creatinine': 0.10,   # Muscle breakdown
        'sodium': 0.05        # Hydration
    }
    
    # Map to molecular weights
    mw_lookup = {
        'lactate': 89.07,
        'cortisol': 362.46,
        'glucose': 180.16,
        'creatinine': 113.12,
        'sodium': 22.99,
        'testosterone': 288.42,
        'iga': 150000  # Large protein, unlikely to be used
    }
    
    # Calculate deviation from normal ranges
    deviations = {}
    
    # Sweat biomarkers
    if ui_data['sweat']['lactate']:
        deviations['lactate'] = abs(ui_data['sweat']['lactate'] - 2.2) / 2.2
    if ui_data['sweat']['glucose']:
        deviations['glucose'] = abs(ui_data['sweat']['glucose'] - 95) / 95
    if ui_data['sweat']['sodium']:
        deviations['sodium'] = abs(ui_data['sweat']['sodium'] - 40) / 40
    
    # Saliva biomarkers
    if ui_data['saliva']['cortisol']:
        deviations['cortisol'] = abs(ui_data['saliva']['cortisol'] - 0.5) / 0.5
    
    # Urine biomarkers
    if ui_data['urine']['creatinine']:
        deviations['creatinine'] = abs(ui_data['urine']['creatinine'] - 1.0) / 1.0
    
    # Select metabolite with highest weighted deviation
    weighted_scores = {}
    for metabolite, deviation in deviations.items():
        weighted_scores[metabolite] = deviation * injury_relevance.get(metabolite, 0)
    
    if weighted_scores:
        primary_metabolite = max(weighted_scores, key=weighted_scores.get)
    else:
        # Default to lactate if no data
        primary_metabolite = 'lactate'
    
    # Determine tissue type
    tissue_map = {
        'lactate': 'sweat',
        'glucose': 'sweat',
        'sodium': 'sweat',
        'cortisol': 'saliva',
        'testosterone': 'saliva',
        'creatinine': 'urine'
    }
    
    primary_tissue = tissue_map.get(primary_metabolite, 'sweat')
    
    # Encode tissue type
    tissue_encoding = {
        'saliva': {'tissue_sweat': 0, 'tissue_urine': 0},
        'sweat': {'tissue_sweat': 1, 'tissue_urine': 0},
        'urine': {'tissue_sweat': 0, 'tissue_urine': 1}
    }
    
    # Build final features
    features = {
        'mw': mw_lookup[primary_metabolite],
        **tissue_encoding[primary_tissue],
        'rms_feat': 0,  # No EMG data
        'zero_crossings': 0,
        'skewness': 0,
        'waveform_length': 0
    }
    
    metadata = {
        'selected_metabolite': primary_metabolite,
        'molecular_weight': mw_lookup[primary_metabolite],
        'tissue_source': primary_tissue,
        'deviation_score': weighted_scores.get(primary_metabolite, 0)
    }
    
    return features, metadata

# Example usage:
features, info = prepare_biomarker_features(user_input)

print(features)
# {
#   'mw': 89.07,
#   'tissue_sweat': 1,
#   'tissue_urine': 0,
#   'rms_feat': 0,
#   'zero_crossings': 0,
#   'skewness': 0,
#   'waveform_length': 0
# }

print(info)
# {
#   'selected_metabolite': 'lactate',
#   'molecular_weight': 89.07,
#   'tissue_source': 'sweat',
#   'deviation_score': 0.2045
# }
```

---

## 📋 **Summary: What to Show Users**

### **In Your Results Screen, Display:**

```
🔬 Analysis Details
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Primary Biomarker:    Lactate
Molecular Weight:     89.07 Da
Sample Source:        Sweat
Elevation Level:      +45% above normal

Risk Score:           51%
Risk Category:        High Risk

Note: Analysis prioritized lactate due to 
significant elevation in sweat sample, which 
is strongly associated with muscle fatigue 
and injury risk.
```

This gives users transparency about:
1. **Which metabolite** was used for prediction
2. **Why** that metabolite was selected
3. **What** the molecular weight represents

---

## ⚠️ **Important Caveats**

### **1. Model Wasn't Trained on Your Data Format**

The GNODE model was trained on:
- 3,500 individual metabolite entries (mw + tissue only)
- 120,000 EMG signal records

It was **NOT** trained on:
- Multiple biomarkers combined
- Concentration values (your UI uses mmol/L, mg/dL, etc.)

### **2. Accuracy Will Be Lower**

Expected accuracy:
- ✅ **With real EMG data**: 94%
- ⚠️ **With biomarkers only (no EMG)**: 75-82% (estimated)
- ⚠️ **With converted concentrations**: 70-78% (estimated)

### **3. You Should Validate This Approach**

Before production deployment:
1. Test with 100+ known cases (injury vs. no injury)
2. Compare predictions to actual outcomes
3. Adjust metabolite selection logic based on results
4. Consider retraining model with concentration data

---

## 🚀 **Next Steps**

1. ✅ Implement the `prepare_biomarker_features()` function in your backend
2. ✅ Add explanatory text in UI showing which metabolite was selected
3. ✅ Include disclaimers about accuracy limitations
4. ✅ Collect data to validate the approach
5. ✅ Plan to retrain model with actual concentration data

---

*Document Created: October 30, 2025*  
*For: GNODE Hamstring Injury Prediction Deployment*
