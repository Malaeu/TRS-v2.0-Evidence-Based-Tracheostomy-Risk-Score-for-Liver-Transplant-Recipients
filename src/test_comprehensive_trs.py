"""
Comprehensive test suite for the Tracheostomy Risk Score (TRS) system.

This test suite validates all components of the TRS system including:
- Core calculation logic
- Constants and configuration
- Validation procedures
- CLI functionality
- Edge cases and error handling
"""

import pytest
import sys
import os
import numpy as np
import pandas as pd
from datetime import datetime
from unittest.mock import patch, MagicMock

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tracheo_risk_score.core import TRSCalculator, TRSResult
from tracheo_risk_score.constants import (
    TRS_CUTPOINTS, TRS_POINTS, RISK_CATEGORIES, 
    OPTIMAL_THRESHOLDS, validate_constants
)
from tracheo_risk_score.validation import BootstrapValidator, PerformanceMetrics
from tracheo_risk_score.utils import (
    format_clinical_output, create_batch_summary,
    validate_patient_data, calculate_youden_index
)


class TestTRSConstants:
    """Test TRS constants and configuration."""
    
    def test_constants_validation(self):
        """Test that all constants are properly validated."""
        assert validate_constants() == True
    
    def test_cutpoints_exist(self):
        """Test that all required cutpoints are defined."""
        required_cutpoints = ["MELD", "SAPS_II", "AGE", "PLATELETS"]
        for cutpoint in required_cutpoints:
            assert cutpoint in TRS_CUTPOINTS
            assert isinstance(TRS_CUTPOINTS[cutpoint], (int, float))
    
    def test_points_exist(self):
        """Test that all required points are defined."""
        required_points = ["MELD", "SAPS_II", "AGE", "PLATELETS", "HCC", "CVVHD", "VHF"]
        for point in required_points:
            assert point in TRS_POINTS
            assert isinstance(TRS_POINTS[point], int)
            assert TRS_POINTS[point] >= 0
    
    def test_risk_categories_valid(self):
        """Test that risk categories are properly defined."""
        assert len(RISK_CATEGORIES) == 3
        for category, data in RISK_CATEGORIES.items():
            assert "range" in data
            assert "mortality_rate" in data
            assert "description" in data
            assert "recommendation" in data
            assert len(data["range"]) == 2
            assert 0 <= data["mortality_rate"] <= 1
    
    def test_optimal_thresholds_valid(self):
        """Test that optimal thresholds are properly defined."""
        for day, threshold_data in OPTIMAL_THRESHOLDS.items():
            assert "threshold" in threshold_data
            assert "sensitivity" in threshold_data
            assert "specificity" in threshold_data
            assert "auc" in threshold_data
            assert 0 <= threshold_data["sensitivity"] <= 1
            assert 0 <= threshold_data["specificity"] <= 1
            assert 0 <= threshold_data["auc"] <= 1


