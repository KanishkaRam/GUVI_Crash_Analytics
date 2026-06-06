create database crash;

use crash; 


CREATE TABLE Traffic_Crashes (
    CRASH_RECORD_ID VARCHAR(150),
    CRASH_DATE DATETIME,
    POSTED_SPEED_LIMIT INT,
    TRAFFIC_CONTROL_DEVICE VARCHAR(100),
    DEVICE_CONDITION VARCHAR(100),
    WEATHER_CONDITION VARCHAR(100),
    LIGHTING_CONDITION VARCHAR(100),
    FIRST_CRASH_TYPE VARCHAR(100),
    TRAFFICWAY_TYPE VARCHAR(150),
    ALIGNMENT VARCHAR(100),
    ROADWAY_SURFACE_COND VARCHAR(100),
    ROAD_DEFECT VARCHAR(100),
    REPORT_TYPE VARCHAR(100),
    CRASH_TYPE VARCHAR(100),
    DAMAGE VARCHAR(100),
    DATE_POLICE_NOTIFIED DATETIME,
    PRIM_CONTRIBUTORY_CAUSE VARCHAR(255),
    SEC_CONTRIBUTORY_CAUSE VARCHAR(255),
    STREET_NO INT,
    STREET_DIRECTION VARCHAR(10),
    STREET_NAME VARCHAR(150),
    BEAT_OF_OCCURRENCE FLOAT,
    NUM_UNITS INT,
    MOST_SEVERE_INJURY VARCHAR(100),
    INJURIES_TOTAL FLOAT,
    INJURIES_FATAL FLOAT,
    INJURIES_INCAPACITATING FLOAT,
    INJURIES_NON_INCAPACITATING FLOAT,
    INJURIES_REPORTED_NOT_EVIDENT FLOAT,
    INJURIES_NO_INDICATION FLOAT,
    INJURIES_UNKNOWN FLOAT,
    CRASH_HOUR INT,
    CRASH_DAY_OF_WEEK INT,
    CRASH_MONTH INT,
    LATITUDE DECIMAL(10,6),
    LONGITUDE DECIMAL(10,6),
    LOCATION VARCHAR(255),
    date DATETIME,
    year INT
);

select *  from traffic_crashes;

# Find the top 5 most dangerous combinations of weather and crash type based on total crashes.
SELECT WEATHER_CONDITION, CRASH_TYPE, COUNT(*) AS total_crashes
FROM Traffic_Crashes
GROUP BY WEATHER_CONDITION, CRASH_TYPE
ORDER BY total_crashes DESC
LIMIT 5;

# Identify the top 10 streets with the highest number of injury crashes. 
SELECT STREET_NAME, COUNT(*) AS injury_crash_count
FROM Traffic_Crashes
WHERE CRASH_TYPE LIKE 'INJURY %'
GROUP BY STREET_NAME
ORDER BY injury_crash_count DESC
LIMIT 10;

# Find the percentage of crashes that resulted in injuries for each crash type.
SELECT CRASH_TYPE,  ROUND( ( SUM(INJURIES_TOTAL) * 100.0) / COUNT(*),  2) AS injury_percentage
FROM Traffic_Crashes
GROUP BY CRASH_TYPE
ORDER BY injury_percentage DESC;

# Determine the peak crash hour for each month
SELECT  CRASH_MONTH,   CRASH_HOUR    
FROM (    
    SELECT CRASH_MONTH,  CRASH_HOUR,  RANK() OVER ( PARTITION BY CRASH_MONTH  ORDER BY COUNT(*) DESC) AS rank_num        
    FROM Traffic_Crashes    
    GROUP BY CRASH_MONTH, CRASH_HOUR
) AS ranked_data
WHERE rank_num = 1
ORDER BY CRASH_MONTH;
 
 #Find the top 5 primary causes of crashes during night time (CRASH_HOUR ≥ 18). 
SELECT  PRIM_CONTRIBUTORY_CAUSE, COUNT(*) AS total_crashes
FROM Traffic_Crashes
WHERE CRASH_HOUR >= 18
GROUP BY PRIM_CONTRIBUTORY_CAUSE
ORDER BY total_crashes DESC
LIMIT 5;

