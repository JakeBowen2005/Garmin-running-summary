import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time_pace_func
import bar_graph_functions
import scatter_regression_functions
import dual_axis_graphs
import email_functions
import sys
import os
import db

#Creating the database
db.init_db()


# Get path to the summaries folder
current_dir = os.path.dirname(os.path.realpath(__file__))
summaries_folder = os.path.join(current_dir, "output", "summaries")

# Add it to Python path
sys.path.append(summaries_folder)

import sum_functions

my_email = "jakeeb05@gmail.com"
my_password = "jsyvqmqwkfxilewg"
#Steps
#Get and clean data / make sure all strings are numbers, missing values are filled and we added the columns we need to summarize

# /Users/jakebowen/Desktop/Pandas/Garmin Data/Activities.csv


user_email = input("Enter email you want summary sent to: ").strip()
user_id = db.get_or_create_user(user_email)

file =input("Input path to garmin csv or drop csv file in terminal: ").strip()
# user_email = input("Input email to send data to: ").strip()
file = file.replace("\\ ", " ") 
data = pd.read_csv(f"{file}")


#Date
data["Date"] = pd.to_datetime(data["Date"])

#Weekday and week columns
data["Weekday"] = data["Date"].dt.day_name()
data["Week_Start"] = data["Date"].dt.to_period("W-SUN").apply(lambda r: r.start_time)
data["Week"] = data["Week_Start"].rank(method="dense").astype(int)


#Turning the strings into numbers
#Filling in missing values with 0
data = data.copy()
cols = ["Distance", "Calories", "Steps", "Total Ascent", "Total Descent", "Avg HR", "Max HR"]
for col in cols:
    data[col] = data[col].astype(str).str.replace(",","").replace("--", "0").astype(float)

#Change the time and paces into integers instead of strings
data["Time"] = data["Time"].apply(time_pace_func.time_converter)
data["Avg Pace"] = data["Avg Pace"].apply(time_pace_func.pace_converter)
data["Best Pace"] = data["Best Pace"].apply(time_pace_func.pace_converter)

#Change Distances due to some being meters
data.loc[data["Distance"] > 100, "Distance"] = round(data["Distance"] / 1609.34, 2)

#Add Months columns
data["Month"] = data["Date"].dt.month_name()
months_ordered = ["January", "February", "March", "April", "May", "June","July",
                   "August", "September", "October", "November", "December"]
data["Month"] = pd.Categorical(data["Month"], ordered=True, categories=months_ordered)

#Adding Zones
zone_bins = [0,120,145,160,175,200]
zone_labels = ["Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5"]
data["Zones"] = pd.cut(data["Avg HR"], bins = zone_bins, labels = zone_labels, right=False)

#Adding Distance bins
distance_bins = [0,5,10,15,20,25,100]
distance_labels = ["0-5", "5-10", "10-15", "15-20", "20-25", "25+"]
data["Distance Ranges"] = pd.cut(data["Distance"], bins = distance_bins, labels = distance_labels, right=False)

#Lastly drop columns
data = data[["Date", "Week", "Weekday", "Month", "Distance", "Avg Pace",
             "Time", "Avg HR", "Max HR", "Best Pace",
             "Zones", "Total Ascent", "Total Descent", "Steps", 
             "Calories", "Distance Ranges"]]

#Put into SQL database
for _, row in data.iterrows():
    row = (
        row["Date"].isoformat(),
        int(row["Week"]),
        row["Weekday"],
        row["Month"],
        float(row["Distance"]),
        float(row["Avg Pace"]),
        float(row["Time"]),
        float(row["Avg HR"]),
        float(row["Max HR"]),
        float(row["Best Pace"]),
        str(row["Zones"]),
        float(row["Total Ascent"]),
        float(row["Total Descent"]),
        int(row["Steps"]),
        float(row["Calories"]),
        str(row["Distance Ranges"])
    )
    db.insert_activity(user_id, row)

#Getting all user data from SQLlite database
sql = """
SELECT
    date,
    week,
    weekday,
    month,
    distance,
    avg_pace,
    time,
    avg_hr,
    max_hr,
    best_pace,
    zones,
    ascent,
    descent,
    steps,
    calories,
    distance_range
FROM activities
WHERE user_id = ?
ORDER BY date;
"""

user_conn = db.get_connection()
all_user_data = pd.read_sql_query(sql, user_conn, params=(user_id))
user_conn.close()

#creating bar graph data
bar_graph_functions.weekly_mile_bar(all_user_data)
bar_graph_functions.monthly_mile_bar(all_user_data)
bar_graph_functions.avg_pace_per_distance_bar(all_user_data)
bar_graph_functions.avg_pace_per_zone(all_user_data)

#creating scatterplot data
scatter_regression_functions.hr_pace_scatter(all_user_data)

#dual axis data
dual_axis_graphs.miles_pace_dual(all_user_data)
dual_axis_graphs.time_miles_dual(all_user_data)

#creating the summary functions
highest_mile_week, wstart_date, wend_date = sum_functions.mile_high_week(all_user_data)
highest_mile_month, mstart_date, mend_date = sum_functions.mile_high_month(all_user_data)
most_aerobic_month = sum_functions.most_aerobic_month(all_user_data)

wstart_date = wstart_date.strftime("%b %d, %Y")
wend_date = wend_date.strftime("%b %d, %Y")

mstart_date = mstart_date.strftime("%b %d, %Y")
mend_date = mend_date.strftime("%b %d, %Y")

start_date = data["Date"].min()
start_date = start_date.strftime("%b %d %Y")
end_date = data["Date"].max()
end_date = end_date.strftime("%b %d %Y")

def create_email_test():
    text = (f"""
          Between the dates: {start_date} - {end_date}
    Your highest mileage week was {highest_mile_week} between {wstart_date} - {wend_date}.
    Your highest mileage month was {round(highest_mile_month,2)} between {mstart_date} - {mend_date}.
    Your most aerboic month was {most_aerobic_month}
          """)
    return text
    
summary_text = create_email_test()


data.to_csv("USER_data.csv")
email_functions.send_email(user_email, summary_text)
