# Supplementary Methods. Detailed Statistical Methodology and Software Specifications

## Overview

This supplementary methods section provides comprehensive details of the statistical methodology, software implementations, and analytical approaches used in the development and validation of the Tracheostomy Risk Score (TRS). The methodology follows current best practices for clinical prediction model development and validation as outlined in the TRIPOD (Transparent Reporting of a multivariable prediction model for Individual Prognosis or Diagnosis) statement.

## Software Environment and Packages

### Primary Analysis Platform
**Software:** Python 3.11.0  
**Operating System:** Ubuntu 22.04 LTS  
**Hardware:** Standard computational environment with adequate memory for bootstrap resampling  

### Core Python Libraries
- **pandas (v1.5.3):** Data manipulation and analysis
- **numpy (v1.24.3):** Numerical computing and array operations
- **scipy (v1.10.1):** Statistical functions and hypothesis testing
- **scikit-learn (v1.2.2):** Machine learning algorithms and model evaluation
- **matplotlib (v3.7.1):** Data visualization and plotting
- **seaborn (v0.12.2):** Statistical data visualization

### Specialized Statistical Libraries
- **lifelines (v0.27.4):** Survival analysis and Kaplan-Meier estimation
- **sksurv (v0.19.0):** Survival analysis with scikit-learn compatibility
- **statsmodels (v0.14.0):** Statistical modeling and hypothesis testing

### Reproducibility Settings
```python
import numpy as np
import random
np.random.seed(42)
random.seed(42)
```

All analyses were conducted with fixed random seeds to ensure reproducibility of results.

## Data Preprocessing and Quality Control

### Missing Data Assessment
Missing data patterns were systematically evaluated using the following approach:

1. **Missingness Patterns:** Assessed using missing data heatmaps and pattern analysis
2. **Missing Data Mechanisms:** Evaluated for Missing Completely at Random (MCAR), Missing at Random (MAR), and Missing Not at Random (MNAR) patterns
3. **Imputation Strategy:** Multiple imputation was not performed due to low missingness rates (<5% for all variables)
4. **Complete Case Analysis:** Patients with missing data for >2 TRS components were excluded from analysis

### Data Validation Procedures
```python
def validate_data_quality(df):
    """
    Comprehensive data quality validation
    """
    # Check for duplicate patient IDs
    assert df['patient_id'].nunique() == len(df), "Duplicate patient IDs detected"
    
    # Validate date ranges
    assert (df['icu_admission_date'] <= df['death_date']).all(), "Invalid date sequences"
    
    # Check laboratory value ranges
    assert (df['meld_score'] >= 6).all(), "MELD scores below minimum threshold"
    assert (df['saps_score'] >= 0).all(), "Negative SAPS II scores detected"
    
    # Validate survival times
    assert (df['survival_time'] > 0).all(), "Non-positive survival times"
    
    return True
```

### Variable Transformations
No transformations were applied to continuous variables to maintain clinical interpretability. All variables were used in their original scale as commonly employed in clinical practice.

## Optimal Cut-point Analysis Methodology

### Receiver Operating Characteristic (ROC) Analysis
The optimal cut-point analysis was performed using a systematic approach to maximize the Youden Index for each continuous variable.

#### Mathematical Framework
For a continuous variable X and binary outcome Y, the optimal cut-point c* is defined as:

```
c* = argmax[Sensitivity(c) + Specificity(c) - 1]
```

Where:
- Sensitivity(c) = P(X ≥ c | Y = 1)
- Specificity(c) = P(X < c | Y = 0)
- Youden Index = Sensitivity + Specificity - 1

#### Implementation
```python
from sklearn.metrics import roc_curve
import numpy as np

def find_optimal_cutpoint(y_true, y_scores):
    """
    Find optimal cut-point using Youden Index
    """
    fpr, tpr, thresholds = roc_curve(y_true, y_scores)
    
    # Calculate Youden Index for each threshold
    youden_index = tpr - fpr
    
    # Find optimal threshold
    optimal_idx = np.argmax(youden_index)
    optimal_threshold = thresholds[optimal_idx]
    optimal_sensitivity = tpr[optimal_idx]
    optimal_specificity = 1 - fpr[optimal_idx]
    
    return {
        'threshold': optimal_threshold,
        'sensitivity': optimal_sensitivity,
        'specificity': optimal_specificity,
        'youden_index': youden_index[optimal_idx]
    }
```

