from typing import Optional
from pygame.math import Vector2
from pygame.surface import Surface
from vi import Agent, Simulation, Config
import polars as pl
from typing import List
import numpy as np
import pandas as pd
from vi.simulation import HeadlessSimulation

class Grass(Agent):


    def __init__(self, images: list[Surface], simulation: HeadlessSimulation, pos: Vector2 | None = None, move: Vector2 | None = None, grow = 1000):
        super().__init__(images, simulation, pos, move)
        self.grow = grow

    def update(self):
        self.freeze_movement()
        number_grass = self.in_proximity_accuracy().filter_kind(Grass).count()
        if self.grow == 0:
            if number_grass < 4:
                self.reproduce()
                self.grow = 1000
        self.grow -= 1

        self.save_data("Type", "Grass")


class Prey(Agent):
    
    def __init__(self, images: list[Surface], simulation: HeadlessSimulation, pos: Vector2 | None = None, move: Vector2 | None = None, energy = 1500):
        super().__init__(images, simulation, pos, move)
        self.energy = energy
    def update(self):
        self.there_is_no_escape()
        
        rep_prob = np.random.uniform()
                
        if rep_prob < 0.0009:
            self.reproduce()


        grass = (
            self.in_proximity_accuracy()
            .filter_kind(Grass)
            .without_distance()
            .first()
        )
        ###########################
        # Comment the following for energy free sim
        ###########################
        grass_num = self.in_proximity_accuracy().filter_kind(Grass).count()
        friend = self.in_proximity_accuracy().filter_kind(Prey).count()
        if grass is not None and grass_num > 1 and friend < 2:
            grass.kill()
            self.reproduce()
            self.energy = 1500
        
        self.energy -= 1
        

        if self.energy == 0:
            self.kill()
        
        self.save_data("Type", "Prey")
        

class Hunter(Agent):
    def __init__(self, images: list[Surface], simulation: HeadlessSimulation, pos: Vector2 | None = None, move: Vector2 | None = None, energy=2000, inner_counter=0, age=0):
        super().__init__(images, simulation, pos, move)
        self.energy = energy
        self.inner_counter = inner_counter
        self.age = age

    def update(self):
        self.there_is_no_escape()
        ##########################
        # Comment the following for energy level sim
        survive = np.random.uniform()
        if survive < 0.0009:
           self.kill()
        ###########################
        prey = (
            self.in_proximity_accuracy()
            .filter_kind(Prey)
            .without_distance()
            .first()
        )
        ###########################
        # Comment the following for energy free sim
        ###########################
        prob = np.random.uniform()
        if prey is not None and prob < 0.009:
            prey.kill()
            self.reproduce()
            self.energy = 2000

        if self.energy == 0:
            self.kill()

        if self.in_proximity_accuracy().count() == 0:
            self.pos += self.move
        else:
            neighbours = list(self.in_proximity_accuracy())
            sum_velocity = Vector2(0,0)

            for boid, _ in neighbours:
                sum_velocity += boid.move.normalize()
            avg_velocity = sum_velocity / len(neighbours)
            alignment = avg_velocity - self.move
            sum_pos = Vector2(0,0)

            for boid, _ in neighbours:
                sum_pos += self.pos - boid.pos

            seperation = sum_pos / len(neighbours)

            avg_pos = Vector2(0,0)
            for boid, _ in neighbours:
                avg_pos += boid.pos
                
            avg_pos = avg_pos / len(neighbours)

            cohesion_force = avg_pos - self.pos
            cohesion = cohesion_force - self.move

            total_force = (alignment * 0.5 +
                            seperation * 0.5 +
                            cohesion * 0.5) / 20
 
            if self.move.length() > sum_velocity.length():
                self.move.normalize() * sum_velocity

            # agent = (
            # self.in_proximity_accuracy()
            # .filter_kind(Hunter2)
            # .without_distance()
            # .first()
            # )
            # neighbor = self.in_proximity_accuracy().filter_kind(Hunter).count()

            # if agent is not None and neighbor < 3:
            #     self.reproduce()
            #     population.pop_hunt += 1
            self.move += total_force
            prob = round(self.age / 150)
            if prob == 0:
                self.pos += self.move
            else:
                self.pos += (self.move) / prob

            self.age += 1
            self.energy -= 1

        self.save_data("Type", "Hunter")

config = Config()
x, y = config.window.as_tuple()

df = (HeadlessSimulation(Config(radius=20, duration=60*450))
.batch_spawn_agents(20, Prey,images=["images/white.png"])
.batch_spawn_agents(10, Hunter,images=["images/red.png"])
.batch_spawn_agents(20, Grass, images=["images/green.png"])
.run()
)
data = df.snapshots
df_snapshots = pd.DataFrame(data)

# Extract first and last column
first_column = df_snapshots.iloc[:, 0]
last_column = df_snapshots.iloc[:, -1]

# Create a new DataFrame with only the first and last column
df_selected = pd.concat([first_column, last_column], axis=1)

# Save the selected data to a CSV file
df_selected.to_csv("datasets/random_attempt/experiment_0_25.csv", index=False)

# df = pd.DataFrame({"Index": population.dct_hunt.keys(),
#     'Hunt': population.dct_hunt.values(),
#                    'Prey': population.dct_prey.values()})

# df.to_csv('dataset_important2.csv', index=False)
# dataframe = pd.DataFrame(data)
# dataframe.to_csv("plot_data.csv", index=False)

# plot = df.snapshots
# df_snapshots = pd.DataFrame(plot)
# df_snapshots.to_csv('agents_count_2.csv',index=False)

# import matplotlib.pyplot as plt
# import numpy as np



# dfs = pd.read_csv('Assignment_2/agents_count_2.csv')
# columns_to_delete = ['0', '2', '3']
# #
# ## Delete the specified columns
# dfss = dfs.drop(columns=columns_to_delete)
# column_name_mapping = {'1': 'id', 
#                       '4': 'pop'}
# #
# ## Rename the columns using the dictionary
# dfsss = dfss.rename(columns=column_name_mapping)
# dfsss.to_csv('Assignment_2/sim_data.csv', index=False)
