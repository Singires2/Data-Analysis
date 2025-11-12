# Data Analytics Project

Comprehensive Python-based data analytics project for cleaning, analyzing, and visualizing business data. This project demonstrates end-to-end data analysis workflow with interactive dashboards, SQL integration, and BI tool exports.

## 🚀 Features

- **Data Loading**: Load data from multiple sources (Seaborn datasets, SQL databases)
- **Data Cleaning**: Handle missing values, outliers, and duplicates
- **Exploratory Data Analysis**: Summary statistics, correlations, and distributions
- **Visualizations**: Static plots (Matplotlib/Seaborn) and interactive charts (Plotly)
- **SQL Integration**: Sample database creation and SQL query demonstrations
- **Interactive Dashboard**: Streamlit-based dashboard with real-time data exploration
- **BI Tool Export**: Export data for Power BI and Tableau
- **Machine Learning Ready**: Uses scikit-learn for advanced analytics

## 📋 Requirements

- Python 3.8+
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- plotly
- streamlit
- sqlalchemy
- openpyxl

## 🔧 Installation

1. Clone this repository:
```bash
git clone https://github.com/Singires2/Data-Analysis.git
cd Data-Analysis
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## 📊 Usage

### 1. Run Complete Data Analysis Pipeline

Execute the main analysis script to perform data loading, cleaning, EDA, and visualization:

```bash
python src/data_analysis.py
```

This will:
- Load sample data from Seaborn
- Clean and preprocess the data
- Generate summary statistics and correlations
- Create visualizations (saved to `visualizations/` directory)
- Export data for BI tools (saved to `exports/` directory)

### 2. SQL Data Extraction

Create a sample SQLite database and demonstrate SQL queries:

```bash
python src/sql_integration.py
```

This will:
- Create a SQLite database at `data/analytics.db`
- Populate it with sample sales data
- Demonstrate various SQL queries
- Create database views for common analyses
- Export query results to CSV files

### 3. Interactive Dashboard

Launch the Streamlit dashboard for interactive data exploration:

```bash
streamlit run src/dashboard.py
```

Dashboard features:
- **Overview**: Dataset statistics and preview
- **Statistics**: Distribution analysis with histograms and box plots
- **Correlations**: Interactive correlation heatmap
- **Relationships**: Scatter plots with trend lines
- **Categorical Analysis**: Bar charts and pie charts
- **Time Series**: Temporal analysis and trends
- **SQL Queries**: Execute custom SQL queries on the database

Access the dashboard at: `http://localhost:8501`

## 📁 Project Structure

```
Data-Analysis/
├── data/                          # Data storage
│   └── analytics.db              # SQLite database (generated)
├── exports/                       # Exported data for BI tools
│   ├── cleaned_data_for_tableau.csv
│   ├── cleaned_data_for_powerbi.xlsx
│   ├── data_dictionary.xlsx
│   ├── category_performance.csv
│   ├── top_customers.csv
│   └── daily_sales_summary.csv
├── sql_queries/                   # SQL query examples
│   └── data_extraction_queries.sql
├── src/                          # Source code
│   ├── data_analysis.py         # Main analysis pipeline
│   ├── sql_integration.py       # SQL database integration
│   └── dashboard.py             # Streamlit dashboard
├── visualizations/               # Generated visualizations
│   ├── distributions.png
│   ├── correlation_heatmap.png
│   ├── pairplot.png
│   └── categorical_*.png
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🎯 Key Components

### Data Analysis Pipeline (`data_analysis.py`)

The main pipeline includes:
- **Data Loading**: Load datasets from Seaborn or custom sources
- **Data Exploration**: Initial data profiling and quality assessment
- **Data Cleaning**: 
  - Handle missing values (median for numerical, mode for categorical)
  - Remove duplicate records
  - Detect outliers using IQR method
- **Exploratory Data Analysis**:
  - Descriptive statistics
  - Correlation analysis
  - Distribution characteristics (skewness, kurtosis)
- **Visualizations**:
  - Distribution plots (histograms and box plots)
  - Correlation heatmaps
  - Pair plots for relationships
  - Categorical analysis charts

### SQL Integration (`sql_integration.py`)

SQL capabilities:
- Create sample SQLite database with realistic data
- Demonstrate various SQL query patterns:
  - Basic data extraction
  - Aggregations and grouping
  - Filtering and sorting
  - Window functions
  - Data quality checks
- Create database views for common analyses
- Export query results to CSV

### Interactive Dashboard (`dashboard.py`)

Streamlit dashboard features:
- **Multiple Data Sources**: Load from Seaborn datasets or SQL database
- **Interactive Visualizations**: Plotly charts with zoom, pan, and hover
- **Real-time Analysis**: Dynamic filtering and exploration
- **SQL Query Interface**: Execute custom queries and download results
- **Export Capabilities**: Download data and visualizations

## 🔄 Integration with BI Tools

### Power BI

1. Open Power BI Desktop
2. Click "Get Data" → "Excel" or "SQLite"
3. Navigate to `exports/cleaned_data_for_powerbi.xlsx` or `data/analytics.db`
4. Load the data and create visualizations

### Tableau

1. Open Tableau
2. Click "Connect" → "Text file" or "SQLite"
3. Navigate to `exports/cleaned_data_for_tableau.csv` or `data/analytics.db`
4. Drag tables to the canvas and start visualizing

## 📈 Example Analyses

The project includes examples of:
- Sales performance analysis by category
- Customer segmentation and behavior
- Time series trend analysis
- Product performance metrics
- Statistical correlations and relationships

## 🛠️ Customization

### Using Your Own Data

Modify `data_analysis.py` to load your own dataset:

```python
# Instead of loading from seaborn
# df = sns.load_dataset('tips')

# Load from CSV
df = pd.read_csv('your_data.csv')

# Or load from SQL
import sqlite3
conn = sqlite3.connect('your_database.db')
df = pd.read_sql_query("SELECT * FROM your_table", conn)
```

### Adding Custom SQL Queries

Add your queries to `sql_queries/data_extraction_queries.sql` or create new query files.

### Extending the Dashboard

Modify `src/dashboard.py` to add new analysis pages or visualizations.

## 📝 SQL Query Examples

The project includes comprehensive SQL examples in `sql_queries/data_extraction_queries.sql`:

1. Basic data extraction
2. Aggregated sales by category
3. Top performing products
4. Customer purchase analysis
5. Monthly sales trends
6. Data quality detection
7. Performance comparisons

## 🎓 Learning Outcomes

This project demonstrates:
- Python data analysis best practices
- Data cleaning and preprocessing techniques
- Statistical analysis and correlation studies
- Data visualization principles
- SQL database operations
- Interactive dashboard development
- BI tool integration
- End-to-end analytics pipeline

## 🤝 Contributing

Feel free to fork this repository and submit pull requests for improvements.

## 📄 License

This project is open source and available for educational purposes.

## 📧 Contact

For questions or suggestions, please open an issue in the repository.

---

**Happy Analyzing! 📊**
