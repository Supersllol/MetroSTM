from graphelib import Graphe
from pilefile import Pile, File
import turtle as t
import math
import time


class Trajet:
    def __init__(self, nom, distance, liste_positions):
        self._nom = nom
        self._liste_positions = liste_positions
        self._distance = distance

    def get_nom(self):
        return self._nom

    def get_liste_positions(self):
        return self._liste_positions

    def get_distance(self):
        return self._distance

    def __str__(self):
        return f"{self._nom}: {self._distance}m, positions: {self._liste_positions}"


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

    def is_down(self):
        return self._isdown

    def set_position(self, position):
        self._position = position

    def __str__(self):
        return self.get_nom()


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

    def __str__(self):
        return f"Ligne {self._nom}: {self._ordre_stations}"


def dijkstra(depart, couleurs):
    """Retourne un dictionnaire contenant les distances les plus courtes
    à partir du point de départ pour se rendre à chaque station en passant
    seulement par les stations de couleurs passées en paramètre"""
    # Seulement utiliser les stations des couleurs passées en paramètre
    exterieur = set(
        station
        for station in graphe_metro.listeSommets()
        if (stations[station.__str__()].get_couleurs() & couleurs) != set()
    )
    # Algorithme de Dijkstra, mais en gardant en mémoire la station précédente
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
    passées en paramètre. Retourne un tuple avec la pile, la distance et les couleurs
    des stations parcourues.
    """
    # Convertir depart et arrivee en sommets s'ils sont des stations
    if type(depart) == Station:
        depart = graphe_metro.sommet(depart.__str__())
    if type(arrivee) == Station:
        arrivee = graphe_metro.sommet(arrivee.__str__())
    dist = dijkstra(depart, couleurs)
    # Refaire le chemin à l'envers en empilant les précédentes
    distance, precedent = dist[arrivee]
    chemin = Pile()
    couleurs_parcourues = set()
    couleurs_parcourues |= stations[arrivee.__str__()].get_couleurs()
    chemin.empile(arrivee)
    while precedent != None:
        chemin.empile(precedent)
        couleurs_precedent = stations[precedent.__str__()].get_couleurs()
        if len(couleurs_precedent) == 1:
            couleurs_parcourues |= couleurs_precedent
        precedent = dist[precedent][1]
    return (chemin, distance, couleurs_parcourues)


def station_plus_proche(point):
    """Retourne la station la plus proche du point, avec la distance avec celle-ci"""
    best_station, best_dist = None, math.inf
    for station in stations.values():
        dist = distance(station.get_position(), point)
        if dist < best_dist:
            best_station = station
            best_dist = dist
    return (best_station, best_dist)


def generer_trajets():
    global trajets
    if choix_depart == None or choix_arrivee == None:
        return
    trajets = []
    depart, dist_depart = station_plus_proche(choix_depart)
    dist_m = dist_depart * ratio_m_pixel
    # Si on peut marcher on rajoute l'option
    dist_direct = distance(choix_depart, choix_arrivee.get_position()) * ratio_m_pixel
    if dist_direct <= DISTANCE_MAX_MARCHER:
        trajets.append(
            Trajet("Marche", dist_direct, [choix_depart, choix_arrivee.get_position()])
        )

    chemin, dist_metro, couleurs_parcourues = meilleur_chemin(
        depart, choix_arrivee, {"jaune", "verte", "bleue", "orange"}
    )
    positions = [choix_depart]
    while not chemin.estvide():
        sommet = chemin.depile()
        positions.append(stations[sommet.__str__()].get_position())
    trajets.append(Trajet("Plus court", dist_m + dist_metro, positions))

    # Si trajet déjà resté sur une ligne, pas besoin de continuer
    print(couleurs_parcourues)
    if len(couleurs_parcourues) == 1:
        print(list(trajet.__str__() for trajet in trajets))
        return
    # Si départ et arrivée sur la même ligne, on rajoute l'option de rester sur la même ligne
    inter_couleurs = depart.get_couleurs() & choix_arrivee.get_couleurs()
    if inter_couleurs != set():
        chemin, dist_metro, couleurs_parcourues = meilleur_chemin(
            depart, choix_arrivee, inter_couleurs
        )
        positions = [choix_depart]
        while not chemin.estvide():
            sommet = chemin.depile()
            positions.append(stations[sommet.__str__()].get_position())
        trajets.append(Trajet("Même couleur", dist_m + dist_metro, positions))

    print(list(trajet.__str__() for trajet in trajets))


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
            # Ordre des stations si commence par @
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
    """Lis le fichier contenant les coordonnées de l'ile à dessiner"""
    with open("coord_ile.txt", "r", encoding="utf8") as fp:
        courante = []
        for ligne in fp:
            if ligne == "" or ligne[0] == "#":
                continue
            ligne = ligne.strip()
            # Rajouter la coordonnée à l'ile courante
            if ligne[0] == "*":
                ligne = ligne[1:]
                ile.append(tuple(float(coord) for coord in ligne.split(",")))
                continue
            # Changer d'ile
            if ligne[0] == "-":
                lacs.append(courante)
                courante = []
                continue

            courante.append(tuple(float(coord) for coord in ligne.split(",")))


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

    # Calculer la différence entre le max et le min
    delta = (abs(maximum[0] - minimum[0]), abs(maximum[1] - minimum[1]))
    # Point qui va devenir le (0, 0) sur l'écran
    point_zero = (minimum[0] + delta[0] / 2, minimum[1] + delta[1] / 2)

    # Plus large que haut
    if delta[0] / delta[1] >= LARGEUR / HAUTEUR:
        # Ratio est en pixel / unité de coordonnée géographique (degré)
        # On utilise la hauteur de l'écran et on la divise par le delta pour occuper
        # toute la hauteur
        ratio = (LARGEUR / 2 - GAP_LARGEUR) / (delta[0] / 2)
    else:
        ratio = (HAUTEUR / 2 - GAP_HAUTEUR) / (delta[1] / 2)

    # Différence avec le nouveau point (0, 0) * ratio donne la nouvelle coord
    # Même chose pour stations, lacs et iles
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

    # Trouver le ratio pour convertir des pixels en mètres
    dist_m = graphe_metro.sommet("Montmorency").poids(
        graphe_metro.sommet("De la Concorde")
    )

    dist_px = distance(
        stations["Montmorency"].get_position(),
        stations["De la Concorde"].get_position(),
    )
    global ratio_m_pixel
    ratio_m_pixel = dist_m / dist_px


