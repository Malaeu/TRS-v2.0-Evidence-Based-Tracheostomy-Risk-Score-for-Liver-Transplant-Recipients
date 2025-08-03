"""
Constants and configuration for the Tracheostomy Risk Score (TRS).

All values are derived from the optimal cut-point analysis as documented
in Supplementary Table S1 of the accompanying manuscript.
"""

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

# TRS Component Cut-points (from Optimal Cut-point Analysis)
TRS_CUTPOINTS = {
    "MELD": 20,      # Sensitivity: 78.6%, Specificity: 69.1%, Youden: 0.477
    "SAPS_II": 42,   # Sensitivity: 75.0%, Specificity: 65.5%, Youden: 0.405  
    "AGE": 52,       # Sensitivity: 67.9%, Specificity: 58.2%, Youden: 0.261
    "PLATELETS": 78, # Sensitivity: 71.4%, Specificity: 63.6%, Youden: 0.350
}

# Point Assignments (based on hazard ratios and statistical significance)
TRS_POINTS = {
    "MELD": 2,       # HR: 3.24 (95% CI: 1.58-6.63), p=0.001
    "SAPS_II": 1,    # HR: 4.50 (95% CI: 1.73-11.70), p=0.002
    "AGE": 1,        # HR: 2.04 (95% CI: 0.84-4.95), p=0.115
    "PLATELETS": 1,  # HR: 5.15 (95% CI: 2.02-13.14), p=0.001
    "HCC": 1,        # OR: 2.89 (95% CI: 1.12-7.45), p=0.032
    "CVVHD": 1,      # OR: 1.78 (95% CI: 0.71-4.47), p=0.212
    "VHF": 1,        # OR: 1.95 (95% CI: 0.65-5.84), p=0.243
}

# Maximum possible TRS score
MAX_SCORE = sum(TRS_POINTS.values())  # = 8 points

# Risk Categories (based on 90-day mortality rates)
RISK_CATEGORIES = {
    "LOW": {
        "range": (0, 1),
        "mortality_rate": 0.10,
        "description": "Low Risk",
        "recommendation": "Standard weaning protocol",
        "color": "green"
    },
    "MEDIUM": {
        "range": (2, 2),  # Changed from (2,3) since HIGH now starts at 3
        "mortality_rate": 0.33,
        "description": "Medium Risk",
        "recommendation": "Enhanced monitoring and assessment",
        "color": "orange"
    },
    "HIGH": {
        "range": (3, 8),  # Changed from (4,8) to align with optimal threshold ≥3
        "mortality_rate": 0.46,
        "description": "High Risk", 
        "recommendation": "Consider early tracheostomy (Day 5-7)",
        "color": "red"
    }
}

# Optimal Decision Thresholds (from Landmark Analysis)
OPTIMAL_THRESHOLDS = {
    "DAY_3": {
        "threshold": 2.0,
        "sensitivity": 1.000,
        "specificity": 0.167,
        "auc": 0.464,
        "sample_size": 64
    },
    "DAY_5": {
        "threshold": 2.0, 
        "sensitivity": 1.000,
        "specificity": 0.244,
        "auc": 0.614,
        "sample_size": 54
    },
    "DAY_7": {  # OPTIMAL MODEL
        "threshold": 3.0,
        "sensitivity": 1.000,
        "specificity": 0.474,
        "auc": 0.754,
        "sample_size": 47
    }
}

# Variable Definitions and Units
VARIABLE_DEFINITIONS = {
    "MELD": {
        "name": "Model for End-Stage Liver Disease Score",
        "unit": "points",
        "range": (6, 40),
        "description": "Primary indicator of liver dysfunction severity"
    },
    "SAPS_II": {
        "name": "Simplified Acute Physiology Score II", 
        "unit": "points",
        "range": (0, 163),
        "description": "Multi-organ dysfunction assessment"
    },
    "AGE": {
        "name": "Age at transplantation",
        "unit": "years", 
        "range": (18, 80),
        "description": "Patient age reflecting physiological reserve"
    },
    "PLATELETS": {
        "name": "Platelet count",
        "unit": "×10³/μL",
        "range": (10, 500),
        "description": "Coagulopathy and liver dysfunction marker"
    },
    "HCC": {
        "name": "Hepatocellular carcinoma",
        "unit": "boolean",
        "description": "Oncological burden and prognosis indicator"
    },
    "CVVHD": {
        "name": "Continuous Veno-Venous Hemodialysis",
        "unit": "boolean", 
        "description": "Multi-organ failure and renal support indicator"
    },
    "VHF": {
        "name": "Atrial fibrillation",
        "unit": "boolean",
        "description": "Cardiovascular comorbidity indicator"
    }
}

