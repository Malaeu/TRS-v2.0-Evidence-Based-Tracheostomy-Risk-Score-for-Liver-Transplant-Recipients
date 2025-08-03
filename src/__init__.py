"""
Tracheostomy Risk Score (TRS) Package

A clinical prediction tool for evidence-based tracheostomy timing decisions
in liver transplant recipients.

This package provides:
- TRS calculation and risk stratification
- Bootstrap validation and performance metrics
- Clinical decision support tools
- Comprehensive statistical analysis pipeline

Example:
    >>> from tracheo_risk_score import TRSCalculator
    >>> calculator = TRSCalculator()
    >>> score = calculator.calculate_score(
    ...     meld=25, saps_ii=45, age=55, platelets=70,
    ...     hcc=True, cvvhd=False, vhf=True
    ... )
    >>> print(f"TRS Score: {score.total_score}")
    >>> print(f"Risk Category: {score.risk_category}")
"""

__version__ = "2.0.0"
__author__ = "Research Team"
__email__ = "research@hospital.org"

from .core import TRSCalculator, TRSResult
from .constants import TRS_CONSTANTS, RISK_CATEGORIES
from .validation import BootstrapValidator, PerformanceMetrics
from .utils import calculate_youden_index, format_clinical_output

__all__ = [
    "TRSCalculator",
    "TRSResult", 
    "TRS_CONSTANTS",
    "RISK_CATEGORIES",
    "BootstrapValidator",
    "PerformanceMetrics",
    "calculate_youden_index",
    "format_clinical_output",
]

