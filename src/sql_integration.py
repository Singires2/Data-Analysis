"""
SQL Database Integration for Data Analytics
Demonstrates data extraction using SQL queries with SQLite
"""

import pandas as pd
import sqlite3
import seaborn as sns
import os


class SQLDataExtractor:
    """Handle SQL-based data extraction and database operations"""
    
    def __init__(self, db_path='data/analytics.db'):
        """
        Initialize SQL Data Extractor
        
        Parameters:
        -----------
        db_path : str
            Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_path)
        print(f"Connected to database: {self.db_path}")
        return self.conn
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("Database connection closed")
    
    def create_sample_database(self):
        """Create a sample database with sales data from seaborn"""
        print("\nCreating sample database...")
        
        # Load sample data
        df = sns.load_dataset('tips')
        
        # Rename columns to match business context
        df_sales = df.copy()
        df_sales = df_sales.rename(columns={
            'total_bill': 'total_amount',
            'tip': 'tip_amount',
            'sex': 'customer_gender',
            'smoker': 'smoking_section',
            'day': 'sale_day',
            'time': 'meal_time',
            'size': 'party_size'
        })
        
        # Add additional columns for demonstration
        df_sales['product_id'] = range(1, len(df_sales) + 1)
        df_sales['product_name'] = df_sales['meal_time'].apply(
            lambda x: f"{x} Special" if x == 'Dinner' else f"{x} Combo"
        )
        df_sales['category'] = df_sales['meal_time']
        df_sales['quantity'] = df_sales['party_size']
        df_sales['price'] = (df_sales['total_amount'] / df_sales['party_size']).round(2)
        df_sales['customer_id'] = (df_sales.index % 50) + 1  # Simulate 50 customers
        
        # Add date column (simulate dates over 2 months)
        df_sales['sale_date'] = pd.date_range(start='2024-01-01', periods=len(df_sales), freq='H')
        df_sales['sale_date'] = df_sales['sale_date'].dt.strftime('%Y-%m-%d')
        
        # Connect and create table
        self.connect()
        
        # Create sales table
        df_sales.to_sql('sales', self.conn, if_exists='replace', index=False)
        print(f"Created 'sales' table with {len(df_sales)} records")
        
        # Create aggregated views
        self._create_views()
        
        self.close()
        print("Sample database created successfully!")
        
        return df_sales
    
    def _create_views(self):
        """Create database views for common queries"""
        
        # Daily sales summary view
        daily_summary_query = """
        CREATE VIEW IF NOT EXISTS daily_sales_summary AS
        SELECT 
            sale_date,
            COUNT(*) as num_transactions,
            SUM(quantity) as total_quantity,
            SUM(total_amount) as daily_revenue,
            AVG(total_amount) as avg_transaction_value
        FROM sales
        GROUP BY sale_date
        ORDER BY sale_date;
        """
        
        # Category performance view
        category_performance_query = """
        CREATE VIEW IF NOT EXISTS category_performance AS
        SELECT 
            category,
            COUNT(*) as total_transactions,
            SUM(quantity) as total_quantity,
            SUM(total_amount) as total_revenue,
            AVG(total_amount) as avg_transaction_value,
            MIN(sale_date) as first_sale,
            MAX(sale_date) as last_sale
        FROM sales
        GROUP BY category
        ORDER BY total_revenue DESC;
        """
        
        # Top customers view
        top_customers_query = """
        CREATE VIEW IF NOT EXISTS top_customers AS
        SELECT 
            customer_id,
            COUNT(*) as total_purchases,
            SUM(total_amount) as total_spent,
            AVG(total_amount) as avg_purchase_value,
            MIN(sale_date) as first_purchase,
            MAX(sale_date) as last_purchase
        FROM sales
        GROUP BY customer_id
        ORDER BY total_spent DESC
        LIMIT 20;
        """
        
        cursor = self.conn.cursor()
        cursor.execute(daily_summary_query)
        cursor.execute(category_performance_query)
        cursor.execute(top_customers_query)
        self.conn.commit()
        print("Created database views: daily_sales_summary, category_performance, top_customers")
    
    def execute_query(self, query, description=""):
        """
        Execute SQL query and return results as DataFrame
        
        Parameters:
        -----------
        query : str
            SQL query to execute
        description : str
            Description of what the query does
            
        Returns:
        --------
        pandas.DataFrame
            Query results
        """
        if description:
            print(f"\n{description}")
        
        print(f"Executing query...")
        
        self.connect()
        df = pd.read_sql_query(query, self.conn)
        self.close()
        
        print(f"Retrieved {len(df)} rows")
        return df
    
    def demonstrate_queries(self):
        """Demonstrate various SQL queries for data extraction"""
        print("\n" + "="*80)
        print("SQL DATA EXTRACTION DEMONSTRATION")
        print("="*80)
        
        # Query 1: Basic data extraction
        query1 = """
        SELECT * FROM sales
        LIMIT 10;
        """
        df1 = self.execute_query(query1, "1. Basic Data Extraction (First 10 rows):")
        print(df1)
        
        # Query 2: Aggregated sales by category
        query2 = """
        SELECT 
            category,
            COUNT(*) as total_transactions,
            SUM(quantity) as total_quantity,
            ROUND(SUM(total_amount), 2) as total_revenue,
            ROUND(AVG(total_amount), 2) as avg_transaction_value
        FROM sales
        GROUP BY category
        ORDER BY total_revenue DESC;
        """
        df2 = self.execute_query(query2, "\n2. Sales Performance by Category:")
        print(df2)
        
        # Query 3: Top performing products
        query3 = """
        SELECT 
            product_name,
            category,
            COUNT(*) as num_sales,
            ROUND(SUM(total_amount), 2) as total_revenue,
            ROUND(AVG(price), 2) as avg_price
        FROM sales
        GROUP BY product_name, category
        ORDER BY total_revenue DESC
        LIMIT 5;
        """
        df3 = self.execute_query(query3, "\n3. Top 5 Performing Products:")
        print(df3)
        
        # Query 4: Customer analysis
        query4 = """
        SELECT 
            customer_id,
            COUNT(*) as total_purchases,
            ROUND(SUM(total_amount), 2) as total_spent,
            ROUND(AVG(total_amount), 2) as avg_purchase_value
        FROM sales
        GROUP BY customer_id
        HAVING COUNT(*) > 5
        ORDER BY total_spent DESC
        LIMIT 10;
        """
        df4 = self.execute_query(query4, "\n4. Top 10 Customers (with >5 purchases):")
        print(df4)
        
        # Query 5: Using views
        query5 = """
        SELECT * FROM category_performance;
        """
        df5 = self.execute_query(query5, "\n5. Category Performance (from view):")
        print(df5)
        
        # Query 6: Time-based analysis
        query6 = """
        SELECT 
            meal_time,
            sale_day,
            COUNT(*) as num_transactions,
            ROUND(SUM(total_amount), 2) as revenue
        FROM sales
        GROUP BY meal_time, sale_day
        ORDER BY meal_time, revenue DESC;
        """
        df6 = self.execute_query(query6, "\n6. Revenue by Meal Time and Day:")
        print(df6)
        
        print("\n" + "="*80)
        print("SQL QUERIES DEMONSTRATION COMPLETED")
        print("="*80)
        print(f"\nDatabase location: {self.db_path}")
        print("You can connect to this database using:")
        print("  - Python: sqlite3 or SQLAlchemy")
        print("  - Power BI: Get Data > SQLite")
        print("  - Tableau: Connect > SQLite")
    
    def export_query_results(self, output_dir='exports'):
        """Export common query results for analysis"""
        print("\n" + "="*80)
        print("EXPORTING QUERY RESULTS")
        print("="*80)
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Export category performance
        query = "SELECT * FROM category_performance;"
        df = self.execute_query(query, "\nExporting category performance...")
        df.to_csv(f'{output_dir}/category_performance.csv', index=False)
        print(f"Saved: {output_dir}/category_performance.csv")
        
        # Export top customers
        query = "SELECT * FROM top_customers;"
        df = self.execute_query(query, "\nExporting top customers...")
        df.to_csv(f'{output_dir}/top_customers.csv', index=False)
        print(f"Saved: {output_dir}/top_customers.csv")
        
        # Export daily summary
        query = "SELECT * FROM daily_sales_summary;"
        df = self.execute_query(query, "\nExporting daily sales summary...")
        df.to_csv(f'{output_dir}/daily_sales_summary.csv', index=False)
        print(f"Saved: {output_dir}/daily_sales_summary.csv")
        
        print("\nQuery results exported successfully!")


def main():
    """Main execution function for SQL demonstration"""
    print("SQL Data Extraction Module")
    print("="*80)
    
    # Initialize extractor
    extractor = SQLDataExtractor()
    
    # Create sample database
    extractor.create_sample_database()
    
    # Demonstrate various queries
    extractor.demonstrate_queries()
    
    # Export query results
    extractor.export_query_results()
    
    print("\nSQL integration complete!")
    print("Database can now be used with BI tools like Power BI and Tableau")


if __name__ == "__main__":
    main()