def dessine_stations():
    """Dessine les stations et les lignes de métro avec leurs noms
    sur l'écran"""
    for ligne in lignes:
        t.tracer(1, 3)
        tortue = t.Turtle()
        tortue.speed(0)
        line_color = ligne.get_couleur()
        tortue.pencolor(line_color)
        tortue.pensize(3)
        tortue.hideturtle()
        tortue.penup()
        # Tracer la ligne en suivant l'ordre des stations
        for nom_station in ligne.get_ordre_stations():
            pos_station = stations[nom_station].get_position()
            tortue.goto(pos_station)
            tortue.pendown()
        tortue.penup()
        tortue.pencolor("black")
        t.tracer(1, 0)
        # Tracer les stations avec un point et son nom
        for nom_station in ligne.get_ordre_stations():
            pos_station = stations[nom_station].get_position()
            tortue.goto(pos_station)
            tortue.dot(8, "black")
            # Alignement du nom
            if stations[nom_station].get_alignement() == "left":
                tortue.seth(0)
            elif stations[nom_station].get_alignement() == "right":
                tortue.seth(180)
            elif stations[nom_station].get_alignement() == "center":
                tortue.seth(90)

            if stations[nom_station].is_down():
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
    """Dessine les lacs sur l'écran"""
    tortue = t.Turtle()
    tortue.hideturtle()
    tortue.speed(0)
    tortue.color(COULEUR_LACS)
    # Remplis les lacs en utilisant les coordonnées du fichier
    for lac in lacs:
        tortue.begin_fill()
        tortue.penup()
        for pos in lac:
            tortue.goto(pos)
            tortue.pendown()
        tortue.end_fill()