### Bootstrap Confidence Intervals
Confidence intervals for optimal cut-points were calculated using bootstrap resampling:

```python
def bootstrap_cutpoint_ci(y_true, y_scores, n_bootstrap=1000, alpha=0.05):
    """
    Calculate bootstrap confidence intervals for optimal cut-points
    """
    bootstrap_cutpoints = []
    
    for i in range(n_bootstrap):
        # Bootstrap sample
        indices = np.random.choice(len(y_true), size=len(y_true), replace=True)
        y_boot = y_true[indices]
        scores_boot = y_scores[indices]
        
        # Find optimal cut-point for bootstrap sample
        result = find_optimal_cutpoint(y_boot, scores_boot)
        bootstrap_cutpoints.append(result['threshold'])
    
    # Calculate confidence intervals
    lower_ci = np.percentile(bootstrap_cutpoints, 100 * alpha/2)
    upper_ci = np.percentile(bootstrap_cutpoints, 100 * (1 - alpha/2))
    
    return lower_ci, upper_ci
```

## Landmark Analysis Implementation

### Theoretical Foundation
Landmark analysis eliminates immortal time bias by fixing specific time points for analysis and excluding patients who experience the outcome before the landmark. This approach ensures that all patients in the analysis have had an equal opportunity to experience the outcome.

### Mathematical Formulation
For landmark time τ, the analysis includes only patients who:
1. Survive beyond time τ: T > τ
2. Remain at risk at time τ
3. Have complete covariate information at time τ

The survival function from landmark τ is:
```
S(t|τ) = P(T > t | T > τ, X(τ))
```

Where X(τ) represents covariates measured at landmark time τ.

### Implementation Details
```python
def create_landmark_dataset(df, landmark_day):
    """
    Create landmark dataset for specified landmark day
    """
    # Filter patients surviving to landmark
    landmark_df = df[df['survival_time'] > landmark_day].copy()
    
    # Adjust survival times from landmark
    landmark_df['landmark_survival_time'] = (
        landmark_df['survival_time'] - landmark_day
    )
    
    # Ensure minimum follow-up time
    landmark_df = landmark_df[landmark_df['landmark_survival_time'] > 0]
    
    # Update event indicator for landmark analysis
    landmark_df['landmark_event'] = np.where(
        (landmark_df['death_90d'] == 1) & 
        (landmark_df['survival_time'] > landmark_day), 1, 0
    )
    
    return landmark_df
```

### Landmark Selection Rationale
Landmark time points (days 3, 5, and 7) were selected based on:
1. **Clinical Relevance:** Typical timeframes for tracheostomy consideration
2. **Sample Size:** Adequate number of patients surviving to each landmark
3. **Event Rate:** Sufficient events for meaningful analysis
4. **Literature Precedent:** Commonly used landmarks in critical care research

## Time-Dependent ROC Analysis

### Methodology
Time-dependent ROC analysis accounts for the censored nature of survival data and provides more accurate estimates of diagnostic performance compared to traditional ROC analysis applied to binary outcomes.

### Mathematical Framework
For survival time T, censoring indicator δ, and marker M, the time-dependent sensitivity and specificity at time t are:

```
Sensitivity(c,t) = P(M > c | T ≤ t, δ = 1)
Specificity(c,t) = P(M ≤ c | T > t)
```

The time-dependent AUC is:
```
AUC(t) = P(M_i > M_j | T_i ≤ t < T_j, δ_i = 1)
```

### Implementation
```python
def time_dependent_roc(survival_times, event_indicator, scores, time_point):
    """
    Calculate time-dependent ROC curve
    """
    # Define cases and controls at time_point
    cases = (survival_times <= time_point) & (event_indicator == 1)
    controls = survival_times > time_point
    
    if cases.sum() == 0 or controls.sum() == 0:
        return None
    
    # Calculate ROC curve
    case_scores = scores[cases]
    control_scores = scores[controls]
    
    # Combine and sort scores
    all_scores = np.concatenate([case_scores, control_scores])
    thresholds = np.unique(all_scores)
    
    tpr_values = []
    fpr_values = []
    
    for threshold in thresholds:
        tpr = np.mean(case_scores >= threshold)
        fpr = np.mean(control_scores >= threshold)
        tpr_values.append(tpr)
        fpr_values.append(fpr)
    
    return np.array(fpr_values), np.array(tpr_values), thresholds
```

