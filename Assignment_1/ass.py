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


class MyAgent(Agent):
    def __init__(self, images: List[Surface], simulation: HeadlessSimulation, pos: Union[Vector2, None] = None, move: Union[Vector2, None] = None, count=20):
        super().__init__(images, simulation, pos, move)
        self.count = count

    def update(self):
        if self.on_site():
            if self.count > 0:
                self.count -= 1
                self.pos += self.move
            else:
                self.freeze_movement()
        else:
            self.pos += self.move
            #self.count = 10
        print(self.count)
        
        
        pass

config = Config()
x, y = config.window.as_tuple()
(
Simulation(Config(radius=25))
                        .spawn_site("images/site.png", x//2, y//2)
                        .batch_spawn_agents(50, MyAgent,images=["images/red.png"])
                        #.spawn_site("images/site.png", x//2, y//2)
                        
                        .run()
)
