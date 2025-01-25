from view import *
from inputs import *
from visual_data import *
from graph import *
from PopUps import *
import news
import random

view = View()
inputs = Inputs()
visual_data = VisualData(view)
economy_graph = EconomyGraph(visual_data)
flash_info = FlashInfo(view.screenSize)
clock = pg.time.Clock()

frames = 0
while not inputs.quit:
    inputs.update()
    # if not economy_graph.has_exploded():
    economy_graph.update_visuals(view, inputs)
    economy_graph.quick_simulation_update()

    
    if (frames % 10 == 0):
        economy_graph.update_simulation()
    
    if (frames % 1000 == 0):
        flash_info.new_msg(random.choice(news.news)[0])

    flash_info.update(inputs)
    flash_info.draw(view)
    view.flip()

    clock.tick(50)
    frames += 1
        

pg.quit()
