import matplotlib.pyplot as plt
import pandas as pd

# Set the dark background style
plt.style.use('dark_background')

# for i in range(9, 30):
df = pd.read_csv(f'datasets/random_attempt/experiment_1_8.csv')

agent_counts = df.groupby(['0', '5']).size().reset_index(name='count')
excluded_agent_type = 'Grass'
agent_counts_filtered = agent_counts[agent_counts['5'] != excluded_agent_type]

pivot_table = agent_counts_filtered.pivot(index='0', columns='5', values='count')

# Plot a line graph
fig, ax = plt.subplots(figsize=(8, 6))
pivot_table.plot(kind='line', stacked=True, ax=ax)

# Customize the plot
plt.xlabel('Time Frames', color='#CCCCCC', fontsize=14)
plt.ylabel('Agent Count', color='#CCCCCC', fontsize=14)
plt.title('Agent Counts for Each Time Frame', color='goldenrod', fontsize=18)
plt.legend(title='Agent Type', facecolor='#222222', edgecolor='#CCCCCC', framealpha=0.7, fontsize=10)

# Set line colors
line_colors = ['#FF6666', '#66FF66', '#6666FF', '#FFFF66', '#66FFFF', '#FF66FF']
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
plt.tight_layout()
plt.savefig(f'datasets/random_attempt/images/Figures_1_8.png')
plt.close()
