from view import *
from inputs import *
from visual_data import *
from graph import *
from PopUps import *
import news
import random
from splash_screen import *
from music import *
from settings import *

view = View()
inputs = Inputs()
music = Music()

visual_data = VisualData(view)
economy_graph = EconomyGraph(visual_data)

flash_info = FlashInfo(view.screenSize)
popups = PopupsContainer()

observer = Observer()
observer.add_observable(popups)
observer.add_observable(flash_info)
observer.add_observable(music)

splash_screen = SplashScreen(view.screenSize)
settings = Settings()

clock = pg.time.Clock()

current_state = "splash_screen"

frames = 0
while not inputs.quit:
    inputs.update()
    # if not economy_graph.has_exploded():
    if current_state == "splash_screen":
        e = splash_screen.update(inputs)
        splash_screen.draw(view)
        if e: current_state = "game"

    elif current_state == "game":
        settings.update(inputs, music)
        flash_info.update(inputs)
        popups.update(inputs)

        economy_graph.update_visuals(view, inputs, observer)
        if frames % 10 == 0:
            economy_graph.update_multigraph()
        
        economy_graph.quick_simulation_update()

        if frames % 50 == 0:
            economy_graph.update_simulation()

        if frames % 1000 == 0:
            flash_info.new_msg(random.choice(news.news)[0])
            observer.notify(EVENT_SOUND, ("news_popup",))

        flash_info.draw(view)
        popups.draw(view)
        settings.draw(view)
    view.flip()

    clock.tick(50)
    frames += 1
        

pg.quit()
