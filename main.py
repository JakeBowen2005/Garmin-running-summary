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

# Get the path to the summary folder
current_dir = os.path.dirname(os.path.realpath(__file__))
summary_folder = os.path.join(current_dir, "summary")

# Add it to the Python path
sys.path.append(summary_folder)

import sum_functions

my_email = "jakeeb05@gmail.com"
my_password = "jsyvqmqwkfxilewg"
#Steps
#Get and clean data / make sure all strings are numbers, missing values are filled and we added the columns we need to summarize

# /Users/jakebowen/Desktop/Pandas/Garmin Data/Activities.csv


user_email = input("Enter email you want summary sent to: ")

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
cols = ["Distance", "Calories", "Steps", "Total Ascent", "Total Descent"]
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

#creating bar graph data
bar_graph_functions.weekly_mile_bar(data)
bar_graph_functions.monthly_mile_bar(data)
bar_graph_functions.avg_pace_per_distance_bar(data)
bar_graph_functions.avg_pace_per_zone(data)

#creating scatterplot data
scatter_regression_functions.hr_pace_scatter(data)

#dual axis data
dual_axis_graphs.miles_pace_dual(data)
dual_axis_graphs.time_miles_dual(data)

#creating the summary functions
highest_mile_week = sum_functions.mile_high_week(data)
highest_mile_month = sum_functions.mile_high_month(data)
most_aerobic_month = sum_functions.most_aerobic_month(data)

start_date = data["Date"].min()
end_date = data["Data"].max()




data.to_csv("USER_data.csv")
email_functions.send_email(user_email)
