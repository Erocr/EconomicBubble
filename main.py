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
    view.multiple_curves(Vec(600, 0), Vec(100, 100),
                         [[-5, 0, 3, 7, 8, 5, 3, 0, -1, 6],
                                 [0, -4, -5, 7, 9, 10, 13, 15, -8, -7, -4, -1, 1, 6]], [(255, 255, 255), (255, 0, 0)])
    view.flip()

    clock.tick(50)

pg.quit()
