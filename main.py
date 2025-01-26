from view import *
from inputs import *
from visual_data import *
from graph import *
import simulation_core as core
from PopUps import *
import news
import random
from splash_screen import *
from end_screen import EndScreen
from music import *
from settings import *
from event_choice import *

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
    observer.add_observable(economy_graph)

    splash_screen = SplashScreen(view.screenSize)
    settings = Settings()

    clock = pg.time.Clock()

    current_state = "splash_screen"

    cards = CardsPair(view)
    observer.add_observable(cards)

    depause_delay = -1

    paused = False
    tutorial = False
    frames = 0
    while not inputs.quit:
        if depause_delay > 0:
            depause_delay -= 1
            if depause_delay <= 0:
                paused = False
        inputs.update()
        music.update(inputs)
        # if not economy_graph.has_exploded():
        if current_state == "splash_screen":
            e = splash_screen.update(inputs)
            splash_screen.draw(view)
            if e: current_state = "game"

        elif current_state == "game":

            if settings.update(inputs, music):
                paused = settings.activated
                tutorial = settings.activated

            if not paused: flash_info.update(inputs)
            popups.update(inputs)

            economy_graph.update_visuals(view, inputs, observer, paused)
            if not paused:
                if frames % 300 == 0:
                    economy_graph.update_multigraph()

                economy_graph.quick_simulation_update()

                if frames % 40 == 0:
                    economy_graph.save_values()
                    economy_graph.update_simulation()

                if frames % 1000 == 0:
                    infoMsg = random.choice(list(news.news.keys()))
                    flash_info.new_msg(infoMsg)
                    observer.notify(EVENT_SOUND, ("news_popup",))
                    economy_graph.apply_action(news.news[infoMsg])

                if economy_graph.has_exploded():
                    current_state = "over"
            
            flash_info.draw(view)
            popups.draw(view)
            settings.draw(view)
            cards.draw()
            if tutorial:
                economy_graph.draw_docs(view)
            if not paused and cards.actif():
                paused = True
            end = cards.update(inputs)
            if end is not None:
                economy_graph.apply_action(economy_graph.actions[end])
                depause_delay = 10

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
