from ogm import occupancy_grid_map
from agent import random_search_agent
from visualizer import step_visualizer
# Redefining the module and goal positions for the test
module_positions = {1: (4, 4, 4), 2: (4, 5, 4), 3: (5, 5, 4)}
final_module_positions = {1: (4, 4, 4), 2: (3, 5, 4), 3: (4, 5, 4)}


output_path = "random_search.gif"
# Reuse the proper classes from provided definitions
ogmap = occupancy_grid_map.OccupancyGridMap(module_positions, final_module_positions, 3)
visualizer = step_visualizer.StepVisualizer(ogmap, output_path = output_path)
agent = random_search_agent.RandomSearchAgent(max_steps=100)
agent.search(ogmap, visualizer)
gif_path = visualizer.animate()
print(gif_path)