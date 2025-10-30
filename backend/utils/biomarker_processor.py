"""
Biomarker data processing utilities
Implements the tissue selection and metabolite prioritization logic
"""

from .metabolite_database import (
    METABOLITE_DATABASE,
    TISSUE_RELEVANCE,
    get_metabolite_info,
    get_molecular_weight,
    get_importance_score,
    calculate_deviation
)


def determine_primary_tissue(biomarker_data):
    """
    Determines which tissue type to use for model input based on:
    1. Elevation scores (how far values are from normal)
    2. Clinical relevance of tissue type
    3. Data completeness
    
    Returns: tuple (primary_tissue, score, details)
    """
    tissue_scores = {}
    
    for tissue_type in ['saliva', 'sweat', 'urine']:
        if tissue_type not in biomarker_data:
            continue
            
        tissue_data = biomarker_data[tissue_type]
        
        # Skip if no data for this tissue
        if not tissue_data or not any(tissue_data.values()):
            continue
        
        # Calculate elevation score (max 2.0 per biomarker)
        elevation_score = 0.0
        valid_biomarkers = 0
        
        for biomarker, value in tissue_data.items():
            if value is None or value == '':
                continue
                
            try:
                value = float(value)
            except (ValueError, TypeError):
                continue
            
            info = get_metabolite_info(tissue_type, biomarker)
            if not info:
                continue
            
            deviation = calculate_deviation(value, info['normal_range'])
            elevation_score += deviation
            valid_biomarkers += 1
        
        if valid_biomarkers == 0:
            continue
        
        # Average elevation score
        avg_elevation = elevation_score / valid_biomarkers
        
        # Clinical relevance score
        relevance = TISSUE_RELEVANCE.get(tissue_type, 0.5)
        
        # Data completeness score (0-0.3)
        total_biomarkers = len(METABOLITE_DATABASE[tissue_type])
        completeness = (valid_biomarkers / total_biomarkers) * 0.3
        
        # Total score = elevation (0-2) + relevance (0-1) + completeness (0-0.3)
        total_score = avg_elevation + relevance + completeness
        
        tissue_scores[tissue_type] = {
            'score': total_score,
            'elevation': avg_elevation,
            'relevance': relevance,
            'completeness': completeness,
            'valid_biomarkers': valid_biomarkers
        }
    
    if not tissue_scores:
        raise ValueError("No valid biomarker data provided")
    
    # Select tissue with highest score
    primary_tissue = max(tissue_scores.items(), key=lambda x: x[1]['score'])
    
    return primary_tissue[0], primary_tissue[1], tissue_scores


def select_primary_metabolite(tissue_data, tissue_type):
    """
    Selects which metabolite from the chosen tissue to use for molecular weight.
    Priority: importance_score * deviation_from_normal
    
    Returns: tuple (biomarker_name, molecular_weight, details)
    """
    metabolite_scores = {}
    
    for biomarker, value in tissue_data.items():
        if value is None or value == '':
            continue
        
        try:
            value = float(value)
        except (ValueError, TypeError):
            continue
        
        info = get_metabolite_info(tissue_type, biomarker)
        if not info:
            continue
        
        # Calculate selection score
        importance = info['importance']
        deviation = calculate_deviation(value, info['normal_range'])
        
        # Score = importance (0-1) * deviation (0-2)
        score = importance * deviation
        
        metabolite_scores[biomarker] = {
            'score': score,
            'value': value,
            'molecular_weight': info['molecular_weight'],
            'importance': importance,
            'deviation': deviation,
            'normal_range': info['normal_range']
        }
    
    if not metabolite_scores:
        raise ValueError(f"No valid metabolites in {tissue_type} data")
    
    # Select metabolite with highest score
    primary_metabolite = max(metabolite_scores.items(), key=lambda x: x[1]['score'])
    
    return (
        primary_metabolite[0],
        primary_metabolite[1]['molecular_weight'],
        metabolite_scores
    )


