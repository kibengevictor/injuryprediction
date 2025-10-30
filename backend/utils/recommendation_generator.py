"""
Generate recommendations based on risk score and biomarker analysis
"""

def generate_recommendations(risk_score, metadata):
    """
    Generate personalized recommendations based on risk score and biomarker data.
    
    Returns: {
        'immediate': [...],
        'followUp': [...],
        'monitoring': [...]
    }
    """
    primary_tissue = metadata.get('primary_tissue', 'unknown')
    primary_biomarker = metadata.get('primary_biomarker', 'unknown')
    
    # Determine risk level
    if risk_score < 25:
        risk_level = 'LOW'
    elif risk_score < 50:
        risk_level = 'MODERATE'
    elif risk_score < 75:
        risk_level = 'HIGH'
    else:
        risk_level = 'CRITICAL'
    
    # Base recommendations by risk level
    recommendations = {
        'LOW': {
            'immediate': [
                'Continue current training regimen with caution',
                'Maintain proper warm-up and cool-down routines',
                'Stay hydrated and maintain balanced nutrition',
                'Monitor for any unusual muscle soreness or tightness'
            ],
            'followUp': [
                'Re-test biomarkers in 2-3 weeks',
                'Consider preventive stretching exercises',
                'Ensure adequate sleep and recovery time'
            ],
            'monitoring': [
                'Track training intensity and volume',
                'Log any discomfort or unusual fatigue',
                'Monthly biomarker monitoring recommended'
            ]
        },
        'MODERATE': {
            'immediate': [
                'Reduce training intensity by 25-30%',
                'Increase rest intervals between sessions',
                'Apply ice after training if discomfort present',
                'Avoid explosive movements and sprinting',
                'Consult with sports medicine professional'
            ],
            'followUp': [
                'Re-test biomarkers within 1 week',
                'Schedule physiotherapy assessment',
                'Implement targeted hamstring strengthening',
                'Review and adjust training load'
            ],
            'monitoring': [
                'Daily check for pain, stiffness, or reduced flexibility',
                'Track recovery time between sessions',
                'Weekly biomarker monitoring recommended',
                'Log all symptoms and training modifications'
            ]
        },
        'HIGH': {
            'immediate': [
                'Rest hamstring muscles for 24-48 hours',
                'Apply ice/compression if pain present',
                'Schedule sports medicine evaluation',
                'Reduce training intensity by 50%',
                'Avoid high-intensity sprinting or jumping'
            ],
            'followUp': [
                'Re-test biomarkers to monitor improvement within 3-5 days',
                'Consider physiotherapy assessment',
                'Implement targeted hamstring strengthening',
                'Review training load and recovery protocols'
            ],
            'monitoring': [
                'Monitor for pain, tightness, or reduced flexibility',
                'Track daily hamstring comfort levels',
                'Log any discomfort during activities',
                'Weekly biomarker monitoring recommended'
            ]
        },
        'CRITICAL': {
            'immediate': [
                'STOP all high-intensity training immediately',
                'Seek immediate sports medicine evaluation',
                'Complete rest for hamstring muscles (48-72 hours minimum)',
                'Apply RICE protocol (Rest, Ice, Compression, Elevation)',
                'Avoid ANY activities that stress hamstrings'
            ],
            'followUp': [
                'Medical examination within 24 hours',
                'Re-test biomarkers within 2-3 days',
                'MRI or ultrasound imaging may be necessary',
                'Develop comprehensive rehabilitation plan',
                'Work with physical therapist on recovery protocol'
            ],
            'monitoring': [
                'Hourly pain and mobility checks initially',
                'Document all symptoms and changes',
                'Daily biomarker monitoring if possible',
                'Track response to rest and treatment',
                'Do not resume training without medical clearance'
            ]
        }
    }
    
    base_recs = recommendations[risk_level]
    
    # Add biomarker-specific recommendations
    specific_recs = get_biomarker_specific_recommendations(
        primary_tissue,
        primary_biomarker,
        metadata
    )
    
    # Merge recommendations
    final_recs = {
        'immediate': base_recs['immediate'] + specific_recs.get('immediate', []),
        'followUp': base_recs['followUp'] + specific_recs.get('followUp', []),
        'monitoring': base_recs['monitoring'] + specific_recs.get('monitoring', [])
    }
    
    return final_recs


def get_biomarker_specific_recommendations(tissue, biomarker, metadata):
    """Generate recommendations specific to the elevated biomarker"""
    
    specific = {
        'immediate': [],
        'followUp': [],
        'monitoring': []
    }
    
    # Lactate-specific recommendations
    if biomarker == 'lactate':
        specific['immediate'].append(
            'Elevated lactate indicates muscle fatigue - ensure adequate recovery'
        )
        specific['followUp'].append(
            'Consider lactate threshold training to improve clearance'
        )
        specific['monitoring'].append(
            'Track post-exercise lactate levels if possible'
        )
    
    # Cortisol-specific recommendations
    elif biomarker == 'cortisol':
        specific['immediate'].append(
            'Elevated cortisol suggests high stress - prioritize recovery and sleep'
        )
        specific['followUp'].append(
            'Implement stress management techniques (meditation, breathing exercises)'
        )
        specific['monitoring'].append(
            'Monitor sleep quality and overall stress levels'
        )
    
    # Protein-specific recommendations
    elif biomarker == 'protein':
        specific['immediate'].append(
            'Elevated protein may indicate muscle damage - avoid intense exercise'
        )
        specific['followUp'].append(
            'Ensure adequate protein intake for muscle repair (1.6-2.2g/kg body weight)'
        )
    
    # Creatinine-specific recommendations
    elif biomarker == 'creatinine':
        specific['immediate'].append(
            'Monitor hydration status carefully'
        )
        specific['followUp'].append(
            'Consider kidney function evaluation if levels remain elevated'
        )
    
    return specific


def get_key_indicators_text(metadata):
    """Generate human-readable text describing key indicators"""
    
    primary_tissue = metadata.get('primary_tissue', 'unknown')
    primary_biomarker = metadata.get('primary_biomarker', 'unknown')
    
    tissue_names = {
        'saliva': 'saliva',
        'sweat': 'sweat',
        'urine': 'urine'
    }
    
    biomarker_descriptions = {
        'lactate': 'elevated lactate levels detected in your biomarkers, indicating significant muscle fatigue and increased hamstring injury risk',
        'cortisol': 'elevated cortisol levels detected, suggesting high stress and potential overtraining',
        'protein': 'elevated protein levels in urine, potentially indicating muscle damage',
        'creatinine': 'elevated creatinine levels, suggesting muscle breakdown',
        'testosterone': 'abnormal testosterone levels, which may affect muscle recovery',
        'glucose': 'abnormal glucose levels, indicating potential metabolic stress',
        'sodium': 'abnormal sodium levels, suggesting electrolyte imbalance',
        'iga': 'abnormal immunoglobulin A levels, potentially indicating immune stress'
    }
    
    description = biomarker_descriptions.get(
        primary_biomarker,
        f'abnormal {primary_biomarker} levels detected in {tissue_names.get(primary_tissue, "your")} biomarkers'
    )
    
    return f"Analysis of your {tissue_names.get(primary_tissue, '')} biomarkers shows {description}."