# Compare average number of injuries in daylight vs darkness conditions. 
SELECT LIGHTING_CONDITION,ROUND(AVG(INJURIES_TOTAL), 2) AS avg_injuries
FROM Traffic_Crashes
WHERE LIGHTING_CONDITION IN ('DAYLIGHT', 'DARKNESS')
GROUP BY LIGHTING_CONDITION;
 
 
#Find which traffic control device type has the highest average injuries per crash.
SELECT TRAFFIC_CONTROL_DEVICE, ROUND(AVG(INJURIES_TOTAL), 2) AS avg_injuries_per_crash 
FROM Traffic_Crashes
GROUP BY TRAFFIC_CONTROL_DEVICE
ORDER BY avg_injuries_per_crash DESC
LIMIT 1;

#Identify the top 5 locations (latitude/longitude) with the highest crash frequency. 
SELECT LATITUDE, LONGITUDE , COUNT(*) AS total_crashes
FROM Traffic_Crashes
GROUP BY LATITUDE, LONGITUDE 
ORDER BY total_crashes DESC
LIMIT 5;

# Find the top 5 streets with the highest injury rate, considering only streets with more than 100 crashes.
SELECT STREET_NAME,  ROUND(  ( SUM(INJURIES_TOTAL) * 100.0 ) / COUNT(*), 2 ) AS injury_rate_percentage
FROM Traffic_Crashes
GROUP BY STREET_NAME
HAVING COUNT(*) >100
order by injury_rate_percentage DESC
LIMIT 5;


#For each year, identify the most common crash type. 
SELECT year, CRASH_TYPE
FROM (
    SELECT year, CRASH_TYPE,   COUNT(*) AS total_crashes,
        RANK() OVER (PARTITION BY year  ORDER BY COUNT(*) DESC ) AS rank_num
    FROM Traffic_Crashes
    GROUP BY year, CRASH_TYPE
    ) AS ranked_crashes
WHERE rank_num = 1
ORDER BY year;

#Find the day of the week with the highest average crashes per hour.   
SELECT CRASH_DAY_OF_WEEK,  ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT CRASH_HOUR),2) AS avg_crashes_per_hour
FROM Traffic_Crashes
GROUP BY CRASH_DAY_OF_WEEK
ORDER BY avg_crashes_per_hour DESC
LIMIT 1;

# Identify high-risk time slots:  Group hours into buckets (Morning, Afternoon, Evening, Night)    Find which bucket has the highest injury crashes
SELECT time_bucket, COUNT(*) AS injury_crashes
FROM (
    SELECT 
        CASE       
            WHEN CRASH_HOUR BETWEEN 5 AND 11
                THEN 'Morning'
			WHEN CRASH_HOUR BETWEEN 12 AND 16
                THEN 'Afternoon'
            WHEN CRASH_HOUR BETWEEN 17 AND 20
                THEN 'Evening'                
            ELSE 'Night'
        END AS time_bucket
    FROM Traffic_Crashes
) AS grouped_data
GROUP BY time_bucket
ORDER BY injury_crashes DESC
LIMIT 1;


#Find the top 3 contributing causes for each crash type.   (Use window functions like ROW_NUMBER() or RANK())
 
 
 
 #Calculate the year-over-year growth rate of crashes.   (Use LAG() window function)
SELECT year, 
    ROUND(((total_crashes - LAG(total_crashes) OVER (ORDER BY year))  * 100.0)  /LAG(total_crashes) OVER (ORDER BY year),  2) AS yoy_growth_rate
FROM (
    SELECT  year, COUNT(*) AS total_crashes
    FROM Traffic_Crashes
    GROUP BY year
) AS yearly_crashes
ORDER BY year;


#Identify hotspot zones: Group nearby locations (round latitude & longitude to 2 decimal places)   Find top 10 zones with highest crashes

SELECT  
    ROUND(LATITUDE, 2) AS hotspot_latitude,
    ROUND(LONGITUDE, 2) AS hotspot_longitude,
    COUNT(*) AS total_crashes
FROM Traffic_Crashes
GROUP BY    ROUND(LATITUDE, 2),    ROUND(LONGITUDE, 2)
ORDER BY total_crashes DESC
LIMIT 10;
 


SELECT * FROM  Traffic_Crashes

