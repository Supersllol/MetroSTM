import turtle as t
import time

ecran = t.Screen()
ecran.title("Les amis")
ecran.setup(1200, 1200)

t.register_shape("ami_1.gif")

player = t.Turtle()
player.penup()
player.shape("ami_1.gif")

time.sleep(2)
player.showturtle
player.forward(200)

# Bouger le personnage

t.exitonclick()