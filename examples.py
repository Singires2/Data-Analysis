"""
Example Usage Demonstrations
Showcase various ways to use the Data Analytics Project
"""

print("="*80)
print("DATA ANALYTICS PROJECT - USAGE EXAMPLES")
print("="*80)

# Example 1: Basic Pipeline Usage
print("\n[Example 1] Using the DataAnalyticsPipeline class")
print("-" * 80)

from src.data_analysis import DataAnalyticsPipeline

# Create pipeline with different datasets
print("\n1a. Analyzing 'tips' dataset:")
pipeline_tips = DataAnalyticsPipeline(dataset_name='tips')
pipeline_tips.load_data()
pipeline_tips.explore_data()
print("\nTips dataset loaded and explored!")

print("\n1b. Analyzing 'iris' dataset:")
pipeline_iris = DataAnalyticsPipeline(dataset_name='iris')
pipeline_iris.load_data()
print("\nIris dataset loaded!")

# Example 2: Data Cleaning
print("\n" + "="*80)
print("[Example 2] Data Cleaning Process")
print("-" * 80)

# Clean the tips data
cleaned_data = pipeline_tips.clean_data()
print(f"\nCleaned data shape: {cleaned_data.shape}")
print(f"Original data shape: {pipeline_tips.df.shape}")

# Example 3: Statistical Analysis
print("\n" + "="*80)
print("[Example 3] Statistical Analysis")
print("-" * 80)

pipeline_tips.exploratory_data_analysis()

# Example 4: SQL Integration
print("\n" + "="*80)
print("[Example 4] SQL Database Operations")
print("-" * 80)

from src.sql_integration import SQLDataExtractor

sql_extractor = SQLDataExtractor()

# Check if database exists
import os
if os.path.exists('data/analytics.db'):
    print("\nDatabase found! Running sample query...")
    
    # Execute a sample query
    query = """
    SELECT category, 
           COUNT(*) as transactions,
           ROUND(AVG(total_amount), 2) as avg_amount
    FROM sales 
    GROUP BY category;
    """
    
    result = sql_extractor.execute_query(query, "Category Summary:")
    print("\nQuery Results:")
    print(result)
else:
    print("\nDatabase not found. Creating sample database...")
    sql_extractor.create_sample_database()
    print("Database created successfully!")

# Example 5: Custom Analysis
print("\n" + "="*80)
print("[Example 5] Custom Data Analysis")
print("-" * 80)

import pandas as pd
import numpy as np

# Access the cleaned data
df = pipeline_tips.df_cleaned

print("\n5a. Custom Calculation - Tip Percentage:")
df['tip_percentage'] = (df['tip'] / df['total_bill'] * 100).round(2)
print(df[['total_bill', 'tip', 'tip_percentage']].head(10))

print("\n5b. Group Analysis - Average Tip by Day and Time:")
group_analysis = df.groupby(['day', 'time'])['tip'].agg(['mean', 'count']).round(2)
print(group_analysis)

print("\n5c. Statistical Insights:")
print(f"Average tip percentage: {df['tip_percentage'].mean():.2f}%")
print(f"Median tip percentage: {df['tip_percentage'].median():.2f}%")
print(f"Tip percentage range: {df['tip_percentage'].min():.2f}% - {df['tip_percentage'].max():.2f}%")

# Example 6: Export Data
print("\n" + "="*80)
print("[Example 6] Exporting Analysis Results")
print("-" * 80)

# Export custom analysis
custom_export_path = 'exports/custom_tip_analysis.csv'
df[['total_bill', 'tip', 'tip_percentage', 'day', 'time', 'size']].to_csv(
    custom_export_path, index=False
)
print(f"\nCustom analysis exported to: {custom_export_path}")

# Example 7: Programmatic Visualization
print("\n" + "="*80)
print("[Example 7] Creating Custom Visualizations")
print("-" * 80)

import matplotlib.pyplot as plt
import seaborn as sns

# Create a custom visualization
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Tip by day
df.groupby('day')['tip'].mean().plot(kind='bar', ax=axes[0], color='steelblue')
axes[0].set_title('Average Tip by Day of Week')
axes[0].set_ylabel('Average Tip ($)')
axes[0].set_xlabel('Day')

# Plot 2: Tip percentage distribution
df['tip_percentage'].hist(bins=30, ax=axes[1], color='coral', edgecolor='black')
axes[1].set_title('Distribution of Tip Percentage')
axes[1].set_xlabel('Tip Percentage (%)')
axes[1].set_ylabel('Frequency')

plt.tight_layout()
plt.savefig('visualizations/custom_tip_analysis.png', dpi=300, bbox_inches='tight')
print("\nCustom visualization saved to: visualizations/custom_tip_analysis.png")
plt.close()

# Example 8: Working with Multiple Datasets
print("\n" + "="*80)
print("[Example 8] Comparing Multiple Datasets")
print("-" * 80)

# Load and compare different datasets
datasets = ['tips', 'iris', 'titanic']
dataset_info = []

for dataset_name in datasets:
    try:
        pipeline = DataAnalyticsPipeline(dataset_name=dataset_name)
        pipeline.load_data()
        
        info = {
            'Dataset': dataset_name,
            'Rows': len(pipeline.df),
            'Columns': len(pipeline.df.columns),
            'Missing Values': pipeline.df.isnull().sum().sum(),
            'Memory (KB)': pipeline.df.memory_usage(deep=True).sum() / 1024
        }
        dataset_info.append(info)
        print(f"✓ Loaded {dataset_name}")
    except Exception as e:
        print(f"✗ Could not load {dataset_name}: {e}")

comparison_df = pd.DataFrame(dataset_info)
print("\nDataset Comparison:")
print(comparison_df.to_string(index=False))

# Summary
print("\n" + "="*80)
print("EXAMPLES COMPLETED")
print("="*80)
print("""
Summary of Examples:
1. Basic pipeline usage with different datasets
2. Data cleaning process demonstration
3. Statistical analysis capabilities
4. SQL database operations
5. Custom data analysis and calculations
6. Exporting results to files
7. Creating custom visualizations
8. Comparing multiple datasets

For more information, see:
- README.md for full documentation
- QUICKSTART.md for getting started
- src/ directory for source code

To run the interactive dashboard:
  streamlit run src/dashboard.py
""")
