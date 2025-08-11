"""
Database Connection Module for Course Platform Analytics
Handles MySQL database connections and query execution
"""

import mysql.connector
import pandas as pd
from typing import Optional, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    """Manages MySQL database connections and query execution"""
    
    def __init__(self, host: str = 'localhost', user: str = 'root', 
                 password: str = '1234', database: str = 'OnlineCourseDB'):
        """
        Initialize database connection parameters
        
        Args:
            host: MySQL server host
            user: Database username
            password: Database password
            database: Database name
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        
    def connect(self) -> bool:
        """
        Establish connection to MySQL database
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            logger.info(f"Successfully connected to database: {self.database}")
            return True
        except mysql.connector.Error as e:
            logger.error(f"Error connecting to database: {e}")
            return False
    
    def execute_query(self, query: str) -> Optional[list]:
        """
        Execute SQL query and return results
        
        Args:
            query: SQL query string
            
        Returns:
            list: Query results or None if error
        """
        if not self.connection:
            logger.error("No database connection established")
            return None
            
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except mysql.connector.Error as e:
            logger.error(f"Error executing query: {e}")
            return None
    
    def fetch_dataframe(self, query: str) -> Optional[pd.DataFrame]:
        """
        Execute query and return results as pandas DataFrame
        
        Args:
            query: SQL query string
            
        Returns:
            pd.DataFrame: Query results as DataFrame or None if error
        """
        if not self.connection:
            logger.error("No database connection established")
            return None
            
        try:
            df = pd.read_sql(query, self.connection)
            logger.info(f"Successfully fetched {len(df)} rows")
            return df
        except Exception as e:
            logger.error(f"Error fetching DataFrame: {e}")
            return None
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")

# Test connection function
def test_connection():
    """Test database connection with sample query"""
    db = DatabaseConnection()
    
    if db.connect():
        # Test with a simple query
        test_query = "SELECT COUNT(*) as total_users FROM user"
        result = db.fetch_dataframe(test_query)
        
        if result is not None:
            print("[SUCCESS] Database connection test successful!")
            print(f"Total users in database: {result['total_users'].iloc[0]}")
        else:
            print("[ERROR] Query execution failed")
        
        db.close()
    else:
        print("[ERROR] Database connection failed")

if __name__ == "__main__":
    test_connection()