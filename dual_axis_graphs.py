import pandas as pd
import matplotlib.pyplot as plt
import time_pace_func
import numpy as np

def miles_pace_dual(data):
    weekly = data.groupby("Week").agg({
        "Distance" : "sum",
        "Avg Pace" : "mean"
    }).reset_index()


    fig, ax1 = plt.subplots(figsize=(10,8))

    #Miles on left axis
    ax1.plot(weekly["Week"], weekly["Distance"], color="purple", label="Weekly Miles")
    ax1.set_ylabel("Miles per Week", color="purple")
    ax1.tick_params(axis='y', labelcolor="purple")

    #Pace on right axis
    ax2 = ax1.twinx()
    ax2.plot(weekly["Week"], weekly["Avg Pace"], color="royalblue", label="Avergae Pace (min/mile)")
    ax2.set_ylabel("Average Pace per Week", color="royalblue")
    ax2.tick_params(axis="y", labelcolor="royalblue")

    plt.title("Weekly Mileage and Pace Trend")

    plt.xticks(np.arange(1, len(weekly["Week"]) + 1, 1))

    plt.tight_layout()
    plt.savefig("output/visuals/weekly_miles_vs_pace.png", dpi=300, bbox_inches="tight")
    plt.show()