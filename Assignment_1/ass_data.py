# Assignment 1
from typing import Optional
from pygame.math import Vector2
from pygame.surface import Surface
from vi import Agent, Simulation, Config
import polars as pl
from typing import List
from typing import Union
import seaborn as sns
from vi.simulation import HeadlessSimulation
import numpy as np
import random
import csv
import pandas as pd

class MyAgent(Agent):
    def __init__(self, images: List[Surface], simulation: HeadlessSimulation, pos: Union[Vector2, None] = None, move: Union[Vector2, None] = None, count=20):
        super().__init__(images, simulation, pos, move)
        self.count = count
        self.join = 0.2
        self.leave = 0.6

    def update(self):
        neighbours = 3
        site_id = self.on_site_id()

        # Save the site id to the DataFrame
        self.save_data("site", site_id)
        genrator = random.randint(0,10)
        entry = 5
        leave = 6
        probs = random.uniform(0,1)
        if self.on_site():
            if genrator == entry:
                if self.count > 0:
                    self.count -= 1
                    self.pos += self.move
                    self.join += 0.05
                else:
                    self.freeze_movement()
            elif self.in_proximity_accuracy().count() >= neighbours:
                if probs >= self.join:
                    self.join += 0.1
                    if self.count > 0:
                        self.count -= 1
                        self.pos += self.move
                    else:
                        self.freeze_movement()

            elif genrator == leave:
                self.pos += self.move
                self.leave += 0.05

            elif self.in_proximity_accuracy().count() <= neighbours:
                if probs >= self.leave:
                    self.leave += 0.1
                    self.continue_movement() 

        else:
                self.pos += self.move

            








        
        


config = Config()
x, y = config.window.as_tuple()

lstx = np.random.choice(range(0,x), 2, replace=False)
lsty = np.random.choice(range(0,y), 2, replace=False)

df = (Simulation(Config(radius=25))
                        .spawn_site("Assignment_1/images/site.png", 200, 300)
                        .spawn_site("Assignment_1/images/site1.png", 500, 300)
                        .batch_spawn_agents(50, MyAgent,images=["Assignment_1/images/red.png"])
                        
                        .run()


                        )


plot = df.snapshots
#print(plot.groupby(['id', 'x', 'y', 'site']))
df_snapshots = pd.DataFrame(plot)
df_snapshots.to_csv('snapshots.csv', index=False)


dfs = pd.read_csv('snapshots.csv')
columns_to_delete = ['0', '4']

# Delete the specified columns
dfss = dfs.drop(columns=columns_to_delete)
column_name_mapping = {'1': 'id',
                       '2': 'x',
                       '3': 'y',
                       '5': 'site'}

# Rename the columns using the dictionary
dfsss = dfss.rename(columns=column_name_mapping)
dfsss.to_csv('filename_updated.csv', index=False)
dfsss.to_excel('filename.xlsx', index=False)
# Print the DataFrame
print(dfsss)



