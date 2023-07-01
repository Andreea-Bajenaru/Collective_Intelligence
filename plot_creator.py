# import matplotlib.pyplot as plt
# import numpy as np
# import matplotlib.ticker as ticker
# plt.style.use('dark_background')
# # Sample data
# categories = ['Rabbit', 'Fox', 'Grass']
# values = [25, 8, 35]

# # Create a figure and axis with smaller size
# fig, ax = plt.subplots(figsize=(8, 6))

# # Set the width of the bars
# bar_width = 0.4

# # Generate x-axis positions for the bars
# x = np.arange(len(categories))

# # Create the bar plot with adjusted positions and width
# ax.bar(x, values, width=bar_width)

# # Set the x-axis tick positions and labels
# ax.set_xticks(x)
# ax.set_xticklabels(categories, fontsize=13)

# # Set the x-axis label
# ax.set_xlabel('Type', labelpad=10, fontsize=14)

# # Set the y-axis label
# ax.set_ylabel('Numbers', labelpad=10, fontsize=14)

# # Set the title
# ax.set_title('Agent numbers for experiment with 35 grasses')

# # Adjust the x-axis limits to center the bars
# ax.set_xlim([-0.5, len(categories)-0.5])
# ax.set_ylim([0, 48])
# # Show the plot
# ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
# plt.show()

# import matplotlib.pyplot as plt
# import numpy as np

# # Define the time range
# time = np.linspace(0, 20, 800)
# plt.style.use('dark_background')
# # Define the linear function
# y = 1000 - (60 * time)

# # Create a figure and axis
# fig, ax = plt.subplots()

# # Plot the linear function
# ax.plot(time, y, color='white')

# # Set the x-axis label
# ax.set_xlabel('Time (seconds)')

# # Set the y-axis label
# ax.set_ylabel('Energy values')

# # Set the title
# ax.set_title('Energy of rabbits')
# ax.set_ylim([0, 1200])
# # Show the plot
# plt.show()
# import matplotlib.pyplot as plt
# plt.style.use('dark_background')
# # Data points
# x = [0, 16.66666667, 33.33333333]
# y = [1, 2, 4]

# # Create a figure and axis
# fig, ax = plt.subplots()

# # Plot the line graph
# ax.plot(x, y, color="green")

# # Set the x-axis label
# ax.set_xlabel('Time (seconds)', labelpad=10)

# # Set the y-axis label
# ax.set_ylabel('Length of A Grass', labelpad=10)

# # Set the title
# ax.set_title('Growth of a Grass in a Batch Over Time')

# # Show the plot
# plt.show()
