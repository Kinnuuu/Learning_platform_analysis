"""
Main script for Course Platform Analytics
Runs the complete analytics pipeline and exports data for Excel dashboard
"""

from database_connection import DatabaseConnection
from analytics_engine import AnalyticsEngine
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to run analytics pipeline"""
    logger.info("Starting Course Platform Analytics Pipeline...")
    
    # Database configuration - Your MySQL credentials
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': '1234',
        'database': 'OnlineCourseDB'
    }
    
    # Initialize database connection
    db = DatabaseConnection(**DB_CONFIG)
    
    try:
        # Connect to database
        if not db.connect():
            logger.error("Failed to connect to database. Please check your credentials.")
            return
        
        # Initialize analytics engine
        analytics = AnalyticsEngine(db)
        
        # Export all analytics data to CSV files
        analytics.export_all_analytics()
        
        logger.info("✅ Analytics pipeline completed successfully!")
        logger.info("📁 Check the 'data_exports' folder for CSV files")
        logger.info("📊 You can now import these CSV files into Excel to create your dashboard")
        
    except Exception as e:
        logger.error(f"Error in analytics pipeline: {e}")
    
    finally:
        # Close database connection
        db.close()

if __name__ == "__main__":
    main()