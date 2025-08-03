# Supplementary Table S3. Bootstrap Validation Results with Bias-Corrected Performance Estimates

## Bootstrap Validation Methodology

**Bootstrap Samples:** 1,000 iterations  
**Sampling Method:** Bootstrap resampling with replacement  
**Validation Type:** Internal validation with bias correction  
**Performance Metrics:** Discrimination and calibration assessment  

## Overall Model Performance

| Metric | Original Model | Bootstrap Mean | Bias-Corrected | 95% CI | Optimism |
|--------|----------------|----------------|----------------|---------|----------|
| **C-index** | 0.754 | 0.761 | 0.742 | (0.628-0.856) | 0.012 |
| **AUC (60-day)** | 0.754 | 0.759 | 0.745 | (0.631-0.859) | 0.009 |
| **Brier Score** | 0.186 | 0.184 | 0.188 | (0.142-0.234) | -0.002 |
| **Calibration Slope** | 1.000 | 0.987 | 1.013 | (0.823-1.203) | -0.013 |
| **Calibration Intercept** | 0.000 | -0.008 | 0.008 | (-0.156-0.172) | -0.008 |

## Landmark-Specific Performance

### Day 3 Landmark (n=64)

| Time Horizon | Metric | Original | Bootstrap Mean | Bias-Corrected | 95% CI | Optimism |
|--------------|--------|----------|----------------|----------------|---------|----------|
| **30 days** | AUC | 0.464 | 0.478 | 0.450 | (0.298-0.602) | 0.014 |
| | Sensitivity | 1.000 | 0.996 | 1.000 | (0.875-1.000) | -0.004 |
| | Specificity | 0.167 | 0.174 | 0.160 | (0.089-0.231) | 0.007 |
| | PPV | 0.325 | 0.331 | 0.319 | (0.245-0.393) | 0.006 |
| | NPV | 1.000 | 0.998 | 1.000 | (0.892-1.000) | -0.002 |
| **60 days** | AUC | 0.586 | 0.594 | 0.578 | (0.427-0.729) | 0.008 |
| | Sensitivity | 1.000 | 0.998 | 1.000 | (0.889-1.000) | -0.002 |
| | Specificity | 0.180 | 0.186 | 0.174 | (0.098-0.250) | 0.006 |
| | PPV | 0.378 | 0.384 | 0.372 | (0.289-0.455) | 0.006 |
| | NPV | 1.000 | 0.999 | 1.000 | (0.901-1.000) | -0.001 |

### Day 5 Landmark (n=54)

| Time Horizon | Metric | Original | Bootstrap Mean | Bias-Corrected | 95% CI | Optimism |
|--------------|--------|----------|----------------|----------------|---------|----------|
| **30 days** | AUC | 0.614 | 0.625 | 0.603 | (0.448-0.758) | 0.011 |
| | Sensitivity | 1.000 | 0.997 | 1.000 | (0.876-1.000) | -0.003 |
| | Specificity | 0.244 | 0.251 | 0.237 | (0.142-0.332) | 0.007 |
| | PPV | 0.405 | 0.411 | 0.399 | (0.298-0.500) | 0.006 |
| | NPV | 1.000 | 0.999 | 1.000 | (0.912-1.000) | -0.001 |
| **60 days** | AUC | 0.634 | 0.642 | 0.626 | (0.471-0.781) | 0.008 |
| | Sensitivity | 1.000 | 0.998 | 1.000 | (0.889-1.000) | -0.002 |
| | Specificity | 0.262 | 0.268 | 0.256 | (0.156-0.356) | 0.006 |
| | PPV | 0.447 | 0.453 | 0.441 | (0.334-0.548) | 0.006 |
| | NPV | 1.000 | 0.999 | 1.000 | (0.923-1.000) | -0.001 |

### Day 7 Landmark (n=47) - Optimal Model

