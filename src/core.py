"""
Core TRS calculation module.

This module contains the main TRSCalculator class and related functionality
for calculating Tracheostomy Risk Scores.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List, Tuple
import logging
from datetime import datetime

from constants import TRS_CUTPOINTS, TRS_POINTS, RISK_CATEGORIES, VARIABLE_DEFINITIONS

logger = logging.getLogger(__name__)


@dataclass
class TRSResult:
    """
    Result of TRS calculation with detailed breakdown.
    
    Attributes:
        total_score: Total TRS score (0-8)
        component_scores: Dictionary of individual component contributions
        risk_category: Risk category (LOW, MEDIUM, HIGH)
        risk_description: Human-readable risk description
        recommendation: Clinical recommendation
        mortality_risk: Estimated 90-day mortality risk
        details: Detailed calculation breakdown
        timestamp: When calculation was performed
        valid: Whether the calculation is valid
        warnings: Any warnings about the calculation
    """
    total_score: int
    component_scores: Dict[str, int]
    risk_category: str
    risk_description: str
    recommendation: str
    mortality_risk: float
    details: List[str]
    timestamp: datetime
    valid: bool = True
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []


class TRSCalculator:
    """
    Tracheostomy Risk Score Calculator.
    
    This class implements the evidence-based TRS calculation as described
    in the accompanying manuscript. All cut-points and weights are derived
    from optimal cut-point analysis and bootstrap validation.
    
    Example:
        >>> calculator = TRSCalculator()
        >>> result = calculator.calculate_score(
        ...     meld=25, saps_ii=45, age=55, platelets=70,
        ...     hcc=True, cvvhd=False, vhf=True
        ... )
        >>> print(f"TRS Score: {result.total_score}")
        >>> print(f"Risk: {result.risk_category}")
    """
    
    def __init__(self, validate_inputs: bool = True, log_calculations: bool = True):
        """
        Initialize TRS Calculator.
        
        Args:
            validate_inputs: Whether to validate input ranges
            log_calculations: Whether to log calculation details
        """
        self.validate_inputs = validate_inputs
        self.log_calculations = log_calculations
        self._setup_logging()
        
        if self.log_calculations:
            logger.info("TRS Calculator initialized")
    
    def _setup_logging(self) -> None:
        """Setup logging configuration."""
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
    
    def calculate_score(
        self,
        meld: Optional[float] = None,
        saps_ii: Optional[float] = None, 
        age: Optional[float] = None,
        platelets: Optional[float] = None,
        hcc: Optional[bool] = None,
        cvvhd: Optional[bool] = None,
        vhf: Optional[bool] = None,
        patient_id: Optional[str] = None
    ) -> TRSResult:
        """
        Calculate TRS score for a patient.
        
        Args:
            meld: MELD score (6-40)
            saps_ii: SAPS II score (0-163)
            age: Age in years (18-80)
            platelets: Platelet count in ×10³/μL (10-500)
            hcc: Hepatocellular carcinoma present
            cvvhd: Continuous veno-venous hemodialysis
            vhf: Atrial fibrillation present
            patient_id: Optional patient identifier for logging
            
        Returns:
            TRSResult: Complete calculation result
            
        Raises:
            ValueError: If inputs are invalid or insufficient data provided
        """
        timestamp = datetime.now()
        
        if self.log_calculations and patient_id:
            logger.info(f"Calculating TRS for patient {patient_id}")
        
        # Validate inputs
        if self.validate_inputs:
            self._validate_inputs(meld, saps_ii, age, platelets, hcc, cvvhd, vhf)
        
        # Check for missing data
        missing_components = self._check_missing_data(
            meld, saps_ii, age, platelets, hcc, cvvhd, vhf
        )
        
        # Calculate component scores
        component_scores = {}
        details = []
        warnings = []
        total_score = 0
        
        # MELD component (2 points if >20)
        if meld is not None:
            if meld > TRS_CUTPOINTS["MELD"]:
                component_scores["MELD"] = TRS_POINTS["MELD"]
                total_score += TRS_POINTS["MELD"]
                details.append(f"MELD > {TRS_CUTPOINTS['MELD']} ({meld:.1f}): +{TRS_POINTS['MELD']} points")
            else:
                component_scores["MELD"] = 0
                details.append(f"MELD ≤ {TRS_CUTPOINTS['MELD']} ({meld:.1f}): +0 points")
        else:
            warnings.append("MELD score missing")
            
        # SAPS II component (1 point if >42)
        if saps_ii is not None:
            if saps_ii > TRS_CUTPOINTS["SAPS_II"]:
                component_scores["SAPS_II"] = TRS_POINTS["SAPS_II"]
                total_score += TRS_POINTS["SAPS_II"]
                details.append(f"SAPS II > {TRS_CUTPOINTS['SAPS_II']} ({saps_ii:.1f}): +{TRS_POINTS['SAPS_II']} points")
            else:
                component_scores["SAPS_II"] = 0
                details.append(f"SAPS II ≤ {TRS_CUTPOINTS['SAPS_II']} ({saps_ii:.1f}): +0 points")
        else:
            warnings.append("SAPS II score missing")
            
        # Age component (1 point if >52)
        if age is not None:
            if age > TRS_CUTPOINTS["AGE"]:
                component_scores["AGE"] = TRS_POINTS["AGE"]
                total_score += TRS_POINTS["AGE"]
                details.append(f"Age > {TRS_CUTPOINTS['AGE']} ({age:.0f} years): +{TRS_POINTS['AGE']} points")
            else:
                component_scores["AGE"] = 0
                details.append(f"Age ≤ {TRS_CUTPOINTS['AGE']} ({age:.0f} years): +0 points")
        else:
            warnings.append("Age missing")
            
        # Platelets component (1 point if <78)
        if platelets is not None:
            if platelets < TRS_CUTPOINTS["PLATELETS"]:
                component_scores["PLATELETS"] = TRS_POINTS["PLATELETS"]
                total_score += TRS_POINTS["PLATELETS"]
                details.append(f"Platelets < {TRS_CUTPOINTS['PLATELETS']} ({platelets:.0f}): +{TRS_POINTS['PLATELETS']} points")
            else:
                component_scores["PLATELETS"] = 0
                details.append(f"Platelets ≥ {TRS_CUTPOINTS['PLATELETS']} ({platelets:.0f}): +0 points")
        else:
            warnings.append("Platelet count missing")
            
        # HCC component (1 point if present)
        if hcc is not None:
            if hcc:
                component_scores["HCC"] = TRS_POINTS["HCC"]
                total_score += TRS_POINTS["HCC"]
                details.append(f"Hepatocellular carcinoma present: +{TRS_POINTS['HCC']} points")
            else:
                component_scores["HCC"] = 0
                details.append("Hepatocellular carcinoma absent: +0 points")
        else:
            warnings.append("HCC status missing")
            
        # CVVHD component (1 point if present)
        if cvvhd is not None:
            if cvvhd:
                component_scores["CVVHD"] = TRS_POINTS["CVVHD"]
                total_score += TRS_POINTS["CVVHD"]
                details.append(f"Continuous veno-venous hemodialysis present: +{TRS_POINTS['CVVHD']} points")
            else:
                component_scores["CVVHD"] = 0
                details.append("Continuous veno-venous hemodialysis absent: +0 points")
        else:
            warnings.append("CVVHD status missing")
            
        # VHF component (1 point if present)
        if vhf is not None:
            if vhf:
                component_scores["VHF"] = TRS_POINTS["VHF"]
                total_score += TRS_POINTS["VHF"]
                details.append(f"Atrial fibrillation present: +{TRS_POINTS['VHF']} points")
            else:
                component_scores["VHF"] = 0
                details.append("Atrial fibrillation absent: +0 points")
        else:
            warnings.append("Atrial fibrillation status missing")
        
        # Determine risk category
        risk_category, risk_data = self._determine_risk_category(total_score)
        
        # Check validity
        valid = len(missing_components) <= 2  # Allow up to 2 missing components
        if not valid:
            warnings.append(f"Too many missing components ({len(missing_components)}). Results may be unreliable.")
        
        if self.log_calculations:
            logger.info(f"TRS calculation complete: Score={total_score}, Risk={risk_category}")
        
        return TRSResult(
            total_score=total_score,
            component_scores=component_scores,
            risk_category=risk_category,
            risk_description=risk_data["description"],
            recommendation=risk_data["recommendation"],
            mortality_risk=risk_data["mortality_rate"],
            details=details,
            timestamp=timestamp,
            valid=valid,
            warnings=warnings
        )
    
    def _validate_inputs(
        self,
        meld: Optional[float],
        saps_ii: Optional[float],
        age: Optional[float], 
        platelets: Optional[float],
        hcc: Optional[bool],
        cvvhd: Optional[bool],
        vhf: Optional[bool]
    ) -> None:
        """Validate input parameters."""
        
        # Validate MELD
        if meld is not None:
            meld_range = VARIABLE_DEFINITIONS["MELD"]["range"]
            if not (meld_range[0] <= meld <= meld_range[1]):
                raise ValueError(f"MELD score must be between {meld_range[0]} and {meld_range[1]}, got {meld}")
        
        # Validate SAPS II
        if saps_ii is not None:
            saps_range = VARIABLE_DEFINITIONS["SAPS_II"]["range"]
            if not (saps_range[0] <= saps_ii <= saps_range[1]):
                raise ValueError(f"SAPS II score must be between {saps_range[0]} and {saps_range[1]}, got {saps_ii}")
        
        # Validate Age
        if age is not None:
            age_range = VARIABLE_DEFINITIONS["AGE"]["range"]
            if not (age_range[0] <= age <= age_range[1]):
                raise ValueError(f"Age must be between {age_range[0]} and {age_range[1]}, got {age}")
        
        # Validate Platelets
        if platelets is not None:
            plt_range = VARIABLE_DEFINITIONS["PLATELETS"]["range"]
            if not (plt_range[0] <= platelets <= plt_range[1]):
                raise ValueError(f"Platelet count must be between {plt_range[0]} and {plt_range[1]}, got {platelets}")
        
        # Boolean variables don't need range validation
        
    def _check_missing_data(
        self,
        meld: Optional[float],
        saps_ii: Optional[float],
        age: Optional[float],
        platelets: Optional[float], 
        hcc: Optional[bool],
        cvvhd: Optional[bool],
        vhf: Optional[bool]
    ) -> List[str]:
        """Check for missing data components."""
        missing = []
        
        if meld is None:
            missing.append("MELD")
        if saps_ii is None:
            missing.append("SAPS_II")
        if age is None:
            missing.append("AGE")
        if platelets is None:
            missing.append("PLATELETS")
        if hcc is None:
            missing.append("HCC")
        if cvvhd is None:
            missing.append("CVVHD")
        if vhf is None:
            missing.append("VHF")
            
        return missing
    
    def _determine_risk_category(self, score: int) -> Tuple[str, Dict[str, Any]]:
        """Determine risk category based on TRS score."""
        for category, data in RISK_CATEGORIES.items():
            min_score, max_score = data["range"]
            if min_score <= score <= max_score:
                return category, data
        
        # Fallback for scores outside defined ranges
        if score < 0:
            return "LOW", RISK_CATEGORIES["LOW"]
        else:
            return "HIGH", RISK_CATEGORIES["HIGH"]
    
    def calculate_batch(self, patients_data: List[Dict[str, Any]]) -> List[TRSResult]:
        """
        Calculate TRS scores for multiple patients.
        
        Args:
            patients_data: List of patient data dictionaries
            
        Returns:
            List[TRSResult]: Results for all patients
        """
        results = []
        
        for i, patient_data in enumerate(patients_data):
            patient_id = patient_data.get('patient_id', f'patient_{i+1}')
            
            try:
                result = self.calculate_score(
                    meld=patient_data.get('meld'),
                    saps_ii=patient_data.get('saps_ii'),
                    age=patient_data.get('age'),
                    platelets=patient_data.get('platelets'),
                    hcc=patient_data.get('hcc'),
                    cvvhd=patient_data.get('cvvhd'),
                    vhf=patient_data.get('vhf'),
                    patient_id=patient_id
                )
                results.append(result)
                
            except Exception as e:
                logger.error(f"Error calculating TRS for {patient_id}: {e}")
                # Create error result
                error_result = TRSResult(
                    total_score=-1,
                    component_scores={},
                    risk_category="ERROR",
                    risk_description="Calculation Error",
                    recommendation="Unable to calculate - check input data",
                    mortality_risk=0.0,
                    details=[f"Error: {str(e)}"],
                    timestamp=datetime.now(),
                    valid=False,
                    warnings=[f"Calculation failed: {str(e)}"]
                )
                results.append(error_result)
        
        return results
    
    def get_component_info(self, component: str) -> Dict[str, Any]:
        """
        Get detailed information about a TRS component.
        
        Args:
            component: Component name (MELD, SAPS_II, AGE, PLATELETS, HCC, CVVHD, VHF)
            
        Returns:
            Dict with component information
            
        Raises:
            ValueError: If component is not recognized
        """
        if component not in VARIABLE_DEFINITIONS:
            raise ValueError(f"Unknown component: {component}")
        
        info = VARIABLE_DEFINITIONS[component].copy()
        
        if component in TRS_CUTPOINTS:
            info["cutpoint"] = TRS_CUTPOINTS[component]
        
        if component in TRS_POINTS:
            info["points"] = TRS_POINTS[component]
        
        return info
    
    def get_all_components_info(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all TRS components."""
        return {
            component: self.get_component_info(component)
            for component in VARIABLE_DEFINITIONS.keys()
        }

