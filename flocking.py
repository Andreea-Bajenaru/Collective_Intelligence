from enum import Enum, auto
import pygame as pg
from pygame.math import Vector2
from vi import Agent, Simulation
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

    def weights(self) -> tuple[float, float, float]:
        return (self.alignment_weight, self.cohesion_weight, self.separation_weight)


class Bird(Agent):
    config: FlockingConfig

    def change_position(self):
        # Pac-man-style teleport to the other end of the screen when trying to escape
        self.there_is_no_escape()
        #YOUR CODE HERE -----------
        # a, b, c = FlockingConfig().weights()
        in_proximity = list(self.in_proximity_accuracy())
        number_of_neighbours = self.in_proximity_accuracy().count()
        if number_of_neighbours == 0:
            self.pos += self.move
        else:
            velocity = Vector2(0,0)
            pos = Vector2(0,0)
            total_pos = Vector2(0,0)
            for agent, dist in in_proximity:
                velocity += agent.move.normalize()
                pos += self.pos - agent.pos
                total_pos += agent.pos
            average_pos = total_pos / number_of_neighbours
            fc = average_pos - self.pos
            cohesion = fc - self.move
            average_vel = velocity / number_of_neighbours
            separtion = pos / number_of_neighbours
            alignment = average_vel - self.move
            acceleration = ((self.config.alignment_weight * alignment) + (self.config.separation_weight * separtion) + (self.config.cohesion_weight * cohesion)) / self.config.mass

            if self.move.length() > self.config.movement_speed:
                self.move += (self.move.normalize() * self.move.length())

            self.move += acceleration 
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
    .run()
)
