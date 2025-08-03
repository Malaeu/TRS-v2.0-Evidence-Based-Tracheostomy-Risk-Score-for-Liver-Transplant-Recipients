# Supplementary Table S1. Detailed TRS Calculation Methodology and Scoring System

## TRS (Tracheostomy Risk Score) Components and Scoring

| Component | Variable | Cut-point | Points Assigned | Rationale | Optimal Cut-point Analysis Results |
|-----------|----------|-----------|-----------------|-----------|-----------------------------------|
| **Liver Function** | MELD Score | >20 | 2 | Primary indicator of liver dysfunction severity | Sensitivity: 78.6%, Specificity: 69.1%, Youden Index: 0.477 |
| **Physiological Severity** | SAPS II Score | >42 | 1 | Multi-organ dysfunction assessment | Sensitivity: 75.0%, Specificity: 65.5%, Youden Index: 0.405 |
| **Demographics** | Age | >52 years | 1 | Decreased physiological reserve | Sensitivity: 67.9%, Specificity: 58.2%, Youden Index: 0.261 |
| **Hematological** | Platelet Count | <78 ×10³/μL | 1 | Coagulopathy and liver dysfunction | Sensitivity: 71.4%, Specificity: 63.6%, Youden Index: 0.350 |
| **Malignancy** | Hepatocellular Carcinoma | Present | 1 | Oncological burden and prognosis | Categorical variable, OR: 2.89 (95% CI: 1.12-7.45) |
| **Renal Support** | CVVHD | Present | 1 | Multi-organ failure indicator | Categorical variable, OR: 1.78 (95% CI: 0.71-4.47) |
| **Cardiac Comorbidity** | Atrial Fibrillation | Present | 1 | Cardiovascular comorbidity | Categorical variable, OR: 1.95 (95% CI: 0.65-5.84) |

## Detailed Scoring Methodology

### Step 1: Data Collection
- **Timing:** All variables assessed at ICU Day 7 (landmark time point)
- **Laboratory Values:** Most recent values within 24 hours of assessment
- **Clinical Variables:** Current status at time of assessment

### Step 2: Cut-point Application
For each continuous variable, apply the optimal cut-point derived from ROC analysis:

```
IF MELD > 20 THEN MELD_points = 2 ELSE MELD_points = 0
IF SAPS_II > 42 THEN SAPS_points = 1 ELSE SAPS_points = 0  
IF Age > 52 THEN Age_points = 1 ELSE Age_points = 0
IF Platelets < 78 THEN PLT_points = 1 ELSE PLT_points = 0
```

For categorical variables:
```
IF HCC = Present THEN HCC_points = 1 ELSE HCC_points = 0
IF CVVHD = Present THEN CVVHD_points = 1 ELSE CVVHD_points = 0
IF VHF = Present THEN VHF_points = 1 ELSE VHF_points = 0
```

### Step 3: Total Score Calculation
```
TRS_Total = MELD_points + SAPS_points + Age_points + PLT_points + HCC_points + CVVHD_points + VHF_points
```

**Score Range:** 0-8 points

### Step 4: Risk Stratification
| TRS Score | Risk Category | 90-Day Mortality Rate | Clinical Action |
|-----------|---------------|----------------------|-----------------|
| 0-1 | Low Risk | 10.0% | Standard weaning protocol |
| 2-3 | Medium Risk | 33.3% | Enhanced monitoring |
| ≥4 | High Risk | 45.7% | Consider early tracheostomy |

## Statistical Validation of Cut-points

### Optimal Cut-point Analysis Methodology
- **Method:** Receiver Operating Characteristic (ROC) analysis
- **Optimization Criterion:** Youden Index (Sensitivity + Specificity - 1)
- **Outcome:** 90-day mortality
- **Validation:** Bootstrap resampling (n=1000)

### Performance Metrics for Each Component

| Variable | AUC (95% CI) | Optimal Cut-point | Sensitivity | Specificity | PPV | NPV | LR+ | LR- |
|----------|--------------|-------------------|-------------|-------------|-----|-----|-----|-----|
| MELD Score | 0.692 (0.578-0.806) | >20 | 0.786 | 0.691 | 0.524 | 0.884 | 2.54 | 0.31 |
| SAPS II | 0.703 (0.591-0.815) | >42 | 0.750 | 0.655 | 0.488 | 0.857 | 2.17 | 0.38 |
| Age | 0.631 (0.512-0.750) | >52 | 0.679 | 0.582 | 0.422 | 0.800 | 1.62 | 0.55 |
| Platelets | 0.675 (0.558-0.792) | <78 | 0.714 | 0.636 | 0.455 | 0.833 | 1.96 | 0.45 |

*AUC: Area Under Curve; PPV: Positive Predictive Value; NPV: Negative Predictive Value; LR+: Positive Likelihood Ratio; LR-: Negative Likelihood Ratio*

## Point Assignment Rationale

### Evidence-Based Weighting
The point assignments were derived from the relative strength of association with 90-day mortality:

1. **MELD Score (2 points):** 
   - Highest individual AUC (0.692)
   - Strong biological plausibility as primary liver function indicator
   - Hazard Ratio: 3.24 (95% CI: 1.58-6.63)

2. **All Other Variables (1 point each):**
   - Similar individual AUCs (0.63-0.70 range)
   - Comparable hazard ratios (1.5-2.9 range)
   - Equal weighting maintains simplicity while preserving discriminative ability

### Validation of Scoring System
- **Internal Validation:** Bootstrap bias-corrected C-index: 0.742 (95% CI: 0.628-0.856)
- **Calibration:** Hosmer-Lemeshow test p=0.378 (good calibration)
- **Discrimination:** Significant separation between risk groups (p<0.001)

## Clinical Implementation Guidelines

### Daily Assessment Protocol
1. **Timing:** Assess TRS daily starting ICU Day 3
2. **Decision Point:** Primary assessment at ICU Day 7
3. **Reassessment:** If clinical deterioration occurs
4. **Documentation:** Record TRS in medical record

### Quality Assurance
- **Training:** Ensure staff familiar with calculation
- **Automation:** Consider electronic health record integration
- **Monitoring:** Track implementation and outcomes
- **Validation:** Periodic review of cut-point performance

### Missing Data Handling
- **Laboratory Values:** Use most recent available within 48 hours
- **Clinical Variables:** Confirm current status with clinical team
- **Incomplete Data:** Do not calculate TRS if >2 components missing

## Limitations and Considerations

### Score Limitations
- **Population Specific:** Derived from liver transplant recipients
- **Single Center:** External validation needed
- **Retrospective:** Prospective validation required

### Clinical Considerations
- **Clinical Judgment:** TRS supplements but does not replace clinical assessment
- **Contraindications:** Consider absolute contraindications to tracheostomy
- **Patient Preferences:** Include in shared decision-making process
- **Multidisciplinary:** Involve surgical, anesthesia, and nursing teams

---

*Abbreviations: TRS, Tracheostomy Risk Score; MELD, Model for End-Stage Liver Disease; SAPS II, Simplified Acute Physiology Score II; HCC, Hepatocellular Carcinoma; CVVHD, Continuous Veno-Venous Hemodialysis; VHF, Atrial Fibrillation; ROC, Receiver Operating Characteristic; AUC, Area Under Curve; CI, Confidence Interval; OR, Odds Ratio; ICU, Intensive Care Unit*

