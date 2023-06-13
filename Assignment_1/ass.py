# Assignment 1
from typing import Optional
from pygame.math import Vector2
from pygame.surface import Surface
from vi import Agent, Simulation, Config
import polars as pl
import seaborn as sns
from vi.simulation import HeadlessSimulation


class MyAgent(Agent):
    def __init__(self, images: list[Surface], simulation: HeadlessSimulation, pos: Vector2 | None = None, move: Vector2 | None = None):
        super().__init__(images, simulation, pos, move)
    
""" def update(self):
        if self.on_site():
        # crave that star damage
            self.freeze_movement()"""

config = Config()
x, y = config.window.as_tuple()

Simulation(Config(radius=50)).batch_spawn_agents(100, MyAgent,
                    images=['images/red.png'
                            ]).spawn_site("images/site.png", 
                                          x//2, y//2).spawn_site("images/output-onlinepngtools.png", x=100, y=100).run()