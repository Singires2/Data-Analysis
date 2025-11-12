"""
Interactive Data Analytics Dashboard using Streamlit and Plotly
Provides interactive visualizations and data exploration capabilities
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import sqlite3
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure page
st.set_page_config(
    page_title="Data Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_data
def load_data(dataset_name='tips'):
    """Load data from seaborn datasets"""
    try:
        df = sns.load_dataset(dataset_name)
        return df
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None


@st.cache_data
def load_sql_data(db_path='data/analytics.db'):
    """Load data from SQLite database"""
    try:
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            df = pd.read_sql_query("SELECT * FROM sales", conn)
            conn.close()
            return df
        else:
            return None
    except Exception as e:
        st.error(f"Error loading from database: {e}")
        return None


def show_overview(df):
    """Display dataset overview"""
    st.header("📋 Dataset Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Rows", f"{len(df):,}")
    with col2:
        st.metric("Total Columns", len(df.columns))
    with col3:
        st.metric("Missing Values", df.isnull().sum().sum())
    with col4:
        st.metric("Duplicate Rows", df.duplicated().sum())
    
    st.subheader("Sample Data")
    st.dataframe(df.head(10), use_container_width=True)
    
    st.subheader("Data Types")
    dtype_df = pd.DataFrame({
        'Column': df.columns,
        'Data Type': df.dtypes.values,
        'Non-Null Count': df.count().values,
        'Unique Values': [df[col].nunique() for col in df.columns]
    })
    st.dataframe(dtype_df, use_container_width=True)


def show_statistics(df):
    """Display statistical analysis"""
    st.header("📊 Statistical Analysis")
    
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if numerical_cols:
        st.subheader("Summary Statistics")
        st.dataframe(df[numerical_cols].describe(), use_container_width=True)
        
        # Distribution analysis
        st.subheader("Distribution Analysis")
        selected_col = st.selectbox("Select column for distribution analysis", numerical_cols)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Histogram with Plotly
            fig_hist = px.histogram(df, x=selected_col, nbins=30,
                                   title=f"Distribution of {selected_col}",
                                   labels={selected_col: selected_col},
                                   color_discrete_sequence=['#636EFA'])
            fig_hist.update_layout(showlegend=False)
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            # Box plot with Plotly
            fig_box = px.box(df, y=selected_col,
                           title=f"Box Plot of {selected_col}",
                           color_discrete_sequence=['#EF553B'])
            st.plotly_chart(fig_box, use_container_width=True)
        
        # Skewness and Kurtosis
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Skewness", f"{df[selected_col].skew():.3f}")
        with col2:
            st.metric("Kurtosis", f"{df[selected_col].kurtosis():.3f}")


def show_correlations(df):
    """Display correlation analysis"""
    st.header("🔗 Correlation Analysis")
    
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numerical_cols) > 1:
        # Correlation matrix
        corr_matrix = df[numerical_cols].corr()
        
        # Interactive heatmap
        fig = px.imshow(corr_matrix,
                       labels=dict(color="Correlation"),
                       x=corr_matrix.columns,
                       y=corr_matrix.columns,
                       color_continuous_scale='RdBu_r',
                       aspect="auto",
                       title="Correlation Matrix")
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
        
        # Strong correlations
        st.subheader("Strong Correlations (|r| > 0.5)")
        strong_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.5:
                    strong_corr.append({
                        'Variable 1': corr_matrix.columns[i],
                        'Variable 2': corr_matrix.columns[j],
                        'Correlation': corr_value
                    })
        
        if strong_corr:
            st.dataframe(pd.DataFrame(strong_corr), use_container_width=True)
        else:
            st.info("No strong correlations found (|r| > 0.5)")


def show_relationships(df):
    """Display relationship visualizations"""
    st.header("📈 Relationship Analysis")
    
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if len(numerical_cols) >= 2:
        col1, col2 = st.columns(2)
        
        with col1:
            x_col = st.selectbox("Select X-axis", numerical_cols, key='x_axis')
        with col2:
            y_col = st.selectbox("Select Y-axis", 
                               [col for col in numerical_cols if col != x_col],
                               key='y_axis')
        
        # Color by categorical variable
        color_col = None
        if categorical_cols:
            color_col = st.selectbox("Color by (optional)", 
                                   ['None'] + categorical_cols)
            if color_col == 'None':
                color_col = None
        
        # Scatter plot
        fig = px.scatter(df, x=x_col, y=y_col, color=color_col,
                        title=f"{y_col} vs {x_col}",
                        trendline="ols",
                        hover_data=df.columns)
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)


def show_categorical_analysis(df):
    """Display categorical variable analysis"""
    st.header("🏷️ Categorical Analysis")
    
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if categorical_cols:
        selected_cat = st.selectbox("Select categorical variable", categorical_cols)
        
        # Value counts
        value_counts = df[selected_cat].value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Bar chart
            fig_bar = px.bar(x=value_counts.index, y=value_counts.values,
                           title=f"Distribution of {selected_cat}",
                           labels={'x': selected_cat, 'y': 'Count'},
                           color=value_counts.values,
                           color_continuous_scale='Viridis')
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            # Pie chart
            fig_pie = px.pie(values=value_counts.values, names=value_counts.index,
                           title=f"Percentage Distribution of {selected_cat}")
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Cross-tabulation with numerical variable
        numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if numerical_cols:
            st.subheader(f"Analysis by {selected_cat}")
            num_col = st.selectbox("Select numerical variable", numerical_cols)
            
            # Box plot by category
            fig = px.box(df, x=selected_cat, y=num_col,
                        title=f"{num_col} by {selected_cat}",
                        color=selected_cat)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No categorical variables found in the dataset")


def show_time_series(df):
    """Display time series analysis if date columns exist"""
    st.header("📅 Time Series Analysis")
    
    # Try to find date columns
    date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    # Also check for columns that might be dates
    for col in df.columns:
        if 'date' in col.lower() or 'time' in col.lower():
            try:
                df[col] = pd.to_datetime(df[col])
                if col not in date_cols:
                    date_cols.append(col)
            except:
                pass
    
    if date_cols:
        date_col = st.selectbox("Select date column", date_cols)
        
        numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if numerical_cols:
            value_col = st.selectbox("Select value column", numerical_cols)
            
            # Ensure date column is datetime
            if df[date_col].dtype != 'datetime64[ns]':
                df[date_col] = pd.to_datetime(df[date_col])
            
            # Sort by date
            df_sorted = df.sort_values(date_col)
            
            # Line plot
            fig = px.line(df_sorted, x=date_col, y=value_col,
                         title=f"{value_col} over Time")
            st.plotly_chart(fig, use_container_width=True)
            
            # Aggregation options
            agg_method = st.selectbox("Aggregation", ['None', 'Daily', 'Weekly', 'Monthly'])
            
            if agg_method != 'None':
                if agg_method == 'Daily':
                    df_agg = df_sorted.groupby(df_sorted[date_col].dt.date)[value_col].mean().reset_index()
                elif agg_method == 'Weekly':
                    df_agg = df_sorted.groupby(pd.Grouper(key=date_col, freq='W'))[value_col].mean().reset_index()
                else:  # Monthly
                    df_agg = df_sorted.groupby(pd.Grouper(key=date_col, freq='M'))[value_col].mean().reset_index()
                
                fig_agg = px.line(df_agg, x=date_col, y=value_col,
                                title=f"{value_col} - {agg_method} Average")
                st.plotly_chart(fig_agg, use_container_width=True)
    else:
        st.info("No date columns found in the dataset")


def show_sql_queries(db_path='data/analytics.db'):
    """Display SQL query interface"""
    st.header("💾 SQL Query Interface")
    
    if not os.path.exists(db_path):
        st.warning("Database not found. Please run sql_integration.py first to create the database.")
        return
    
    st.info("Database connected. You can run custom SQL queries below.")
    
    # Predefined queries
    st.subheader("Predefined Queries")
    
    query_options = {
        "All Sales Data": "SELECT * FROM sales LIMIT 100;",
        "Sales by Category": """
            SELECT category, 
                   COUNT(*) as transactions,
                   ROUND(SUM(total_amount), 2) as revenue
            FROM sales 
            GROUP BY category 
            ORDER BY revenue DESC;
        """,
        "Top Customers": """
            SELECT customer_id,
                   COUNT(*) as purchases,
                   ROUND(SUM(total_amount), 2) as total_spent
            FROM sales 
            GROUP BY customer_id 
            ORDER BY total_spent DESC 
            LIMIT 10;
        """,
        "Daily Performance": "SELECT * FROM daily_sales_summary;",
        "Category Performance": "SELECT * FROM category_performance;"
    }
    
    selected_query = st.selectbox("Select a query", list(query_options.keys()))
    
    if st.button("Execute Predefined Query"):
        try:
            conn = sqlite3.connect(db_path)
            result_df = pd.read_sql_query(query_options[selected_query], conn)
            conn.close()
            
            st.success(f"Query executed successfully! Retrieved {len(result_df)} rows.")
            st.dataframe(result_df, use_container_width=True)
        except Exception as e:
            st.error(f"Query execution failed: {e}")
    
    # Custom query
    st.subheader("Custom SQL Query")
    st.warning("⚠️ This is a demo feature. Only use SELECT queries. Do not use with untrusted data sources.")
    custom_query = st.text_area("Enter your SQL query:", 
                                value="SELECT * FROM sales LIMIT 10;",
                                height=150)
    
    if st.button("Execute Custom Query"):
        # Basic validation - only allow SELECT queries
        query_upper = custom_query.strip().upper()
        if not query_upper.startswith('SELECT'):
            st.error("⚠️ Only SELECT queries are allowed for security reasons.")
            return
        
        # Check for dangerous keywords
        dangerous_keywords = ['DROP', 'DELETE', 'INSERT', 'UPDATE', 'ALTER', 'CREATE', 'EXEC', 'EXECUTE']
        if any(keyword in query_upper for keyword in dangerous_keywords):
            st.error("⚠️ Query contains disallowed keywords. Only SELECT queries are permitted.")
            return
        
        try:
            conn = sqlite3.connect(db_path)
            # Set read-only mode for safety
            conn.execute("PRAGMA query_only = ON;")
            result_df = pd.read_sql_query(custom_query, conn)
            conn.close()
            
            st.success(f"Query executed successfully! Retrieved {len(result_df)} rows.")
            st.dataframe(result_df, use_container_width=True)
            
            # Option to download results
            csv = result_df.to_csv(index=False)
            st.download_button(
                label="Download Results as CSV",
                data=csv,
                file_name="query_results.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"Query execution failed: {e}")


def main():
    """Main dashboard function"""
    
    # Title
    st.title("📊 Interactive Data Analytics Dashboard")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.title("Dashboard Controls")
    st.sidebar.markdown("---")
    
    # Data source selection
    data_source = st.sidebar.radio(
        "Select Data Source",
        ["Seaborn Dataset", "SQL Database"]
    )
    
    df = None
    
    if data_source == "Seaborn Dataset":
        dataset_name = st.sidebar.selectbox(
            "Select Dataset",
            ['tips', 'titanic', 'iris', 'diamonds', 'flights']
        )
        df = load_data(dataset_name)
        
    else:  # SQL Database
        db_path = 'data/analytics.db'
        df = load_sql_data(db_path)
        if df is None:
            st.warning("SQL database not found. Please run `python src/sql_integration.py` first.")
            return
    
    if df is None:
        st.error("Failed to load data. Please check your data source.")
        return
    
    # Navigation
    st.sidebar.markdown("---")
    st.sidebar.subheader("Navigation")
    
    page = st.sidebar.radio(
        "Select Analysis Type",
        ["Overview", "Statistics", "Correlations", "Relationships", 
         "Categorical Analysis", "Time Series", "SQL Queries"]
    )
    
    # Display selected page
    if page == "Overview":
        show_overview(df)
    elif page == "Statistics":
        show_statistics(df)
    elif page == "Correlations":
        show_correlations(df)
    elif page == "Relationships":
        show_relationships(df)
    elif page == "Categorical Analysis":
        show_categorical_analysis(df)
    elif page == "Time Series":
        show_time_series(df)
    elif page == "SQL Queries":
        show_sql_queries()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "This interactive dashboard provides comprehensive data analysis "
        "capabilities with multiple visualization options and SQL query support."
    )
    
    # Download data option
    st.sidebar.markdown("---")
    st.sidebar.subheader("Export Data")
    if st.sidebar.button("Download Current Data"):
        csv = df.to_csv(index=False)
        st.sidebar.download_button(
            label="Download as CSV",
            data=csv,
            file_name=f"data_export_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )


if __name__ == "__main__":
    main()
