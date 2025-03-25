import pandas as pd
import matplotlib.pyplot as plt
import os

# csv we want to analyze
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
csv_path = os.path.join(BASE_DIR, "data", "output_data", "tracking_data.csv")


def analyze_traffic(output_path):

    fps = 30

    # Read data
    df= pd.read_csv(csv_path)
    df["second"]=df["frame"]/30

    # how many vehicles there are in everys second
    counts = df.groupby("second")["class"].nunique().reset_index()
    counts["second"]=counts["second"].round(1)
    counts.columns=["second","vehicle_count"]

    # Average speed per minute
    avg_speed= df.groupby("second")["speed_kph"].mean().reset_index()
    avg_speed["speed_kph"]= avg_speed["speed_kph"].round(1)
    avg_speed["second"]=avg_speed["second"].round(1)
    avg_speed.columns= ["second", "avg_speed_kph"]
    
    traffic= pd.merge(counts, avg_speed, on="second")

    # 1st Graph
    plt.figure(figsize=(8,4))
    plt.plot(traffic["second"], traffic["vehicle_count"])
    plt.title("Vehicle per second")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{output_path}/vehicle_per_second.png")

    # 2nd graph
    plt.figure(figsize=(8,4))
    plt.plot(traffic["second"], traffic["avg_speed_kph"])
    plt.title("avg_speed_kph per second")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{output_path}/speed_per_second.png")  

    traffic.to_csv(f"{output_path}/traffic_analyzed.csv", index=False)
    