class TestTRSCalculator:
    """Test TRS calculator core functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.calculator = TRSCalculator(log_calculations=False)
    
    def test_calculator_initialization(self):
        """Test calculator initialization."""
        calc = TRSCalculator()
        assert calc.validate_inputs == True
        assert calc.log_calculations == True
        
        calc_no_validation = TRSCalculator(validate_inputs=False, log_calculations=False)
        assert calc_no_validation.validate_inputs == False
        assert calc_no_validation.log_calculations == False
    
    def test_perfect_score_calculation(self):
        """Test calculation with all risk factors present."""
        result = self.calculator.calculate_score(
            meld=30,      # >20: +2 points
            saps_ii=50,   # >42: +1 point
            age=60,       # >52: +1 point
            platelets=50, # <78: +1 point
            hcc=True,     # +1 point
            cvvhd=True,   # +1 point
            vhf=True      # +1 point
        )
        
        assert result.total_score == 8  # Maximum possible score
        assert result.risk_category == "HIGH"
        assert result.valid == True
        assert len(result.warnings) == 0
    
    def test_zero_score_calculation(self):
        """Test calculation with no risk factors present."""
        result = self.calculator.calculate_score(
            meld=15,       # ≤20: +0 points
            saps_ii=35,    # ≤42: +0 points
            age=45,        # ≤52: +0 points
            platelets=100, # ≥78: +0 points
            hcc=False,     # +0 points
            cvvhd=False,   # +0 points
            vhf=False      # +0 points
        )
        
        assert result.total_score == 0
        assert result.risk_category == "LOW"
        assert result.valid == True
        assert len(result.warnings) == 0
    
    def test_medium_risk_calculation(self):
        """Test calculation resulting in medium risk."""
        result = self.calculator.calculate_score(
            meld=25,      # >20: +2 points
            saps_ii=40,   # ≤42: +0 points
            age=50,       # ≤52: +0 points
            platelets=90, # ≥78: +0 points
            hcc=False,    # +0 points
            cvvhd=False,  # +0 points
            vhf=False     # +0 points
        )
        
        assert result.total_score == 2  # Only MELD contributes
        assert result.risk_category == "MEDIUM"
        assert result.valid == True
    
    def test_missing_data_handling(self):
        """Test handling of missing data."""
        result = self.calculator.calculate_score(
            meld=25,
            saps_ii=None,  # Missing
            age=None,      # Missing
            platelets=70,
            hcc=True,
            cvvhd=None,    # Missing
            vhf=False
        )
        
        assert result.valid == False  # 3 missing components (>2 threshold)
        assert len(result.warnings) == 4  # 3 missing + 1 "too many missing" warning
        assert "SAPS II score missing" in result.warnings
        assert "Age missing" in result.warnings
        assert "CVVHD status missing" in result.warnings
        assert any("Too many missing components (3)" in warning for warning in result.warnings)
    
    def test_too_much_missing_data(self):
        """Test handling when too much data is missing."""
        result = self.calculator.calculate_score(
            meld=None,     # Missing
            saps_ii=None,  # Missing
            age=None,      # Missing
            platelets=None, # Missing
            hcc=None,      # Missing
            cvvhd=True,
            vhf=False
        )
        
        assert result.valid == False  # >2 missing components
        assert len(result.warnings) >= 5
    
    def test_input_validation(self):
        """Test input validation."""
        # Test MELD out of range
        with pytest.raises(ValueError, match="MELD score must be between"):
            self.calculator.calculate_score(meld=50)  # Too high
        
        with pytest.raises(ValueError, match="MELD score must be between"):
            self.calculator.calculate_score(meld=0)   # Too low
        
        # Test SAPS II out of range
        with pytest.raises(ValueError, match="SAPS II score must be between"):
            self.calculator.calculate_score(saps_ii=200)  # Too high
        
        # Test age out of range
        with pytest.raises(ValueError, match="Age must be between"):
            self.calculator.calculate_score(age=100)  # Too high
        
        # Test platelets out of range
        with pytest.raises(ValueError, match="Platelet count must be between"):
            self.calculator.calculate_score(platelets=1000)  # Too high
    
    def test_batch_calculation(self):
        """Test batch calculation functionality."""
        patients_data = [
            {
                "meld": 25, "saps_ii": 45, "age": 55, "platelets": 70,
                "hcc": True, "cvvhd": False, "vhf": True, "patient_id": "P001"
            },
            {
                "meld": 15, "saps_ii": 35, "age": 45, "platelets": 100,
                "hcc": False, "cvvhd": False, "vhf": False, "patient_id": "P002"
            }
        ]
        
        results = self.calculator.calculate_batch(patients_data)
        
        assert len(results) == 2
        assert all(isinstance(r, TRSResult) for r in results)
        assert results[0].total_score > results[1].total_score  # P001 higher risk
    
    def test_component_info(self):
        """Test component information retrieval."""
        meld_info = self.calculator.get_component_info("MELD")
        
        assert "name" in meld_info
        assert "description" in meld_info
        assert "cutpoint" in meld_info
        assert "points" in meld_info
        assert meld_info["cutpoint"] == TRS_CUTPOINTS["MELD"]
        assert meld_info["points"] == TRS_POINTS["MELD"]
        
        # Test invalid component
        with pytest.raises(ValueError, match="Unknown component"):
            self.calculator.get_component_info("INVALID")
    
    def test_all_components_info(self):
        """Test retrieval of all component information."""
        all_info = self.calculator.get_all_components_info()
        
        assert len(all_info) == 7  # All TRS components
        for component in ["MELD", "SAPS_II", "AGE", "PLATELETS", "HCC", "CVVHD", "VHF"]:
            assert component in all_info


class TestTRSResult:
    """Test TRS result data structure."""
    
    def test_result_creation(self):
        """Test TRS result creation."""
        result = TRSResult(
            total_score=5,
            component_scores={"MELD": 2, "SAPS_II": 1},
            risk_category="HIGH",
            risk_description="High Risk",
            recommendation="Consider early tracheostomy",
            mortality_risk=0.47,
            details=["MELD > 20: +2 points"],
            timestamp=datetime.now(),
            valid=True
        )
        
        assert result.total_score == 5
        assert result.risk_category == "HIGH"
        assert result.valid == True
        assert result.warnings == []  # Default empty list
    
    def test_result_with_warnings(self):
        """Test TRS result with warnings."""
        warnings = ["Missing data", "Out of range value"]
        result = TRSResult(
            total_score=3,
            component_scores={},
            risk_category="MEDIUM",
            risk_description="Medium Risk",
            recommendation="Monitor closely",
            mortality_risk=0.33,
            details=[],
            timestamp=datetime.now(),
            valid=False,
            warnings=warnings
        )
        
        assert result.warnings == warnings
        assert result.valid == False


class TestBootstrapValidator:
    """Test bootstrap validation functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        # Create synthetic test data
        np.random.seed(42)
        n_patients = 100
        
        self.test_data = pd.DataFrame({
            'meld': np.random.normal(22, 8, n_patients).clip(6, 40),
            'saps_ii': np.random.normal(44, 12, n_patients).clip(0, 163),
            'age': np.random.normal(56, 15, n_patients).clip(18, 80),
            'platelets': np.random.normal(82, 40, n_patients).clip(10, 500),
            'hcc': np.random.choice([True, False], n_patients, p=[0.3, 0.7]),
            'cvvhd': np.random.choice([True, False], n_patients, p=[0.35, 0.65]),
            'vhf': np.random.choice([True, False], n_patients, p=[0.26, 0.74]),
            'death_90d': np.random.choice([0, 1], n_patients, p=[0.6, 0.4]),
            'survival_time': np.random.exponential(45, n_patients).clip(1, 90)
        })
        
        self.validator = BootstrapValidator(n_bootstrap=10, random_seed=42)  # Small n for testing
    
    def test_validator_initialization(self):
        """Test validator initialization."""
        validator = BootstrapValidator()
        assert validator.n_bootstrap == 1000  # Default value
        assert validator.random_seed == 42    # Default value
        
        custom_validator = BootstrapValidator(n_bootstrap=500, random_seed=123)
        assert custom_validator.n_bootstrap == 500
        assert custom_validator.random_seed == 123
    
    def test_performance_calculation(self):
        """Test performance metrics calculation."""
        performance = self.validator._calculate_performance(
            self.test_data, 'death_90d', 'survival_time'
        )
        
        assert isinstance(performance, PerformanceMetrics)
        assert 0 <= performance.c_index <= 1
        assert 0 <= performance.auc <= 1
        assert performance.brier_score >= 0
        assert 0 <= performance.sensitivity <= 1
        assert 0 <= performance.specificity <= 1
    
    def test_c_index_calculation(self):
        """Test C-index calculation."""
        scores = np.array([1, 2, 3, 4, 5])
        outcomes = np.array([0, 0, 1, 1, 1])
        
        c_index = self.validator._calculate_c_index(scores, outcomes)
        assert 0.5 <= c_index <= 1.0  # Should be better than random
    
    def test_hosmer_lemeshow_test(self):
        """Test Hosmer-Lemeshow goodness-of-fit test."""
        np.random.seed(42)
        outcomes = np.random.choice([0, 1], 100)
        probabilities = np.random.uniform(0, 1, 100)
        
        p_value = self.validator._hosmer_lemeshow_test(outcomes, probabilities)
        assert 0 <= p_value <= 1


