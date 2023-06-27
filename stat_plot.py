# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
 
# # Creating dataset
# data = pd.read_csv("datasets/random_attempt/stat2.csv")
# experiment1 = data["Experiment_1"][:30]

# fig = plt.figure(figsize=(10, 7))
 
# # Creating plot
# box_plot = plt.boxplot(experiment1)

# # Hide the outliers
# for flier in box_plot['fliers']:
#     flier.set(marker='', color='w')

# # Calculate and plot the mean value
# mean_value = np.mean(experiment1)
# plt.plot([0.925, 1.072], [mean_value, mean_value], color='r', linestyle='-', linewidth=2, label='Mean')

# # Set the legend
# plt.legend()

# # Show plot
# plt.show()

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Set the dark background style
plt.style.use('dark_background')

# Creating dataset
data = pd.read_csv("datasets/random_attempt/stat2.csv")
experiment1 = data["Mean_1"][:30]
experiment2 = data["Mean_2"][:30]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 7))

# Creating plot 1
ax1.boxplot(experiment1)

# Hide the outliers
# for flier in ax1['fliers']:
#     flier.set(marker='', color='w')

# Calculate and plot the mean value
mean_value1 = np.mean(experiment1)
mean_value2 = np.mean(experiment2)
ax1.plot([0.925, 1.072], [mean_value1, mean_value1], color='yellow', linestyle='-', linewidth=1, label='Mean')
ax1.set_ylim([0, 550])

# Set the legend for plot 1
ax1.legend()
ax1.set_title('Experiment with 20 grasses')

# Creating plot 2
ax2.boxplot(experiment2)
ax2.set_ylim([0, 550])

# Hide the outliers
# for flier in ax2['fliers']:
#     flier.set(marker='', color='w')

# Calculate and plot the mean value
ax2.plot([0.925, 1.072], [mean_value1, mean_value1], color='yellow', linestyle='-', linewidth=1, label='Mean')

# Set the legend for plot 2
ax2.legend()
ax2.set_title('Experiment with 35 grasses')

# Add title to the figure
fig.suptitle('Box Plots for Experiments')

# Adjust spacing between subplots
plt.subplots_adjust(wspace=0.1)

# Show plots
plt.show()
