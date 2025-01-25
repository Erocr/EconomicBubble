from view import *
from inputs import *
from game import *

view = View()
inputs = Inputs()
game = Game()
clock = pg.time.Clock()

while not inputs.quit:
    inputs.update()

    game.update(inputs)

    game.draw(view)
    view.flip()

    clock.tick(50)

pg.quit()
