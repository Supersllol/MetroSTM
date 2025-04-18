from graphelib import Graphe
from pilefile import Pile, File
import turtle as t

LARGEUR = 800
HAUTEUR = 800

ecran = t.Screen()
ecran.title("Métro de Montréal")
ecran.setup(LARGEUR, HAUTEUR)

gif = "tung tung tung sahur.gif"
gif2 = "tralalero tralala.gif"

ecran.register_shape(gif)
ecran.register_shape(gif2)
test = t.Turtle()
test2 = t.Turtle()
test.shape(gif)
test2.shape(gif2)

ecran.exitonclick()
