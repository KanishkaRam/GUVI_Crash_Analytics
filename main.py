import streamlit as st
import pandas as pd
from PIL import Image
import csv
import mysql.connector
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.express as px


page_bg_img =""" 
<style>
[data-testid ="stSidebarContent"]{
background-color :#566606;
font-size: x-large;
font-family: sans-serif;
}
</style>
"""

st.title('**TRAFFIC CRASH ANALYTICS & SAFETY INTELLIGENCE PLATFORM**')


# MySQL Connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="crash"
)

cursor = connection.cursor()

# CSV Path
path = r"C:\Users\RAaM\OneDrive\Desktop\Traffic Crash Project\Traffic_CrashesData.csv"

# Insert data from CSV file to Mysql table
# query ="""
#     INSERT INTO traffic_crashes (
#     CRASH_RECORD_ID,
#     CRASH_DATE,
#     POSTED_SPEED_LIMIT,
#     TRAFFIC_CONTROL_DEVICE,
#     DEVICE_CONDITION,
#     WEATHER_CONDITION,
#     LIGHTING_CONDITION,
#     FIRST_CRASH_TYPE,
#     TRAFFICWAY_TYPE,
#     ALIGNMENT,
#     ROADWAY_SURFACE_COND,
#     ROAD_DEFECT,
#     REPORT_TYPE,
#     CRASH_TYPE,
#     DAMAGE,
#     DATE_POLICE_NOTIFIED,
#     PRIM_CONTRIBUTORY_CAUSE,
#     SEC_CONTRIBUTORY_CAUSE,
#     STREET_NO,
#     STREET_DIRECTION,
#     STREET_NAME,
#     BEAT_OF_OCCURRENCE,
#     NUM_UNITS,
#     MOST_SEVERE_INJURY,
#     INJURIES_TOTAL,
#     INJURIES_FATAL,
#     INJURIES_INCAPACITATING,
#     INJURIES_NON_INCAPACITATING,
#     INJURIES_REPORTED_NOT_EVIDENT,
#     INJURIES_NO_INDICATION,
#     INJURIES_UNKNOWN,
#     CRASH_HOUR,
#     CRASH_DAY_OF_WEEK,
#     CRASH_MONTH,
#     LATITUDE,
#     LONGITUDE,
#     LOCATION,
#     date,
#     year
# )
# VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s)
# """
# batch_size = 1000
# data_batch = []

# with open(path, mode='r', encoding='utf-8') as csv_file:

#     csv_reader = csv.reader(csv_file)
#     header = next(csv_reader)
#     print("Total Header Columns:", len(header))
#     for row_number, row in enumerate(csv_reader, start=1):

#         try:
#             row = [None if value == '' else value for value in row]  ## Convert '' values to null 
#             if row[1]:    ## Convert CRASH_DATE Format
#                 row[1] = datetime.strptime(row[1], "%m/%d/%Y %I:%M:%S %p")

#             if row[15]:  ## Convert DATE_POLICE_NOTIFIED Format
#                 row[15] = datetime.strptime(row[15], "%m/%d/%Y %I:%M:%S %p" )

#             cursor.execute(query, tuple(row))

#         except Exception as e:
#             print(f"Error at row {row_number}")
#             print(e)
#             print(row)
#             break

#         connection.commit()

# print("CSV data inserted successfully!")

# # Close
# cursor.close()
# connection.close() 


st.markdown(page_bg_img, unsafe_allow_html=True)
menu = st.sidebar.radio('**MENU**' , ['*Home*','*Analytics*'])

if menu =='*Home*':    
    st.write("Traffic crash data contains valuable insights that can help improve road safety, optimize emergency response, and support policy decisions. ")
    img = Image.open(r"C:\Users\RAaM\OneDrive\Desktop\Traffic Crash Project\car_crash.webp")
    st.image(img, caption='Crash Analysis')