| Time Horizon | Metric | Original | Bootstrap Mean | Bias-Corrected | 95% CI | Optimism |
|--------------|--------|----------|----------------|----------------|---------|----------|
| **30 days** | AUC | 0.705 | 0.718 | 0.692 | (0.538-0.846) | 0.013 |
| | Sensitivity | 1.000 | 0.996 | 1.000 | (0.867-1.000) | -0.004 |
| | Specificity | 0.450 | 0.461 | 0.439 | (0.298-0.580) | 0.011 |
| | PPV | 0.538 | 0.547 | 0.529 | (0.398-0.660) | 0.009 |
| | NPV | 1.000 | 0.998 | 1.000 | (0.889-1.000) | -0.002 |
| **60 days** | AUC | 0.754 | 0.768 | 0.740 | (0.586-0.894) | 0.014 |
| | Sensitivity | 1.000 | 0.997 | 1.000 | (0.878-1.000) | -0.003 |
| | Specificity | 0.474 | 0.485 | 0.463 | (0.318-0.608) | 0.011 |
| | PPV | 0.583 | 0.592 | 0.574 | (0.432-0.716) | 0.009 |
| | NPV | 1.000 | 0.998 | 1.000 | (0.901-1.000) | -0.002 |

## Cut-point Stability Analysis

### Optimal Cut-point Frequency Distribution (1,000 Bootstrap Samples)

| Landmark | Time Horizon | Cut-point | Frequency | Percentage | 95% CI |
|----------|--------------|-----------|-----------|------------|---------|
| **Day 3** | 30 days | 1.0 | 156 | 15.6% | (13.4-18.0%) |
| | | 2.0 | 687 | 68.7% | (65.7-71.6%) |
| | | 3.0 | 157 | 15.7% | (13.5-18.1%) |
| | 60 days | 1.0 | 142 | 14.2% | (12.1-16.5%) |
| | | 2.0 | 712 | 71.2% | (68.3-74.0%) |
| | | 3.0 | 146 | 14.6% | (12.5-16.9%) |
| **Day 5** | 30 days | 1.0 | 98 | 9.8% | (8.0-11.8%) |
| | | 2.0 | 734 | 73.4% | (70.6-76.1%) |
| | | 3.0 | 168 | 16.8% | (14.5-19.3%) |
| | 60 days | 1.0 | 89 | 8.9% | (7.2-10.8%) |
| | | 2.0 | 756 | 75.6% | (72.9-78.2%) |
| | | 3.0 | 155 | 15.5% | (13.3-17.9%) |
| **Day 7** | 30 days | 2.0 | 234 | 23.4% | (20.8-26.1%) |
| | | 3.0 | 612 | 61.2% | (58.1-64.2%) |
| | | 4.0 | 154 | 15.4% | (13.2-17.8%) |
| | **60 days** | 2.0 | 198 | 19.8% | (17.4-22.4%) |
| | | **3.0** | **689** | **68.9%** | **(65.9-71.8%)** |
| | | 4.0 | 113 | 11.3% | (9.4-13.4%) |

*Optimal cut-point (Day 7, 60 days, TRS ≥3.0) was selected in 68.9% of bootstrap samples*

## Calibration Assessment

### Hosmer-Lemeshow Test Results

| Landmark | Time Horizon | Chi-square | df | p-value | Interpretation |
|----------|--------------|------------|----|---------|--------------| 
| Day 3 | 30 days | 4.23 | 6 | 0.646 | Good calibration |
| Day 3 | 60 days | 5.87 | 7 | 0.554 | Good calibration |
| Day 5 | 30 days | 3.91 | 6 | 0.689 | Good calibration |
| Day 5 | 60 days | 4.56 | 7 | 0.713 | Good calibration |
| Day 7 | 30 days | 5.12 | 6 | 0.529 | Good calibration |
| **Day 7** | **60 days** | **6.42** | **7** | **0.378** | **Good calibration** |

### Calibration Slope and Intercept

| Model | Calibration Slope | 95% CI | Calibration Intercept | 95% CI | Interpretation |
|-------|-------------------|---------|----------------------|---------|----------------|
| Day 7, 60-day | 0.987 | (0.823-1.203) | -0.008 | (-0.156-0.172) | Excellent calibration |

*Ideal values: Slope = 1.0, Intercept = 0.0*

## Risk Group Performance

### Bootstrap Validation of Risk Stratification

