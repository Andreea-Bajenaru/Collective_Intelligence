from enum import Enum, auto

import pygame as pg
from pygame.math import Vector2
from vi import Agent, Simulation
from vi.config import Config, dataclass, deserialize


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
            self.pos += self.move        
            #END CODE -----------------
    def update(self):
        site_id = self.on_site_id()
        # Save the site id to the DataFrame
        # if site_id is not None:
        #     self.save_data("site", int(site_id))
        # else:
        #     self.save_data("site", site_id)

        # bool(site_id) would be inaccurate
        # as a site_id of 0 will return False.
        # Therefore, we check whether it is not None instead.
        print("site_id", site_id)
        if site_id is not None:
            # Inspect the site
            self.freeze_movement()

class SiteInspector(Agent):
    def update(self):
        site_id = self.on_site_id()
        if site_id is not None:
            self.save_data("site", int(site_id))
        # Save the site id to the DataFrame
        else:
            self.save_data("site", site_id)

        # bool(site_id) would be inaccurate
        # as a site_id of 0 will return False.
        # Therefore, we check whether it is not None instead.
        if site_id is not None:
            # Inspect the site
            self.freeze_movement()


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
            radius=20,
            seed=1,
        )
    )
    .spawn_site("images/bubble-full.png", 375, 375)
    .batch_spawn_agents(50, Bird, images=["images/bird.png"])
    .run()
)
