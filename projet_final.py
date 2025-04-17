from graphelib import Graphe
from pilefile import Pile, File
import turtle as t

LARGEUR = 800
HAUTEUR = 800

ecran = t.Screen()
ecran.title("Métro de Montréal")
ecran.setup(LARGEUR, HAUTEUR)

gif = "tralalero tralala.gif"

ecran.register_shape(gif)
test = t.Turtle()
test.shape(gif)
test.shapesize(0.5, 0.5, 0.5)

ecran.exitonclick()
