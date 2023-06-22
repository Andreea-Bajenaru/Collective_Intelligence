import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Set the dark background style
plt.style.use('dark_background')

# Creating dataset
data = pd.read_csv("datasets/random_attempt/stat2.csv")
experiment1 = data["Experiment_2"][:30]

fig = plt.figure(figsize=(10, 7))

# Creating plot
box_plot = plt.boxplot(experiment1)

# Hide the outliers
# for flier in box_plot['fliers']:
#     flier.set(marker='', color='w')

mean_value = np.mean(experiment1)

# Add the mean value as text
plt.text(0.94, mean_value, f"Mean: {mean_value:.2f}", color='white', fontsize=12, va='bottom')

# Set the legend
plt.legend()

# Add title
plt.title("Box Plot of 30 Experiments with 35 Grasses")

# Add y-axis label
plt.ylabel("Number of cycles")

# Add x-axis label  
plt.xlabel("Experiment")

# Show plot
plt.show()
