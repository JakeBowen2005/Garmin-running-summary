import pandas as pd
import matplotlib.pyplot as plt
import time_pace_func
import numpy as np
#Scatterplot to show a correlation between average pace and average heart rate
def hr_pace_scatter(data):
    #Filtering outliers
    q1 = data["Avg Pace"].quantile(0.25)
    q3 = data["Avg Pace"].quantile(0.75)
    iqr = q3-q1

    low = q1 - 1.5*(iqr)
    high = q3+ 1.5*(iqr)

    data = data[(data["Avg Pace"] >= low) & (data["Avg Pace"] <= high)]


    #Fit the regression line
    z = np.polyfit(data["Avg Pace"], data["Avg HR"], 1)
    # np.polyfit(x,y,1) fits a polynomial of degree 1 return [m,b] in y=m(x)+b
    p = np.poly1d(z)
    #Converts that [m, b] array into a callable function.
    # You can now compute predicted y-values: p(150) gives pace at HR=150.

    predicted_hr = p(data["Avg Pace"])
    ss_res = np.sum((data["Avg HR"] - predicted_hr) ** 2)
    ss_tot = np.sum((data["Avg HR"] - np.mean(data["Avg HR"])) ** 2)
    r2 = 1-(ss_res/ss_tot)

    plt.figure(figsize=(10,8))
    sc = plt.scatter(data["Avg Pace"], data["Avg HR"], c=data["Distance"],cmap="viridis", alpha=0.5)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.plot(data["Avg Pace"], p(data["Avg Pace"]), color="red", label="Trendline")

    slope, intercept = z

    plt.text(
        x=data["Avg Pace"].min() + 0.1,
        y=data["Avg HR"].max() -5,
        s=f"y = {slope:.2f}x + {intercept:.1f}\nR² = {r2:.2f}",
        fontsize=11, color="black", bbox=dict(facecolor="white", alpha=0.7)
    )

    #Titles
    plt.colorbar(sc, label="Distance (miles)")  
    plt.title("Heart Rate vs Pace with Distance Coloring and Regression Line")
    plt.xlabel("Average Pace (min/mile)")
    plt.ylabel("Average Heart Rate")
    plt.tight_layout()
    plt.savefig("output/visuals/pace_hr_regression.png", dpi=300, bbox_inches="tight")
    # plt.show()