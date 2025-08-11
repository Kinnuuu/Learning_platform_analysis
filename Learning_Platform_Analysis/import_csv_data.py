"""
Import CSV data into MySQL course table
Maps udemy_courses.csv columns to your course table structure
"""

import pandas as pd
import mysql.connector
from database_connection import DatabaseConnection
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def import_udemy_courses():
    """Import udemy_courses.csv into the course table"""
    
    # Read the CSV file
    try:
        df = pd.read_csv('udemy_courses.csv')
        logger.info(f"Successfully loaded CSV with {len(df)} rows")
        print(f"CSV columns: {list(df.columns)}")
        print(f"First few rows:")
        print(df.head())
    except Exception as e:
        logger.error(f"Error reading CSV file: {e}")
        return
    
    # Connect to database
    db = DatabaseConnection()
    if not db.connect():
        logger.error("Failed to connect to database")
        return
    
    try:
        cursor = db.connection.cursor()
        
        # Clear existing data (optional - remove this if you want to keep existing data)
        # cursor.execute("DELETE FROM course")
        # logger.info("Cleared existing course data")
        
        # First, let's check the actual table structure
        cursor.execute("DESCRIBE course")
        columns = cursor.fetchall()
        print("Actual course table columns:")
        for col in columns:
            print(f"  {col[0]} - {col[1]}")
        
        # Prepare the insert query with correct column names from your schema
        insert_query = """
        INSERT INTO course (
            course_id, course_title, course_url, price, num_subscription, 
            num_review, num_lec, level, content_duration, publised_timestamp, 
            subject, is_paid
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Process each row
        inserted_count = 0
        for index, row in df.iterrows():
            try:
                # Map CSV columns to database columns
                values = (
                    int(row['course_id']),                    # course_id
                    str(row['course_title'])[:500],           # course_title (truncate to fit)
                    str(row['url'])[:500],                    # course_url
                    float(row['price']) if pd.notna(row['price']) else 0.0,  # price
                    int(row['num_subscribers']) if pd.notna(row['num_subscribers']) else 0,  # num_subscription
                    int(row['num_reviews']) if pd.notna(row['num_reviews']) else 0,  # num_review
                    int(row['num_lectures']) if pd.notna(row['num_lectures']) else 0,  # num_lec
                    str(row['level'])[:50],                   # level
                    float(row['content_duration']) if pd.notna(row['content_duration']) else 0.0,  # content_duration
                    str(row['published_timestamp'])[:19],     # publised_timestamp (truncate to fit datetime)
                    str(row['subject'])[:100],                # subject
                    bool(row['is_paid'])                      # is_paid
                )
                
                cursor.execute(insert_query, values)
                inserted_count += 1
                
                if inserted_count % 100 == 0:
                    logger.info(f"Inserted {inserted_count} rows...")
                    
            except Exception as e:
                logger.warning(f"Error inserting row {index}: {e}")
                continue
        
        # Commit the changes
        db.connection.commit()
        logger.info(f"Successfully imported {inserted_count} courses into database")
        
        # Verify the import
        cursor.execute("SELECT COUNT(*) FROM course")
        total_courses = cursor.fetchone()[0]
        logger.info(f"Total courses in database: {total_courses}")
        
        cursor.close()
        
    except Exception as e:
        logger.error(f"Error during import: {e}")
        db.connection.rollback()
    
    finally:
        db.close()

def add_sample_users_and_enrollments():
    """Add sample users and enrollments to test the analytics"""
    
    db = DatabaseConnection()
    if not db.connect():
        return
    
    try:
        cursor = db.connection.cursor()
        
        # Add sample users
        users_data = [
            (1, 'john_doe', 'john@email.com', 'John', 'Doe', 'free', 'USA', True),
            (2, 'jane_smith', 'jane@email.com', 'Jane', 'Smith', 'premium', 'UK', True),
            (3, 'bob_wilson', 'bob@email.com', 'Bob', 'Wilson', 'pro', 'Canada', True),
            (4, 'alice_brown', 'alice@email.com', 'Alice', 'Brown', 'premium', 'Australia', True),
            (5, 'charlie_davis', 'charlie@email.com', 'Charlie', 'Davis', 'free', 'Germany', True)
        ]
        
        user_query = """
        INSERT IGNORE INTO user (user_id, username, email, first_name, last_name, subscription_type, country, is_active)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.executemany(user_query, users_data)
        logger.info("Added sample users")
        
        # Add sample enrollments (erp table)
        # Get some course IDs first
        cursor.execute("SELECT course_id FROM course LIMIT 10")
        course_ids = [row[0] for row in cursor.fetchall()]
        
        if course_ids:
            enrollments_data = [
                (1, course_ids[0], 'completed', 100, 5),
                (1, course_ids[1], 'in_progress', 75, None),
                (2, course_ids[0], 'completed', 100, 4),
                (2, course_ids[2], 'in_progress', 50, None),
                (3, course_ids[1], 'completed', 100, 5),
                (4, course_ids[3], 'not_started', 0, None),
                (5, course_ids[0], 'in_progress', 25, None)
            ]
            
            enrollment_query = """
            INSERT IGNORE INTO erp (user_id, course_id, completion_status, progress_per, rating_given)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            cursor.executemany(enrollment_query, enrollments_data)
            logger.info("Added sample enrollments")
        
        # Add sample subscriptions
        subscriptions_data = [
            (2, 'premium', '2024-01-01', '2024-12-31', 29.99, 'active'),
            (3, 'pro', '2024-02-01', '2024-12-31', 49.99, 'active'),
            (4, 'premium', '2024-03-01', '2024-12-31', 29.99, 'active')
        ]
        
        subscription_query = """
        INSERT IGNORE INTO subscriptions (user_id, plan_type, start_date, end_date, monthely_fee, status)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        cursor.executemany(subscription_query, subscriptions_data)
        logger.info("Added sample subscriptions")
        
        db.connection.commit()
        logger.info("Sample data added successfully!")
        
    except Exception as e:
        logger.error(f"Error adding sample data: {e}")
        db.connection.rollback()
    
    finally:
        cursor.close()
        db.close()

if __name__ == "__main__":
    print("=== Importing Udemy Courses CSV ===")
    import_udemy_courses()
    
    print("\n=== Adding Sample Users and Enrollments ===")
    add_sample_users_and_enrollments()
    
    print("\n=== Testing Analytics ===")
    from analytics_engine import test_analytics
    test_analytics()