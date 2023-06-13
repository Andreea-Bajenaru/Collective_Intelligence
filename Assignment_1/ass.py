# Assignment 1
from typing import Optional
from pygame.math import Vector2
from pygame.surface import Surface
from vi import Agent, Simulation, Config
import polars as pl
from typing import List
from typing import Union
#import seaborn as sns
from vi.simulation import HeadlessSimulation
import numpy as np


class MyAgent(Agent):
    def __init__(self, images: List[Surface], simulation: HeadlessSimulation, pos: Union[Vector2, None] = None, move: Union[Vector2, None] = None, count=np.random.randint(20,50)):
        super().__init__(images, simulation, pos, move)
        self.count = count

    def update(self):
        
        # count how many individuals yo have met
        nei = self.in_proximity_accuracy().count()
        assume = nei * 1.5
        p_leave =  nei / (nei + 1) # change global num of ind
        if self.on_site():
            if self.count > 0:
                self.count -= 1
                self.pos += self.move
            else:
                self.freeze_movement()
                leave = np.random.uniform() - 0.4 # makes theme stay when the meet a lot of agents.
                # we could implement a second probability of moving.
                if leave > p_leave:
                    self.continue_movement()

        else:
            self.pos += self.move

config = Config()
x, y = config.window.as_tuple()
(
Simulation(Config(radius=20,seed=1))
                        .spawn_site("images/site_small.png", x//3, y//2)
                        .spawn_site("images/site.png", x//1.5, y//2)
                        .batch_spawn_agents(50, MyAgent,images=["images/red.png"])
                        #.spawn_site("images/site.png", x//2, y//2)
                        
                        .run()
)