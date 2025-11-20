import pandas as pd

#Highest Mile Week
def mile_high_week(data):
    miles_perweek = data.groupby("Week")["Distance"].sum()
    return miles_perweek.max()

#Highest Mile Month

def mile_high_month(data):
    miles_month = data.groupby("Month")["Distance"].sum()
    return miles_month.max()

#Most Aerobic Month
#Most Distance and lowest average Heart over a month

def most_aerobic_month(data):
    #group by the month
    monthly = data.groupby("Month").agg({
        "Distance" : "sum",
        "Avg Hr": "mean"
    })

    #computing aerobic score
    monthly["AerobicScore"] = monthly["Distance"] / monthly["Avg Hr"]
    return monthly["AerobicScore"].idxmax()


    
