# Course Platform Analytics Dashboard

A comprehensive analytics solution for online course platforms (like Udemy) that connects to a MySQL database, extracts analytics data, and creates an interactive Excel dashboard.

## Project Structure

```
course-platform-analytics/
├── .kiro/specs/course-platform-analytics/
│   ├── requirements.md          # Project requirements
│   ├── design.md               # Technical design document
│   └── tasks.md                # Implementation tasks
├── database_connection.py       # MySQL database connection module
├── analytics_engine.py         # Analytics queries and data export
├── main.py                     # Main pipeline script
├── requirements.txt            # Python dependencies
├── data_exports/               # Generated CSV files (created when running)
└── README.md                   # This file
```

## Database Schema

The project uses a MySQL database `OnlineCourseDB` with the following tables:
- `user` - User information and subscription types
- `cat` - Course categories
- `course` - Course details and metadata
- `erp` - Enrollments and course progress
- `course_interactions` - User interaction tracking
- `subscriptions` - Subscription and payment data

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Database Connection
Update the database credentials in `main.py`:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'OnlineCourseDB'
}
```

### 3. Run Analytics Pipeline
```bash
python main.py
```

This will:
- Connect to your MySQL database
- Execute all analytics queries
- Export results to CSV files in `data_exports/` folder

## Generated CSV Files

The pipeline generates the following CSV files for Excel import:

### User Analytics
- `user_distribution.csv` - Subscription type distribution
- `user_registration_trends.csv` - User registration trends over time

### Course Analytics
- `course_popularity.csv` - Top performing courses
- `course_completion_rates.csv` - Completion rates by course level

### Revenue Analytics
- `revenue_metrics.csv` - Revenue breakdown by subscription plan
- `churn_analysis.csv` - Churn rates by plan type

### Engagement Analytics
- `user_engagement.csv` - User engagement by subscription type
- `cohort_analysis.csv` - User retention analysis

### Platform KPIs
- `platform_kpis.csv` - Overall platform metrics

## Excel Dashboard Creation

After running the pipeline:

1. **Open Excel** and create a new workbook
2. **Import CSV files** into separate sheets
3. **Create pivot tables** for data analysis
4. **Build charts** and visualizations
5. **Design dashboard layout** with KPI cards
6. **Add slicers** for interactivity

### Recommended Dashboard Structure

- **Dashboard Sheet**: Main overview with KPIs and key charts
- **User Analytics Sheet**: User distribution and trends
- **Course Analytics Sheet**: Course performance metrics
- **Revenue Analytics Sheet**: Revenue and subscription analysis
- **Engagement Analytics Sheet**: User engagement and retention

## Analytics Queries

The project includes comprehensive SQL analytics:

- User subscription distribution and trends
- Course popularity and completion rates
- Revenue analysis and churn metrics
- User engagement and cohort analysis
- Platform-wide KPIs

## Troubleshooting

### Database Connection Issues
- Verify MySQL server is running
- Check database credentials
- Ensure `OnlineCourseDB` database exists
- Verify user has proper permissions

### Missing Data
- Check if tables have data
- Verify table names match the schema
- Run individual queries to test data availability

### CSV Export Issues
- Ensure write permissions in project directory
- Check available disk space
- Verify pandas installation

## Next Steps

1. Run the analytics pipeline to generate CSV files
2. Create Excel dashboard using the exported data
3. Set up data refresh automation (optional)
4. Customize charts and visualizations as needed

## Support

For issues or questions, refer to the project specification files in `.kiro/specs/course-platform-analytics/`