def prepare_model_features(biomarker_data, emg_data=None):
    """
    Converts biomarker data to GNODE model input features.
    
    Input: biomarker_data = {
        'saliva': {'cortisol': 5.2, 'testosterone': 85, ...},
        'sweat': {'lactate': 3.2, ...},
        'urine': {...}
    }
    
    Output: {
        'mw': float,
        'tissue_sweat': 0 or 1,
        'tissue_urine': 0 or 1,
        'rms_feat': float,
        'zero_crossings': float,
        'skewness': float,
        'waveform_length': float
    }
    """
    from config import Config
    
    # Step 1: Determine primary tissue
    primary_tissue, tissue_scores, all_scores = determine_primary_tissue(biomarker_data)
    
    # Step 2: Select primary metabolite from that tissue
    tissue_data = biomarker_data[primary_tissue]
    primary_biomarker, molecular_weight, metabolite_scores = select_primary_metabolite(
        tissue_data, primary_tissue
    )
    
    # Step 3: Encode tissue type (one-hot with drop_first=True)
    # Saliva = baseline [0, 0]
    # Sweat = [1, 0]
    # Urine = [0, 1]
    tissue_encoding = {
        'saliva': {'tissue_sweat': 0, 'tissue_urine': 0},
        'sweat': {'tissue_sweat': 1, 'tissue_urine': 0},
        'urine': {'tissue_sweat': 0, 'tissue_urine': 1}
    }
    
    tissue_features = tissue_encoding[primary_tissue]
    
    # Step 4: Handle EMG features (use defaults if not provided)
    emg_features = Config.DEFAULT_EMG_VALUES.copy()
    if emg_data:
        emg_features.update(emg_data)
    
    # Step 5: Combine all features
    model_input = {
        'mw': molecular_weight,
        **tissue_features,
        **emg_features
    }
    
    # Return features plus metadata for transparency
    metadata = {
        'primary_tissue': primary_tissue,
        'primary_biomarker': primary_biomarker,
        'tissue_scores': all_scores,
        'metabolite_scores': metabolite_scores,
        'molecular_weight': molecular_weight
    }
    
    return model_input, metadata


def validate_biomarker_data(biomarker_data):
    """
    Validates biomarker data structure and values.
    Returns: (is_valid, errors)
    """
    errors = []
    
    if not isinstance(biomarker_data, dict):
        errors.append("Biomarker data must be a dictionary")
        return False, errors
    
    valid_tissues = ['saliva', 'sweat', 'urine']
    has_data = False
    
    for tissue in valid_tissues:
        if tissue not in biomarker_data:
            continue
        
        tissue_data = biomarker_data[tissue]
        
        if not isinstance(tissue_data, dict):
            errors.append(f"{tissue} data must be a dictionary")
            continue
        
        for biomarker, value in tissue_data.items():
            if value is None or value == '':
                continue
            
            has_data = True
            
            # Check if biomarker exists in database
            if biomarker not in METABOLITE_DATABASE.get(tissue, {}):
                errors.append(f"Unknown biomarker: {tissue}.{biomarker}")
                continue
            
            # Validate value is numeric
            try:
                float_value = float(value)
                
                # Check if within reasonable bounds (extended range)
                info = get_metabolite_info(tissue, biomarker)
                if info:
                    min_val, max_val = info['normal_range']
                    extended_min = min_val * 0.1  # Allow 10x below
                    extended_max = max_val * 10   # Allow 10x above
                    
                    if float_value < extended_min or float_value > extended_max:
                        errors.append(
                            f"{tissue}.{biomarker} value {float_value} is extremely "
                            f"out of range (expected roughly {min_val}-{max_val} {info['unit']})"
                        )
            except (ValueError, TypeError):
                errors.append(f"{tissue}.{biomarker} must be a number, got: {value}")
    
    if not has_data:
        errors.append("No valid biomarker data provided")
    
    return len(errors) == 0, errors
