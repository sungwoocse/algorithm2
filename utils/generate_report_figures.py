import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Experimental results data (Updated)
datasets = ['test15', 'a280', 'xql662', 'kz9976', 'mona-lisa100K']
cities = [15, 280, 662, 9976, 100000]

# Tour costs (Updated with new experiment results)
mst_costs = [559.44, 3575.45, 3648.01, 1457917.44, 8328201.67]
held_karp_costs = [559.44, None, None, None, None]  # Only for small instances
proposed_costs = [559.44, 3148.11, 3244.81, 1346903.56, 6886142.58]

# Runtime (seconds) (Updated with new experiment results)
mst_times = [0.000, 0.044, 0.045, 21.070, 3300.1]
held_karp_times = [2.585, None, None, None, None]
proposed_times = [0.000, 0.008, 0.032, 10.282, 218.1]

# Calculate improvement percentages
improvements = []
speedups = []
for i in range(len(datasets)):
    if mst_costs[i] and proposed_costs[i]:
        improvement = ((mst_costs[i] - proposed_costs[i]) / mst_costs[i]) * 100
        improvements.append(improvement)
        speedup = mst_times[i] / proposed_times[i] if proposed_times[i] > 0 else 1
        speedups.append(speedup)
    else:
        improvements.append(0)
        speedups.append(1)

def generate_performance_table():
    """Generate LaTeX table for performance comparison"""
    table_data = {
        'Dataset': datasets,
        'Cities': cities,
        'MST Cost': [f"{cost:.2f}" if cost else "N/A" for cost in mst_costs],
        'Proposed Cost': [f"{cost:.2f}" if cost else "N/A" for cost in proposed_costs],
        'Improvement (%)': [f"{imp:.1f}" if imp > 0 else "0.0" for imp in improvements],
        'MST Time (s)': [f"{time:.3f}" if time else "N/A" for time in mst_times],
        'Proposed Time (s)': [f"{time:.3f}" if time else "N/A" for time in proposed_times],
        'Speedup': [f"{sp:.1f}×" if sp > 1 else "1.0×" for sp in speedups]
    }
    
    df = pd.DataFrame(table_data)
    
    # Generate LaTeX table
    latex_table = """\\begin{table}[h]
\\centering
\\caption{Performance Comparison Across Datasets}
\\label{tab:performance}
\\begin{tabular}{|l|r|r|r|r|r|r|r|}
\\hline
\\textbf{Dataset} & \\textbf{Cities} & \\textbf{MST Cost} & \\textbf{Proposed Cost} & \\textbf{Improv.} & \\textbf{MST Time} & \\textbf{Proposed Time} & \\textbf{Speedup} \\\\
\\hline"""
    
    for _, row in df.iterrows():
        latex_table += f"\n{row['Dataset']} & {row['Cities']} & {row['MST Cost']} & {row['Proposed Cost']} & {row['Improvement (%)']}\\% & {row['MST Time (s)']} & {row['Proposed Time (s)']} & {row['Speedup']} \\\\"
    
    latex_table += """
\\hline
\\end{tabular}
\\end{table}"""
    
    return latex_table

def generate_quality_improvement_chart():
    """Generate bar chart for solution quality improvements"""
    plt.figure(figsize=(10, 6))
    
    # Filter out datasets with improvements
    valid_datasets = [datasets[i] for i in range(len(datasets)) if improvements[i] > 0]
    valid_improvements = [improvements[i] for i in range(len(improvements)) if improvements[i] > 0]
    
    bars = plt.bar(valid_datasets, valid_improvements, color=['#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
    
    plt.title('Solution Quality Improvement Over MST Approximation', fontsize=14, fontweight='bold')
    plt.xlabel('Dataset', fontsize=12)
    plt.ylabel('Improvement (%)', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar, value in zip(bars, valid_improvements):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, 
                f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('quality_improvement.png', dpi=300, bbox_inches='tight')
    plt.savefig('quality_improvement.pdf', bbox_inches='tight')
    plt.show()

def generate_runtime_comparison_chart():
    """Generate runtime comparison chart"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Chart 1: Runtime comparison for all datasets
    x = np.arange(len(datasets))
    width = 0.35
    
    ax1.bar(x - width/2, mst_times, width, label='MST', color='#ff7f0e', alpha=0.8)
    ax1.bar(x + width/2, proposed_times, width, label='Hybrid Algorithm', color='#1f77b4', alpha=0.8)
    
    ax1.set_xlabel('Dataset')
    ax1.set_ylabel('Runtime (seconds)')
    ax1.set_title('Runtime Comparison')
    ax1.set_xticks(x)
    ax1.set_xticklabels(datasets, rotation=45)
    ax1.legend()
    ax1.set_yscale('log')  # Log scale for better visualization
    ax1.grid(True, alpha=0.3)
    
    # Chart 2: Speedup factors
    valid_speedups = [speedups[i] for i in range(len(speedups)) if speedups[i] > 1]
    valid_datasets_speedup = [datasets[i] for i in range(len(datasets)) if speedups[i] > 1]
    
    bars2 = ax2.bar(valid_datasets_speedup, valid_speedups, color='#2ca02c', alpha=0.8)
    ax2.set_xlabel('Dataset')
    ax2.set_ylabel('Speedup Factor (×)')
    ax2.set_title('Runtime Speedup Over MST')
    ax2.grid(True, alpha=0.3)
    
    # Add value labels
    for bar, value in zip(bars2, valid_speedups):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, 
                f'{value:.1f}×', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('runtime_comparison.png', dpi=300, bbox_inches='tight')
    plt.savefig('runtime_comparison.pdf', bbox_inches='tight')
    plt.show()

def generate_scalability_chart():
    """Generate scalability analysis chart"""
    plt.figure(figsize=(10, 6))
    
    # Plot tour costs vs number of cities
    plt.loglog(cities, mst_costs, 'o-', label='MST Approximation', linewidth=2, markersize=8)
    plt.loglog(cities, proposed_costs, 's-', label='Hybrid Algorithm', linewidth=2, markersize=8)
    
    plt.xlabel('Number of Cities', fontsize=12)
    plt.ylabel('Tour Cost', fontsize=12)
    plt.title('Algorithm Scalability: Tour Cost vs Problem Size', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    
    # Annotate key points
    for i, (x, y1, y2) in enumerate(zip(cities, mst_costs, proposed_costs)):
        if i > 0:  # Skip test15 as it's too small to see improvement clearly
            improvement = ((y1 - y2) / y1) * 100
            plt.annotate(f'{improvement:.1f}% better', 
                        xy=(x, y2), xytext=(x*0.7, y2*0.8),
                        arrowprops=dict(arrowstyle='->', color='red', alpha=0.7),
                        fontsize=9, color='red')
    
    plt.tight_layout()
    plt.savefig('scalability_analysis.png', dpi=300, bbox_inches='tight')
    plt.savefig('scalability_analysis.pdf', bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    print("Generating performance table...")
    latex_table = generate_performance_table()
    
    # Save table to file
    with open('performance_table.tex', 'w') as f:
        f.write(latex_table)
    
    print("LaTeX table saved to performance_table.tex")
    
    print("\nGenerating charts...")
    generate_quality_improvement_chart()
    generate_runtime_comparison_chart() 
    generate_scalability_chart()
    
    print("\nAll figures generated successfully!")
    print("Files created:")
    print("- performance_table.tex")
    print("- quality_improvement.png/pdf")
    print("- runtime_comparison.png/pdf") 
    print("- scalability_analysis.png/pdf") 