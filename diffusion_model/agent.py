from mesa import Agent
import random

INFECTION_RATES = (0.1, 0.2, 0.3, 0.4, 0.5)

class DiffusionAgent(Agent):
    """
    Agent with an infection level in [0, +), and a per-agent infection_rate.
    - infected_level >= 1.0 -> considered infected (red)
    - infected_level == 0.0 at init for non-infected (green)
    - infected_rate randomly picked for non-infected agents
    """
    def __init__(self, unique_id, model, infected=False):
        super().__init__(unique_id, model)
        self.infected_level = 1.0 if infected else 0.0
        # Only matters for non-infected; infected can keep a placeholder
        self.infection_rate = random.choice(INFECTION_RATES)

    @property
    def infected(self) -> bool:
        return self.infected_level >= 1.0

    def step(self):
        self._move_random_or_stay()
        self._interact()

    def _move_random_or_stay(self):
        # Choose a random neighborhood cell including staying in place.
        candidates = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=True
        )
        new_pos = random.choice(candidates)
        self.model.grid.move_agent(self, new_pos)

    def _interact(self):
        # If non-infected and ANY neighbor is infected this step,
        # add this agent's infection_rate to infected_level.
        if self.infected:
            return
        

        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False)
        any_infected = any(getattr(ag, "infected", False) for ag in neighbors)

        if any_infected:
            self.infected_level += self.infection_rate
            # Cap is not strictly necessary, but keeps values tidy
            if self.infected_level > 1.0:
                self.infected_level = 1.0
