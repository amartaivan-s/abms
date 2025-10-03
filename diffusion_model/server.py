from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider

from model import DiffusionModel

# --- Portrayal ---
def agent_portrayal(agent):
    color = "Red" if agent.infected else "Green"
    r = 0.6 + 0.6 * min(agent.infected_level, 1.0)
    return {"Shape": "circle", "Filled": "true", "Layer": 1, "Color": color, "r": r}

# --- Fixed Canvas size ---
CANVAS_WIDTH_PX = 500
CANVAS_HEIGHT_PX = 500

# FIX grid to max expected size (e.g., 50x50)
grid = CanvasGrid(agent_portrayal, 50, 50, CANVAS_WIDTH_PX, CANVAS_HEIGHT_PX)

# --- Charts ---
chart_counts = ChartModule(
    [
        {"Label": "Infected", "Color": "#d62728"},
        {"Label": "Susceptible", "Color": "#2ca02c"},
    ],
    data_collector_name="datacollector",
    canvas_height=200,
)

chart_avg = ChartModule(
    [{"Label": "AvgInfectedLevel", "Color": "#1f77b4"}],
    data_collector_name="datacollector",
    canvas_height=150,
)

# --- User parameters ---
model_params = {
    "N_infected": Slider("Initial infected agents (N)", 10, 0, 500, 1),
    "M_susceptible": Slider("Initial non-infected agents (M)", 90, 0, 1000, 1),
    "K": Slider("Grid size K (K x K)", 50, 10, 50, 1),
}

# --- ModularServer ---
server = ModularServer(
    DiffusionModel,
    [grid, chart_counts, chart_avg],
    "Diffusion / Infection / Social Spread Model (Mesa 2.x)",
    model_params,
)

server.port = 8521

if __name__ == "__main__":
    server.launch()