def dessine_ile():
    """Dessine l'ile St-Hélène pour la station Jean-Drapeau"""
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


def dessine_bouton_depart():
    """Dessine le bouton servant à choisir la position de départ"""
    tortue = t.Turtle()
    tortue.hideturtle()
    tortue.penup()
    tortue.goto(POS_BOUTON_DEPART)
    tortue.color("red")
    tortue.begin_fill()
    tortue.setheading(0)
    for i in range(4):
        tortue.forward(TAILLE_BOUTON_DEPART)
        tortue.right(90)
    tortue.end_fill()


def dessine_bouton_generer():
    """Dessine le bouton servant à générer les trajets"""
    tortue = t.Turtle()
    tortue.hideturtle()
    tortue.penup()
    tortue.goto(POS_BOUTON_GENERER)
    tortue.color("gray")
    tortue.begin_fill()
    tortue.setheading(0)
    for i in range(2):
        tortue.forward(LARGEUR_BOUTON_GENERER)
        tortue.right(90)
        tortue.forward(HAUTEUR_BOUTON_GENERER)
        tortue.right(90)
    tortue.end_fill()
    tortue.color("black")
    tortue.goto(POS_TEXTE_GENERER)
    tortue.write("Générer", font=("Arial", 8, "bold"))

def dessine_animations(liste_de_positions):
    """Dessine le chemin à faire selon une liste de position"""
    anim = t.Turtle()
    anim.hideturtle()
    anim.color('#056cf1')
    anim.penup()
    anim.pensize(5)
    anim.goto(liste_de_positions[0])
    anim.pendown()
    
    for position in range(len(liste_de_positions)):
        anim.goto(liste_de_positions[position])

def choix_station(x, y):
    """Retourne la station qui correspond à l'endroit cliqué (ou None si aucune)"""
    for station in stations.values():
        pos = station.get_position()
        # Si les coordonnées du clic se situent dans un rectangle autour de la station
        if (pos[0] - RAYON_CLIC <= x <= pos[0] + RAYON_CLIC) and (
            pos[1] - RAYON_CLIC <= y <= pos[1] + RAYON_CLIC
        ):
            global choix_arrivee
            t.tracer(1, 3)
            tortue_cercle_arrivee.goto(pos)
            tortue_cercle_arrivee.showturtle()
            choix_arrivee = station
            texte_depart_arrivee()
            return station

    return None


def dans_rectangle(x, y, min_x, max_x, min_y, max_y):
    """Retourne un booléen qui correspond à si le point (x, y) est dans
    la zone spécifiée par les paramètres (on assume un rectangle)"""
    return (min_x <= x <= max_x) and (min_y <= y <= max_y)


def clic(x, y):
    """Gère les cas possibles lorsque l'usager clique sur l'écran"""
    # Différents boutons possibles
    if dans_rectangle(
        x,
        y,
        POS_BOUTON_DEPART[0],
        POS_BOUTON_DEPART[0] + TAILLE_BOUTON_DEPART,
        POS_BOUTON_DEPART[1] - TAILLE_BOUTON_DEPART,
        POS_BOUTON_DEPART[1],
    ):
        input_depart()
    elif dans_rectangle(
        x,
        y,
        POS_BOUTON_GENERER[0],
        POS_BOUTON_GENERER[0] + LARGEUR_BOUTON_GENERER,
        POS_BOUTON_GENERER[1] - HAUTEUR_BOUTON_GENERER,
        POS_BOUTON_GENERER[1],
    ):
        generer_trajets()
    else:
        choix_station(x, y)


def texte_depart_arrivee():
    """Affiche à l'écran les choix de station de départ et d'arrivée"""
    t.tracer(0)
    tortue_depart_arrivee.clear()
    tortue_depart_arrivee.goto(POS_TEXTE_DEPART)
    tortue_depart_arrivee.write(f"Départ: {choix_depart}", font=("Arial", 8, "bold"))
    tortue_depart_arrivee.goto(POS_TEXTE_ARRIVEE)
    tortue_depart_arrivee.write(f"Arrivée: {choix_arrivee}", font=("Arial", 8, "bold"))


