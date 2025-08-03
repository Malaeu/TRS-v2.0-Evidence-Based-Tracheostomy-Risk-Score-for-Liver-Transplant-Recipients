# =Ê FIGURES CATALOG - TRS v2.0 Research Project

## Overview
Comprehensive catalog of all visualizations generated for the TRS v2.0 research project. All figures are publication quality (300 DPI).

## =Á Main Figures (figures/main/)

### 1. Decision Curve Analysis (dca_corrected.png)
- **Purpose**: Clinical utility demonstration across threshold probabilities
- **Content**: Net benefit curves for TRS vs. treat-all vs. treat-none strategies
- **Key insight**: TRS provides superior clinical benefit 10-70% threshold range

### 2. Risk Stratification (risk_stratification.png)  
- **Purpose**: TRS score distribution and risk categories
- **Content**: Bar chart with patient distribution, mortality rates by category
- **Key insight**: Clear separation of risk groups with distinct mortality patterns

### 3. Time-Dependent ROC Curves (time_dependent_roc_curves.png)
- **Purpose**: Discriminative performance across time horizons
- **Content**: ROC curves for 30, 60, 90-day mortality with AUC values
- **Key insight**: Consistent excellent performance across all time points

### 4. TRS Distribution (trs_distribution.png)
- **Purpose**: Population-level TRS score distribution
- **Content**: Histogram with mean, median, quartile markers
- **Key insight**: Good discrimination across the full score range

## =Á Supplementary Figures (figures/supplementary/)

### S1. Calibration Assessment (figure_S1_calibration_CLEAN.png)
- **Purpose**: Model calibration across risk deciles
- **Content**: Observed vs. predicted mortality with confidence intervals
- **Key insight**: Excellent calibration with minimal deviation

### S2. Kaplan-Meier Curves (figure_S2_km_corrected.png)
- **Purpose**: Survival analysis by TRS risk categories
- **Content**: KM curves with confidence intervals and risk tables
- **Key insight**: Clear separation validating risk stratification

### S3. ROC Analysis Matrix (figure_S3_roc_CLEAN.png)
- **Purpose**: Comprehensive ROC analysis across scenarios
- **Content**: Multiple ROC curves for different landmark timepoints
- **Key insight**: Day 7 landmark shows optimal performance

## <¨ Technical Specifications

- **Resolution**: 300 DPI (publication quality)
- **Format**: PNG (lossless compression)
- **Font**: Arial/Helvetica family
- **Quality Control**:  Verified for accuracy and clarity

## =Ê Summary

| Category | Main | Supplementary | Total |
|----------|------|---------------|-------|
| **ROC Analysis** | 1 | 1 | 2 |
| **Survival Analysis** | 0 | 1 | 1 |
| **Clinical Utility** | 1 | 0 | 1 |
| **Calibration** | 0 | 1 | 1 |
| **Distribution** | 2 | 0 | 2 |
| **Total** | **4** | **3** | **7** |

---

*All figures generated using validated Python scripts in `src/plotting/`*  
*Last updated: August 2025*