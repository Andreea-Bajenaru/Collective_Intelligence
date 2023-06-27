from typing import Optional
from pygame.math import Vector2
from pygame.surface import Surface
from vi import Agent, Simulation, Config
import polars as pl
from typing import List
import numpy as np
import pandas as pd
from vi.simulation import HeadlessSimulation


class CountPop():
    def __init__(self, pop_prey=20, pop_hunt=10,rad=20, counter1=0, counter2=0):
        self.pop_prey = pop_prey
        self.pop_hunt = pop_hunt
        self.rad = rad
        self.counter1 = counter1
        self.counter2 = counter2

pop = CountPop()

class Grass(Agent):
    def __init__(self, images: list[Surface], simulation: HeadlessSimulation, pos: Vector2 | None = None, move: Vector2 | None = None, grow = 700):
        super().__init__(images, simulation, pos, move)
        self.grow = grow

    def update(self):
        self.freeze_movement()
        plant = (self.in_proximity_accuracy().filter_kind(Grass).first())
        if plant is not None:
            if plant[1] <= pop.rad:
                number_grass = self.in_proximity_accuracy().filter_kind(Grass).count()
                if self.grow == 0:
                    if number_grass < 4:
                        self.reproduce()
                        self.grow = 700
        else:
            number_grass = self.in_proximity_accuracy().filter_kind(Grass).count()
            if self.grow == 0:
                if number_grass < 4:
                    self.reproduce()
                    self.grow = 700

        self.grow -= 1

        self.save_data("Type", "Grass")


class Prey(Agent):
    def __init__(self, images: list[Surface], simulation: HeadlessSimulation, pos: Vector2 | None = None, move: Vector2 | None = None, energy = 1100, counter=25, counter2=0):
        super().__init__(images, simulation, pos, move)
        self.energy = energy
        self.counter = counter
        self.counter2 = counter2
    
    def flee(self):
        neighbours = list(self.in_proximity_accuracy())
        sum_velocity = Vector2(0,0)
        for boid, _ in neighbours:
            sum_velocity += boid.move.normalize()
        avg_velocity = sum_velocity / len(neighbours)
        alignment = avg_velocity - 2*self.move
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
                        seperation * 0.502 +
                        cohesion * 0.5) / 20
        if self.move.length() > sum_velocity.length():
            self.move.normalize() * sum_velocity
        return total_force

    def update(self):
        self.there_is_no_escape()
        
        if self.on_site():
            neighbor = self.in_proximity_accuracy().filter_kind(Prey).count()
            self.counter -= 1
            if self.counter == 0:
                self.freeze_movement()
                self.counter = 5
            self.counter2 += 1
            if 200 > self.counter2 > 100 and neighbor > 0:
                self.reproduce()
                self.counter2 = 0
                self.counter = 25
                self.continue_movement()
            elif self.counter2 > 200:
                self.continue_movement()
                self.counter2 = 0
                self.counter = 25
        else:
            self.counter = 25

            rep_prob = np.random.uniform()        
            if rep_prob < 0.0009:
                self.reproduce()

            grass= (
            self.in_proximity_accuracy()
            .filter_kind(Grass)
            .first()
            )
            if grass is not None:
                grass_num = self.in_proximity_accuracy().filter_kind(Grass).count() if grass[1] <= pop.rad else None

                friend = self.in_proximity_accuracy().filter_kind(Prey).count()
                if grass_num is not None and grass_num > 1 and friend < 2:
                    grass[0].kill()
                    self.reproduce()
                    self.energy = 1100

            # hunt = self.in_proximity_accuracy().filter_kind(Hunter).first()
            # hunt2 = self.in_proximity_accuracy().filter_kind(Hunter2).first()
            # if hunt is not None or hunt2 is not None:
            #     prob = np.random.uniform()
            #     if prob < 0.001:
            #         self.move += self.flee()

        self.pos += self.move


        self.energy -= 1
        if self.energy == 0:
            self.kill()
        
        self.save_data("Type", "Prey") 

class Hunter(Agent):
    def __init__(self, images: list[Surface], simulation: HeadlessSimulation, pos: Vector2 | None = None, move: Vector2 | None = None, energy=1000, inner_counter=0, age=0, count=0):
        super().__init__(images, simulation, pos, move)
        self.energy = energy
        self.inner_counter = inner_counter
        self.age = age
        self.count = count

    def update(self):
        self.there_is_no_escape()
        ##########################
        # Comment the following for energy level sim
        pop.counter1 += 1
        if self.on_site():
            self.move = self.move * -1
        if pop.counter1 > 5000:
            survive = np.random.uniform()
            if survive < 0.0009:
                self.kill()
        ###########################
        random = np.random.uniform()
        prey = (
            self.in_proximity_accuracy()
            .filter_kind(Prey)
            .first()
            )
        if prey is not None and prey[1] <= pop.rad and random < 0.05:
            prey[0].kill()
            #self.reproduce()
            self.energy = 1000

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

            self.move += total_force
            prob = round(self.age / 150)
            if prob == 0:
                self.pos += self.move
            else:
                self.pos += (self.move) / prob

            self.age += 1
            self.energy -= 1
            self.count += 1

            n = (self.in_proximity_accuracy().filter_kind(Hunter2).first())
            if n is not None and pop.rad >= n[1]:
                # neighbor = self.in_proximity_accuracy().filter_kind(Hunter2).count()
                neighbor = self.in_proximity_accuracy().filter_kind(Hunter2).count()
                prob = np.random.uniform()
                if self.count > 200:
                    if neighbor == 1 and prob > 0.0019:
                        self.reproduce()
                        self.count = 0

        self.save_data("Type", "Hunter")

