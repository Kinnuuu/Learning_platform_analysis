CREATE DATABASE OnlineCourseDB;

USE OnlineCourseDB;
create table user (
user_id int primary key ,
userName varchar(50) unique not null,
email varchar(50),
first_name varchar(50) not null,
last_name varchar(50) not null,
subscription_type enum('free','premium','pro') default 'free',
regi_date timestamp default current_timestamp,
last_login timestamp,
country varchar(50),
is_active boolean default true
);

create table cat
(
cat_id int primary key auto_increment,
cat_name varchar(50) not null,
description text,
created_at timestamp default current_timestamp
);

create table course
(
course_id int primary key auto_increment,
course_title varchar(500) not null,
course_url varchar(500),
price decimal(10,2),
num_subscription int default 0,
num_review int default 0,
num_lec int default 0,
level varchar(50),
content_duration decimal(10,2),
publised_timestamp timestamp,
subject varchar(100),
instructor_name varchar(200),
is_paid boolean default false,
cat_id int,
created_at timestamp default current_timestamp,
foreign key (cat_id) 
references cat(cat_id)
);

create table erp(
erp_id int primary key auto_increment,
user_id int,
course_id int,
erp_date timestamp default current_timestamp,
completion_status enum('not_started', 'in_progress', 'completed') default 'not_started',
progress_per int default 0,
rating_given int check(rating_given between 1 and 5),
foreign key (user_id) references user (user_id),
foreign key (course_id) references course(course_id)
);

create table course_interactions(
interaction_id int primary key auto_increment,
user_id int,
course_id int,
interaction_type enum('view', 'enroll', 'complete', 'rate', 'review') not null,
interaction_data timestamp default current_timestamp,
session_duration int,
foreign key (user_id) references user (user_id),
foreign key (course_id) references course(course_id)
);

create table subscriptions(
subscription_id int primary key auto_increment,
user_id int,
plan_type enum('premiun','pro') not null,
start_date date not null,
end_date date not null,
monthely_fee decimal (10,2) not null,
status enum('active', 'expired', 'cancelled') default 'active',
foreign key (user_id) references user (user_id)
);

alter table subscriptions
modify column plan_type enum('premium','pro')not null;

show columns from subscriptions;
SHOW VARIABLES WHERE Variable_name = 'hostname';

--  Analytics queries

SELECT
    subscription_type,
    COUNT(*) AS user_count,
    ROUND(COUNT(*) / (SELECT COUNT(*) FROM user) * 100, 2) AS percentage 
FROM user
GROUP BY subscription_type
ORDER BY user_count DESC;

-- premium vs free users trend over time 
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
    subscription_type;

SHOW COLUMNS FROM user;

show tables;

-- course popularity analysis
select
	c.course_title,
	c.instructor_name,
	c.subject,
	count(e.erp_id) as total_erps,
	avg(e.rating_given) as avg_rating,
    c.price
from course c
left join erp e on c.course_id = e.course_id
group by c.course_id
order by total_erps desc
limit 10;

-- course interaction analysis
USE  OnlineCourseDB;  -- Replace with your real database name

SELECT 
    c.subject,
    COUNT(DISTINCT ci.user_id) AS unique_users_interacted,
    COUNT(ci.intraction_id) AS total_interactions,
    AVG(ci.session_duration) AS avg_session_duration
FROM course c
JOIN course_intractions ci
    ON c.course_id = ci.course_id
GROUP BY c.subject
ORDER BY total_interactions DESC;

show databases;

show columns from course_interactions;

show tables;

SHOW TABLES LIKE '%interact%';
SHOW TABLES LIKE '%course%'; 

SELECT table_schema, table_name 
FROM information_schema.tables 
WHERE table_name LIKE '%interact%';

SHOW GRANTS;

-- revenue analyze
select 
	s.plan_type,
    count(*) as active_subscriptions,
    sum(s.monthely_fee) as monthely_revenue,
    avg(s.monthely_fee) as avg_monthely_fee
from subscriptions s
where s.status = 'active'
group by s.plan_type;

-- User Engagement metrics
select 
	u.subscription_type,
    count(distinct e.course_id) as avg_courses_enrolled,
    avg(e.progress_per) as avg_completion_rate,
    count(distinct ci.interaction_id) as total_interactions
from user u
left join erp e on u.user_id = e.user_id
left join course_interactions ci on u.user_id = ci.user_id
group by u.subscription_type;
    
describe erp;

-- course completion rate
select
    c.level,
    count(*) as total_erps,
    count(case when e.completion_status = 'completed' then 1 end) as completions,
    round(
        count(case when e.completion_status = 'completed' then 1 end) * 100.0/count(*),
        2
    ) as completion_rate
from course c
join erp e on c.course_id = e.course_id
group by c.level;

describe user;

-- ADVANCE ANALYTICS
-- cohort analysis