# Performance Metrics (from Bootstrap Validation)
PERFORMANCE_METRICS = {
    "C_INDEX": {
        "original": 0.754,
        "bootstrap_mean": 0.761,
        "bias_corrected": 0.742,
        "ci_95": (0.628, 0.856),
        "optimism": 0.012
    },
    "AUC_60_DAY": {
        "original": 0.754,
        "bootstrap_mean": 0.759, 
        "bias_corrected": 0.745,
        "ci_95": (0.631, 0.859),
        "optimism": 0.009
    },
    "BRIER_SCORE": {
        "original": 0.186,
        "bootstrap_mean": 0.184,
        "bias_corrected": 0.188,
        "ci_95": (0.142, 0.234),
        "optimism": -0.002
    }
}

# Clinical Implementation Settings
CLINICAL_SETTINGS = {
    "LANDMARK_DAY": 7,           # Optimal assessment day
    "DECISION_THRESHOLD": 3.0,   # TRS threshold for tracheostomy consideration
    "FOLLOWUP_DAYS": 90,         # Primary outcome timeframe
    "MIN_ICU_STAY": 3,          # Minimum ICU stay for TRS calculation
    "MAX_MISSING_COMPONENTS": 2, # Maximum missing TRS components allowed
}

# Validation Settings
VALIDATION_SETTINGS = {
    "BOOTSTRAP_ITERATIONS": 1000,
    "RANDOM_SEED": 42,
    "CONFIDENCE_LEVEL": 0.95,
    "HOSMER_LEMESHOW_BINS": 10,
    "CALIBRATION_TOLERANCE": 0.05,
}

# Logging Configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False
        }
    }
}

# Consolidated constants for backward compatibility
TRS_CONSTANTS = {
    "cutpoints": TRS_CUTPOINTS,
    "points": TRS_POINTS,
    "risk_categories": RISK_CATEGORIES,
    "thresholds": OPTIMAL_THRESHOLDS,
    "variables": VARIABLE_DEFINITIONS,
    "performance": PERFORMANCE_METRICS,
    "clinical": CLINICAL_SETTINGS,
    "validation": VALIDATION_SETTINGS,
}

def validate_constants() -> bool:
    """
    Validate that all constants are properly defined and consistent.
    
    Returns:
        bool: True if all validations pass
        
    Raises:
        ValueError: If any validation fails
    """
    logger.info("Validating TRS constants...")
    
    # Check that all TRS components have both cutpoints and points
    cutpoint_keys = set(TRS_CUTPOINTS.keys())
    point_keys = set(k for k in TRS_POINTS.keys() if k not in ["HCC", "CVVHD", "VHF"])
    
    if cutpoint_keys != point_keys:
        raise ValueError(f"Mismatch between cutpoint and point keys: {cutpoint_keys} vs {point_keys}")
    
    # Check risk category ranges don't overlap
    ranges = [cat["range"] for cat in RISK_CATEGORIES.values()]
    for i, range1 in enumerate(ranges):
        for j, range2 in enumerate(ranges[i+1:], i+1):
            if not (range1[1] < range2[0] or range2[1] < range1[0]):
                raise ValueError(f"Overlapping risk category ranges: {range1} and {range2}")
    
    # Check that optimal threshold is within valid TRS range
    max_score = sum(TRS_POINTS.values())
    for day, threshold_data in OPTIMAL_THRESHOLDS.items():
        threshold = threshold_data["threshold"]
        if not (0 <= threshold <= max_score):
            raise ValueError(f"Invalid threshold for {day}: {threshold} (max possible: {max_score})")
    
    logger.info("All TRS constants validated successfully")
    return True

# Validate constants on import
if __name__ != "__main__":
    validate_constants()

