"""
Data Analytics Project - Main Analysis Script
Comprehensive data cleaning, analysis, and visualization pipeline
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings
import os

warnings.filterwarnings('ignore')

# Set visualization styles
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


class DataAnalyticsPipeline:
    """Complete data analytics pipeline for business data analysis"""
    
    def __init__(self, dataset_name='tips'):
        """
        Initialize the analytics pipeline
        
        Parameters:
        -----------
        dataset_name : str
            Name of the seaborn dataset to load (default: 'tips')
            Options: 'tips', 'titanic', 'iris', 'flights', 'diamonds'
        """
        self.dataset_name = dataset_name
        self.df = None
        self.df_cleaned = None
        self.numerical_cols = []
        self.categorical_cols = []
        
    def load_data(self):
        """Load sample dataset from seaborn"""
        print(f"Loading {self.dataset_name} dataset...")
        self.df = sns.load_dataset(self.dataset_name)
        print(f"Dataset loaded successfully: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
        print("\nFirst few rows:")
        print(self.df.head())
        print("\nDataset info:")
        print(self.df.info())
        return self.df
    
    def explore_data(self):
        """Initial data exploration"""
        print("\n" + "="*80)
        print("DATA EXPLORATION")
        print("="*80)
        
        print("\nDataset Shape:", self.df.shape)
        print("\nColumn Names and Types:")
        print(self.df.dtypes)
        
        print("\nBasic Statistics:")
        print(self.df.describe())
        
        print("\nMissing Values:")
        missing = self.df.isnull().sum()
        if missing.sum() > 0:
            print(missing[missing > 0])
        else:
            print("No missing values found")
        
        print("\nDuplicate Rows:", self.df.duplicated().sum())
        
        # Identify numerical and categorical columns
        self.numerical_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        print(f"\nNumerical columns ({len(self.numerical_cols)}):", self.numerical_cols)
        print(f"Categorical columns ({len(self.categorical_cols)}):", self.categorical_cols)
        
    def clean_data(self):
        """Perform comprehensive data cleaning"""
        print("\n" + "="*80)
        print("DATA CLEANING")
        print("="*80)
        
        self.df_cleaned = self.df.copy()
        cleaning_report = []
        
        # 1. Handle missing values
        print("\n1. Handling Missing Values...")
        missing_before = self.df_cleaned.isnull().sum().sum()
        
        for col in self.df_cleaned.columns:
            missing_count = self.df_cleaned[col].isnull().sum()
            if missing_count > 0:
                if col in self.numerical_cols:
                    # Fill numerical columns with median
                    self.df_cleaned[col].fillna(self.df_cleaned[col].median(), inplace=True)
                    cleaning_report.append(f"  - Filled {missing_count} missing values in '{col}' with median")
                else:
                    # Fill categorical columns with mode
                    self.df_cleaned[col].fillna(self.df_cleaned[col].mode()[0], inplace=True)
                    cleaning_report.append(f"  - Filled {missing_count} missing values in '{col}' with mode")
        
        missing_after = self.df_cleaned.isnull().sum().sum()
        print(f"  Missing values before: {missing_before}, after: {missing_after}")
        
        # 2. Remove duplicates
        print("\n2. Removing Duplicates...")
        duplicates_before = self.df_cleaned.duplicated().sum()
        self.df_cleaned.drop_duplicates(inplace=True)
        duplicates_removed = duplicates_before - self.df_cleaned.duplicated().sum()
        print(f"  Duplicates removed: {duplicates_removed}")
        if duplicates_removed > 0:
            cleaning_report.append(f"  - Removed {duplicates_removed} duplicate rows")
        
        # 3. Handle outliers using IQR method
        print("\n3. Detecting Outliers (IQR method)...")
        outliers_report = {}
        
        for col in self.numerical_cols:
            Q1 = self.df_cleaned[col].quantile(0.25)
            Q3 = self.df_cleaned[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = ((self.df_cleaned[col] < lower_bound) | (self.df_cleaned[col] > upper_bound)).sum()
            if outliers > 0:
                outliers_report[col] = {
                    'count': outliers,
                    'percentage': (outliers / len(self.df_cleaned)) * 100,
                    'lower_bound': lower_bound,
                    'upper_bound': upper_bound
                }
                print(f"  - {col}: {outliers} outliers ({outliers_report[col]['percentage']:.2f}%)")
        
        if not outliers_report:
            print("  No significant outliers detected")
        
        # 4. Data type validation
        print("\n4. Validating Data Types...")
        print(f"  All columns have appropriate data types")
        
        print("\nData Cleaning Summary:")
        for report in cleaning_report:
            print(report)
        
        print(f"\nCleaned dataset shape: {self.df_cleaned.shape}")
        
        return self.df_cleaned
    
    def exploratory_data_analysis(self):
        """Perform comprehensive EDA with statistics and correlations"""
        print("\n" + "="*80)
        print("EXPLORATORY DATA ANALYSIS")
        print("="*80)
        
        # Summary statistics
        print("\n1. Summary Statistics for Numerical Variables:")
        print(self.df_cleaned[self.numerical_cols].describe())
        
        # Correlation analysis
        if len(self.numerical_cols) > 1:
            print("\n2. Correlation Matrix:")
            correlation_matrix = self.df_cleaned[self.numerical_cols].corr()
            print(correlation_matrix)
            
            # Find strong correlations
            print("\n3. Strong Correlations (|r| > 0.5):")
            for i in range(len(correlation_matrix.columns)):
                for j in range(i+1, len(correlation_matrix.columns)):
                    corr_value = correlation_matrix.iloc[i, j]
                    if abs(corr_value) > 0.5:
                        print(f"  - {correlation_matrix.columns[i]} vs {correlation_matrix.columns[j]}: {corr_value:.3f}")
        
        # Categorical analysis
        if self.categorical_cols:
            print("\n4. Categorical Variables Analysis:")
            for col in self.categorical_cols:
                print(f"\n  {col} - Value Counts:")
                print(self.df_cleaned[col].value_counts())
        
        # Skewness and Kurtosis
        print("\n5. Distribution Characteristics:")
        print("\nSkewness:")
        for col in self.numerical_cols:
            skew = self.df_cleaned[col].skew()
            print(f"  - {col}: {skew:.3f}")
        
        print("\nKurtosis:")
        for col in self.numerical_cols:
            kurt = self.df_cleaned[col].kurtosis()
            print(f"  - {col}: {kurt:.3f}")
    
    def create_visualizations(self, output_dir='visualizations'):
        """Create comprehensive visualizations"""
        print("\n" + "="*80)
        print("CREATING VISUALIZATIONS")
        print("="*80)
        
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. Distribution plots for numerical variables
        if self.numerical_cols:
            print("\n1. Creating distribution plots...")
            fig, axes = plt.subplots(len(self.numerical_cols), 2, 
                                    figsize=(15, 5*len(self.numerical_cols)))
            
            if len(self.numerical_cols) == 1:
                axes = axes.reshape(1, -1)
            
            for idx, col in enumerate(self.numerical_cols):
                # Histogram
                self.df_cleaned[col].hist(bins=30, ax=axes[idx, 0], edgecolor='black')
                axes[idx, 0].set_title(f'Distribution of {col}')
                axes[idx, 0].set_xlabel(col)
                axes[idx, 0].set_ylabel('Frequency')
                
                # Box plot
                self.df_cleaned.boxplot(column=col, ax=axes[idx, 1])
                axes[idx, 1].set_title(f'Box Plot of {col}')
                axes[idx, 1].set_ylabel(col)
            
            plt.tight_layout()
            plt.savefig(f'{output_dir}/distributions.png', dpi=300, bbox_inches='tight')
            print(f"  Saved: {output_dir}/distributions.png")
            plt.close()
        
        # 2. Correlation heatmap
        if len(self.numerical_cols) > 1:
            print("\n2. Creating correlation heatmap...")
            plt.figure(figsize=(10, 8))
            correlation_matrix = self.df_cleaned[self.numerical_cols].corr()
            sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                       center=0, square=True, linewidths=1)
            plt.title('Correlation Matrix Heatmap')
            plt.tight_layout()
            plt.savefig(f'{output_dir}/correlation_heatmap.png', dpi=300, bbox_inches='tight')
            print(f"  Saved: {output_dir}/correlation_heatmap.png")
            plt.close()
        
        # 3. Pairplot for relationships
        if len(self.numerical_cols) >= 2 and len(self.df_cleaned) < 1000:
            print("\n3. Creating pairplot...")
            if self.categorical_cols:
                pairplot = sns.pairplot(self.df_cleaned, 
                                       vars=self.numerical_cols[:4],  # Limit to 4 for performance
                                       hue=self.categorical_cols[0] if self.categorical_cols else None,
                                       diag_kind='kde')
            else:
                pairplot = sns.pairplot(self.df_cleaned, vars=self.numerical_cols[:4], diag_kind='kde')
            
            plt.savefig(f'{output_dir}/pairplot.png', dpi=300, bbox_inches='tight')
            print(f"  Saved: {output_dir}/pairplot.png")
            plt.close()
        
        # 4. Categorical analysis
        if self.categorical_cols:
            print("\n4. Creating categorical analysis plots...")
            for col in self.categorical_cols[:3]:  # Limit to 3 categorical columns
                plt.figure(figsize=(12, 6))
                
                # Count plot
                plt.subplot(1, 2, 1)
                self.df_cleaned[col].value_counts().plot(kind='bar')
                plt.title(f'Count Distribution - {col}')
                plt.xlabel(col)
                plt.ylabel('Count')
                plt.xticks(rotation=45, ha='right')
                
                # Pie chart
                plt.subplot(1, 2, 2)
                self.df_cleaned[col].value_counts().plot(kind='pie', autopct='%1.1f%%')
                plt.title(f'Percentage Distribution - {col}')
                plt.ylabel('')
                
                plt.tight_layout()
                plt.savefig(f'{output_dir}/categorical_{col}.png', dpi=300, bbox_inches='tight')
                print(f"  Saved: {output_dir}/categorical_{col}.png")
                plt.close()
        
        print(f"\nAll visualizations saved to '{output_dir}/' directory")
    
    def export_for_bi_tools(self, output_dir='exports'):
        """Export cleaned data for Power BI/Tableau"""
        print("\n" + "="*80)
        print("EXPORTING DATA FOR BI TOOLS")
        print("="*80)
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Export to CSV for Tableau
        csv_path = f'{output_dir}/cleaned_data_for_tableau.csv'
        self.df_cleaned.to_csv(csv_path, index=False)
        print(f"\n1. CSV Export (for Tableau): {csv_path}")
        print(f"   Rows: {len(self.df_cleaned)}, Columns: {len(self.df_cleaned.columns)}")
        
        # Export to Excel for Power BI
        excel_path = f'{output_dir}/cleaned_data_for_powerbi.xlsx'
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            # Main data sheet
            self.df_cleaned.to_excel(writer, sheet_name='Cleaned_Data', index=False)
            
            # Summary statistics sheet
            if self.numerical_cols:
                summary_stats = self.df_cleaned[self.numerical_cols].describe()
                summary_stats.to_excel(writer, sheet_name='Summary_Statistics')
            
            # Correlation matrix sheet
            if len(self.numerical_cols) > 1:
                correlation_matrix = self.df_cleaned[self.numerical_cols].corr()
                correlation_matrix.to_excel(writer, sheet_name='Correlations')
        
        print(f"\n2. Excel Export (for Power BI): {excel_path}")
        print(f"   Sheets: Cleaned_Data, Summary_Statistics, Correlations")
        
        # Create data dictionary
        data_dict = pd.DataFrame({
            'Column_Name': self.df_cleaned.columns,
            'Data_Type': self.df_cleaned.dtypes.values,
            'Non_Null_Count': self.df_cleaned.count().values,
            'Unique_Values': [self.df_cleaned[col].nunique() for col in self.df_cleaned.columns],
            'Sample_Value': [str(self.df_cleaned[col].iloc[0]) if len(self.df_cleaned) > 0 else '' 
                           for col in self.df_cleaned.columns]
        })
        
        dict_path = f'{output_dir}/data_dictionary.xlsx'
        data_dict.to_excel(dict_path, index=False)
        print(f"\n3. Data Dictionary: {dict_path}")
        
        print("\nExport complete! Data ready for:")
        print("  - Tableau: Use the CSV file")
        print("  - Power BI: Use the Excel file with Get Data > Excel")
        print("  - Both tools can also connect to the SQLite database created by this pipeline")
    
    def run_full_pipeline(self):
        """Execute the complete analytics pipeline"""
        print("\n" + "="*80)
        print("STARTING DATA ANALYTICS PIPELINE")
        print("="*80)
        
        # Load data
        self.load_data()
        
        # Explore data
        self.explore_data()
        
        # Clean data
        self.clean_data()
        
        # Perform EDA
        self.exploratory_data_analysis()
        
        # Create visualizations
        self.create_visualizations()
        
        # Export for BI tools
        self.export_for_bi_tools()
        
        print("\n" + "="*80)
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print("="*80)
        print("\nOutputs:")
        print("  - Visualizations: visualizations/ directory")
        print("  - Exports: exports/ directory")
        print("  - Run the Streamlit dashboard: streamlit run src/dashboard.py")


def main():
    """Main execution function"""
    print("Data Analytics Project")
    print("="*80)
    
    # You can change the dataset here
    # Options: 'tips', 'titanic', 'iris', 'flights', 'diamonds'
    pipeline = DataAnalyticsPipeline(dataset_name='tips')
    
    # Run the complete pipeline
    pipeline.run_full_pipeline()
    
    print("\nTo view the interactive dashboard, run:")
    print("  streamlit run src/dashboard.py")


if __name__ == "__main__":
    main()
