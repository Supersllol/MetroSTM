from graphelib import Graphe
from pilefile import Pile, File
import turtle as t

LARGEUR = 1000
HAUTEUR = 800

GAP_HAUTEUR = 50
GAP_LARGEUR = 50

ecran = t.Screen()
ecran.title("Métro de Montréal")
ecran.setup(LARGEUR, HAUTEUR)

ligne_verte = {
    "Angrignon": (45.4461, -73.6035),
    "Monk": (45.4527, -73.5942),
    "Jolicoeur": (45.4573, -73.5866),
    "Verdun": (45.4620, -73.5776),
    "De l'Église": (45.4636, -73.5706),
    "LaSalle": (45.4708, -73.5675),
    "Charlevoix": (45.4781, -73.5677),
    "Lionel-Groulx": (45.4860, -73.5794),
    "Atwater": (45.4898, -73.5858),
    "Guy-Concordia": (45.4956, -73.5804),
    "Peel": (45.5010, -73.5746),
    "McGill": (45.5045, -73.5715),
    "Place-des-Arts": (45.5076, -73.5683),
    "Saint-Laurent": (45.5104, -73.5649),
    "Berri-UQAM": (45.5151, -73.5617),
    "Beaudry": (45.5193, -73.5566),
    "Papineau": (45.5240, -73.5517),
    "Frontenac": (45.5310, -73.5491),
    "Préfontaine": (45.5398, -73.5519),
    "Joliette": (45.5461, -73.5516),
    "Pie-IX": (45.5540, -73.5522),
    "Viau": (45.5605, -73.5493),
    "Assomption": (45.5685, -73.5485),
    "Cadillac": (45.5765, -73.5456),
    "Langelier": (45.5830, -73.5412),
    "Radisson": (45.5873, -73.5394),
    "Honoré-Beaugrand": (45.5891, -73.5368),
}

ligne_orange = {
    "Côte-Vertu": (45.5142, -73.6831),
    "Du Collège": (45.5069, -73.6750),
    "De la Savane": (45.4998, -73.6654),
    "Namur": (45.4937, -73.6542),
    "Plamondon": (45.4962, -73.6419),
    "Côte-Sainte-Catherine": (45.4919, -73.6350),
    "Snowdon": (45.4843, -73.6280),
    "Villa-Maria": (45.4804, -73.6173),
    "Vendôme": (45.4734, -73.6033),
    "Place-Saint-Henri": (45.4776, -73.5874),
    "Lionel-Groulx": (45.4860, -73.5794),
    "Georges-Vanier": (45.4902, -73.5749),
    "Lucien-L'Allier": (45.4943, -73.5714),
    "Bonaventure": (45.4979, -73.5673),
    "Square-Victoria-OACI": (45.5014, -73.5635),
    "Place-d'Armes": (45.5053, -73.5599),
    "Champ-de-Mars": (45.5097, -73.5565),
    "Berri-UQAM": (45.5151, -73.5617),
    "Sherbrooke": (45.5192, -73.5667),
    "Mont-Royal": (45.5252, -73.5809),
    "Laurier": (45.5299, -73.5868),
    "Rosemont": (45.5353, -73.5943),
    "Beaubien": (45.5391, -73.6000),
    "Jean-Talon": (45.5401, -73.6112),
    "Jarry": (45.5454, -73.6200),
    "Crémazie": (45.5501, -73.6277),
    "Sauvé": (45.5537, -73.6350),
    "Henri-Bourassa": (45.5559, -73.6510),
    "Cartier": (45.5573, -73.6818),
    "De la Concorde": (45.5580, -73.7009),
    "Montmorency": (45.5579, -73.7205),
}

ligne_jaune = {
    "Berri-UQAM": (45.5151, -73.5617),
    "Jean-Drapeau": (45.5150, -73.5333),
    "Longueuil-Université-de-Sherbrooke": (45.5248, -73.5226),
}

ligne_bleue = {
    "Snowdon": (45.4843, -73.6280),
    "Côte-des-Neiges": (45.4962, -73.6240),
    "Université-de-Montréal": (45.5015, -73.6249),
    "Édouard-Montpetit": (45.5078, -73.6161),
    "Outremont": (45.5162, -73.6136),
    "Acadie": (45.5240, -73.6225),
    "Parc": (45.5316, -73.6193),
    "De Castelnau": (45.5367, -73.6148),
    "Jean-Talon": (45.5401, -73.6112),
    "Fabre": (45.5450, -73.6062),
    "D'Iberville": (45.5499, -73.6015),
    "Saint-Michel": (45.5584, -73.6006),
}

lignes = [ligne_verte, ligne_orange, ligne_jaune, ligne_bleue]

maximum = (
    ligne_jaune["Longueuil-Université-de-Sherbrooke"][1],
    ligne_verte["Honoré-Beaugrand"][0],
)

minimum = (ligne_orange["Montmorency"][1], ligne_verte["Angrignon"][0])

delta = (abs(maximum[0] - minimum[0]), abs(maximum[1] - minimum[1]))
point_zero = (minimum[0] + delta[0] / 2, minimum[1] + delta[1] / 2)

if delta[0] > delta[1]:
    # Plus large que haut
    ratio = (LARGEUR / 2 - GAP_LARGEUR) / (delta[0] / 2)
else:
    ratio = (HAUTEUR / 2 - GAP_HAUTEUR) / (delta[1] / 2)

for ligne in lignes:
    for station in ligne.keys():
        pos = ligne[station]
        ligne[station] = (
            (pos[1] - point_zero[0]) * ratio,
            (pos[0] - point_zero[1]) * ratio,
        )
        new = t.Turtle(shape="circle")
        new.penup()
        new.goto(ligne[station][0], ligne[station][1])


# print(point_zero)

ecran.exitonclick()
