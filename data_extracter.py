import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('dataset_important.csv')

# Extract the features from the DataFrame
feature1 = df['Hunt']
feature2 = df['Prey']
feature3 = df["Index"]
# Plotting the graph
plt.plot(feature3, feature1, label='Hunt')
plt.plot(feature3, feature2, label='Prey')
plt.xlabel('Time Frame')
plt.ylabel('Value')
plt.title('Graph of Hunt and Prey')
plt.legend()
plt.show()