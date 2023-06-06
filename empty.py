from vi import Agent, Config, Simulation


class MyAgent(Agent):
    def update(self):
        if self.in_proximity_accuracy().count() > 0:
            self.change_image(1)  # red
        else:
            self.change_image(0)  # white


(
    Simulation(Config(radius=15))
    .batch_spawn_agents(
        500,
        MyAgent,  # 👈 use our own MyAgent class
        images=[
            "examples/images/white.png",
            "examples/images/red.png",
        ],
    )
    .run()
)