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

# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd

# # Set the dark background style
# plt.style.use('dark_background')

# # Creating dataset
# data = pd.read_csv("datasets/random_attempt/stat2.csv")
# experiment1 = data["Mean_1"][:30]
# experiment2 = data["Mean_2"][:30]

# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 7))

# # Creating plot 1
# ax1.boxplot(experiment1)

# # Hide the outliers
# # for flier in ax1['fliers']:
# #     flier.set(marker='', color='w')

# # Calculate and plot the mean value
# mean_value1 = np.mean(experiment1)
# mean_value2 = np.mean(experiment2)
# ax1.plot([0.925, 1.072], [mean_value1, mean_value1], color='yellow', linestyle='-', linewidth=1, label='Mean')
# ax1.set_ylim([0, 550])

# # Set the legend for plot 1
# ax1.legend()
# ax1.set_title('Experiment with 20 grasses')

# # Creating plot 2
# ax2.boxplot(experiment2)
# ax2.set_ylim([0, 550])

# # Hide the outliers
# # for flier in ax2['fliers']:
# #     flier.set(marker='', color='w')

# # Calculate and plot the mean value
# ax2.plot([0.925, 1.072], [mean_value1, mean_value1], color='yellow', linestyle='-', linewidth=1, label='Mean')

# # Set the legend for plot 2
# ax2.legend()
# ax2.set_title('Experiment with 35 grasses')

# # Add title to the figure
# fig.suptitle('Box Plots for Experiments')

# # Adjust spacing between subplots
# plt.subplots_adjust(wspace=0.1)

# # Show plots
# plt.show()
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
plt.style.use('dark_background')
# Sample data
categories = ['Rabbit', 'Fox', 'Grass']
values = [25, 25, 35]

# Create a figure and axis with smaller size
fig, ax = plt.subplots(figsize=(8, 6))

# Set the width of the bars
bar_width = 0.4

# Generate x-axis positions for the bars
x = np.arange(len(categories))

# Create the bar plot with adjusted positions and width
ax.bar(x, values, width=bar_width)

# Set the x-axis tick positions and labels
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=13)

# Set the x-axis label
ax.set_xlabel('Type', labelpad=10, fontsize=14)

# Set the y-axis label
ax.set_ylabel('Numbers', labelpad=10, fontsize=14)

# Set the title
ax.set_title('Agent numbers for experiment with nests')

# Adjust the x-axis limits to center the bars
ax.set_xlim([-0.5, len(categories)-0.5])
ax.set_ylim([0, 48])
# Show the plot
ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
plt.show()