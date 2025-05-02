# Projet de métro: Adrien Cordier, Hans Hamelin, Simon Lacroix, Antoni Lafontaine

from graphelib import Graphe
from pilefile import Pile
import turtle as t
import math
import time

"""
Classes
"""


class Station:
    """Classe représentant une station de métro"""

    def __init__(self, nom, couleurs, position, alignement, is_down):
        self._nom = nom
        self._couleurs = couleurs
        self._position = position
        # alignement et is_down servent à placer le nom de la station sur la carte
        self._alignement = alignement
        self._is_down = is_down

    def get_nom(self):
        return self._nom

    def get_couleurs(self):
        return self._couleurs

    def get_position(self):
        return self._position

    def get_alignement(self):
        return self._alignement

    def is_down(self):
        return self._is_down

    def set_position(self, position):
        self._position = position

    def __str__(self):
        return self.get_nom()


class Ligne:
    """Classe représentant une ligne de stations de métro"""

    def __init__(self, nom, couleur, ordre_stations):
        # ordre_stations est une liste de noms de station selon l'ordre de la ligne
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


class Trajet:
    """Classe représentant le trajet d'un wagon de métro"""

    def __init__(self, nom, distance, liste_stations):
        self._nom = nom
        self._liste_stations = liste_stations
        self._distance = distance

    def get_nom(self):
        return self._nom

    def get_liste_stations(self):
        return self._liste_stations

    def get_distance(self):
        return self._distance

    def __str__(self):
        return f"{self._nom}: {self._distance:.2f}m"


class Bouton:
    """Classe représentant un bouton affiché dans le module turtle"""

    def __init__(self, nom, pos_bouton, pos_texte, couleur, largeur, hauteur):
        self._nom = nom
        self._pos_bouton = pos_bouton
        self._pos_texte = pos_texte
        self._couleur = couleur
        self._largeur = largeur
        self._hauteur = hauteur
        self._visible = False

        self._tortue = t.Turtle()
        self._tortue.hideturtle()
        self._tortue.penup()

    def dessine_bouton(self):
        t.tracer(0, 0)
        self._tortue.goto(self._pos_bouton)
        self._tortue.color(self._couleur)
        self._tortue.begin_fill()
        self._tortue.setheading(0)
        # Remplir le rectangle correspondant au bouton
        for i in range(2):
            self._tortue.forward(self._largeur)
            self._tortue.left(90)
            self._tortue.forward(self._hauteur)
            self._tortue.left(90)
        self._tortue.end_fill()
        self._tortue.goto(self._pos_texte)
        self._tortue.color("black")
        self._tortue.write(self._nom, font=("Arial", 8, "bold"))
        self._visible = True

    def clic_dans_bouton(self, x, y):
        if not self._visible:
            return False
        # Si le clic se trouve dans la zone associée au bouton
        return (self._pos_bouton[0] <= x <= self._pos_bouton[0] + self._largeur) and (
            self._pos_bouton[1] <= y <= self._pos_bouton[1] + self._hauteur
        )

    def efface_bouton(self):
        self._tortue.clear()
        self._visible = False

    def est_visible(self):
        return self._visible

    def change_nom(self, nom):
        self._nom = nom


# Fonctions de lecture de fichiers et de setup
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
            # Si commence par @, c'est l'ordre des stations d'une ligne
            if ligne[0] == "@":
                ligne = ligne[1:]
                ligne = ligne.split("*")
                nom = ligne[0]
                lignes.append(Ligne(nom, couleurs_lignes[nom], ligne[1:]))
                continue
            # Nom de la station et sa position
            depart, ligne = ligne.split("(")
            position, ligne = ligne.split(")")
            position = tuple(float(a) for a in position.split(","))
            # Station connectées et couleurs de la station principale
            connexions, couleurs = ligne.split("%")
            connexions = tuple(tuple(i.split("*")) for i in connexions.split("&"))
            couleurs = couleurs.split("=")[0]
            couleurs = set(couleurs.split("$"))
            # Alignement du nom de la station
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
            # Ajout au dictionnaire de la nouvelle station
            stations[depart] = Station(depart, couleurs, position, alignement, isdown)
            # Ajout au graphe des nouvelles arêtes
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


