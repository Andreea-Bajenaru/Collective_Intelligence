from typing import Optional
from pygame.math import Vector2
from pygame.surface import Surface
from vi import Agent, Simulation, Config
import polars as pl
from typing import List
import numpy as np
import pandas as pd
from vi.simulation import HeadlessSimulation

# find a way to count the population

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


class Prey(Agent):
    
    def __init__(self, images: list[Surface], simulation: HeadlessSimulation, pos: Vector2 | None = None, move: Vector2 | None = None, energy = 1000):
        super().__init__(images, simulation, pos, move)
        self.energy = energy

    def update(self):
        self.there_is_no_escape()
        rep_prob = np.random.uniform()
                
        if rep_prob < 0.0004:
            self.reproduce()

        prey = (
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
        if prey is not None and grass_num > 1 and friend < 2:
            prey.kill()
            self.reproduce()
        
        self.energy -= 1

        if self.energy == 0:
            self.kill()
        self.pos += self.move


class Hunter(Agent):
    def __init__(self, images: list[Surface], simulation: HeadlessSimulation, pos: Vector2 | None = None, move: Vector2 | None = None, energy=1200):
        super().__init__(images, simulation, pos, move)
        self.energy = energy

    def update(self):
        self.there_is_no_escape()
        ###########################

        # Comment the following for energy level sim
        survive = np.random.uniform()
        if survive < 0.000001:
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
        self.energy -= 1
        ###########################
        if prey is not None:
            prey.kill()
            self.reproduce()
            self.energy = 1200
        ###########################
        # Comment the following for energy free sim
        if self.energy == 0:
            self.kill()
        ###########################

        if self.in_proximity_accuracy().count() == 0:
            self.pos += self.move
        else:
            # Part 1 - Alignment
            # First we need to create a list with all the neigbours of an individual
            neighbours = list(self.in_proximity_accuracy())
            # Here we initialise the sum_velocity as a Vector2(0,0) so later we can calculate the sum of the velocities
            sum_velocity = Vector2(0,0)
            # Then we loop through the list and add the velocity of each neighbour to the sum
            for boid, _ in neighbours:
                # The velocity has to be normalized otherwise the birds stop moving when they meet a neighbour
                sum_velocity += boid.move.normalize()

            # Then we calculate the average velocity of the neighbours, which is done by dividing the sum of the velocities
            # by the number of neighbours
            avg_velocity = sum_velocity / len(neighbours)
            alignment = avg_velocity - self.move
            sum_pos = Vector2(0,0)
            # Then we loop through the list and add the position of each neighbour to the sum
            for boid, _ in neighbours:
                # Just the positions would result in a wrong value, 
                # so for each neighbouring individual we subtract its position from the bird position
                sum_pos += self.pos - boid.pos

            # Then we calculate the average position of the neighbours
            # This helps make sure that the birds don't converge (overlap) in the same position 
            seperation = sum_pos / len(neighbours)

            # Part 3 - Cohesion
            # Here we initialise the avg_pos as a Vector2(0,0) so later we can calculate the average position
            avg_pos = Vector2(0,0)
            # Then we loop through the list and add the position of each neighbour to the sum
            for boid, _ in neighbours:
                avg_pos += boid.pos

            # Then we calculate the average position of the neighbours (similarly to the avg_velocity)
            avg_pos = avg_pos / len(neighbours)

            # The birds adjust their cohesion force according to their neighbours,
            # so the cohesion is calculated by subtracting the position of the individual from the average position
            # This helps the bird joining the flock
            cohesion_force = avg_pos - self.pos
            cohesion = cohesion_force - self.move

            # Finally we calculate the total force by adding the three forces together, multiplied by their respective weights
            # Then we divide by the mass to make the merging of the flock more natural
            total_force = (alignment * 0.5 +
                            seperation * 0.5 +
                            cohesion * 0.5) / 20
 
            # If the speed of the birds becomes too high, we decrease it
            if self.move.length() > sum_velocity.length():
                self.move.normalize() * sum_velocity

            # We add the total force to the move of the bird
            self.move += total_force
            # # We update the position of the bird
            self.pos += self.move


config = Config()
x, y = config.window.as_tuple()

df = (Simulation(Config(radius=25, fps_limit=120))
                        .batch_spawn_agents(18, Prey,images=["images/white.png"])
                        .batch_spawn_agents(10, Hunter,images=["images/red.png"])
                        .batch_spawn_agents(15, Grass, images=["images/green.png"])
                        .run()
                        )

plot = df.snapshots
df_snapshots = pd.DataFrame(plot)
df_snapshots.to_csv('Assignment_2/agents_count.csv',index=False)


dfs = pd.read_csv('Assignment_2/agents_count.csv')
columns_to_delete = ['0', '2', '3']
#
## Delete the specified columns
dfss = dfs.drop(columns=columns_to_delete)
column_name_mapping = {'1': 'id', 
                      '4': 'pop'}
#
## Rename the columns using the dictionary
dfsss = dfss.rename(columns=column_name_mapping)
dfsss.to_csv('Assignment_2/sim_data.csv', index=False)

