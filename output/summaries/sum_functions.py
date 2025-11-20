import pandas as pd
import datetime as dt

#Highest Mile Week
def mile_high_week(data):
    miles_perweek = data.groupby("Week")["Distance"].sum()

    # find the week with the most miles
    best_week = miles_perweek.idxmax()
    max_miles = miles_perweek.max()

    # get the start and end dates for that week
    week_dates = data[data["Week"] == best_week]["Date"]
    start_date = week_dates.min()
    end_date = week_dates.max()

    return max_miles, start_date, end_date

#Highest Mile Month

def mile_high_month(data):
    miles_month = data.groupby("Month")["Distance"].sum()
    #find the month with the most miles
    best_month = miles_month.idxmax()
    max_miles = miles_month.max()

    #get the start and end dates for that week
    week_dates = data[data["Month"] == best_month]["Date"]
    start_date = week_dates.min()
    end_date = week_dates.max()
    return max_miles, start_date, end_date

#Most Aerobic Month
#Most Distance and lowest average Heart over a month

def most_aerobic_month(data):
    #group by the month
    data["MonthPeriod"] = data["Date"].dt.to_period("M")

    monthly = data.groupby("MonthPeriod").agg({
        "Distance" : "sum",
        "Avg HR": "mean",
    })

    #computing aerobic score
    monthly["AerobicScore"] = monthly["Distance"] / monthly["Avg HR"]

    best_month = monthly["AerobicScore"].idxmax()
    best_date = best_month.to_timestamp()
    return best_date.strftime("%B %Y")


    
