"""
Metabolite database with molecular weights, normal ranges, and clinical importance
"""

METABOLITE_DATABASE = {
    'saliva': {
        'cortisol': {
            'name': 'Cortisol',
            'molecular_weight': 362.46,  # Da
            'formula': 'C21H30O5',
            'normal_range': (0.1, 15.0),  # μg/dL
            'unit': 'μg/dL',
            'importance': 0.8,  # Scale 0-1 for injury prediction
            'description': 'Stress hormone indicator'
        },
        'testosterone': {
            'name': 'Testosterone',
            'molecular_weight': 288.42,  # Da
            'formula': 'C19H28O2',
            'normal_range': (10.0, 200.0),  # pg/mL
            'unit': 'pg/mL',
            'importance': 0.6,
            'description': 'Anabolic hormone, muscle recovery'
        },
        'iga': {
            'name': 'Immunoglobulin A',
            'molecular_weight': 385.0,  # Da (approximate for subunit)
            'formula': 'Variable',
            'normal_range': (10.0, 500.0),  # μg/mL
            'unit': 'μg/mL',
            'importance': 0.5,
            'description': 'Immune function indicator'
        }
    },
    'sweat': {
        'sodium': {
            'name': 'Sodium',
            'molecular_weight': 22.99,  # Da
            'formula': 'Na+',
            'normal_range': (0.5, 3.0),  # mmol/L
            'unit': 'mmol/L',
            'importance': 0.4,
            'description': 'Electrolyte balance'
        },
        'lactate': {
            'name': 'Lactate',
            'molecular_weight': 89.07,  # Da
            'formula': 'C3H5O3-',
            'normal_range': (0.5, 4.0),  # mmol/L
            'unit': 'mmol/L',
            'importance': 1.0,  # HIGHEST importance for injury prediction
            'description': 'Muscle fatigue and metabolic stress indicator'
        },
        'glucose': {
            'name': 'Glucose',
            'molecular_weight': 180.16,  # Da
            'formula': 'C6H12O6',
            'normal_range': (50.0, 150.0),  # mg/dL
            'unit': 'mg/dL',
            'importance': 0.7,
            'description': 'Energy metabolism'
        }
    },
    'urine': {
        'creatinine': {
            'name': 'Creatinine',
            'molecular_weight': 113.12,  # Da
            'formula': 'C4H7N3O',
            'normal_range': (20.0, 400.0),  # mg/dL
            'unit': 'mg/dL',
            'importance': 0.6,
            'description': 'Muscle breakdown product'
        },
        'protein': {
            'name': 'Protein',
            'molecular_weight': 66500.0,  # Da (approximate, albumin)
            'formula': 'Variable',
            'normal_range': (0.0, 20.0),  # mg/dL
            'unit': 'mg/dL',
            'importance': 0.7,
            'description': 'Muscle damage indicator'
        },
        'ph': {
            'name': 'pH',
            'molecular_weight': 1.0,  # Not applicable, using dummy value
            'formula': 'H+',
            'normal_range': (4.5, 8.0),  # pH units
            'unit': 'pH',
            'importance': 0.3,
            'description': 'Acid-base balance'
        }
    }
}

# Tissue type clinical relevance scores
TISSUE_RELEVANCE = {
    'sweat': 1.0,    # Most relevant for athletic injury prediction
    'urine': 0.7,    # Moderately relevant
    'saliva': 0.5    # Less relevant but still useful
}

def get_metabolite_info(tissue_type, biomarker_name):
    """Get metabolite information from database"""
    if tissue_type not in METABOLITE_DATABASE:
        return None
    if biomarker_name not in METABOLITE_DATABASE[tissue_type]:
        return None
    return METABOLITE_DATABASE[tissue_type][biomarker_name]

def get_molecular_weight(tissue_type, biomarker_name):
    """Get molecular weight for a specific biomarker"""
    info = get_metabolite_info(tissue_type, biomarker_name)
    return info['molecular_weight'] if info else None

def get_normal_range(tissue_type, biomarker_name):
    """Get normal range for a specific biomarker"""
    info = get_metabolite_info(tissue_type, biomarker_name)
    return info['normal_range'] if info else None

def get_importance_score(tissue_type, biomarker_name):
    """Get clinical importance score for injury prediction"""
    info = get_metabolite_info(tissue_type, biomarker_name)
    return info['importance'] if info else 0.0

def calculate_deviation(value, normal_range):
    """Calculate how much a value deviates from normal range (0-2 scale)"""
    min_val, max_val = normal_range
    mid_point = (min_val + max_val) / 2
    range_width = max_val - min_val
    
    # Calculate deviation as percentage above/below midpoint
    deviation = abs(value - mid_point) / (range_width / 2)
    
    # Cap at 2.0 (200% deviation)
    return min(deviation, 2.0)