def input_depart():
    global choix_depart
    while True:
        reponse = t.textinput("Où suis-je", "Où êtes-vous? (x,y): ")
        if reponse == None:
            return

        parties = reponse.split(",")
        if len(parties) == 2:
            try:
                x = int(parties[0].strip())
                y = int(parties[1].strip())
                if (
                    -LARGEUR / 2 <= x <= LARGEUR / 2
                    and -HAUTEUR / 2 <= y <= HAUTEUR / 2
                ):
                    choix_depart = (x, y)
                    t.tracer(1, 3)
                    tortue_cercle_depart.goto(x, y)
                    tortue_cercle_depart.showturtle()
                    texte_depart_arrivee()
                    return
                else:
                    print(
                        "Les coordonnées doivent être dans les limites 0-1280 pour x et 0-750 pour y."
                    )
            except ValueError:
                print("Veuillez entrer deux nombres entiers séparés par une virgule.")
        else:
            print("Veuillez entrer deux nombres séparés par une virgule.")


"""
Le Métro
"""

LARGEUR = 1920
HAUTEUR = 1010

GAP_HAUTEUR = 50
GAP_LARGEUR = 50

POS_TEXTE_DEPART = (-(LARGEUR / 2) + GAP_LARGEUR * 2, -HAUTEUR / 6)
POS_TEXTE_ARRIVEE = (POS_TEXTE_DEPART[0], POS_TEXTE_DEPART[1] - 25)
POS_TEXTE_GENERER = (POS_TEXTE_DEPART[0], POS_TEXTE_ARRIVEE[1] - 25)

TAILLE_BOUTON_DEPART = 17
POS_BOUTON_DEPART = (
    POS_TEXTE_DEPART[0] - GAP_LARGEUR / 2,
    POS_TEXTE_DEPART[1] + TAILLE_BOUTON_DEPART / 1.1,
)

POS_BOUTON_GENERER = (POS_TEXTE_DEPART[0] - 15, POS_TEXTE_ARRIVEE[1] - 10)
HAUTEUR_BOUTON_GENERER = 17
LARGEUR_BOUTON_GENERER = 75

COULEUR_LACS = "#07426F"
COULEUR_TERRE = "#D7E7F6"

RAYON_CLIC = 6

DISTANCE_MAX_MARCHER = 2500


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

# ami_2 comme gif de personnage
t.register_shape("ami_2.gif")

stations = {}
graphe_metro = Graphe(False)
lignes = []
lacs = []
ile = []
trajets = []
ratio_m_pixel = 0

choix_arrivee = None
choix_depart = None

# code pour générer le personnage
# t.register_shape("ami_2.gif")

# player = t.Turtle()
# player.hideturtle
# player.penup()
# player.shape("ami_2.gif")

tortue_depart_arrivee = t.Turtle()
tortue_depart_arrivee.hideturtle()
tortue_depart_arrivee.penup()
tortue_depart_arrivee.shape("ami_2.gif")

tortue_cercle_arrivee = t.Turtle(shape="circle")
tortue_cercle_arrivee.shapesize(0.5)
tortue_cercle_arrivee.speed(0)
tortue_cercle_arrivee.penup()
tortue_cercle_arrivee.color("aqua")
tortue_cercle_arrivee.hideturtle()

tortue_cercle_depart = t.Turtle(shape="ami_1.gif")
tortue_cercle_depart.shapesize(0.5)
tortue_cercle_depart.speed(0)
tortue_cercle_depart.penup()
tortue_cercle_depart.color("red")
tortue_cercle_depart.hideturtle()

lire_fichier_metro()
lire_fichier_ile()
conversion_pos()

# test = meilleur_chemin(
#     graphe_metro.sommet("Honoré-Beaugrand"),
#     graphe_metro.sommet("Côte-Vertu"),
#     {"orange", "verte", "bleue"},
# )
# print(test[0], test[1])

l = [(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)]
dessine_animations(l)


dessine_lacs()
dessine_ile()
dessine_stations()
texte_depart_arrivee()
dessine_bouton_depart()
dessine_bouton_generer()


ecran.listen()
ecran.onscreenclick(clic)
ecran.mainloop()
