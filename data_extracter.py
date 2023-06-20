import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('proper_data5.csv')


agent_counts = df.groupby(['0', '5']).size().reset_index(name='count')
print(agent_counts)
excluded_agent_type = 'Grass'
agent_counts_filtered = agent_counts[agent_counts['5'] != excluded_agent_type]


pivot_table = agent_counts_filtered.pivot(index='0', columns='5', values='count')

# Plot a bar graph
pivot_table.plot(kind='line', stacked=True)

# Customize the plot
plt.xlabel('Time Frames')
plt.ylabel('Agent Count')
plt.title('Agent Counts for Each Time Frame')
plt.legend(title='Agent Type')

# Display the plot
plt.show()