### Confidence Intervals for Time-Dependent AUC
Bootstrap confidence intervals for time-dependent AUC were calculated using the following approach:

```python
def bootstrap_time_dependent_auc(survival_times, event_indicator, scores, 
                                time_point, n_bootstrap=1000):
    """
    Bootstrap confidence intervals for time-dependent AUC
    """
    bootstrap_aucs = []
    
    for i in range(n_bootstrap):
        # Bootstrap sample
        indices = np.random.choice(len(survival_times), 
                                 size=len(survival_times), replace=True)
        
        surv_boot = survival_times[indices]
        event_boot = event_indicator[indices]
        scores_boot = scores[indices]
        
        # Calculate AUC for bootstrap sample
        fpr, tpr, _ = time_dependent_roc(surv_boot, event_boot, 
                                       scores_boot, time_point)
        if fpr is not None:
            auc = np.trapz(tpr, fpr)
            bootstrap_aucs.append(auc)
    
    return np.array(bootstrap_aucs)
```

## TRS Score Development and Validation

### Score Construction Methodology
The TRS was constructed using a points-based system where points were assigned based on the strength of association with the outcome.

#### Point Assignment Algorithm
```python
def assign_points_based_on_hazard_ratio(hazard_ratio):
    """
    Assign points based on hazard ratio magnitude
    """
    if hazard_ratio >= 2.0:
        return 2
    elif hazard_ratio >= 1.5:
        return 1
    else:
        return 0
```

#### Score Calculation
```python
def calculate_trs_score(patient_data):
    """
    Calculate TRS score for a patient
    """
    score = 0
    
    # MELD score component (2 points if >20)
    if patient_data['meld'] > 20:
        score += 2
    
    # SAPS II component (1 point if >42)
    if patient_data['saps_ii'] > 42:
        score += 1
    
    # Age component (1 point if >52)
    if patient_data['age'] > 52:
        score += 1
    
    # Platelet component (1 point if <78)
    if patient_data['platelets'] < 78:
        score += 1
    
    # Comorbidity components (1 point each)
    score += patient_data['hcc']  # Hepatocellular carcinoma
    score += patient_data['cvvhd']  # Continuous veno-venous hemodialysis
    score += patient_data['vhf']  # Atrial fibrillation
    
    return score
```

### Internal Validation Methodology

#### Bootstrap Validation Procedure
Internal validation was performed using bootstrap resampling to assess optimism and provide bias-corrected performance estimates.

```python
def bootstrap_validation(df, n_bootstrap=1000):
    """
    Comprehensive bootstrap validation
    """
    original_performance = calculate_model_performance(df)
    bootstrap_performances = []
    
    for i in range(n_bootstrap):
        # Create bootstrap sample
        bootstrap_sample = df.sample(n=len(df), replace=True)
        
        # Develop model on bootstrap sample
        bootstrap_model = develop_trs_model(bootstrap_sample)
        
        # Test on bootstrap sample (apparent performance)
        apparent_performance = test_model(bootstrap_model, bootstrap_sample)
        
        # Test on original sample (test performance)
        test_performance = test_model(bootstrap_model, df)
        
        # Calculate optimism
        optimism = apparent_performance - test_performance
        bootstrap_performances.append({
            'apparent': apparent_performance,
            'test': test_performance,
            'optimism': optimism
        })
    
    # Calculate bias-corrected performance
    mean_optimism = np.mean([p['optimism'] for p in bootstrap_performances])
    bias_corrected = original_performance - mean_optimism
    
    return {
        'original': original_performance,
        'bias_corrected': bias_corrected,
        'optimism': mean_optimism,
        'bootstrap_results': bootstrap_performances
    }
```

#### Calibration Assessment
Model calibration was assessed using the Hosmer-Lemeshow goodness-of-fit test and calibration plots.