select
	date_format(u.regi_date, '%Y-%m') as registration_month,
    count(distinct u.user_id) as total_users,
    count(distinct case when u.last_login >= date_sub(now(), interval 30 day) then u.user_id end) as active_last_30_days,
    round(
		count(distinct case when u.last_login >= date_sub(now(), interval 30 day) then u.user_id end) * 100.0/ count(distinct u.user_id),
        2
        ) as retention_rate
from user u
group by date_format(u.regi_date, '%Y-%m')
order by registration_month;

-- churn analysis

select
	s.plan_type,
    count(*) as total_subscriptions,
    count(case when s.status = 'cancelled' then 1 end) as churned,
    round(count(case when s.status = 'cancelled' then 1 end)* 100.0/count(*), 2) as churn_rate
from subscriptions s
group by s.plan_type;

-- overall platfrom KPIs
select
	 (Select count(*) from user where is_active = TRUE) as total_active_users,
     (select count(*) from user where subscription_type != 'free') as paid_users,
     (select count(*) from course) as total_courses,
     (select sum(monthely_fee) from subscriptions where status = 'active') as monthely_recurring_revenue,
     (select avg(rating_given) from erp where rating_given is not null) as avg_course_rating;
     
     -- Quick test queries
SELECT COUNT(*) FROM user;
SELECT COUNT(*) FROM cours;
SELECT COUNT(*) FROM erp;

-- Test one analytics query
SELECT subscription_type, COUNT(*) FROM user GROUP BY subscription_type;

-- Add more users for better analytics
INSERT INTO user (user_id, username, email, first_name, last_name, subscription_type, country, last_login) VALUES
(1, 'alex_martin', 'alex@email.com', 'Alex', 'Martin', 'free', 'Spain', '2024-06-12 12:00:00'),
(2, 'emma_davis', 'emma@email.com', 'Emma', 'Davis', 'premium', 'Italy', '2024-06-17 16:30:00'),
(3, 'chris_lee', 'chris@email.com', 'Chris', 'Lee', 'pro', 'South Korea', '2024-06-20 09:45:00');

-- Add more enrollments
INSERT INTO erp (user_id, course_id, completion_status, progress_per, rating_given) VALUES
(9, 1, 'in_progress', 25, NULL),
(10, 3, 'completed', 100, 4),
(11, 7, 'not_started', 0, NULL);

SELECT * FROM user WHERE user_id IN (9, 10, 11);

-- Compare column types
DESCRIBE user;
DESCRIBE erp;

-- Verify the join works
SELECT u.user_id, c.course_id
FROM user u
CROSS JOIN course c
WHERE u.user_id IN (9, 10, 11)
AND c.course_id IN (1, 3, 7);


-- Check all required foreign keys exist
SELECT 
  (SELECT COUNT(*) FROM user WHERE user_id = 9) as user_9_exists,
  (SELECT COUNT(*) FROM user WHERE user_id = 10) as user_10_exists,
  (SELECT COUNT(*) FROM user WHERE user_id = 11) as user_11_exists,
  (SELECT COUNT(*) FROM course WHERE course_id = 1) as course_1_exists,
  (SELECT COUNT(*) FROM course WHERE course_id = 3) as course_3_exists,
  (SELECT COUNT(*) FROM course WHERE course_id = 7) as course_7_exists;
  
  

-- Check if the record inserted
SELECT * FROM erp WHERE user_id = 11 AND course_id = 7;

-- Check constraints are properly enforced
SELECT @@foreign_key_checks;


USE OnlineCourseDB;

-- Create the erp table (enrollments)
CREATE TABLE IF NOT EXISTS erp (
    erp_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    course_id INT,
    erp_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completion_status ENUM('not_started', 'in_progress', 'completed') DEFAULT 'not_started',
    progress_per INT DEFAULT 0,
    rating_given INT CHECK(rating_given BETWEEN 1 AND 5),
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

-- Create subscriptions table (with monthely_fee spelling)
CREATE TABLE IF NOT EXISTS subscriptions (
    subscription_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    plan_type ENUM('premium', 'pro') NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    monthely_fee DECIMAL(10, 2) NOT NULL,
    status ENUM('active', 'expired', 'cancelled') DEFAULT 'active',
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

DESCRIBE subscriptions;


-- Check for active subscriptions
SELECT plan_type, COUNT(*) 
FROM subscriptions 
WHERE status = 'active'
GROUP BY plan_type;

drop table erp;
describe erp;

create table erp(
erp_id int primary key auto_increment,
user_id int,
course_id int,
erp_date timestamp default current_timestamp,
completion_status enum('not_started', 'in_progress', 'completed') default 'not_started',
progress_per int default 0,
rating_given int check(rating_given between 1 and 5),
foreign key (user_id) references user (user_id),
foreign key (course_id) references course(course_id)
);

describe erp;