"""
Analytics Engine for Course Platform Analytics
Contains all analytics queries and data export functions
"""

import pandas as pd
from database_connection import DatabaseConnection
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AnalyticsEngine:
    """Handles all analytics queries and data exports"""
    
    def __init__(self, db_connection: DatabaseConnection):
        """
        Initialize analytics engine with database connection
        
        Args:
            db_connection: DatabaseConnection instance
        """
        self.db = db_connection
        self.export_dir = "data_exports"
        
        # Create export directory if it doesn't exist
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)
    
    def get_user_distribution(self) -> pd.DataFrame:
        """Get user subscription type distribution"""
        query = """
        SELECT
            subscription_type,
            COUNT(*) AS user_count,
            ROUND(COUNT(*) / (SELECT COUNT(*) FROM user) * 100, 2) AS percentage 
        FROM user
        GROUP BY subscription_type
        ORDER BY user_count DESC
        """
        return self.db.fetch_dataframe(query)
    
    def get_user_registration_trends(self) -> pd.DataFrame:
        """Get premium vs free users trend over time"""
        query = """
        SELECT 
            DATE_FORMAT(regi_date, '%Y-%m') AS month,
            subscription_type,
            COUNT(*) AS new_users
        FROM user
        GROUP BY 
            month,
            subscription_type
        ORDER BY 
            month, 
            subscription_type
        """
        return self.db.fetch_dataframe(query)
    
    def get_course_popularity(self) -> pd.DataFrame:
        """Get course popularity analysis"""
        query = """
        SELECT
            c.course_title,
            c.instructor_name,
            c.subject,
            COUNT(e.erp_id) as total_enrollments,
            AVG(e.rating_given) as avg_rating,
            c.price
        FROM course c
        LEFT JOIN erp e ON c.course_id = e.course_id
        GROUP BY c.course_id
        ORDER BY total_enrollments DESC
        LIMIT 20
        """
        return self.db.fetch_dataframe(query)
    
    def get_completion_rates(self) -> pd.DataFrame:
        """Get course completion rates by level"""
        query = """
        SELECT
            c.level,
            COUNT(*) as total_enrollments,
            COUNT(CASE WHEN e.completion_status = 'completed' THEN 1 END) as completions,
            ROUND(
                COUNT(CASE WHEN e.completion_status = 'completed' THEN 1 END) * 100.0/COUNT(*),
                2
            ) as completion_rate
        FROM course c
        JOIN erp e ON c.course_id = e.course_id
        GROUP BY c.level
        """
        return self.db.fetch_dataframe(query)
    
    def get_revenue_metrics(self) -> pd.DataFrame:
        """Get revenue analysis by subscription plan"""
        query = """
        SELECT 
            s.plan_type,
            COUNT(*) as active_subscriptions,
            SUM(s.monthely_fee) as monthly_revenue,
            AVG(s.monthely_fee) as avg_monthly_fee
        FROM subscriptions s
        WHERE s.status = 'active'
        GROUP BY s.plan_type
        """
        return self.db.fetch_dataframe(query)
    
    def get_churn_analysis(self) -> pd.DataFrame:
        """Get churn analysis by plan type"""
        query = """
        SELECT
            s.plan_type,
            COUNT(*) as total_subscriptions,
            COUNT(CASE WHEN s.status = 'cancelled' THEN 1 END) as churned,
            ROUND(COUNT(CASE WHEN s.status = 'cancelled' THEN 1 END)* 100.0/COUNT(*), 2) as churn_rate
        FROM subscriptions s
        GROUP BY s.plan_type
        """
        return self.db.fetch_dataframe(query)
    
    def get_engagement_metrics(self) -> pd.DataFrame:
        """Get user engagement metrics by subscription type"""
        query = """
        SELECT 
            u.subscription_type,
            COUNT(DISTINCT e.course_id) as avg_courses_enrolled,
            AVG(e.progress_per) as avg_completion_rate,
            COUNT(DISTINCT ci.interaction_id) as total_interactions
        FROM user u
        LEFT JOIN erp e ON u.user_id = e.user_id
        LEFT JOIN course_interactions ci ON u.user_id = ci.user_id
        GROUP BY u.subscription_type
        """
        return self.db.fetch_dataframe(query)
    
    def get_cohort_analysis(self) -> pd.DataFrame:
        """Get cohort analysis for user retention"""
        query = """
        SELECT
            DATE_FORMAT(u.regi_date, '%Y-%m') as registration_month,
            COUNT(DISTINCT u.user_id) as total_users,
            COUNT(DISTINCT CASE WHEN u.last_login >= DATE_SUB(NOW(), INTERVAL 30 DAY) THEN u.user_id END) as active_last_30_days,
            ROUND(
                COUNT(DISTINCT CASE WHEN u.last_login >= DATE_SUB(NOW(), INTERVAL 30 DAY) THEN u.user_id END) * 100.0/ COUNT(DISTINCT u.user_id),
                2
            ) as retention_rate
        FROM user u
        GROUP BY DATE_FORMAT(u.regi_date, '%Y-%m')
        ORDER BY registration_month
        """
        return self.db.fetch_dataframe(query)
    
    def get_platform_kpis(self) -> pd.DataFrame:
        """Get overall platform KPIs"""
        query = """
        SELECT
            (SELECT COUNT(*) FROM user WHERE is_active = TRUE) as total_active_users,
            (SELECT COUNT(*) FROM user WHERE subscription_type != 'free') as paid_users,
            (SELECT COUNT(*) FROM course) as total_courses,
            (SELECT SUM(monthely_fee) FROM subscriptions WHERE status = 'active') as monthly_recurring_revenue,
            (SELECT AVG(rating_given) FROM erp WHERE rating_given IS NOT NULL) as avg_course_rating
        """
        return self.db.fetch_dataframe(query)
    
    def export_to_csv(self, dataframe: pd.DataFrame, filename: str):
        """
        Export DataFrame to CSV file
        
        Args:
            dataframe: pandas DataFrame to export
            filename: name of the CSV file
        """
        if dataframe is not None and not dataframe.empty:
            filepath = os.path.join(self.export_dir, filename)
            dataframe.to_csv(filepath, index=False)
            logger.info(f"Exported {len(dataframe)} rows to {filepath}")
        else:
            logger.warning(f"No data to export for {filename}")
    
    def export_all_analytics(self):
        """Export all analytics data to CSV files"""
        logger.info("Starting analytics data export...")
        
        # Export user analytics
        user_dist = self.get_user_distribution()
        self.export_to_csv(user_dist, "user_distribution.csv")
        
        user_trends = self.get_user_registration_trends()
        self.export_to_csv(user_trends, "user_registration_trends.csv")
        
        # Export course analytics
        course_pop = self.get_course_popularity()
        self.export_to_csv(course_pop, "course_popularity.csv")
        
        completion_rates = self.get_completion_rates()
        self.export_to_csv(completion_rates, "course_completion_rates.csv")
        
        # Export revenue analytics
        revenue = self.get_revenue_metrics()
        self.export_to_csv(revenue, "revenue_metrics.csv")
        
        churn = self.get_churn_analysis()
        self.export_to_csv(churn, "churn_analysis.csv")
        
        # Export engagement analytics
        engagement = self.get_engagement_metrics()
        self.export_to_csv(engagement, "user_engagement.csv")
        
        cohort = self.get_cohort_analysis()
        self.export_to_csv(cohort, "cohort_analysis.csv")
        
        # Export KPIs
        kpis = self.get_platform_kpis()
        self.export_to_csv(kpis, "platform_kpis.csv")
        
        logger.info("Analytics data export completed!")

# Test function
def test_analytics():
    """Test analytics engine functionality"""
    db = DatabaseConnection()
    
    if db.connect():
        analytics = AnalyticsEngine(db)
        
        # Test one query
        user_dist = analytics.get_user_distribution()
        if user_dist is not None:
            print("[SUCCESS] Analytics engine test successful!")
            print("User Distribution:")
            print(user_dist)
        else:
            print("[ERROR] Analytics query failed")
        
        db.close()
    else:
        print("[ERROR] Database connection failed")

if __name__ == "__main__":
    test_analytics()