new = t.Turtle(shape="circle")
            new.color(ligne.get_couleur())
            new.shapesize(0.5)
            new.speed(0)
            new.penup()
            new.goto(
                stations[station].get_position()[0], stations[station].get_position()[1]
            )