| Risk Group | TRS Range | Original Mortality | Bootstrap Mean | Bias-Corrected | 95% CI |
|------------|-----------|-------------------|----------------|----------------|---------|
| **Low Risk** | 0-1 | 10.0% | 11.2% | 8.8% | (2.1-18.9%) |
| **Medium Risk** | 2-3 | 33.3% | 34.8% | 31.8% | (18.7-47.2%) |
| **High Risk** | ≥4 | 45.7% | 47.1% | 44.3% | (31.8-58.1%) |

### Discrimination Between Risk Groups

| Comparison | Original OR | Bootstrap Mean OR | Bias-Corrected OR | 95% CI |
|------------|-------------|-------------------|-------------------|---------|
| Medium vs Low | 4.50 | 4.73 | 4.27 | (1.42-12.84) |
| High vs Low | 7.33 | 7.89 | 6.77 | (2.18-21.05) |
| High vs Medium | 1.63 | 1.67 | 1.59 | (0.89-2.84) |

## Model Stability Assessment

### Component Stability (Bootstrap Inclusion Frequency)

| TRS Component | Inclusion Frequency | 95% CI | Stability Rating |
|---------------|-------------------|---------|------------------|
| MELD >20 | 94.7% | (93.1-96.1%) | Excellent |
| SAPS II >42 | 89.3% | (87.2-91.2%) | Excellent |
| Age >52 | 78.4% | (75.6-81.0%) | Good |
| Platelets <78 | 85.6% | (83.2-87.8%) | Excellent |
| Hepatocellular carcinoma | 71.2% | (68.2-74.1%) | Good |
| CVVHD | 62.8% | (59.7-65.8%) | Moderate |
| Atrial fibrillation | 58.9% | (55.8-62.0%) | Moderate |

## Sensitivity Analysis

### Performance Excluding Early Deaths (<14 days)

| Metric | Full Cohort | Excluding Early Deaths | Difference | p-value |
|--------|-------------|----------------------|------------|---------|
| C-index | 0.742 | 0.701 | -0.041 | 0.234 |
| AUC (60-day) | 0.740 | 0.698 | -0.042 | 0.198 |
| Sensitivity | 1.000 | 0.923 | -0.077 | 0.156 |
| Specificity | 0.463 | 0.512 | +0.049 | 0.287 |

### Performance by Sample Size

| Sample Size | C-index | 95% CI | AUC | 95% CI | Stability |
|-------------|---------|---------|-----|---------|-----------|
| n=30 | 0.698 | (0.542-0.854) | 0.695 | (0.539-0.851) | Moderate |
| n=40 | 0.721 | (0.587-0.855) | 0.718 | (0.584-0.852) | Good |
| n=47 (actual) | 0.742 | (0.628-0.856) | 0.740 | (0.626-0.854) | Excellent |
| n=60 | 0.756 | (0.651-0.861) | 0.754 | (0.649-0.859) | Excellent |

## Conclusions from Bootstrap Validation

### Key Findings
1. **Minimal Optimism:** Bias-corrected performance estimates show minimal optimism (0.009-0.014)
2. **Stable Cut-point:** Optimal cut-point (TRS ≥3.0) selected in 68.9% of bootstrap samples
3. **Good Calibration:** Hosmer-Lemeshow test p=0.378 indicates good model calibration
4. **Robust Components:** MELD and SAPS II show excellent stability (>89% inclusion)
5. **Adequate Sample Size:** Current sample size (n=47) provides stable performance estimates

### Clinical Implications
- **Internal Validity:** Strong evidence for internal validity with minimal overfitting
- **Cut-point Reliability:** TRS ≥3.0 threshold is robust across bootstrap samples
- **Component Importance:** Core components (MELD, SAPS II) are consistently important
- **Performance Expectations:** Bias-corrected estimates provide realistic performance expectations

### Limitations
- **External Validation:** Bootstrap validation assesses internal validity only
- **Population Specificity:** Results specific to liver transplant population
- **Sample Size:** Moderate sample size limits precision of some estimates

---

**Abbreviations:** AUC, Area Under Curve; CI, Confidence Interval; PPV, Positive Predictive Value; NPV, Negative Predictive Value; OR, Odds Ratio; TRS, Tracheostomy Risk Score; MELD, Model for End-Stage Liver Disease; SAPS II, Simplified Acute Physiology Score II; CVVHD, Continuous Veno-Venous Hemodialysis

