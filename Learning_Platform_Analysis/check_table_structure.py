"""
Check the actual structure of the course table
"""

from database_connection import DatabaseConnection

def check_course_table():
    """Check the actual column names in the course table"""
    
    db = DatabaseConnection()
    if not db.connect():
        print("Failed to connect to database")
        return
    
    try:
        cursor = db.connection.cursor()
        
        # Check table structure
        cursor.execute("DESCRIBE course")
        columns = cursor.fetchall()
        
        print("Actual course table columns:")
        print("-" * 40)
        for col in columns:
            print(f"{col[0]:<25} | {col[1]}")
        print("-" * 40)
        
        cursor.close()
        
    except Exception as e:
        print(f"Error checking table: {e}")
    
    finally:
        db.close()

if __name__ == "__main__":
    check_course_table()