class Hunter2(Agent):
    def __init__(self, images: list[Surface], simulation: HeadlessSimulation, pos: Vector2 | None = None, move: Vector2 | None = None, energy=1050, age=0, count=0):
        super().__init__(images, simulation, pos, move)
        self.age = age
        self.energy = energy
        self.count = count

    def update(self):
        self.there_is_no_escape()
        ##########################
        # Comment the following for energy level sim
        pop.counter2 += 1
        if self.on_site():
            self.move = self.move * -1
        if pop.counter2 > 5000:
            survive = np.random.uniform()
            if survive < 0.0009:
                self.kill()
        ###########################
        prey = (
            self.in_proximity_accuracy()
            .filter_kind(Prey)
            .first()
        )
        ###########################
        # Comment the following for energy free sim
        ###########################
        prob = np.random.uniform()
        if prey is not None and prob < 0.02 and pop.rad >= prey[1]:
            prey[0].kill()
            #self.reproduce()
            self.energy = 1050

        if self.energy == 0:
            self.kill()

        self.age += 1
        age = round(self.age / 150)
        if age == 0:
            self.pos += self.move
        else:
            self.pos += (self.move / age)

        self.count += 1
        n = (self.in_proximity_accuracy().filter_kind(Hunter).first())
        if n is not None and pop.rad >= n[1]:
            # neighbor = self.in_proximity_accuracy().filter_kind(Hunter2).count()
            neighbor = self.in_proximity_accuracy().filter_kind(Hunter).count()
            prob = np.random.uniform()
            if self.count > 200:
                if neighbor == 1 and prob > 0.002:
                    self.reproduce()
                    self.move = self.move * -1
                    self.count = 0

        self.energy -= 1
        self.save_data("Type", "Hunter")

# Baseline
# Only Grass
# Only Sexual rep
# Only Nests
# All combined (grass, sex, nests)
# You can change parameters, mention them next to the video

# RQ: How is the stability of the simulation affected by adding different elements found in nature that make the simulation more realistic?
# Make hypothesis right after formulation the rq, what do you expect to happen?
# 30 simulations for each
# You create a stability score based on number of peaks and something related to height of peaks
# You store for each simulation that score and then test:\
# Tests:
# Baseline vs Grass
# Baseline vs sex
# baseline vs Nests
# Baseline vs all combined
# You show one box with the 5 scenarios
# You show in one slide results for all 4 tests



config = Config()
x, y = config.window.as_tuple()

df = (Simulation(Config(radius=50, fps_limit=600000 ,duration=60*480))
.batch_spawn_agents(25, Prey,images=["images/white.png"])
.batch_spawn_agents(15, Hunter,images=["images/red.png"])
.batch_spawn_agents(35, Grass, images=["images/green.png"])
.batch_spawn_agents(15, Hunter2, images=["images/blue.png"])
# .spawn_site("images/yellow_circle1.png", 200, 100)
# .spawn_site("images/yellow_circle1.png", 500, 350)
.run()
.snapshots
.groupby('frame')
.agg([
    pl.col("Type").eq("Grass").sum().alias("Grass"),
    pl.col("Type").eq("Prey").sum().alias("Prey"),
    pl.col("Type").eq("Hunter").sum().alias("Hunter")
    ])
.sort("frame")
)

df_snapshots = pd.DataFrame(df)
new_column_names = ["Time_Frame", "Grass", "Prey", "Hunter"]
df_snapshots.columns = new_column_names
df_snapshots.to_csv(f"datasets/random_attempt/week_3/try_2_0.csv", index=False)
# data = df.snapshots
# df_snapshots = pd.DataFrame(data)
# # Extract first and last column
# first_column = df_snapshots.iloc[:, 0]
# last_column = df_snapshots.iloc[:, -1]
# # Create a new DataFrame with only the first and last column
# df_selected = pd.concat([first_column, last_column], axis=1)
# agent_counts = df_selected.groupby([first_column, last_column]).size().reset_index(name='count')
# # Save the selected data to a CSV file
# agent_counts.to_csv(f"Assignment_3/datasets/try0.csv", index=False)

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
