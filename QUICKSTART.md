# Quick Start Guide

This guide will help you get started with the Data Analytics Project in minutes.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. **Clone the repository** (if you haven't already):
```bash
git clone https://github.com/Singires2/Data-Analysis.git
cd Data-Analysis
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Usage Options

### Option 1: Run Everything at Once (Recommended for first time)

```bash
python main.py --all
```

This will:
- Run the complete data analysis pipeline
- Create visualizations
- Set up the SQL database
- Export data for BI tools

**Output locations:**
- `visualizations/` - All generated charts and plots
- `exports/` - Data files for Power BI and Tableau
- `data/` - SQLite database

### Option 2: Run Individual Components

**Data Analysis Only:**
```bash
python main.py --analysis
```

**SQL Integration Only:**
```bash
python main.py --sql
```

**Interactive Dashboard:**
```bash
python main.py --dashboard
```

Or directly:
```bash
streamlit run src/dashboard.py
```

### Option 3: Run Scripts Directly

**Main Analysis:**
```bash
python src/data_analysis.py
```

**SQL Demo:**
```bash
python src/sql_integration.py
```

## What You Get

After running the pipeline, you'll have:

1. **Static Visualizations** (in `visualizations/`):
   - Distribution plots
   - Correlation heatmaps
   - Pair plots
   - Categorical analysis charts

2. **BI-Ready Exports** (in `exports/`):
   - `cleaned_data_for_tableau.csv` - Ready for Tableau import
   - `cleaned_data_for_powerbi.xlsx` - Ready for Power BI import
   - `data_dictionary.xlsx` - Data schema documentation
   - Various CSV exports from SQL queries

3. **SQL Database** (in `data/`):
   - `analytics.db` - SQLite database with sample data
   - Can be connected to BI tools directly

## Connecting to BI Tools

### Power BI

1. Open Power BI Desktop
2. Click "Get Data" → "Excel" or "More" → "Database" → "SQLite"
3. For Excel: Select `exports/cleaned_data_for_powerbi.xlsx`
4. For SQLite: Select `data/analytics.db`

### Tableau

1. Open Tableau
2. Click "Connect" → "Text file" or "More" → "SQLite"
3. For CSV: Select `exports/cleaned_data_for_tableau.csv`
4. For SQLite: Select `data/analytics.db`

## Interactive Dashboard Features

When you run the dashboard, you can:

- **Explore Data**: View dataset overview and statistics
- **Analyze Distributions**: Interactive histograms and box plots
- **Study Correlations**: Dynamic correlation heatmaps
- **Examine Relationships**: Scatter plots with trend lines
- **Analyze Categories**: Bar charts and pie charts
- **Query Database**: Execute custom SQL queries
- **Export Results**: Download data and query results

## Customization

### Use Your Own Data

Edit `src/data_analysis.py` and modify the dataset:

```python
# Change this line
pipeline = DataAnalyticsPipeline(dataset_name='tips')

# To load your own CSV
pipeline.df = pd.read_csv('your_data.csv')
```

### Change Visualizations

Edit the `create_visualizations()` method in `src/data_analysis.py` to customize charts.

### Add SQL Queries

Add your queries to `sql_queries/data_extraction_queries.sql` or create new SQL files.

## Troubleshooting

### Import Errors

If you get import errors, ensure all packages are installed:
```bash
pip install -r requirements.txt
```

### Streamlit Not Starting

Try running with explicit python:
```bash
python -m streamlit run src/dashboard.py
```

### Database Not Found

Run the SQL integration first:
```bash
python src/sql_integration.py
```

## Next Steps

1. **Explore the Dashboard**: Run `python main.py --dashboard` to see interactive visualizations
2. **Review SQL Queries**: Check `sql_queries/data_extraction_queries.sql` for examples
3. **Export to BI Tools**: Use files in `exports/` directory with Power BI or Tableau
4. **Customize Analysis**: Modify scripts in `src/` to analyze your own data

## Getting Help

For detailed documentation, see [README.md](README.md)

For issues or questions, please open an issue in the repository.

---

**Happy Analyzing! 📊**
