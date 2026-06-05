import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

data = {
    "route": [
        "Desert Route","Desert Route","Desert Route","Desert Route","Desert Route",
        "Desert Route","Desert Route","Desert Route","Desert Route","Desert Route",

        "Mountain Route","Mountain Route","Mountain Route","Mountain Route",
        "Mountain Route","Mountain Route","Mountain Route","Mountain Route",
        "Mountain Route","Mountain Route",

        "Coastal Route","Coastal Route","Coastal Route","Coastal Route","Coastal Route",
        "Coastal Route","Coastal Route","Coastal Route","Coastal Route","Coastal Route"
    ],

    "airspeed_kmh": [
        430, 450, 470, 490, 510,
        530, 550, 570, 590, 610,

        440, 460, 480, 500, 520,
        540, 560, 580, 600, 620,

        420, 445, 475, 495, 515,
        535, 555, 575, 595, 615
    ],

    "fuel_burn_lph": [
        178, 188, 194, 208, 214,
        227, 233, 249, 255, 271,

        182, 190, 201, 210, 222,
        236, 239, 253, 266, 272,

        170, 186, 197, 205, 220,
        224, 242, 246, 262, 268
    ]
}

df = pd.DataFrame(data)

fig1, ax1 = plt.subplots(figsize=(10, 6))

site_colors = {"Desert Route": "steelblue", 
               "Mountain Route": "seagreen", 
               "Coastal Route": "coral"}
site_markers = {"Desert Route": "o", 
                "Mountain Route": "s", 
                "Coastal Route": "^"}
site_labels = {"Desert Route": "Desert Route", 
               "Mountain Route": "Mountain Route", 
               "Coastal Route": "Coastal Route"}

for site, group in df.groupby("route"):
        ax1.scatter(
                group["airspeed_kmh"],
                group["fuel_burn_lph"],
                color=site_colors[site],
                marker=site_markers[site],
                label=site_labels[site],
                s=100,
                edgecolors="black",
                linewidths=0.8
        )

ax1.set_title(
        "Airspeed-Fuel Burn Relationship at Different Flight Routes", 
        fontsize=14, pad=15)

ax1.set_xlabel("Airspeed (km/h)", fontsize=12, labelpad=10)
ax1.set_ylabel("Fuel Burn (L/h)", fontsize=12, labelpad=10)
ax1.tick_params(axis="both", labelsize=11)
ax1.set_xlim(400, 625)
ax1.set_ylim(160, 280)
ax1.tick_params(axis="both", labelsize=12)
ax1.legend(framealpha=0.9, fontsize=12)
ax1.grid(True, linestyle="--", alpha=0.4)

plt.tight_layout()
plt.show()

### Linear Regression Analysis

X = df["airspeed_kmh"].values.reshape(-1, 1)
y = df["fuel_burn_lph"].values

model = LinearRegression()
model.fit(X, y)

y_pred = model.predict(X)

slope = model.coef_[0]
intercept = model.intercept_
sse = np.sum((y - y_pred)**2)
sst = np.sum((y - np.mean(y))**2)
r2 = model.score(X, y) 

print(f"Slope:      {slope:.4f}")
print(f"Intercept:  {intercept:.4f}")
print(f"R²:         {r2:.4f}")
print(f"SSE:        {sse:.4f}")
print(f"SST:        {sst:.4f}")

# Plot the data and regression line

fig1, ax2 = plt.subplots(figsize=(10, 6))

for site, group in df.groupby("route"):
        ax2.scatter(
                group["airspeed_kmh"],
                group["fuel_burn_lph"],
                color=site_colors[site],
                marker=site_markers[site],
                label=site_labels[site],
                s=100,
                edgecolors="black",
                linewidths=0.8,
                zorder=2 # Plot scatter points in front
        )


ax2.plot(X, model.predict(X), color="black", linewidth=2, 
         label=f"Regression: Airspeed = {slope:.4f} x Fuel_Burn + {intercept:.4f}",
         zorder=1) # Plot regression line behind scatter points
         
ax2.set_title("Linear Regression: Airspeed vs Fuel Burn", fontsize=14, pad=15)
ax2.set_xlabel("Airspeed (km/h)", fontsize=12, labelpad=10)
ax2.set_ylabel("Fuel Burn (L/h)", fontsize=12, labelpad=10)
ax2.set_xlim(400, 625)
ax2.set_ylim(160, 280)
ax2.tick_params(axis="both", labelsize=12)
ax2.legend(framealpha=0.9, fontsize=12)
ax2.grid(True, linestyle="--", alpha=0.4)

plt.tight_layout()
plt.show()