from graphelib import Graphe
from pilefile import Pile, File
import turtle as t
import math


class Station:
    def __init__(self, nom, couleurs, position, alignement, isdown):
        self._nom = nom
        self._couleurs = couleurs
        self._position = position
        self._alignement = alignement
        self._isdown = isdown

    def get_nom(self):
        return self._nom

    def get_couleurs(self):
        return self._couleurs

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
    exterieur = set(
        station
        for station in graphe_metro.listeSommets()
        if (stations[station.__str__()].get_couleurs() & couleurs) != set()
    )

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
                    dist[b] = (new_dist, a)
    return dist


def meilleur_chemin(depart, arrivee, couleurs):
    """Retourne le chemin le plus court entre la station d'arrivée et de départ
    sous la forme d'une pile, en passant seulement par les stations des couleurs
    passées en paramètre. Retourne un tuple avec la pile et la distance.
    """
    chemin = Pile()
    dist = dijkstra(depart, couleurs)
    distance, precedent = dist[arrivee]
    chemin.empile(arrivee)
    while precedent != None:
        chemin.empile(precedent)
        precedent = dist[precedent][1]
    return (chemin, distance)


def lire_fichier_metro():
    """Lis le fichier contenant l'information sur le réseau de métro. Construit un
    graphe reliant les stations avec les distances entre elles, crée des stations
    avec leurs position et leur(s) couleur(s), et initialise les lignes de métro
    avec les stations dans le bon ordre.
    """
    with open("reseau_metro.txt", "r", encoding="utf8") as fp:
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
            couleurs = couleurs.split("=")[0]
            couleurs = set(couleurs.split("$"))

            alignement = ligne.split("=")
            if len(alignement) == 2:
                alignement2 = alignement[1].split("!")
                if len(alignement2) == 2:
                    alignement = alignement2[0]
                else:
                    alignement = alignement[1]
            else:
                alignement = "left"

            if "!" in ligne_og:
                isdown = True
            else:
                isdown = False

            stations[depart] = Station(depart, couleurs, position, alignement, isdown)

            for connexion in connexions:
                if len(connexion) != 2:
                    continue
                (station, distance) = connexion
                graphe_metro.ajouteArete(depart, station, float(distance))


def lire_fichier_ile():
    with open("coord_ile.txt", "r", encoding="utf8") as fp:
        current = []
        for ligne in fp:
            if ligne == "" or ligne[0] == "#":
                continue
            ligne = ligne.strip()

            if ligne[0] == "*":
                ligne = ligne[1:]
                ile.append(tuple(float(coord) for coord in ligne.split(",")))
                continue

            if ligne[0] == "-":
                lacs.append(current)
                current = []
                continue

            current.append(tuple(float(coord) for coord in ligne.split(",")))


def distance(point_a, point_b):
    """Prends deux tuples et retourne la distance entre les deux points"""
    return ((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2) ** 0.5


def conversion_pos():
    """Convertis les coordonnées géographiques pour être dans le référentiel de l'écran."""
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

    for lac in lacs:
        for j in range(len(lac)):
            lac[j] = (
                (lac[j][1] - point_zero[0]) * ratio,
                (lac[j][0] - point_zero[1]) * ratio,
            )

    for i in range(len(ile)):
        ile[i] = (
            (ile[i][1] - point_zero[0]) * ratio,
            (ile[i][0] - point_zero[1]) * ratio,
        )


def dessine_stations():
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

            if stations[nom_station].get_alignement() == "left":
                tortue.seth(0)
            elif stations[nom_station].get_alignement() == "right":
                tortue.seth(180)
            elif stations[nom_station].get_alignement() == "center":
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


def dessine_lacs():
    tortue = t.Turtle()
    tortue.hideturtle()
    tortue.speed(0)
    tortue.color(COULEUR_LACS)
    for lac in lacs:
        tortue.begin_fill()
        tortue.penup()
        for pos in lac:
            tortue.goto(pos)
            tortue.pendown()
        tortue.end_fill()


def dessine_ile():
    tortue = t.Turtle()
    tortue.hideturtle()
    tortue.speed(0)
    tortue.color(COULEUR_TERRE)
    tortue.begin_fill()
    tortue.penup()
    for pos in ile:
        tortue.goto(pos)
        tortue.pendown()
    tortue.end_fill()


def user_input():
    t.textinput("Où suis-je", "Où êtes-vous?: ")


LARGEUR = 1280
HAUTEUR = 750

GAP_HAUTEUR = 50
GAP_LARGEUR = 50

COULEUR_LACS = "#07426F"
COULEUR_TERRE = "#D7E7F6"
# au besoin...
# gris foncé: #2b2b2b
# gris pâle: #666666

ecran = t.Screen()
ecran.title("Métro de la SDF")
ecran.setup(LARGEUR, HAUTEUR)
ecran.bgcolor(COULEUR_TERRE)
couleurs_lignes = {
    "jaune": "#FCD205",
    "verte": "#01A852",
    "bleue": "#1182CE",
    "orange": "#F47416",
}

stations = {}
graphe_metro = Graphe(False)
lignes = []
lacs = []
ile = []

lire_fichier_metro()
lire_fichier_ile()
conversion_pos()

# test = meilleur_chemin(
#     graphe_metro.sommet("Montmorency"),
#     graphe_metro.sommet("Côte-Vertu"),
#     {"orange"},
# )
# print(test[0], test[1])

dessine_lacs()
dessine_ile()
dessine_stations()
ecran.exitonclick()
