import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('datasets/random_attempt/experiment_1_3.csv')

agent_counts = df.groupby(['0', '5']).size().reset_index(name='count')
print(agent_counts)
excluded_agent_type = 'Grass'
agent_counts_filtered = agent_counts[agent_counts['5'] != excluded_agent_type]

pivot_table = agent_counts_filtered.pivot(index='0', columns='5', values='count')

# Plot a line graph
fig, ax = plt.subplots()
pivot_table.plot(kind='line', stacked=True, ax=ax)

# Customize the plot
plt.xlabel('Time Frames', color='red')
plt.ylabel('Agent Count', color='blue')
plt.title('Agent Counts for Each Time Frame', color='green')
plt.legend(title='Agent Type', facecolor='yellow', edgecolor='black', framealpha=0.7)

# Set background color
fig.patch.set_facecolor('lightgray')

# Set line colors
ax.set_prop_cycle(color=['purple', 'orange', 'cyan', 'magenta', 'brown', 'gray'])

# Show the plot
plt.show()
