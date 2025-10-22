import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time_pace_func.py
#Steps
#Get and clean data / make sure all strings are numbers, missing values are filled and we added the columns we need to summarize



file =input("Input path to garmin csv: ")
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

