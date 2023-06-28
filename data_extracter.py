import matplotlib.pyplot as plt
import pandas as pd
import scipy.signal as signal
import numpy as np
import csv

# # Set the dark background style
# plt.style.use('dark_background')
# data = {}
# data2 = {}
# results = {}
# for i in range(30):
# # Load the data from CSV
df = pd.read_csv(f'datasets/random_attempt/week_3/try_2_5.csv')
peaks, peaks2 = signal.find_peaks(df["Prey"], distance=4000, height=0)
print(peaks2)
# results.update({i:peaks2.values()})

    # agent_counts = df.groupby(["0", "5"]).size().reset_index(name='count')
    # excluded_agent_type = 'Grass'
    # agent_counts_filtered = agent_counts[agent_counts['5'] != excluded_agent_type]

    # pivot_table = agent_counts_filtered.pivot(index='0', columns='5', values='count')
    

    # # abcd = pivot_table["Prey"].values

    # # Plot a line graph
    # # fig, ax = plt.subplots(figsize=(8, 6))
    # # pivot_table.plot(kind='line', stacked=True, ax=ax)

    # # Calculate peaks
    # peaks, peaks2 = signal.find_peaks(pivot_table["Prey"], distance=4000, height=0)
    # results.update({i:peaks2.values()})


# csv_file_path = "peak_results2.csv"

# # Write the results to the CSV file
# with open(csv_file_path, 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Experiment combined', 'Peaks combined'])  # Write the header
    
#     for experiment, peaks_list in results.items():
#         for peaks_array in peaks_list:
#             writer.writerow([experiment] + peaks_array.tolist())

# print("Peak results have been saved to", csv_file_path)


# Calculate agent counts
# agent_counts = df.groupby([]).size().reset_index(name='count')
# excluded_agent_type = 'Grass'
# agent_counts_filtered = agent_counts[agent_counts['5'] != excluded_agent_type]

# pivot_table = agent_counts_filtered.pivot(index='0', columns='5', values='count')

# abcd = pivot_table["Prey"].values

# Plot a line graph
# fig, ax = plt.subplots(figsize=(8, 6))
# pivot_table.plot(kind='line', stacked=True, ax=ax)

# Calculate peaks
# peaks, peaks2 = signal.find_peaks(df["Prey"], distance=4000, height=0)

#Determine the number of peaks when a point is the highest among 100 points
# highest_point_index = pivot_table.values.flatten().argmax()
# highest_point_peaks = [peak for peak in peaks if (highest_point_index - 50) <= peak <= (highest_point_index + 50)]
# # num_peaks = len(highest_point_peaks)
# for i in peaks:
#     print(abcd[i])
# for key, values in peaks2.items():
#     value = values.tolist()
#     sum = np.sum(value)
#     number = len(value)
#     mean = sum / number
#     data.update({i:number})
#     data2.update({i:mean})
#     # data2.update({i:number})
# print(data)
# print(data2)
    # df = pd.DataFrame(data)
    # filename = 'datasets/random_attempt/peak_graph.csv'
    # df.to_csv(filename, index=False)

# # df2 = pd.DataFrame(data2)
# # filename2 = 'datasets/random_attempt/peak_graph2.csv'
# # df2.to_csv(filename2, index=False)

# Customize the plot
# plt.xlabel('Time Frames', color='#CCCCCC', fontsize=14)
# plt.ylabel('Agent Count', color='#CCCCCC', fontsize=14)
# plt.title('Agent Counts for Each Time Frame', color='goldenrod', fontsize=18)
# plt.legend(title='Agent Type', facecolor='#222222', edgecolor='#CCCCCC', framealpha=0.7, fontsize=10)

# # Set line colors
# line_colors = ['#FF6666', '#66FF66', '#6666FF', '#FFFF66', '#66FFFF', '#FF66FF']
# ax.set_prop_cycle(color=line_colors)

# # Set grid color
# ax.grid(color='#333333', linestyle='--', linewidth=0.5)

# # Set spines color
# ax.spines['bottom'].set_color('#CCCCCC')
# ax.spines['left'].set_color('#CCCCCC')
# ax.spines['top'].set_color('none')
# ax.spines['right'].set_color('none')

# # Set tick colors
# ax.tick_params(axis='x', colors='#CCCCCC')
# ax.tick_params(axis='y', colors='#CCCCCC')

# # Print the number of peaks
# print("Number of Peaks:", num_peaks)

# # Save the plot
# plt.tight_layout()
# plt.savefig('datasets/random_attempt/images/Figures_1_11.png')
# plt.close()





import matplotlib.pyplot as plt
import pandas as pd

plt.style.use('dark_background')

# Read the data from CSV
df = pd.read_csv('datasets/random_attempt/week_3/try_2_5.csv')
# print(df["Prey"].mean())
# Plot a line graph
fig, ax = plt.subplots(figsize=(8, 6))
df.plot(x='Time_Frame', y=['Prey', 'Hunter'], kind='line', stacked=False, ax=ax)

# Customize the plot
plt.xlabel('Time Frames', color='#CCCCCC', fontsize=14)
plt.ylabel('Agent Count', color='#CCCCCC', fontsize=14)
plt.title('Agent Counts for Each Time Frame', color='goldenrod', fontsize=18)
plt.legend(title='Agent Type', facecolor='#222222', edgecolor='#CCCCCC', framealpha=0.7, fontsize=10)

# Set line colors
line_colors = ['#FF0000', '#0000FF']  # Modified line colors (red and blue)
ax.set_prop_cycle(color=line_colors)

# Set grid color
ax.grid(color='#333333', linestyle='--', linewidth=0.5)

# Set spines color
ax.spines['bottom'].set_color('#CCCCCC')
ax.spines['left'].set_color('#CCCCCC')
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')

# Set tick colors
ax.tick_params(axis='x', colors='#CCCCCC')
ax.tick_params(axis='y', colors='#CCCCCC')
# Save the plot
# plt.ylim(0, 200)
plt.tight_layout()
plt.show()




# import matplotlib.pyplot as plt
# import pandas as pd

# plt.style.use('dark_background')

# # Read the data from CSV
# df = pd.read_csv('Assignment_3/datasets/try_54.csv')

# # Group the data by 100 time frames
# grouped_df = df.groupby(df.index // 600).mean()

# # Plot a line graph with scatter markers
# fig, ax = plt.subplots(figsize=(8, 6))
# ax.plot(grouped_df['Prey'], grouped_df['Hunter'], marker='o', color='#FF0000', linewidth=2)

# # Customize the plot
# plt.xlabel('Number of Prey', color='#CCCCCC', fontsize=14)
# plt.ylabel('Number of Hunters', color='#CCCCCC', fontsize=14)
# plt.title('Number of Hunters vs Number of Prey (per 600 Time Frames)', color='goldenrod', fontsize=18)
# plt.grid(color='#333333', linestyle='--', linewidth=0.5)

# # Set spines color
# ax.spines['bottom'].set_color('#CCCCCC')
# ax.spines['left'].set_color('#CCCCCC')
# ax.spines['top'].set_color('none')
# ax.spines['right'].set_color('none')

# # Set tick colors
# ax.tick_params(axis='x', colors='#CCCCCC')
# ax.tick_params(axis='y', colors='#CCCCCC')

# # Save the plot
# plt.tight_layout()
# plt.show()