```python
def hosmer_lemeshow_test(y_true, y_prob, n_bins=10):
    """
    Hosmer-Lemeshow goodness-of-fit test
    """
    # Create bins based on predicted probabilities
    bin_boundaries = np.percentile(y_prob, np.linspace(0, 100, n_bins + 1))
    bin_boundaries[0] = -np.inf
    bin_boundaries[-1] = np.inf
    
    # Assign observations to bins
    bin_indices = np.digitize(y_prob, bin_boundaries) - 1
    
    chi_square = 0
    for i in range(n_bins):
        bin_mask = bin_indices == i
        if bin_mask.sum() == 0:
            continue
            
        observed_events = y_true[bin_mask].sum()
        expected_events = y_prob[bin_mask].sum()
        observed_non_events = bin_mask.sum() - observed_events
        expected_non_events = bin_mask.sum() - expected_events
        
        # Chi-square contribution
        if expected_events > 0:
            chi_square += (observed_events - expected_events)**2 / expected_events
        if expected_non_events > 0:
            chi_square += (observed_non_events - expected_non_events)**2 / expected_non_events
    
    # Calculate p-value
    from scipy.stats import chi2
    p_value = 1 - chi2.cdf(chi_square, df=n_bins - 2)
    
    return chi_square, p_value
```

## Survival Analysis Methodology

### Kaplan-Meier Estimation
Survival curves were estimated using the Kaplan-Meier method with the following implementation:

```python
def kaplan_meier_estimator(survival_times, event_indicator):
    """
    Kaplan-Meier survival function estimation
    """
    # Sort by survival time
    sorted_indices = np.argsort(survival_times)
    sorted_times = survival_times[sorted_indices]
    sorted_events = event_indicator[sorted_indices]
    
    # Find unique event times
    unique_times = np.unique(sorted_times[sorted_events == 1])
    
    survival_function = []
    current_survival = 1.0
    
    for t in unique_times:
        # Number at risk just before time t
        at_risk = np.sum(sorted_times >= t)
        
        # Number of events at time t
        events = np.sum((sorted_times == t) & (sorted_events == 1))
        
        # Update survival probability
        if at_risk > 0:
            current_survival *= (1 - events / at_risk)
        
        survival_function.append((t, current_survival))
    
    return survival_function
```

### Log-Rank Test Implementation
Group comparisons were performed using the log-rank test:

```python
def log_rank_test(group1_times, group1_events, group2_times, group2_events):
    """
    Log-rank test for comparing survival curves
    """
    # Combine data
    all_times = np.concatenate([group1_times, group2_times])
    all_events = np.concatenate([group1_events, group2_events])
    all_groups = np.concatenate([np.zeros(len(group1_times)), 
                                np.ones(len(group2_times))])
    
    # Find unique event times
    unique_times = np.unique(all_times[all_events == 1])
    
    observed_minus_expected = 0
    variance = 0
    
    for t in unique_times:
        # At risk in each group
        at_risk_1 = np.sum((all_times >= t) & (all_groups == 0))
        at_risk_2 = np.sum((all_times >= t) & (all_groups == 1))
        total_at_risk = at_risk_1 + at_risk_2
        
        # Events in each group
        events_1 = np.sum((all_times == t) & (all_events == 1) & (all_groups == 0))
        events_2 = np.sum((all_times == t) & (all_events == 1) & (all_groups == 1))
        total_events = events_1 + events_2
        
        if total_at_risk > 0 and total_events > 0:
            # Expected events in group 1
            expected_1 = (at_risk_1 * total_events) / total_at_risk
            
            # Contribution to test statistic
            observed_minus_expected += events_1 - expected_1
            
            # Contribution to variance
            if total_at_risk > 1:
                variance += (at_risk_1 * at_risk_2 * total_events * 
                           (total_at_risk - total_events)) / (total_at_risk**2 * (total_at_risk - 1))
    
    # Calculate test statistic
    if variance > 0:
        test_statistic = observed_minus_expected**2 / variance
        from scipy.stats import chi2
        p_value = 1 - chi2.cdf(test_statistic, df=1)
    else:
        test_statistic = 0
        p_value = 1
    
    return test_statistic, p_value
```

## Model Performance Metrics

### Discrimination Measures
Model discrimination was assessed using multiple metrics:

