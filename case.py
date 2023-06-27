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
    def __init__(self, pop_prey=20, pop_hunt=10,rad=25):
        self.pop_prey = pop_prey
        self.pop_hunt = pop_hunt
        self.rad = rad

pop = CountPop()

class Grass(Agent):

    def __init__(self, images: list[Surface], simulation: HeadlessSimulation, pos: Vector2 | None = None, move: Vector2 | None = None, grow = 750):
        super().__init__(images, simulation, pos, move)
        self.grow = grow

    def update(self):
        self.freeze_movement()
        number_grass = self.in_proximity_accuracy().filter_kind(Grass).count()
        if self.grow == 0:
            if number_grass < 4:
                self.reproduce()
                self.grow = 750
        self.grow -= 1
        self.save_data("Type", "Grass")


class Prey(Agent):
    
    def __init__(self, images: list[Surface], simulation: HeadlessSimulation, pos: Vector2 | None = None, move: Vector2 | None = None, energy = 1500):
        super().__init__(images, simulation, pos, move)
        self.energy = energy

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
        rep_prob = np.random.uniform()
                
        if rep_prob < 0.001:
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
                self.energy = 1500
        self.energy -= 1
        
        hunt = self.in_proximity_accuracy().filter_kind(Hunter).first()
        if hunt is not None:
            prob = np.random.uniform()
            if prob < 0.001:
                self.move += self.flee()
        self.energy -= 1
            
           
        if self.energy == 0:
            self.kill()

        self.pos += self.move
        self.save_data("Type", "Prey")


class Hunter(Agent):
    def __init__(self, images: list[Surface], simulation: HeadlessSimulation, pos: Vector2 | None = None, move: Vector2 | None = None, energy=1200):
        super().__init__(images, simulation, pos, move)
        self.energy = energy

    def flock(self):
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
        return total_force

    def update(self):
        self.there_is_no_escape()
        ###########################

        # Comment the following for energy level sim
        survive = np.random.uniform()
        if survive < 0.0009:
           self.kill()
        ###########################
        prey = (
            self.in_proximity_accuracy()
            .filter_kind(Prey)
            .first()
        )
        self.energy -= 1
        ###########################
        if prey is not None and prey[1] <= pop.rad:
            prey[0].kill()
            self.reproduce()
            self.energy = 1200
        ###########################
        # Comment the following for energy free sim
        if self.energy == 0:
            self.kill()
        ###########################
        nei = self.in_proximity_accuracy().filter_kind(Hunter).first()

        if nei is not None:
            if self.in_proximity_accuracy().count() == 0:
                self.pos += self.move
                #print(self.in_proximity_accuracy().filter_kind(Hunter).first())
            else:
                if nei[1] <= pop.rad:
                    total_force = self.flock()
                    self.move += total_force
                    # # We update the position of the bird
                    self.pos += self.move

        self.save_data("Type", "Hunter")

config = Config()
x, y = config.window.as_tuple()

df = (Simulation(Config(radius=50,duration=10*60*60))
                        .batch_spawn_agents(20, Prey,images=["images/white.png"])
                        .batch_spawn_agents(10, Hunter,images=["images/red.png"])
                        .batch_spawn_agents(20, Grass, images=["images/green.png"])
                        .run()
                        )
# plot = df.snapshots

# data = pd.DataFrame(plot)
# data.to_csv('Assignment 2/agents_count.csv',index=False)

# import matplotlib.pyplot as plt
# import numpy as np



# dfs = pd.read_csv('Assignment_2/agents_count_2.csv')
# columns_to_delete = ['0', '2', '3']
# #
# ## Delete the specified columns
# dfss = dfs.drop(columns=columns_to_delete)
#column_name_mapping = {'1': 'id', 
#                       '4': 'pop'}
# #
# ## Rename the columns using the dictionary
#dfsss = dfss.rename(columns=column_name_mapping)
# dfsss.to_csv('Assignment_2/sim_data.csv', index=False)
