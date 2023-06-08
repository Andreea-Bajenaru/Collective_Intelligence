from enum import Enum, auto

import pygame as pg
from pygame.math import Vector2
from vi import Agent, Simulation
from typing import Generator, Tuple
from vi.config import Config, dataclass, deserialize
import numpy as np


@deserialize
@dataclass
class FlockingConfig(Config):
    alignment_weight: float = 0.5
    cohesion_weight: float = 0.5
    separation_weight: float = 0.5

    delta_time: float = 3

    mass: int = 20

    def weights(self) -> Tuple[float, float, float]:
        return (self.alignment_weight, self.cohesion_weight, self.separation_weight)


class Bird(Agent):
    config: FlockingConfig

    def avoid_stuff(self):
        # This method changes the self.move value so the agent avoid obstacles
        dir = Vector2(0,0)
        for obstacle in self.obstacle_intersections(scale=1.5):
            dif = (obstacle + self.pos) 
            dir += dif.normalize()
        return dir
    
    def obstacle_coord(self):
        # This method identifies and returns the coordinates that the agent
        # should consider as obstacles
        coordinates = []
        start_x = 0
        start_y = 0
        # The variable obs holds the centre point of an obstacle
        # and sinse we know the shape and position of the obstacle
        # we can calculate the rest.
        for obs in self.obstacle_intersections():
                # Retrieve X coordinates of the obstacle
                start_x = int(obs[0])
                # Retrieve Y coordinates of the obstacle
                start_y = int(obs[1])
                # The max size can be edited accordin to the obstacle
                max_size = 200
                half_size = max_size // 2
                # We loop through the coordinates of the obstacle
                for x in range(start_x - half_size, start_x + half_size + 1):
                    for y in range(start_y - half_size, start_y + half_size + 1):
                        # We check if the coordinates are within the screen
                        if 0 <= x <= 750 and 0 <= y <= 750:
                            # We apend the coordinates to a list, in the Vector2 format
                            # since this is what the engine uses.
                            coordinates.append(Vector2(x, y))
        # Return the coordinates
        return coordinates

    def change_position(self):
        # Pac-man-style teleport to the other end of the screen when trying to escape
        self.there_is_no_escape()
        #YOUR CODE HERE -----------

        # For simplicity, we refer to the current agent as "Bird" and the neighbouring agents as "Individuals" or "Neighbours"
        
        # If a bird has no neigbours, it continues wandering
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
            # The birds adjust their alignment accourding to their neighbours, 
            # so the alignment is calculated by subtracting the move of the individual from the average velicity
            # This helps the bird joining the flock
            alignment = avg_velocity - self.move

            # Part 2 - Seperation
            # Here we initialise the sum_pos as a Vector2(0,0) so later we can calculate the sum of the positions
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
            total_force = (alignment * self.config.alignment_weight +
                            seperation * self.config.separation_weight +
                            cohesion * self.config.cohesion_weight) / self.config.mass
 
            # If the speed of the birds becomes too high, we decrease it
            if self.move.length() > sum_velocity.length():
                self.move.normalize() * sum_velocity

            # We add the total force to the move of the bird
            self.move += total_force
            
            # Part 4 - Obstacle Avoidance
            # Here we initialise the coordinates list
            coordinates = self.obstacle_coord()
            
            # We loop through the list and check if the bird is close to an obstacle
            want = 20
            for i in range(0, len(coordinates)):
                if self.pos.distance_to(coordinates[i]) <= want:
                    # If the agent is closer to the obstacle than we want
                    # it moves away
                    self.move = self.avoid_stuff()

            # We update the position of the bird
            self.pos += self.move        
            #END CODE -----------------
        
class Hunter(Bird):
    """
    A Hunter is a Bird that tries to catch other Birds.
    This is an experiment that we ended up not building upon or improving.
    """
    config: FlockingConfig
    
    def change_position(self):
        # Pac-man-style teleport to the other end of the screen when trying to escape
        self.there_is_no_escape()
        
        #YOUR CODE HERE -----------
        # Agent wanders around until it finds the "Prey". This could be improved. 
        self.pos += self.move
        
    def update(self):
        prey = (
            self.in_proximity_accuracy()
            .without_distance()
            .filter_kind(Bird)
            .first()
        )

        if prey is not None:
            prey.kill()
        

class Selection(Enum):
    ALIGNMENT = auto()
    COHESION = auto()
    SEPARATION = auto()


class FlockingLive(Simulation):
    selection: Selection = Selection.ALIGNMENT
    config: FlockingConfig

    def handle_event(self, by: float):
        if self.selection == Selection.ALIGNMENT:
            self.config.alignment_weight += by
        elif self.selection == Selection.COHESION:
            self.config.cohesion_weight += by
        elif self.selection == Selection.SEPARATION:
            self.config.separation_weight += by

    def before_update(self):
        super().before_update()

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.handle_event(by=0.1)
                elif event.key == pg.K_DOWN:
                    self.handle_event(by=-0.1)
                elif event.key == pg.K_1:
                    self.selection = Selection.ALIGNMENT
                elif event.key == pg.K_2:
                    self.selection = Selection.COHESION
                elif event.key == pg.K_3:
                    self.selection = Selection.SEPARATION

        a, c, s = self.config.weights()
        print(f"A: {a:.1f} - C: {c:.1f} - S: {s:.1f}")

config = Config()
x, y = config.window.as_tuple()

(
    FlockingLive(
        FlockingConfig(
            image_rotation=True,
            movement_speed=1,
            radius=50,
            seed=1,
        )
    )
    .batch_spawn_agents(50, Bird, images=["images/bird.png"])
    #.spawn_agent(Hunter, images=["images/green.png"])
    .spawn_obstacle("images/triangle@200px.png", x // 2 , y // 2)
    .run()
    
)
