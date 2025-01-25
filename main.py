from view import *
from inputs import *
from visual_data import *
from graph import *

view = View()
inputs = Inputs()
visual_data = VisualData(view)
economy_graph = EconomyGraph(visual_data)
clock = pg.time.Clock()

while not inputs.quit:
    inputs.update()

    economy_graph.update_visuals(view, inputs)
    view.flip()

    clock.tick(50)

pg.quit()
