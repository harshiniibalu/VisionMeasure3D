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

# GRAPH 1: Actual Distance vs Measured Distance

plt.figure(figsize=(8, 5))

plt.scatter(
    actual_distances,
    measured_distances,
    label="D455 Measurements"
)

# Ideal measurement reference line
plt.plot(
    [min(actual_distances), max(actual_distances)],
    [min(actual_distances), max(actual_distances)],
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

plt.scatter(
    actual_distances,
    estimated_widths,
    label="Estimated Width"
)

# Actual width reference line
plt.axhline(
    y=actual_width,
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

plt.scatter(
    actual_distances,
    estimated_heights,
    label="Estimated Height"
)

# Actual height reference line
plt.axhline(
    y=actual_height,
    linestyle="--",
    label="Actual Height (9.2 cm)"
)

plt.xlabel("Actual Distance (m)")
plt.ylabel("Estimated Height (cm)")
plt.title("Estimated Height vs Actual Distance")

plt.legend()
plt.grid(True)

plt.show()