import pandas as pd
import matplotlib.pyplot as plt

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