class TestUtilityFunctions:
    """Test utility functions."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.sample_result = TRSResult(
            total_score=5,
            component_scores={"MELD": 2, "SAPS_II": 1, "AGE": 1, "HCC": 1},
            risk_category="HIGH",
            risk_description="High Risk",
            recommendation="Consider early tracheostomy (Day 5-7)",
            mortality_risk=0.47,
            details=["MELD > 20 (25.0): +2 points", "SAPS II > 42 (45.0): +1 points"],
            timestamp=datetime.now(),
            valid=True,
            warnings=[]
        )
    
    def test_clinical_output_formatting(self):
        """Test clinical output formatting."""
        output = format_clinical_output(self.sample_result)
        
        assert "TRACHEOSTOMY RISK SCORE" in output
        assert "TRS SCORE: 5/8" in output
        assert "High Risk" in output
        assert "Consider early tracheostomy" in output
        assert "VALID" in output
    
    def test_clinical_output_with_warnings(self):
        """Test clinical output with warnings."""
        result_with_warnings = TRSResult(
            total_score=3,
            component_scores={"MELD": 2},
            risk_category="MEDIUM",
            risk_description="Medium Risk",
            recommendation="Enhanced monitoring",
            mortality_risk=0.33,
            details=["MELD > 20: +2 points"],
            timestamp=datetime.now(),
            valid=False,
            warnings=["Missing data for SAPS II", "Age out of range"]
        )
        
        output = format_clinical_output(result_with_warnings)
        assert "WARNINGS:" in output
        assert "Missing data for SAPS II" in output
        assert "INVALID" in output
    
    def test_batch_summary_creation(self):
        """Test batch summary creation."""
        results = [
            TRSResult(0, {}, "LOW", "Low Risk", "Standard", 0.1, [], datetime.now(), True),
            TRSResult(3, {}, "MEDIUM", "Medium Risk", "Monitor", 0.33, [], datetime.now(), True),
            TRSResult(6, {}, "HIGH", "High Risk", "Tracheostomy", 0.47, [], datetime.now(), True),
        ]
        
        summary = create_batch_summary(results)
        
        assert summary["total_patients"] == 3
        assert summary["valid_calculations"] == 3
        assert summary["invalid_calculations"] == 0
        assert "score_statistics" in summary
        assert "risk_distribution" in summary
        assert summary["score_statistics"]["mean"] == 3.0  # (0+3+6)/3
    
    def test_patient_data_validation(self):
        """Test patient data validation."""
        # Valid data
        valid_data = {
            "meld": 25, "saps_ii": 45, "age": 55, "platelets": 70,
            "hcc": True, "cvvhd": False, "vhf": True
        }
        errors = validate_patient_data(valid_data)
        assert len(errors) == 0
        
        # Invalid data - out of range
        invalid_data = {
            "meld": 50,  # Too high
            "saps_ii": 200,  # Too high
            "age": 100,  # Too high
            "platelets": 1000,  # Too high
            "hcc": "yes"  # Should be boolean
        }
        errors = validate_patient_data(invalid_data)
        assert len(errors) > 0
        assert any("MELD score out of range" in error for error in errors)
        assert any("must be boolean" in error for error in errors)
        
        # Insufficient data
        insufficient_data = {"meld": 25, "age": 55}  # Only 2 components
        errors = validate_patient_data(insufficient_data)
        assert len(errors) > 0
        assert any("Insufficient data" in error for error in errors)
    
    def test_youden_index_calculation(self):
        """Test Youden index calculation."""
        y_true = [0, 0, 1, 1, 1, 1, 0, 0, 1, 1]
        y_scores = [0.1, 0.2, 0.3, 0.6, 0.7, 0.8, 0.15, 0.25, 0.9, 0.95]
        
        result = calculate_youden_index(y_true, y_scores)
        
        assert "optimal_threshold" in result
        assert "sensitivity" in result
        assert "specificity" in result
        assert "youden_index" in result
        assert 0 <= result["sensitivity"] <= 1
        assert 0 <= result["specificity"] <= 1
        assert result["youden_index"] == result["sensitivity"] + result["specificity"] - 1


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.calculator = TRSCalculator(log_calculations=False)
    
    def test_boundary_values(self):
        """Test calculations with boundary values."""
        # Test exact cutpoint values
        result_at_cutpoint = self.calculator.calculate_score(
            meld=20,      # Exactly at cutpoint
            saps_ii=42,   # Exactly at cutpoint
            age=52,       # Exactly at cutpoint
            platelets=78, # Exactly at cutpoint
            hcc=False, cvvhd=False, vhf=False
        )
        
        # At cutpoint should not trigger (using > and < comparisons)
        assert result_at_cutpoint.total_score == 0
        
        # Test just above/below cutpoints
        result_above_cutpoint = self.calculator.calculate_score(
            meld=20.1, saps_ii=42.1, age=52.1, platelets=77.9,
            hcc=False, cvvhd=False, vhf=False
        )
        
        assert result_above_cutpoint.total_score == 5  # All 4 continuous variables + age triggered
    
    def test_extreme_values(self):
        """Test with extreme but valid values."""
        result_extreme = self.calculator.calculate_score(
            meld=40,    # Maximum MELD
            saps_ii=163, # Maximum SAPS II
            age=80,     # Maximum age
            platelets=10, # Minimum platelets
            hcc=True, cvvhd=True, vhf=True
        )
        
        assert result_extreme.total_score == 8  # Maximum possible
        assert result_extreme.valid == True
    
    def test_all_none_values(self):
        """Test with all None values."""
        result = self.calculator.calculate_score(
            meld=None, saps_ii=None, age=None, platelets=None,
            hcc=None, cvvhd=None, vhf=None
        )
        
        assert result.total_score == 0  # No contributions possible
        assert result.valid == False   # Too much missing data
        assert len(result.warnings) == 8  # All 7 components missing + 1 "too many missing" warning
    
    def test_mixed_none_and_valid(self):
        """Test with mix of None and valid values."""
        result = self.calculator.calculate_score(
            meld=25,      # Valid, triggers +2
            saps_ii=None, # Missing
            age=55,       # Valid, triggers +1
            platelets=None, # Missing
            hcc=True,     # Valid, triggers +1
            cvvhd=None,   # Missing
            vhf=False     # Valid, no trigger
        )
        
        assert result.total_score == 4  # 2+1+1+0
        assert result.valid == False    # 3 missing (>2 threshold)
        assert len(result.warnings) == 4  # 3 missing + 1 "too many missing" warning


class TestIntegration:
    """Integration tests for the complete TRS system."""
    
    def test_end_to_end_workflow(self):
        """Test complete workflow from data to result."""
        # Initialize calculator
        calculator = TRSCalculator()
        
        # Calculate score
        result = calculator.calculate_score(
            meld=25, saps_ii=45, age=55, platelets=70,
            hcc=True, cvvhd=False, vhf=True,
            patient_id="TEST_001"
        )
        
        # Verify result
        assert isinstance(result, TRSResult)
        assert result.valid == True
        assert result.total_score > 0
        
        # Format output
        clinical_output = format_clinical_output(result)
        assert len(clinical_output) > 0
        assert "TRS SCORE" in clinical_output
        
        # Test batch processing
        batch_data = [
            {"meld": 25, "saps_ii": 45, "age": 55, "platelets": 70,
             "hcc": True, "cvvhd": False, "vhf": True},
            {"meld": 15, "saps_ii": 35, "age": 45, "platelets": 100,
             "hcc": False, "cvvhd": False, "vhf": False}
        ]
        
        batch_results = calculator.calculate_batch(batch_data)
        assert len(batch_results) == 2
        assert all(r.valid for r in batch_results)
        
        # Create summary
        summary = create_batch_summary(batch_results)
        assert summary["total_patients"] == 2
        assert summary["valid_calculations"] == 2
    
    def test_constants_consistency(self):
        """Test consistency between constants and implementation."""
        calculator = TRSCalculator()
        
        # Test that all cutpoints are used correctly
        for component, cutpoint in TRS_CUTPOINTS.items():
            info = calculator.get_component_info(component)
            assert info["cutpoint"] == cutpoint
        
        # Test that all points are assigned correctly
        for component, points in TRS_POINTS.items():
            if component in TRS_CUTPOINTS:  # Continuous variables
                info = calculator.get_component_info(component)
                assert info["points"] == points
    
    def test_risk_category_assignment(self):
        """Test that risk categories are assigned correctly."""
        calculator = TRSCalculator()
        
        # Test each risk category
        for category, data in RISK_CATEGORIES.items():
            min_score, max_score = data["range"]
            
            # Test minimum score for category
            # Create a scenario that yields exactly min_score
            if min_score == 0:
                result = calculator.calculate_score(
                    meld=15, saps_ii=35, age=45, platelets=100,
                    hcc=False, cvvhd=False, vhf=False
                )
                assert result.risk_category == category
            
            # Test maximum score for category (if not the highest category)
            if category != "HIGH":
                # This is more complex as we need to construct exact scores
                pass  # Could be implemented with more sophisticated test data generation


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])

