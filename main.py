from view import *
from inputs import *


view = View()
inputs = Inputs()

while not inputs.quit:
    inputs.update()
    view.text("Hello Je mange quelque chose", Vec(100, 0), 200)
    view.flip()
pg.quit()
