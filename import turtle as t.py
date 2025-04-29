import turtle as t
import time

ecran = t.Screen()
ecran.title("Métro de la SDF")
ecran.setup(1200, 1200)

t.register_shape("allo2.gif")

player = t.Turtle()
player.penup()
player.shape("allo2.gif")

# Bouger le personnage

t.done()