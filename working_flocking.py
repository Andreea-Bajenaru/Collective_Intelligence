from enum import Enum, auto

import pygame as pg
from pygame.math import Vector2
from vi import Agent, Simulation
from typing import Tuple
from vi.config import Config, dataclass, deserialize


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

    def change_position(self):
        # Pac-man-style teleport to the other end of the screen when trying to escape
        self.there_is_no_escape()
        #YOUR CODE HERE -----------

        # For simplicity, we refer to the current agent as "Bird" and the neighbouring agents as "Individuals" or "Neighbours"

        # If a bird has no neigbours, it continues wandering,
        if self.in_proximity_accuracy().count() == 0:
            self.pos += self.move
    
        else:
            # Part 1 - Alignment
            # First we need to create a list with all the neigbours of an individual.
            neighbours = list(self.in_proximity_accuracy())
            # Then we initiate the sum.
            sum_velocity = Vector2(0,0)
            # Then we loop through the list and add the velocity of each neighbour to the sum.
            for boid, _ in neighbours:
                # The velocity has to be normalized otherwise the birds stop moving when they meet a neighbour
                sum_velocity += boid.move.normalize()

            # Then we calculate the average velocity of the neighbours.
            avg_velocity = sum_velocity / len(neighbours)
            # The birds adjust their alignment accourding to their neighbours, 
            # so the alignment is calculated by subtracting the move of the individual from the average velicity.
            # This helps the bird join the flock.
            alignment = avg_velocity - self.move

            # Part 2 - Seperation
            # We initialize the sum of the positions
            sum_pos = Vector2(0,0)
            # Then we loop through the list and add the position of each neighbour to the sum.
            for boid, _ in neighbours:
                # Just the positions would result in a wrong value, 
                # so for each neighbouring individual we subtract its position from the bird position. 
                sum_pos += self.pos - boid.pos

            # Then we calculate the average position of the neighbours.
            # This helps make sure that the birds don't converge in the same position (overlap)
            seperation = sum_pos / len(neighbours)

            # Part 3 - Cohesion
            # We initialize the average position
            avg_pos = Vector2(0,0)
            # Then we loop through the list and add the position of each neighbour to the sum.
            for boid, _ in neighbours:
                avg_pos += boid.pos

            # Then we calculate the average position of the neighbours.
            avg_pos = avg_pos / len(neighbours)

            # The birds adjust their cohesion force accourding to their neighbours,
            # so the cohesion is calculated by subtracting the position of the individual from the average position.
            # This helps the bird join the flock.
            cohesion_force = avg_pos - self.pos
            cohesion = cohesion_force - self.move

            # Finally we calculate the total force by adding the three forces together. Multiplied by their individual weight.
            # Then we divide by the mass to make the merging of the flock more natural.
            total_force = (alignment * self.config.alignment_weight +
                            seperation * self.config.separation_weight +
                            cohesion * self.config.cohesion_weight) / self.config.mass
 
            # If the speed of the birds becomes too high, we decrease it.
            if self.move.length() > sum_velocity.length():
                self.move.normalize() * sum_velocity

            # We add the total force to the move of the bird.
            self.move += total_force
            # We update the position of the bird.
            self.pos += self.move
        #END CODE -----------------


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
    .spawn_obstacle("images/triangle@50px.png", x //2 , y // 2)
    .run()
    
)
