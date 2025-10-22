import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time_pace_func

my_email = "jakeeb05@gmail.com"
my_password = "jsyvqmqwkfxilewg"
#Steps
#Get and clean data / make sure all strings are numbers, missing values are filled and we added the columns we need to summarize

# /Users/jakebowen/Desktop/Pandas/Garmin Data/Activities.csv


file =input("Input path to garmin csv: ").strip()
user_email = input("Input email to send data to: ").strip()
data = pd.read_csv(f"{file}")

#Date
data["Date"] = pd.to_datetime(data["Date"])

#Weekday and week columns
data["Weekday"] = data["Date"].dt.day_name()
data["Week_Start"] = data["Date"].dt.to_period("W-SUN").apply(lambda r: r.start_time)
data["Week"] = data["Week_Start"].rank(method="dense").astype(int)

#Dropping columns
data = data[["Date", "Week", "Weekday", "Distance", "Calories", "Time", "Avg HR", "Max HR", 
             "Avg Pace", "Best Pace", "Total Ascent", "Total Descent", "Steps"]]

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

#Lastly drop columns
data = data[["Date", "Week", "Weekday", "Distance", "Calories",
             "Time", "Avg HR", "Max HR", "Avg Pace", "Best Pace",
             "Zones", "Total Ascent", "Total Descent", "Steps"]]

print(data.head(5))
print(user_email)
data.to_csv("user_data.csv", index=False)