#### C-index (Concordance Index)
```python
def concordance_index(survival_times, event_indicator, risk_scores):
    """
    Calculate Harrell's C-index
    """
    concordant_pairs = 0
    total_pairs = 0
    
    for i in range(len(survival_times)):
        for j in range(i + 1, len(survival_times)):
            # Only consider pairs where one patient has an event
            if event_indicator[i] == 1 and survival_times[i] < survival_times[j]:
                total_pairs += 1
                if risk_scores[i] > risk_scores[j]:
                    concordant_pairs += 1
            elif event_indicator[j] == 1 and survival_times[j] < survival_times[i]:
                total_pairs += 1
                if risk_scores[j] > risk_scores[i]:
                    concordant_pairs += 1
    
    return concordant_pairs / total_pairs if total_pairs > 0 else 0.5
```

#### Integrated Brier Score
```python
def integrated_brier_score(survival_times, event_indicator, predicted_probs, 
                          time_points):
    """
    Calculate integrated Brier score
    """
    brier_scores = []
    
    for t in time_points:
        # True outcomes at time t
        y_true = (survival_times <= t) & (event_indicator == 1)
        
        # Predicted probabilities at time t
        y_pred = predicted_probs
        
        # Brier score at time t
        brier_t = np.mean((y_true - y_pred)**2)
        brier_scores.append(brier_t)
    
    # Integrate over time
    integrated_brier = np.trapz(brier_scores, time_points)
    
    return integrated_brier, brier_scores
```

### Clinical Utility Measures

#### Net Benefit Calculation
```python
def net_benefit(y_true, y_pred_prob, threshold):
    """
    Calculate net benefit for decision curve analysis
    """
    # True positive rate
    tp_rate = np.mean(y_true[y_pred_prob >= threshold])
    
    # False positive rate
    fp_rate = np.mean(~y_true[y_pred_prob >= threshold])
    
    # Proportion classified as positive
    positive_rate = np.mean(y_pred_prob >= threshold)
    
    # Net benefit
    net_benefit = tp_rate * positive_rate - fp_rate * positive_rate * (threshold / (1 - threshold))
    
    return net_benefit
```

## Quality Assurance and Reproducibility

### Code Review and Testing
All analytical code underwent systematic review and testing:

1. **Unit Testing:** Individual functions tested with known inputs and expected outputs
2. **Integration Testing:** Complete analytical pipeline tested with simulated data
3. **Validation Testing:** Results compared with established statistical software (R)

### Documentation Standards
All code was documented following PEP 8 standards with comprehensive docstrings:

```python
def example_function(parameter1, parameter2):
    """
    Brief description of function purpose.
    
    Parameters
    ----------
    parameter1 : type
        Description of parameter1
    parameter2 : type
        Description of parameter2
    
    Returns
    -------
    return_type
        Description of return value
    
    Examples
    --------
    >>> example_function(value1, value2)
    expected_output
    """
    # Implementation
    pass
```

### Version Control and Reproducibility
- **Git Version Control:** All code versioned with detailed commit messages
- **Environment Management:** Complete package versions documented
- **Seed Management:** Fixed random seeds for all stochastic procedures
- **Data Provenance:** Complete audit trail of data transformations

## Limitations and Assumptions

### Statistical Assumptions
1. **Proportional Hazards:** Assumed for Cox regression models (tested using Schoenfeld residuals)
2. **Independence:** Observations assumed independent (appropriate for single-center study)
3. **Missing Data:** Assumed missing completely at random (MCAR) for variables with <5% missingness
4. **Linearity:** Linear relationship assumed for continuous variables in logistic regression

### Methodological Limitations
1. **Internal Validation Only:** Bootstrap validation provides internal validity assessment only
2. **Single Center:** Results may not generalize to other institutions
3. **Retrospective Design:** Potential for unmeasured confounding
4. **Sample Size:** Limited power for subgroup analyses

### Computational Limitations
1. **Bootstrap Iterations:** Limited to 1,000 iterations due to computational constraints
2. **Precision:** Floating-point precision limitations in probability calculations
3. **Memory:** Large datasets may require memory optimization

## Conclusion

This comprehensive methodological framework ensures the reliability, validity, and reproducibility of the TRS development and validation. The combination of rigorous statistical methods, comprehensive validation procedures, and transparent reporting provides a solid foundation for clinical implementation and future research.

---

**Software Availability:** All analysis code is available upon reasonable request and with appropriate institutional approvals.

**Computational Resources:** Analyses were performed on standard computational hardware with no special requirements beyond the specified software environment.

**Data Sharing:** Deidentified data may be available for research purposes subject to institutional review board approval and data sharing agreements.

