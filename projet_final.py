from graphelib import Graphe
from pilefile import Pile, File
import turtle as t
import math


class Station:
    def __init__(self, nom, lignes, position, alignement, isdown):
        self._nom = nom
        self._lignes = lignes
        self._position = position
        self._alignement = alignement
        self._isdown = isdown

    def get_nom(self):
        return self._nom

    def get_ligne(self):
        return self._lignes

    def get_position(self):
        return self._position

    def get_alignement(self):
        return self._alignement

    def get_alignement(self):
        return self._alignement
    
    def isdown(self):
        return self._isdown

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


def dijkstra(depart, couleurs):
    exterieur = set(graphe_metro.listeSommets())
    dist = {s: [math.inf, None] for s in exterieur}
    dist[depart][0] = 0
    while len(exterieur) > 0:
        dmin = math.inf
        for s in exterieur:
            if dist[s][0] < dmin:
                (a, dmin) = (s, dist[s][0])
        exterieur.remove(a)
        for b in a.listeVoisins():
            if b in exterieur:
                new_dist = dist[a][0] + a.poids(b)
                if dist[b][0] > new_dist:
                    dist[b] = (new_dist, a.__str__())
    return dist


def meilleur_chemin(depart, arrivee, couleurs):
    """Retourne le chemin le plus court entre la station d'arrivée et de départ,
    en passant seulement par les stations des couleurs passées en paramètre.
    """


def lire_fichier_metro(nom_fichier):
    """Lis le fichier contenant l'information sur le réseau de métro. Construit un
    graphe reliant les stations avec les distances entre elles, crée des stations
    avec leurs position et leur(s) couleur(s), et initialise les lignes de métro
    avec les stations dans le bon ordre.
    """
    with open(nom_fichier, "r", encoding="utf8") as fp:
        for ligne in fp:
            if ligne == "" or ligne[0] == "#":
                continue

            ligne_og = ligne
            ligne = ligne.strip()

            if ligne[0] == "@":
                ligne = ligne[1:]
                ligne = ligne.split("*")
                nom = ligne[0]
                lignes.append(Ligne(nom, couleurs_lignes[nom], ligne[1:]))
                continue

            depart, ligne = ligne.split("(")
            position, ligne = ligne.split(")")
            position = tuple(float(a) for a in position.split(","))

            connexions, couleurs = ligne.split("%")
            connexions = tuple(tuple(i.split("*")) for i in connexions.split("&"))
            couleurs = tuple(couleurs.split("$"))

            alignement = ligne.split("=")
            if len(alignement) == 2:
                alignement2 = alignement[1].split("!")
                if len(alignement2) == 2:
                    alignement = alignement2[0]
                else:
                    alignement = alignement[1]
            else:
                alignement = 'left'

            if '!' in ligne_og:
                isdown = True
            else:
                isdown = False

            stations[depart] = Station(depart, couleurs, position, alignement, isdown)

            for connexion in connexions:
                if len(connexion) != 2:
                    continue
                (station, distance) = connexion
                graphe_metro.ajouteArete(depart, station, float(distance))


def distance(point_a, point_b):
    """Prends deux tuples et retourne la distance entre les deux points"""
    return ((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2) ** 0.5


def conversion_pos():
    """Convertis les positions des stations pour être dans le référentiel de l'écran."""
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

    for nom_station in stations.keys():
        pos = stations[nom_station].get_position()
        new_pos = (
            (pos[1] - point_zero[0]) * ratio,
            (pos[0] - point_zero[1]) * ratio,
        )
        stations[nom_station].set_position(new_pos)

def dessine_stations():
    global alignement

    for ligne in lignes:
        tortue = t.Turtle()
        tortue.speed(0)
        line_color = ligne.get_couleur()
        tortue.pencolor(line_color)
        tortue.pensize(3)
        tortue.hideturtle()
        tortue.penup()
        for nom_station in ligne.get_ordre_stations():
            pos_station = stations[nom_station].get_position()
            tortue.goto(pos_station)
            tortue.pendown()
        tortue.penup()
        tortue.pencolor("black")
        for nom_station in ligne.get_ordre_stations():
            pos_station = stations[nom_station].get_position()
            tortue.goto(pos_station)
            tortue.dot(8, "black")

            if stations[nom_station].get_alignement() == 'left':
                tortue.seth(0)
            elif stations[nom_station].get_alignement() == 'right':
                tortue.seth(180)
            elif stations[nom_station].get_alignement() == 'center':
                tortue.seth(90)

            if stations[nom_station].isdown():
                tortue.seth(270)
                tortue.forward(10)
            tortue.forward(5)
        
            tortue.pencolor("black")
            tortue.write(
                nom_station,
                False,
                align=stations[nom_station].get_alignement(),
                font=("Arial", 8, "bold"),
            )


LARGEUR = 1280
HAUTEUR = 750

GAP_HAUTEUR = 50
GAP_LARGEUR = 50

ecran = t.Screen()
ecran.title("Métro de la SDF")
ecran.setup(LARGEUR, HAUTEUR)
ecran.bgcolor("#D7E7F6")
# couleur lac: #07426f
# au besoin...
# gris foncé: #2b2b2b
# gris pâle: #666666
couleurs_lignes = {
    "jaune": "#FCD205",
    "verte": "#01A852",
    "bleue": "#1182CE",
    "orange": "#F47416",
}

stations = {}
graphe_metro = Graphe(False)
lignes = []

lire_fichier_metro("reseau_metro.txt")
conversion_pos()
resultat = dijkstra(graphe_metro.sommet("Montmorency"), None)
print(list((som.__str__(), res[0], res[1]) for som, res in resultat.items()))

dessine_stations()
ecran.exitonclick()
