from graphelib import Graphe
from pilefile import Pile, File
import turtle as t


LARGEUR = 1500
HAUTEUR = 800

GAP_HAUTEUR = 50
GAP_LARGEUR = 50

ecran = t.Screen()
ecran.title("Métro de Montréal")
ecran.setup(LARGEUR, HAUTEUR)


def distance(point_a, point_b):
    """Prends deux tuples et retourne la distance entre les deux points"""
    return ((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2) ** 0.5


pos_vertes = {
    "Angrignon": (45.44632663047244, -73.60438711239586),
    "Monk": (45.45113793597787, -73.59369024231648),
    "Jolicoeur": (45.456959918306445, -73.58191609861242),
    "Verdun": (45.459274239361626, -73.57178397519435),
    "De l'Église": (45.461774201465914, -73.56778156851156),
    "LaSalle": (45.47078387668829, -73.5659081574753),
    "Charlevoix": (45.4783006998537, -73.56983724163561),
    "Lionel-Groulx": (45.48284553457747, -73.5801148437035),
    "Atwater": (45.48939286874781, -73.58465153063497),
    "Guy-Concordia": (45.49576927254413, -73.57871894023853),
    "Peel": (45.50092730279481, -73.5745084700718),
    "McGill": (45.50404316223521, -73.57175459497526),
    "Place-des-Arts": (45.50780216925632, -73.5693345229893),
    "Saint-Laurent": (45.510843218908995, -73.56462334814317),
    "Berri-UQAM": (45.515061686485794, -73.56170677295312),
    "Beaudry": (45.51898897841842, -73.55599233475945),
    "Papineau": (45.52373599331382, -73.55267315869503),
    "Frontenac": (45.53314303795326, -73.55284006027358),
    "Préfontaine": (45.541453942129955, -73.55491874295),
    "Joliette": (45.54705407604158, -73.5522483186083),
    "Pie-IX": (45.5536842533481, -73.55221797293709),
    "Viau": (45.56117413763484, -73.54774197751738),
    "L'Assomption": (45.56933219450834, -73.54736265583931),
    "Cadillac": (45.57689433490281, -73.54728679160522),
    "Langelier": (45.58279889374338, -73.54387289689205),
    "Radisson": (45.58940638495715, -73.53958873597698),
    "Honoré-Beaugrand": (45.59690601105572, -73.53616273612703),
}

pos_oranges = {
    "Côte-Vertu": (45.514038768636055, -73.6829183584655),
    "Du Collège": (45.50941496850408, -73.67454986633142),
    "De la Savane": (45.50037678595598, -73.6609564310472),
    "Namur": (45.49500205974604, -73.65357137081895),
    "Plamondon": (45.49483660611086, -73.63911962860185),
    "Côte-Sainte-Catherine": (45.49243747402053, -73.6338517700045),
    "Snowdon": (45.485435276656894, -73.62821843821655),
    "Villa-Maria": (45.47957542305685, -73.62041857433667),
    "Vendôme": (45.47390294507783, -73.6043393879233),
    "Place-Saint-Henri": (45.47708526407733, -73.58610036664305),
    "Lionel-Groulx": (45.482802454355806, -73.58049991429569),
    "Georges-Vanier": (45.48891254051816, -73.57684672760146),
    "Lucien-L'Allier": (45.495046660169315, -73.57116588593638),
    "Bonaventure": (45.49805031291756, -73.56722704843452),
    "Square-Victoria-OACI": (45.50191326408405, -73.5626759902202),
    "Place-d'Armes": (45.50576434313652, -73.56030338472793),
    "Champ-de-Mars": (45.51020933216487, -73.55681128937808),
    "Berri-UQAM": (45.515020501746925, -73.56130245765378),
    "Sherbrooke": (45.51827318970493, -73.56848695489798),
    "Mont-Royal": (45.524540995265234, -73.58137979800767),
    "Laurier": (45.527122442329926, -73.58634959599692),
    "Rosemont": (45.531220033887976, -73.59749406570799),
    "Beaubien": (45.535482062710294, -73.60492118338372),
    "Jean-Talon": (45.53962155453471, -73.61391869254315),
    "Jarry": (45.54317627925457, -73.62870465000702),
    "Crémazie": (45.54589970663174, -73.63877582614458),
    "Sauvé": (45.549800576580935, -73.65610078954457),
    "Henri-Bourassa": (45.55607437808822, -73.66764172154079),
    "Cartier": (45.56016430122332, -73.6817113213702),
    "De la Concorde": (45.56068026832499, -73.71011112563573),
    "Montmorency": (45.558458178795746, -73.72222663530799),
}

pos_jaunes = {
    "Berri-UQAM": (45.515020501746925, -73.56130245765378),
    "Jean-Drapeau": (45.5125115109037, -73.53275360012107),
    "Longueuil-Université-de-Sherbrooke": (45.52486652235229, -73.52203511856905),
}

pos_bleues = {
    "Snowdon": (45.48556677167683, -73.62748819318881),
    "Côte-des-Neiges": (45.49684239370873, -73.62338787475127),
    "Université-de-Montréal": (45.50272651255283, -73.61837071097955),
    "Édouard-Montpetit": (45.51012593876159, -73.61244375114761),
    "Outremont": (45.52008485268856, -73.61498809615652),
    "Acadie": (45.52341509408773, -73.62373672600935),
    "Parc": (45.53045484959906, -73.62391165194198),
    "De Castelnau": (45.535434032102714, -73.61991157383676),
    "Jean-Talon": (45.53962056492105, -73.61378186795355),
    "Fabre": (45.54660634088847, -73.6081464033723),
    "D'Iberville": (45.5537894890579, -73.60215435101786),
    "Saint-Michel": (45.559874990313844, -73.60010065469058),
}

lignes = [pos_vertes, pos_oranges, pos_jaunes, pos_bleues]

maximum = (
    pos_jaunes["Longueuil-Université-de-Sherbrooke"][1],
    pos_vertes["Honoré-Beaugrand"][0],
)

minimum = (pos_oranges["Montmorency"][1], pos_vertes["Angrignon"][0])

delta = (abs(maximum[0] - minimum[0]), abs(maximum[1] - minimum[1]))
point_zero = (minimum[0] + delta[0] / 2, minimum[1] + delta[1] / 2)

if delta[0] / delta[1] >= LARGEUR / HAUTEUR:
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
        new.speed(0)
        new.penup()
        new.goto(ligne[station][0], ligne[station][1])

distance_ratio = 844.29 / distance(pos_vertes["Angrignon"], pos_vertes["Monk"])

ecran.exitonclick()