def conversion_pos():
    """Convertis les coordonnées géographiques pour être dans le référentiel de l'écran."""
    # Stations plus à l'est et au nord
    maximum = (
        stations["Longueuil"].get_position()[1],
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
            int((pos[1] - point_zero[0]) * ratio),
            int((pos[0] - point_zero[1]) * ratio),
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
    # Utilisation de moyenne de distance entre les stations
    dist_m_tot = 0
    dist_px_tot = 0
    for station_a, station_b, dist_m in graphe_metro.listeAretes(True):
        dist_m_tot += dist_m
        dist_px_tot += distance(
            stations[station_a].get_position(), stations[station_b].get_position()
        )

    global ratio_m_pixel
    ratio_m_pixel = dist_m_tot / dist_px_tot


# Fonctions de graphes / trajets
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
    # Avant de commencer à dépiler on met l'arrivée
    chemin.empile(arrivee)
    while precedent != None:
        chemin.empile(precedent)
        couleurs_precedent = stations[precedent.__str__()].get_couleurs()
        # Ne compte pas les correspondances parmi les couleurs parcourues, serait trop
        if len(couleurs_precedent) == 1:
            couleurs_parcourues |= couleurs_precedent
        precedent = dist[precedent][1]
    return (chemin, distance, couleurs_parcourues)


def generer_trajets():
    """Génère les trajets possibles entre le choix de point de départ et la station d'arrivée.
    Peut générer jusqu'à 3 trajets (marche, chemin le plus court, rester sur la même ligne)
    """
    global trajets
    trajets = []
    # Si choix pas valides, sortir
    if choix_depart == None or choix_arrivee == None:
        return
    depart, dist_depart = station_plus_proche(choix_depart)
    dist_marche = dist_depart * ratio_m_pixel
    # Si on peut marcher on rajoute l'option
    dist_direct = distance(choix_depart, choix_arrivee.get_position()) * ratio_m_pixel
    depart_est_arrivee = depart == choix_arrivee
    # Assez proche ou si seule option
    if dist_direct <= DISTANCE_MAX_MARCHER or depart_est_arrivee:
        trajets.append(Trajet("Marche", dist_direct, [choix_arrivee]))
    # Si la plus proche est l'arrivée éviter de faire dijkstra, aller directement
    if depart_est_arrivee:
        return

    # Trouver le meilleur chemin entre départ et arrivée, 4 couleurs acceptées
    chemin, dist_metro, couleurs_parcourues = meilleur_chemin(
        depart, choix_arrivee, {"jaune", "verte", "bleue", "orange"}
    )
    positions = []
    while not chemin.estvide():
        sommet = chemin.depile()
        positions.append(stations[sommet.__str__()])

    trajets.append(Trajet("Plus court", dist_marche + dist_metro, positions))

    # Si trajet reste sur la même ligne pas besoin de continuer, déjà le plus court
    if len(couleurs_parcourues) == 1:
        return

    # Si départ et arrivée sur la même ligne, on rajoute l'option de rester sur la même ligne
    inter_couleurs = depart.get_couleurs() & choix_arrivee.get_couleurs()
    # S'il n'y a pas de couleurs en commun
    if inter_couleurs == set():
        return
    # Refaire dijkstra seulement avec la couleur en commun
    chemin, dist_metro, couleurs_parcourues = meilleur_chemin(
        depart, choix_arrivee, inter_couleurs
    )
    positions = []
    while not chemin.estvide():
        sommet = chemin.depile()
        positions.append(stations[sommet.__str__()])
    trajets.append(Trajet("Même couleur", dist_marche + dist_metro, positions))


"""
# Fonctions de dessin
"""


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


def dessine_trajet_choisi():
    """Dessine le trajet à l'écran"""
    if len(trajets) == 0:
        return
    liste_de_positions = [
        station.get_position() for station in trajets[choix_trajet].get_liste_stations()
    ]
    t.tracer(1, 3)
    tortue_preview_trajet.color(couleurs_boutons_trajets[choix_trajet])
    tortue_preview_trajet.penup()
    tortue_preview_trajet.clear()
    tortue_preview_trajet.goto(choix_depart)
    tortue_preview_trajet.pendown()

    for position in range(len(liste_de_positions)):
        tortue_preview_trajet.goto(liste_de_positions[position])


def texte_depart_arrivee():
    """Affiche à l'écran les choix de station de départ et d'arrivée"""
    t.tracer(0)
    tortue_texte_choix.clear()
    tortue_texte_choix.goto(POS_TEXTE_DEPART)
    tortue_texte_choix.write(f"Départ: {choix_depart}", font=("Arial", 8, "bold"))
    tortue_texte_choix.goto(POS_TEXTE_ARRIVEE)
    tortue_texte_choix.write(f"Arrivée: {choix_arrivee}", font=("Arial", 8, "bold"))


def texte_trajet():
    """Affiche toutes les stations parcourues par le trajet choisi"""
    tortue_texte_trajet.goto(POS_TEXTE_STATIONS)
    trajet = trajets[choix_trajet]
    noms = [station.__str__() for station in trajet.get_liste_stations()]
    noms = "\n- ".join(noms)
    tortue_texte_trajet.write(
        f"{trajet}\n- {noms}",
        font=("Arial", 12, "bold"),
    )


def animation_déplacement():
    """Animation qui exécute le déplacement"""
    global choix_depart
    global choix_arrivee
    global suit_trajet
    suit_trajet = True
    cacher_options()
    texte_trajet()
    t.tracer(1, 15)
    liste_de_positions = [
        station.get_position() for station in trajets[choix_trajet].get_liste_stations()
    ]

    tortue_personnage.shape("ami_1.gif")
    tortue_personnage.speed(1)
    tortue_personnage.pendown()

    tortue_personnage.goto(liste_de_positions[0])  # aka la station de départ
    # Si pas seulement marcher (1 station)
    if len(liste_de_positions) != 1:
        time.sleep(0.5)
        # Changer de forme
        tortue_personnage.shape("metro_1.gif")
        tortue_personnage.speed(2)

        # déplacements dans les stations
        for position in range(1, len(liste_de_positions)):
            tortue_personnage.goto(liste_de_positions[position])

    tortue_personnage.penup()
    # Recacher les choses une fois le trajet fini
    tortue_cercle_arrivee.hideturtle()
    time.sleep(0.5)
    tortue_personnage.shape("ami_1.gif")
    tortue_personnage.speed(2)

    # jump, jump, jump
    tortue_personnage.speed(1)
    tortue_personnage.goto((tortue_personnage.xcor() - 20, tortue_personnage.ycor()))
    tortue_personnage.speed(2)
    for i in range(3):
        tortue_personnage.goto(
            (tortue_personnage.xcor(), tortue_personnage.ycor() + 60)
        )
        tortue_personnage.goto(
            (tortue_personnage.xcor(), tortue_personnage.ycor() - 60)
        )
    tortue_personnage.speed(0)
    t.tracer(0, 0)
    suit_trajet = False
    choix_arrivee = None
    choix_depart = tortue_personnage.pos()
    texte_depart_arrivee()


"""
Fonctions gérant les clics de l'usager
"""


def clic(x, y):
    """Gère les cas possibles lorsque l'usager clique sur l'écran"""
    global choix_depart
    global choix_trajet
    # Différents boutons possibles
    # Si présentement en train de suivre le trajet, clic ne fait rien
    if suit_trajet:
        return
    tortue_texte_trajet.clear()
    if bouton_generer.clic_dans_bouton(x, y):
        generer_trajets()
        changer_options_trajets()
        choix_trajet = 0
        dessine_trajet_choisi()
    elif bouton_go.clic_dans_bouton(x, y):
        animation_déplacement()
    elif choix_station(x, y) != None:
        cacher_options()
        return
    elif clic_boutons_trajets(x, y) != None:
        return
    else:
        # Si aucune des autres options, utiliser la coordonnée comme point de départ
        choix_depart = (x, y)
        t.tracer(1, 3)
        tortue_personnage.goto(x, y)
        tortue_personnage.showturtle()
        texte_depart_arrivee()
        cacher_options()


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
            choix_arrivee = station
            tortue_cercle_arrivee.goto(pos)
            tortue_cercle_arrivee.showturtle()
            texte_depart_arrivee()
            return station

    return None


def clic_boutons_trajets(x, y):
    """Vérifie si un des boutons de trajets a été cliqué"""
    global choix_trajet
    for i in range(len(boutons_trajets)):
        if boutons_trajets[i].clic_dans_bouton(x, y):
            choix_trajet = i
            dessine_trajet_choisi()
            return i
    return None


"""
Fonctions gérant l'affichage des trajets possibles
"""


def creer_boutons_trajets():
    """Crée les 3 boutons de trajets qui peuvent être affichés"""
    for i in range(3):
        boutons_trajets.append(
            Bouton(
                f"Trajet {i}",
                (POS_1ER_BOUTON_TRAJET[0], POS_1ER_BOUTON_TRAJET[1] + i * GAP_TEXTE),
                (POS_1ER_TEXTE_TRAJET[0], POS_1ER_TEXTE_TRAJET[1] + i * GAP_TEXTE),
                couleurs_boutons_trajets[i],
                TAILLE_BOUTON_TRAJET,
                TAILLE_BOUTON_TRAJET,
            )
        )


def changer_options_trajets():
    """Mettre à jour les options possibles de trajets et les afficher"""
    if len(trajets) == 0:
        return
    cacher_options()
    bouton_go.dessine_bouton()
    for i in range(len(trajets)):
        bouton = boutons_trajets[i]
        trajet = trajets[i]
        bouton.change_nom(trajet.__str__())
        bouton.dessine_bouton()


def cacher_options():
    """Cacher tout ce qui a trait aux trajets"""
    t.tracer(0, 0)
    bouton_go.efface_bouton()
    tortue_preview_trajet.clear()
    tortue_personnage.clear()
    for bouton in boutons_trajets:
        bouton.efface_bouton()


"""
Fonctions gérant l'affichage des trajets possibles
"""


def distance(point_a, point_b):
    """Prends deux tuples et retourne la distance entre les deux points"""
    return ((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2) ** 0.5


def station_plus_proche(point):
    """Retourne la station la plus proche du point, avec la distance avec celle-ci"""
    best_station, best_dist = None, math.inf
    for station in stations.values():
        dist = distance(station.get_position(), point)
        if dist < best_dist:
            best_station = station
            best_dist = dist
    return (best_station, best_dist)


"""
Le Métro
"""


# Constantes pour l'écran
LARGEUR = 1920
HAUTEUR = 1010

# Configuration des positions des objets sur l'écran
GAP_HAUTEUR = 50
GAP_LARGEUR = 50
GAP_TEXTE = 25

HAUTEUR_BOUTONS = 17
LARGEUR_BOUTON_GENERER = 75
LARGEUR_BOUTON_GO = 44
TAILLE_BOUTON_TRAJET = 17

POS_TEXTE_DEPART = (-(LARGEUR / 2) + GAP_LARGEUR * 2, -HAUTEUR / 6)
POS_TEXTE_ARRIVEE = (POS_TEXTE_DEPART[0], POS_TEXTE_DEPART[1] - GAP_TEXTE)
POS_TEXTE_GENERER = (POS_TEXTE_DEPART[0] + 10, POS_TEXTE_ARRIVEE[1] - GAP_TEXTE)
POS_1ER_TEXTE_TRAJET = (POS_TEXTE_GENERER[0] + 200, POS_TEXTE_ARRIVEE[1])
POS_TEXTE_GO = (POS_1ER_TEXTE_TRAJET[0] + 45, POS_TEXTE_GENERER[1])
POS_TEXTE_STATIONS = (-(LARGEUR / 2 - GAP_LARGEUR), (POS_TEXTE_DEPART[1] + 40))

POS_1ER_BOUTON_TRAJET = (
    POS_1ER_TEXTE_TRAJET[0] - GAP_TEXTE,
    POS_1ER_TEXTE_TRAJET[1] - 1,
)
POS_BOUTON_GENERER = (POS_TEXTE_GENERER[0] - 15, POS_TEXTE_GENERER[1] - 1)
POS_BOUTON_GO = (POS_TEXTE_GO[0] - 15, POS_TEXTE_GO[1] - 1)

# Constantes utiles
COULEUR_LACS = "#6EA6D4"
COULEUR_TERRE = "#D7E7F6"

RAYON_CLIC = 6

DISTANCE_MAX_MARCHER = 1000

couleurs_lignes = {
    "jaune": "#FCD205",
    "verte": "#01A852",
    "bleue": "#1182CE",
    "orange": "#F47416",
}

# Configuration de l'écran
ecran = t.Screen()
ecran.title("Métro de la STM")
ecran.setup(LARGEUR, HAUTEUR)
ecran.bgcolor(COULEUR_TERRE)


# Déclaration des variables
stations = {}
graphe_metro = Graphe(False)
lignes = []
lacs = []
ile = []
trajets = []
boutons_trajets = []
couleurs_boutons_trajets = ["#FF0000", "#8B00FF", "#AAFF00"]
bouton_generer = Bouton(
    "Générer",
    POS_BOUTON_GENERER,
    POS_TEXTE_GENERER,
    "gray",
    LARGEUR_BOUTON_GENERER,
    HAUTEUR_BOUTONS,
)
bouton_go = Bouton(
    "Go", POS_BOUTON_GO, POS_TEXTE_GO, "gray", LARGEUR_BOUTON_GO, HAUTEUR_BOUTONS
)
ratio_m_pixel = 0

choix_arrivee = None
choix_depart = None
choix_trajet = 0
suit_trajet = False

# Enregistrer les deux gif
t.register_shape("ami_1.gif")
t.register_shape("metro_1.gif")

# Tortue qui écrit le texte qui montre les choix
tortue_texte_choix = t.Turtle()
tortue_texte_choix.hideturtle()
tortue_texte_choix.penup()

# Tortue qui écrit le texte qui affiche le trajet suivi
tortue_texte_trajet = t.Turtle()
tortue_texte_trajet.hideturtle()
tortue_texte_trajet.penup()

# Tortue qui affiche la station d'arrivée
tortue_cercle_arrivee = t.Turtle(shape="circle")
tortue_cercle_arrivee.shapesize(0.5)
tortue_cercle_arrivee.speed(0)
tortue_cercle_arrivee.penup()
tortue_cercle_arrivee.color("aqua")
tortue_cercle_arrivee.hideturtle()

# Tortue qui affiche les options de trajets
tortue_options_trajets = t.Turtle()
tortue_options_trajets.hideturtle()
tortue_options_trajets.penup()

# Tortue qui dessine les trajets possibles
tortue_preview_trajet = t.Turtle()
tortue_preview_trajet.hideturtle()
tortue_preview_trajet.speed(0)
tortue_preview_trajet.penup()
tortue_preview_trajet.pensize(5)

# Setup sur l'écran
lire_fichier_metro()
lire_fichier_ile()
conversion_pos()

# Affichage de l'interface
dessine_lacs()
dessine_ile()
dessine_stations()
texte_depart_arrivee()
creer_boutons_trajets()
bouton_generer.dessine_bouton()

# Tortue qui identifie la position de l'usager
# Mise après les lacs pour pouvoir passer par-dessus
tortue_personnage = t.Turtle(shape="ami_1.gif")
tortue_personnage.speed(0)
tortue_personnage.color("#056CF1")
tortue_personnage.pensize(5)
tortue_personnage.penup()
tortue_personnage.hideturtle()

# Le clic de l'usager est ce qui détermine ce qui se passe
ecran.listen()
ecran.onscreenclick(clic)
ecran.mainloop()
