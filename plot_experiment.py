
import csv
import matplotlib.pyplot as plt

# Actual dimensions of the box
actual_width = 16.6
actual_height = 9.1

# Lists to store experimental readings
actual_distances = []
measured_distances = []
estimated_widths = []
estimated_heights = []

with open("experiment_data.csv", "r") as file:

    reader = csv.DictReader(file)

    for row in reader:
        actual_distances.append(float(row["Actual Distance (m)"]))
        measured_distances.append(float(row["Measured Distance (m)"]))
        estimated_widths.append(float(row["Estimated Width (cm)"]))
        estimated_heights.append(float(row["Estimated Height (cm)"]))

print("Experimental data loaded successfully!")
print("Total readings:", len(actual_distances))


# Sort all readings according to actual distance
sorted_data = sorted(
    zip(actual_distances, measured_distances,
        estimated_widths, estimated_heights)
)

actual_distances = [row[0] for row in sorted_data]
measured_distances = [row[1] for row in sorted_data]
estimated_widths = [row[2] for row in sorted_data]
estimated_heights = [row[3] for row in sorted_data]


# GRAPH 1: Actual Distance vs Measured Distance

plt.figure(figsize=(8, 5))

# Original blue measurement points
plt.scatter(
    actual_distances,
    measured_distances,
    color="blue",
    label="D455 Measurements",
    zorder=3
)

# Red line connecting all measured points
plt.plot(
    actual_distances,
    measured_distances,
    color="red",
    linestyle="-",
    linewidth=2,
    label="Connected Measurements",
    zorder=2
)

# Ideal measurement reference line
plt.plot(
    [min(actual_distances), max(actual_distances)],
    [min(actual_distances), max(actual_distances)],
    color="blue",
    linestyle="--",
    label="Ideal Measurement"
)

plt.xlabel("Actual Distance (m)")
plt.ylabel("Measured Depth (m)")
plt.title("Actual Distance vs D455 Measured Depth")

plt.legend()
plt.grid(True)

plt.show()


# GRAPH 2: Estimated Width vs Actual Distance

plt.figure(figsize=(8, 5))

# Original blue measurement points
plt.scatter(
    actual_distances,
    estimated_widths,
    color="blue",
    label="Estimated Width",
    zorder=3
)

# Red line connecting all estimated width points
plt.plot(
    actual_distances,
    estimated_widths,
    color="red",
    linestyle="-",
    linewidth=2,
    label="Connected Measurements",
    zorder=2
)

# Actual width reference line
plt.axhline(
    y=actual_width,
    color="blue",
    linestyle="--",
    label="Actual Width (16.6 cm)"
)

plt.xlabel("Actual Distance (m)")
plt.ylabel("Estimated Width (cm)")
plt.title("Estimated Width vs Actual Distance")

plt.legend()
plt.grid(True)

plt.show()


# GRAPH 3: Estimated Height vs Actual Distance

plt.figure(figsize=(8, 5))

# Original blue measurement points
plt.scatter(
    actual_distances,
    estimated_heights,
    color="blue",
    label="Estimated Height",
    zorder=3
)

# Red line connecting all estimated height points
plt.plot(
    actual_distances,
    estimated_heights,
    color="red",
    linestyle="-",
    linewidth=2,
    label="Connected Measurements",
    zorder=2
)

# Actual height reference line
plt.axhline(
    y=actual_height,
    color="blue",
    linestyle="--",
    label="Actual Height (9.1 cm)"
)

plt.xlabel("Actual Distance (m)")
plt.ylabel("Estimated Height (cm)")
plt.title("Estimated Height vs Actual Distance")

plt.legend()
plt.grid(True)

plt.show()