if menu == '*Analytics*' :
    option = st.selectbox('',  
                          [ "CHOOSE A CRASH ANALYSIS:",
                           " Top 5 most dangerous combinations of weather and crash type", 
                           " Top 10 streets with the highest number of injury crashes",
                           " Percentage of crashes that resulted in injuries for each crash type",
                           " Peak crash hour for each month",
                           " Top 5 primary causes of crashes during night time", 
                           " Average number of injuries in daylight vs darkness conditions",
                           " Traffic control device type has the highest average injuries per crash",
                           " Top 5 locations (latitude/longitude) with the highest crash frequency",
                           " Top 5 streets with the highest injury rate", 
                           " Most common crash type",
                           " Day of the week with the highest average crashes per hour",
                           " High-risk time slots",
                           " Top 3 contributing causes for each crash type", 
                           " Year-over-year growth rate of crashes",
                           " Hotspot zones"
                            ]
                        )
    
    if option == " Top 5 most dangerous combinations of weather and crash type":
        st.write("Top 5 most dangerous combinations of weather and crash type")
        query ="""SELECT WEATHER_CONDITION, CRASH_TYPE, COUNT(*) AS total_crashes
                    FROM Traffic_Crashes
                    GROUP BY WEATHER_CONDITION, CRASH_TYPE
                    ORDER BY total_crashes DESC
                    LIMIT 5;"""
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data,  columns=["WEATHER_CONDITION", "CRASH_TYPE", "TOTAL_CRASHES"] )
        st.table(df)
        if st.button("Show Graph"):
            # Combine labels
            df["Combination"] = df["WEATHER_CONDITION"] + " + " + df["CRASH_TYPE"]
            st.subheader("Top 5 Dangerous Weather + Crash Combinations")
            st.bar_chart(data=df, x="Combination", y="TOTAL_CRASHES" ,horizontal=True)

    if option == " Top 10 streets with the highest number of injury crashes":
        st.write("Top 10 streets with the highest number of injury crashes")
        query ="""SELECT STREET_NAME, COUNT(*) AS injury_crash_count
                    FROM Traffic_Crashes
                    WHERE CRASH_TYPE LIKE 'INJURY %'
                    GROUP BY STREET_NAME
                    ORDER BY injury_crash_count DESC
                    LIMIT 10;"""
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data,  columns=["STREET_NAME", "INJURY_CRASH_COUNT"] )
        st.table(df)
        if st.button("Show Graph"):
            st.subheader("Top 10 streets with the highest number of injury crashes")
            st.bar_chart(data=df, x="STREET_NAME", y="INJURY_CRASH_COUNT" )
    
    if option == " Percentage of crashes that resulted in injuries for each crash type":
        st.write("Percentage of crashes that resulted in injuries for each crash type")
        query ="""SELECT CRASH_TYPE,  ROUND( ( SUM(INJURIES_TOTAL) * 100.0) / COUNT(*),  2) AS injury_percentage
                    FROM Traffic_Crashes
                    GROUP BY CRASH_TYPE
                    ORDER BY injury_percentage DESC;"""
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data,  columns=["CRASH_TYPE", "INJURY_PERCENTAGE"] )
        st.table(df)
        colors = ['#FF9999', '#66B3FF', ]
        if st.button("Show Graph"):
            fig = px.pie(df, values="INJURY_PERCENTAGE", names="CRASH_TYPE", title="Injury Percentage by Crash Type" ,color=colors)
            st.plotly_chart(fig)


    if option == " Peak crash hour for each month":
        st.write("Peak crash hour for each month")
        query ="""SELECT  CRASH_MONTH,   CRASH_HOUR    
                    FROM (    
                        SELECT CRASH_MONTH,  CRASH_HOUR,  RANK() OVER ( PARTITION BY CRASH_MONTH  ORDER BY COUNT(*) DESC) AS rank_num        
                        FROM Traffic_Crashes    
                        GROUP BY CRASH_MONTH, CRASH_HOUR
                    ) AS ranked_data
                    WHERE rank_num = 1
                    ORDER BY CRASH_MONTH;"""
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data,  columns=["CRASH_MONTH", "PEAK_CRASH_HOUR"] )
        st.table(df)
        if st.button("Show Graph"):
         st.scatter_chart(df, x="CRASH_MONTH", y="PEAK_CRASH_HOUR", x_label="CRASH_MONTH", y_label="PEAK_CRASH_HOUR")

    if option == " Top 5 primary causes of crashes during night time":
        st.write("Top 5 primary causes of crashes during night time")    
        query ="""SELECT  PRIM_CONTRIBUTORY_CAUSE, COUNT(*) AS total_crashes
                    FROM Traffic_Crashes
                    WHERE CRASH_HOUR >= 18
                    GROUP BY PRIM_CONTRIBUTORY_CAUSE
                    ORDER BY total_crashes DESC
                    LIMIT 5;"""
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data,  columns=["PRIMARY_CAUSE_OF_CRASH", "TOTAL_CRASHES"] )
        st.table(df)
        if st.button("Show Graph"):
           st.line_chart(df, x="PRIMARY_CAUSE_OF_CRASH", y="TOTAL_CRASHES", x_label="PRIMARY_CAUSE_OF_CRASH", y_label="TOTAL_CRASHES")
            


    if option == " Average number of injuries in daylight vs darkness conditions":
        st.write("Average number of injuries in daylight vs darkness conditions")
        query ="""SELECT LIGHTING_CONDITION,ROUND(AVG(INJURIES_TOTAL), 2) AS avg_injuries
                    FROM Traffic_Crashes
                    WHERE LIGHTING_CONDITION IN ('DAYLIGHT', 'DARKNESS')
                    GROUP BY LIGHTING_CONDITION;"""
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data,  columns=["LIGHTING_CONDITION", "AVERAGE_INJURIES"] )
        st.table(df)
        if st.button("Show Graph"):
           fig = px.bar(df,x="LIGHTING_CONDITION",y="AVERAGE_INJURIES", color="LIGHTING_CONDITION"    )
           st.plotly_chart(fig, use_container_width=True)

    if option == " Traffic control device type has the highest average injuries per crash":
        st.write("Traffic control device type has the highest average injuries per crash")
        query ="""SELECT TRAFFIC_CONTROL_DEVICE, ROUND(AVG(INJURIES_TOTAL), 2) AS avg_injuries_per_crash 
                    FROM Traffic_Crashes
                    GROUP BY TRAFFIC_CONTROL_DEVICE
                    ORDER BY avg_injuries_per_crash DESC
                    LIMIT 1;"""
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data,  columns=["TRAFFIC_CONTROL_DEVICE", "AVERAGE_INJURIES_PER_CRASH"] )
        st.table(df)
        
    if option == " Top 5 locations (latitude/longitude) with the highest crash frequency":
        st.write("Top 5 locations (latitude/longitude) with the highest crash frequency")
        query ="""SELECT LATITUDE, LONGITUDE , COUNT(*) AS total_crashes
                    FROM Traffic_Crashes
                    GROUP BY LATITUDE, LONGITUDE 
                    ORDER BY total_crashes DESC
                    LIMIT 5;"""
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data,  columns=["LATITUDE", "LONGITUDE", "TOTAL_CRASHES"] )
        st.table(df)
        if st.button("Show Graph"):
            st.subheader("Top 5 locations (latitude/longitude) with the highest crash frequency")
            fig = px.scatter(df,  x="LONGITUDE", y="LATITUDE", size="TOTAL_CRASHES", color="TOTAL_CRASHES")
            st.plotly_chart(fig)

    
    if option == " Top 5 streets with the highest injury rate":
        st.write("Top 5 streets with the highest injury rate")
        query ="""SELECT STREET_NAME,  ROUND(  ( SUM(INJURIES_TOTAL) * 100.0 ) / COUNT(*), 2 ) AS injury_rate_percentage
                    FROM Traffic_Crashes
                    GROUP BY STREET_NAME
                    HAVING COUNT(*) >100
                    order by injury_rate_percentage DESC
                    LIMIT 5;"""
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data,  columns=["STREET_NAME", "INJURY_RATE_PERCENTAGE"] )
        st.table(df)
        if st.button("Show Graph"):
            st.subheader("Top 5 streets with the highest injury rate")
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.vlines( x=df["STREET_NAME"],ymin=0, ymax=df["INJURY_RATE_PERCENTAGE"])
            ax.scatter( df["STREET_NAME"], df["INJURY_RATE_PERCENTAGE"], s=100)
            ax.set_xlabel("STREET_NAME")
            ax.set_ylabel("INJURY_RATE_PERCENTAGE")
            ax.set_title("STREETS WITH HIGHEST INJURY RATE")
            st.pyplot(fig)
                
    if option == " Most common crash type":
        st.write("Most common crash type")    
        query ="""SELECT year, CRASH_TYPE
                    FROM (
                        SELECT year, CRASH_TYPE, COUNT(*) AS total_crashes,
                            RANK() OVER (PARTITION BY year  ORDER BY COUNT(*) DESC ) AS rank_num
                        FROM Traffic_Crashes
                        GROUP BY year, CRASH_TYPE
                        ) AS ranked_crashes
                    WHERE rank_num = 1
                    ORDER BY year;"""
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data,  columns=["year", "CRASH_TYPE"] )
        st.table(df)
     

    if option == " Day of the week with the highest average crashes per hour":
        st.write("Day of the week with the highest average crashes per hour")
        query ="""SELECT CRASH_DAY_OF_WEEK,  ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT CRASH_HOUR),2) AS avg_crashes_per_hour
                    FROM Traffic_Crashes
                    GROUP BY CRASH_DAY_OF_WEEK
                    ORDER BY avg_crashes_per_hour DESC
                    LIMIT 1;"""
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data,  columns=["CRASH_DAY_OF_WEEK", "AVERAGE_CRASHES_PER_HOUR"] )
        st.table(df)
       

    if option == " High-risk time slots":
        st.write("High-risk time slots")
        query ="""SELECT time_bucket, COUNT(*) AS injury_crashes
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
                    LIMIT 1;"""
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data,  columns=["TIME_BUCKET", "INJURY_CRASHES"] )
        st.table(df)
       
            
    if option == " Top 3 contributing causes for each crash type":
        st.write("Top 3 contributing causes for each crash type")
        query =""" SELECT PRIM_CONTRIBUTORY_CAUSE, CRASH_TYPE
        FROM (
            SELECT PRIM_CONTRIBUTORY_CAUSE, CRASH_TYPE,   COUNT(*) AS total_crashes,
            RANK() OVER (PARTITION BY PRIM_CONTRIBUTORY_CAUSE  ORDER BY COUNT(*) DESC ) AS rank_num
            FROM Traffic_Crashes
            GROUP BY PRIM_CONTRIBUTORY_CAUSE, CRASH_TYPE
        ) AS ranked_crashes
        WHERE rank_num = 1
        ORDER BY PRIM_CONTRIBUTORY_CAUSE
        LIMIT 3;"""
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data,  columns=["PRIM_CONTRIBUTORY_CAUSE", "CRASH_TYPE"] )
        st.table(df)
        

    if option == " Year-over-year growth rate of crashes":
        st.write("Year-over-year growth rate of crashes")
        query ="""SELECT year, 
                    ROUND(((total_crashes - LAG(total_crashes) OVER (ORDER BY year))  * 100.0)  /LAG(total_crashes) OVER (ORDER BY year),  2) AS yoy_growth_rate
                FROM (
                    SELECT  year, COUNT(*) AS total_crashes
                    FROM Traffic_Crashes
                    GROUP BY year
                ) AS yearly_crashes
                ORDER BY year;"""
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data,  columns=["YEAR", "YEAR_OVER_YEAR_GROWTH_RATE"] )
        st.table(df)
        if st.button("Show Graph"):
            #st.subheader("YEAR-OVER-YEAR GROWTH RATE OF CRASHES")
            #st.line_chart(df, x="YEAR", y="YEAR_OVER_YEAR_GROWTH_RATE" )
            plot_df = df.dropna()
            fig = px.line(plot_df,x="YEAR", y="YEAR_OVER_YEAR_GROWTH_RATE",markers=True,title="Year-Over-Year Growth Rate of Crashes")
            fig.update_layout( xaxis_title="Year",yaxis_title="Growth Rate (%)"  )
            st.plotly_chart(fig, use_container_width=True)
            
    if option == " Hotspot zones":
        st.write("Hotspot zones")
        query ="""SELECT  
                    ROUND(LATITUDE, 2) AS hotspot_latitude,
                    ROUND(LONGITUDE, 2) AS hotspot_longitude,
                    COUNT(*) AS total_crashes
                FROM Traffic_Crashes
                GROUP BY    ROUND(LATITUDE, 2),    ROUND(LONGITUDE, 2)
                ORDER BY total_crashes DESC
                LIMIT 10;"""
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data,  columns=["LATITUDE", "LONGITUDE", "TOTAL_CRASHES"] )
        st.table(df)
        if st.button("Show Graph"):
           fig = px.scatter(df,x="LONGITUDE",  y="LATITUDE",size="TOTAL_CRASHES", color="TOTAL_CRASHES", hover_data=["TOTAL_CRASHES"], title="Top 10 Crash Hotspot Zones" )
           st.plotly_chart(fig, use_container_width=True)