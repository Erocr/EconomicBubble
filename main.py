from view import *
from inputs import *
from PopUps import *

view = View()
inputs = Inputs()
clock = pg.time.Clock()
popups = PopupsContainer()

frame = 0
while not inputs.quit:
    inputs.update()

    popups.update(inputs)
    popups.draw(view)
    view.flip()
    frame += 1

    clock.tick(50)

pg.quit()
