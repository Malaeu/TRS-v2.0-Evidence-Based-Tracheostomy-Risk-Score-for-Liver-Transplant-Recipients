#!/usr/bin/env python3
"""
Corrected Decision Curve Analysis Plot for TRS Model
Fixes:
1. Red "Treat All" line goes below 0 (no clipping)
2. Updated annotation text to "10-55%"
3. Added Y-axis label "Net Benefit (patients per 100)"
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def calculate_net_benefit(threshold, prevalence=0.39, sensitivity=1.0, specificity=0.474):
    """
    Calculate net benefit for decision curve analysis
    
    Args:
        threshold: Threshold probability
        prevalence: Disease prevalence (39% mortality in our cohort)
        sensitivity: Model sensitivity (100% for TRS ≥3)
        specificity: Model specificity (47.4% for TRS ≥3)
    
    Returns:
        Net benefit value (can be negative)
    """
    if threshold == 0:
        return prevalence
    if threshold == 1:
        return 0
    
    # True positives and false positives per 100 patients
    tp = prevalence * sensitivity * 100
    fp = (1 - prevalence) * (1 - specificity) * 100
    
    # Net benefit = (TP - FP * (threshold/(1-threshold))) / 100
    net_benefit = (tp - fp * (threshold / (1 - threshold))) / 100
    
    return net_benefit

def create_corrected_dca_plot():
    """Create corrected Decision Curve Analysis plot"""
    
    # Create threshold range
    thresholds = np.linspace(0.01, 0.99, 100)
    
    # Calculate net benefits
    trs_benefits = []
    treat_all_benefits = []
    treat_none_benefits = []
    
    for threshold in thresholds:
        # TRS Model net benefit
        trs_nb = calculate_net_benefit(threshold, prevalence=0.39, 
                                     sensitivity=1.0, specificity=0.474)
        trs_benefits.append(trs_nb)
        
        # Treat All strategy (no clipping - can go negative!)
        treat_all_nb = 0.39 - (1 - 0.39) * (threshold / (1 - threshold))
        treat_all_benefits.append(treat_all_nb)
        
        # Treat None strategy (always 0)
        treat_none_benefits.append(0.0)
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plot curves
    ax.plot(thresholds, trs_benefits, 'b-', linewidth=3, label='TRS Model')
    ax.plot(thresholds, treat_all_benefits, 'r--', linewidth=2, label='Treat All')
    ax.plot(thresholds, treat_none_benefits, 'k:', linewidth=2, label='Treat None')
    
    # Formatting
    ax.set_xlabel('Threshold Probability', fontsize=14, fontweight='bold')
    ax.set_ylabel('Net Benefit (patients per 100)', fontsize=14, fontweight='bold')  # Fixed Y-axis label
    ax.set_title('Decision Curve Analysis for TRS Model', fontsize=16, fontweight='bold')
    
    # Set axis limits
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.1, 0.4)  # Allow negative values to show
    
    # Add grid
    ax.grid(True, alpha=0.3)
    
    # Add legend
    ax.legend(loc='upper right', fontsize=12)
    
    # Add corrected annotation
    ax.annotate('TRS provides clinical benefit\nacross threshold probabilities 10-55%',  # Fixed text
                xy=(0.35, 0.15), xytext=(0.6, 0.27),
                arrowprops=dict(arrowstyle='->', color='blue', lw=1.5),
                fontsize=11, ha='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.7))
    
    # Tight layout
    plt.tight_layout()
    
    return fig

if __name__ == "__main__":
    # Create corrected plot
    fig = create_corrected_dca_plot()
    
    # Save to figures directory with high DPI
    output_path = Path("figures/dca_corrected.png")
    fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    
    print(f"✅ Corrected Decision Curve Analysis saved to: {output_path}")
    print("🔧 Fixes applied:")
    print("   1. Red 'Treat All' line now goes below 0 (no clipping)")
    print("   2. Updated annotation to '10-55%'")
    print("   3. Added Y-axis label 'Net Benefit (patients per 100)'")
    
    plt.show()

