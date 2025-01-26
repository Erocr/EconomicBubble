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

    splash_screen = SplashScreen(view.screenSize)
    settings = Settings()

    clock = pg.time.Clock()

    current_state = "splash_screen"

    cards = CardsPair(view)
    observer.add_observable(cards)
    cards.set_cards("akjf aojbdja joa jbsjalsc pk hao", "qksjsnq jsdaojbcak,cabs aoskja")

    paused = False
    tutorial = False
    frames = 0
    while not inputs.quit:
        inputs.update() 
        # if not economy_graph.has_exploded():
        if current_state == "splash_screen":
            e = splash_screen.update(inputs)
            splash_screen.draw(view)
            if e: current_state = "game"

        elif current_state == "game":

            if settings.update(inputs, music):
                paused = settings.activated
                tutorial = settings.activated

            end = cards.update(inputs)
            if end is not None:
                economy_graph.apply_action(end)
            if not paused:
                paused = cards.actif()

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
                    infoMsg = random.choice(news.news.keys())
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
