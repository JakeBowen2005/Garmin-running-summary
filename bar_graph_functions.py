import pandas as pd
import matplotlib.pyplot as plt
import time_pace_func
#Bar Graph showing weekly total miles

def weekly_mile_bar(data):
    miles_per_week = data.groupby("Week")["Distance"].sum()

    #getting start and end dates
    start_date = data["Date"].min().strftime("%b %d, %Y")
    end_date = data["Date"].max().strftime("%b %d, %Y")

    plt.figure(figsize=(10,8))
    miles_per_week.plot(kind="bar", color="purple")
    plt.title(f"Total Miles per Week || {start_date} - {end_date}")
    plt.xlabel(f"Weeks")
    plt.ylabel("Total Miles per week  (mon-sun) ")
    plt.xticks(rotation=0)

    for i, value in enumerate(miles_per_week):
        plt.text(
            x=i,
            y= value + 1,
            s = f"{value:.1f}",
            fontsize=10,
            color="black",
            ha="center",
            va="bottom"
        )
    plt.tight_layout()
    #Saves graph in the folder
    plt.savefig("output/visuals/weekly_miles.png", dpi=300, bbox_inches="tight")
    plt.show()

#Bar Graph showing monthly total miles

def monthly_mile_bar(data):
    monthly_miles = data.groupby("Month")["Distance"].sum()
    monthly_miles = monthly_miles[monthly_miles > 0]

     #getting start and end dates
    start_date = data["Date"].min().strftime("%b %d, %Y")
    end_date = data["Date"].max().strftime("%b %d, %Y")

    plt.figure(figsize=(10,8))
    monthly_miles.plot(kind="bar", color="purple")
    plt.title(f'Total Miles per Month || {start_date} - {end_date}')
    plt.xlabel(f"Months")
    plt.ylabel("Miles per month")
    plt.xticks(rotation=0)

    for i, value in enumerate(monthly_miles):
        plt.text(
            x=i,
            y = value+1,
            s = f"{value:.1f}",
            fontsize=10,
            color="black",
            ha="center",
            va="bottom"
        )
    plt.tight_layout()

    plt.savefig("output/visuals/monthly_miles.png", dpi=300, bbox_inches="tight")
    plt.show()


#Bar Graph showing the avgerage pace per distance range
def avg_pace_per_distance_bar(data):
    avg_pace_distance = data.groupby("Distance Ranges")["Avg Pace"].mean().round(2).dropna()

    #getting start and end dates
    start_date = data["Date"].min().strftime("%b %d, %Y")
    end_date = data["Date"].max().strftime("%b %d, %Y")

    plt.figure(figsize=(10,8))
    avg_pace_distance.plot(kind="bar", color="purple")
    plt.title(f"Avgerage Pace per Distance || {start_date} - {end_date}")
    plt.xlabel("Distance in Miles")
    plt.ylabel("Pace (min/mile)")
    plt.xticks(rotation=0)

    for i, value in enumerate(avg_pace_distance):
        plt.text(
            x=i,
            y=value+0.05,
            s=time_pace_func.float_to_pace(value),
            ha="center",
            va="bottom",
            fontsize=10,
            color="black"
            )    
    plt.tight_layout()
    plt.savefig("output/visuals/average_pace_per_distance.png", dpi=300, bbox_inches="tight")
    plt.show()

#bar graph showing avergae per heart rate zone
def avg_pace_per_zone(data):
    pace_per_zone = data.groupby("Zones")["Avg Pace"].mean().round(2).dropna()
    #getting start and end dates
    start_date = data["Date"].min().strftime("%b %d, %Y")
    end_date = data["Date"].max().strftime("%b %d, %Y")

    plt.figure(figsize=(10,8))
    pace_per_zone.plot(kind="bar", color="purple")
    plt.title(f"Average Pace per Zones {start_date} - {end_date}")
    plt.xlabel("Zones")
    plt.ylabel("Average pace (min/mile)")
    plt.xticks(rotation=0)

    for i, value in enumerate(pace_per_zone):
        plt.text(
            x=i,
            y=value+0.01,
            s=time_pace_func.float_to_pace(value),
            ha="center",
            va="bottom",
            fontsize=10,
            color="black"
        )

    plt.tight_layout()
    plt.savefig("output/visuals/pace_per_zone.png", dpi=300, bbox_inches="tight")
    plt.show()




