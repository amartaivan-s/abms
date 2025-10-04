from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import random

from agent import DiffusionAgent

class DiffusionModel(Model):
    """
    Diffusion / social spread / infection model:
    - Start with N infected, M non-infected on a KxK grid.
    - Each step: move randomly (or stay), then interact with neighbors.
    """
    def __init__(self, N_infected=10, M_susceptible=90, K=30, seed=None):
        super().__init__(seed=seed)

        self.N_infected = int(N_infected)
        self.M_susceptible = int(M_susceptible)
        self.K = int(K)

        self.grid = MultiGrid(self.K, self.K, torus=False)
        self.schedule = RandomActivation(self)

        # Place infected agents (red)
        all_positions = [(x, y) for x in range(self.K) for y in range(self.K)]
        random.shuffle(all_positions)

        # Ensure don't exceed grid capacity
        total_agents = self.N_infected + self.M_susceptible
        if total_agents > self.K * self.K:
            raise ValueError("Too many agents for KxK grid cells.")

        uid = 0
        for _ in range(self.N_infected):
            a = DiffusionAgent(uid, self, infected=True)
            self.schedule.add(a)
            self.grid.place_agent(a, all_positions[uid])
            uid += 1

        # Place non-infected agents (green)
        for _ in range(self.M_susceptible):
            a = DiffusionAgent(uid, self, infected=False)
            self.schedule.add(a)
            self.grid.place_agent(a, all_positions[uid])
            uid += 1

        # Data collector
        self.datacollector = DataCollector(
            model_reporters={
                "infected": DiffusionModel.current_infected,
                "susceptible": DiffusionModel.current_susceptible,
                "avg_Level": DiffusionModel.current_infected_level
            }
        )

        
        self.running = True

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

        # Stop automatically if everyone infected
        if all(ag.infected for ag in self.schedule.agents):
            self.running = False

    @staticmethod

    def current_infected(model) -> int:
        return sum(1 for ag in model.schedule.agents if ag.infected)

    @staticmethod

    def current_susceptible(model) -> int:
        return sum(1 for ag in model.schedule.agents if not ag.infected)

    @staticmethod
    def current_infected_level(model) -> float:
        return sum(ag.infected_level for ag in model.schedule.agents) / len(model.schedule.agents)
                