import pandas as pd
import matplotlib.pyplot as plt
import time_pace_func
import numpy as np
#Scatterplot to show a correlation between average pace and average heart rate
def hr_pace_scatter(data):
    plt.figure(figsize=(10,8))
    plt.scatter(data["Avg Pace"], data["Avg HR"], color="royalblue", alpha=0.5)
    plt.grid(True, linestyle="--", alpha=0.4)

    #Adding linear regression line
    z = np.polyfit(data["Avg Pace"], data["Avg HR"], 1)
    # np.polyfit(x,y,1) fits a polynomial of degree 1 return [m,b] in y=m(x)+b
    p = np.poly1d(z)
    #Converts that [m, b] array into a callable function.
    # You can now compute predicted y-values: p(150) gives pace at HR=150.
    plt.plot(data["Avg Pace"], p(data["Avg Pace"]), color="red", label="Trendline")


    plt.title("Avergae Pace vs Heart Rate")
    plt.xlabel("Average Pace (min/mile)")
    plt.ylabel("Average Heart Rate")
    plt.tight_layout()
    plt.show()