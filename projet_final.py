from graphelib import Graphe
from pilefile import Pile, File
import turtle as t


class Station:
    def __init__(self, nom, ligne, position):
        self._nom = nom
        self._ligne = ligne
        self._position = position

    def get_nom(self):
        return self._nom

    def get_ligne(self):
        return self._ligne

    def get_position(self):
        return self._position

    def set_position(self, position):
        self._position = position


class Ligne:
    def __init__(self, nom, couleur, ordre_stations):
        self._nom = nom
        self._couleur = couleur
        self._ordre_stations = ordre_stations

    def get_nom(self):
        return self._nom

    def get_couleur(self):
        return self._couleur

    def get_ordre_stations(self):
        return self._ordre_stations


def lire_fichier_metro(nom_fichier):
    """Lis le fichier contenant l'information sur le réseau de métro, en construisant un
    graphe reliant les stations avec les distances entre elles, et en créant des stations
    avec leurs position et leur(s) couleur(s)
    """
    g = Graphe(False)
    with open(nom_fichier, "r", encoding="utf8") as fp:
        for ligne in fp:
            if ligne == "" or ligne[0] == "#":
                continue
            ligne = ligne.strip()

            depart, ligne = ligne.split("(")

            position, ligne = ligne.split(")")
            position = tuple(float(a) for a in position.split(","))

            connexions, couleurs = ligne.split("%")
            connexions = tuple(tuple(i.split("*")) for i in connexions.split("&"))
            couleurs = tuple(couleurs.split("$"))

            stations[depart] = Station(depart, couleurs, position)

            for connexion in connexions:
                if len(connexion) != 2:
                    continue

                (station, distance) = connexion
                g.ajouteArete(depart, station, distance)
    return g


def distance(point_a, point_b):
    """Prends deux tuples et retourne la distance entre les deux points"""
    return ((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2) ** 0.5


def conversion_pos():
    """Convertis les positions des stations pour être dans le référentiel de l'écran"""
    # Stations plus à l'est et au nord
    maximum = (
        stations["Longueuil-Université-de-Sherbrooke"].get_position()[1],
        stations["Honoré-Beaugrand"].get_position()[0],
    )

    # Stations plus à l'ouest et au sud
    minimum = (
        stations["Montmorency"].get_position()[1],
        stations["Angrignon"].get_position()[0],
    )

    delta = (abs(maximum[0] - minimum[0]), abs(maximum[1] - minimum[1]))
    point_zero = (minimum[0] + delta[0] / 2, minimum[1] + delta[1] / 2)

    if delta[0] / delta[1] >= LARGEUR / HAUTEUR:
        # Plus large que haut
        ratio = (LARGEUR / 2 - GAP_LARGEUR) / (delta[0] / 2)
    else:
        ratio = (HAUTEUR / 2 - GAP_HAUTEUR) / (delta[1] / 2)

    for ligne in lignes:
        for station in ligne.get_ordre_stations():
            pos = stations[station].get_position()
            # print("old", pos)
            new_pos = (
                (pos[1] - point_zero[0]) * ratio,
                (pos[0] - point_zero[1]) * ratio,
            )
            # print("new", new_pos)
            stations[station].set_position(new_pos)
            new = t.Turtle(shape="circle")
            new.color(ligne.get_couleur())
            new.shapesize(0.5)
            new.speed(0)
            new.penup()
            new.goto(
                stations[station].get_position()[0], stations[station].get_position()[1]
            )


LARGEUR = 1200
HAUTEUR = 750

GAP_HAUTEUR = 50
GAP_LARGEUR = 50

ecran = t.Screen()
ecran.title("Métro de Montréal")
ecran.setup(LARGEUR, HAUTEUR)

stations = {}
graphe_metro = lire_fichier_metro("reseau_metro.txt")

lignes = [
    Ligne(
        "jaune",
        "yellow",
        ["Berri-UQAM", "Jean-Drapeau", "Longueuil-Université-de-Sherbrooke"],
    ),
    Ligne(
        "orange",
        "orange",
        [
            "Côte-Vertu",
            "Du Collège",
            "De la Savane",
            "Namur",
            "Plamondon",
            "Côte-Sainte-Catherine",
            "Snowdon",
            "Villa-Maria",
            "Vendôme",
            "Place-Saint-Henri",
            "Lionel-Groulx",
            "Georges-Vanier",
            "Lucien-L'Allier",
            "Bonaventure",
            "Square-Victoria-OACI",
            "Place-d'Armes",
            "Champ-de-Mars",
            "Berri-UQAM",
            "Sherbrooke",
            "Mont-Royal",
            "Laurier",
            "Rosemont",
            "Beaubien",
            "Jean-Talon",
            "Jarry",
            "Crémazie",
            "Sauvé",
            "Henri-Bourassa",
            "Cartier",
            "De la Concorde",
            "Montmorency",
        ],
    ),
    Ligne(
        "verte",
        "green",
        [
            "Angrignon",
            "Monk",
            "Jolicoeur",
            "Verdun",
            "De l'Église",
            "LaSalle",
            "Charlevoix",
            "Lionel-Groulx",
            "Atwater",
            "Guy-Concordia",
            "Peel",
            "McGill",
            "Place-des-Arts",
            "Berri-UQAM",
            "Beaudry",
            "Papineau",
            "Frontenac",
            "Préfontaine",
            "Joliette",
            "Pie-IX",
            "Viau",
            "L'Assomption",
            "Cadillac",
            "Langelier",
            "Radisson",
            "Honoré-Beaugrand",
        ],
    ),
    Ligne(
        "bleue",
        "blue",
        [
            "Snowdon",
            "Côte-des-Neiges",
            "Université-de-Montréal",
            "Édouard-Montpetit",
            "Outremont",
            "Acadie",
            "Parc",
            "De Castelnau",
            "Jean-Talon",
            "Fabre",
            "D'Iberville",
            "Saint-Michel",
        ],
    ),
]

conversion_pos()

ecran.exitonclick()
