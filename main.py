from view import *
from inputs import *
from visual_data import *
from graph import *
from PopUps import *
import news
import random
from splash_screen import *
from end_screen import EndScreen
from music import *
from settings import *

view = View()
inputs = Inputs()
music = Music()

while not inputs.quit:
    endScreen = EndScreen(view)
    observer = Observer()
    visual_data = VisualData(view)
    economy_graph = EconomyGraph(visual_data, observer)

    flash_info = FlashInfo(view.screenSize)
    popups = PopupsContainer()

    observer.add_observable(popups)
    observer.add_observable(flash_info)
    observer.add_observable(music)

    splash_screen = SplashScreen(view.screenSize)
    settings = Settings()

    clock = pg.time.Clock()

    current_state = "splash_screen"

    paused = False
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
            paused = settings.activated

            if not paused: flash_info.update(inputs)
            popups.update(inputs)

            economy_graph.update_visuals(view, inputs, observer, paused)
            if frames % 10 == 0 and not paused:
                economy_graph.update_multigraph()

            if not paused:
                economy_graph.quick_simulation_update()

            if frames % 50 == 0 and not paused:
                economy_graph.update_simulation()

            if frames % 1000 == 0 and not paused:
                flash_info.new_msg(random.choice(news.news)[0])
                observer.notify(EVENT_SOUND, ("news_popup",))

            if economy_graph.has_exploded():
                current_state = "over"
            
            flash_info.draw(view)
            popups.draw(view)
            settings.draw(view)
        
        elif current_state == "over":
            endScreen.update(inputs)
            endScreen.draw(view)
            if (endScreen.play_again_bool == True):
                break


        view.flip()

        clock.tick(50)
        if not paused:
            frames += 1

    


pg.quit()
