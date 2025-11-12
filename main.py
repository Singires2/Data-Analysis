#!/usr/bin/env python3
"""
Main Entry Point for Data Analytics Project
Orchestrates the complete analytics workflow
"""

import os
import sys
import argparse


def print_banner():
    """Print project banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║          Data Analytics Project                           ║
    ║    Complete Python Data Analysis Pipeline                 ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def run_data_analysis():
    """Run main data analysis pipeline"""
    print("\n" + "="*70)
    print("RUNNING DATA ANALYSIS PIPELINE")
    print("="*70)
    
    from src.data_analysis import main as analysis_main
    analysis_main()


def run_sql_integration():
    """Run SQL integration module"""
    print("\n" + "="*70)
    print("RUNNING SQL INTEGRATION")
    print("="*70)
    
    from src.sql_integration import main as sql_main
    sql_main()


def run_dashboard():
    """Run interactive dashboard"""
    print("\n" + "="*70)
    print("LAUNCHING INTERACTIVE DASHBOARD")
    print("="*70)
    print("\nStarting Streamlit dashboard...")
    print("Dashboard will open in your browser at http://localhost:8501")
    print("Press Ctrl+C to stop the dashboard\n")
    
    os.system("streamlit run src/dashboard.py")


def run_all():
    """Run complete workflow"""
    print_banner()
    print("\nRunning complete analytics workflow...\n")
    
    # Step 1: Data Analysis
    print("\n[1/2] Running data analysis pipeline...")
    run_data_analysis()
    
    # Step 2: SQL Integration
    print("\n[2/2] Running SQL integration...")
    run_sql_integration()
    
    print("\n" + "="*70)
    print("WORKFLOW COMPLETED SUCCESSFULLY")
    print("="*70)
    print("\nGenerated outputs:")
    print("  📁 visualizations/ - Static visualizations")
    print("  📁 exports/ - Data exports for BI tools")
    print("  📁 data/ - SQLite database")
    print("\nNext steps:")
    print("  🚀 Run interactive dashboard: python main.py --dashboard")
    print("  📊 Open Power BI/Tableau and import data from exports/")
    print("  💾 Explore SQL database at data/analytics.db")


def main():
    """Main entry point with argument parsing"""
    parser = argparse.ArgumentParser(
        description="Data Analytics Project - Complete Python Analysis Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --all              Run complete workflow
  python main.py --analysis         Run data analysis only
  python main.py --sql              Run SQL integration only
  python main.py --dashboard        Launch interactive dashboard
        """
    )
    
    parser.add_argument('--all', action='store_true',
                       help='Run complete workflow (analysis + SQL)')
    parser.add_argument('--analysis', action='store_true',
                       help='Run data analysis pipeline only')
    parser.add_argument('--sql', action='store_true',
                       help='Run SQL integration only')
    parser.add_argument('--dashboard', action='store_true',
                       help='Launch interactive Streamlit dashboard')
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if not any(vars(args).values()):
        print_banner()
        parser.print_help()
        print("\n💡 Tip: Start with 'python main.py --all' to run the complete workflow")
        return
    
    # Execute based on arguments
    if args.all:
        run_all()
    elif args.analysis:
        print_banner()
        run_data_analysis()
    elif args.sql:
        print_banner()
        run_sql_integration()
    elif args.dashboard:
        print_banner()
        run_dashboard()


if __name__ == "__main__":
    main()
