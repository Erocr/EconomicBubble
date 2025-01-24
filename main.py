from view import *
from inputs import *


view = View()
inputs = Inputs()

while not inputs.quit:
    inputs.update()
pg.quit()
