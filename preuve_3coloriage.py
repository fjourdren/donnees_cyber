from enum import Enum
import random
import hashlib
import secrets

# ensemble des couleurs
class Color(Enum):
    RED   = 1
    GREEN = 2
    BLUE  = 3


# fonction pour retirer les doublons dans une liste de tuple
def removeDuplicates(lst): 
    return [t for t in (set(tuple(i) for i in lst))] 


# noeud du graphe contenant la couleur
class Node():
    def __init__(self, color):
        self.color = color


# class d'un graphe
class Graph():
    def __init__(self, nb_nodes, link_probability):
        self.nb_nodes = nb_nodes # nombre de noeuds du graphe

        self.nodes = [] # liste des noeuds du graphe
        self.adjMatrix = [] # liste des lien entre les noeuds
        
    
        # création des noeuds avec des couleurs random
        for i in range(nb_nodes):
            self.nodes.append(Node(random.choice(list(Color))))

        # boucle qui génère les sous tableaux pour avoir des tableaux 2D. Préparation de la structure de donnée
        for x in range(nb_nodes):
            self.adjMatrix.append([0 for i in range(nb_nodes)])

        # boucle entre chaque noeuds afin de vérifier si on créer un lien ou pas
        for i in range(nb_nodes):
            for j in range(nb_nodes):
                node_i = self.nodes[i]
                node_j = self.nodes[j]

                rand = random.random()

                # si les couleurs sont différentes et que l'aléatoire < à la probabilité, alors on ajoute un lien
                if node_i.color != node_j.color and rand < link_probability:
                    self.adjMatrix[i][j] = 1
                    self.adjMatrix[j][i] = 1

    # génère un affichage de la matrice d'adjacence
    def showMatriceAdjacence(self):
        print('{:4}'.format(" "), end = '')
        for x in range(self.nb_nodes):
            print('{:4}'.format(x), end = '')
        print()

        for x in range(self.nb_nodes):
            print('{:4}'.format(x), end = '')
            for y in range(self.nb_nodes):
                if self.adjMatrix[x][y] == 1:
                    print('{:4}'.format(1), end = '')
                else:
                    print('{:4}'.format(" "), end = '')
            print()
    
    def getEdgesTuples(self):
        list_edge = []

        for x in range(self.nb_nodes):
            for y in range(self.nb_nodes):
                if self.adjMatrix[x][y] == 1:
                    if x < y:
                        list_edge.append((x, y))
                    else:
                        list_edge.append((y, x))
        
        return list_edge

    def getEdgesTuplesWithoutDup(self):
        return removeDuplicates(self.getEdgesTuples())


# permutation des couleurs dans les n
def colorPermutation(nodes):
    new_nodes = []
    color_available = list(Color)
    shift = random.randint(0, len(color_available) - 2)
    for n in nodes:
        new_nodes.append(Node(color_available[(n.color.value + shift) % len(color_available)]))
    return new_nodes

# fonction pour mettre en gage les couleurs
def miseEnGageColoriage(nodes, tableau_128b_aleatoire):
    out = []

    for i in range(len(nodes)):
        raw_string = str(nodes[i].color.value + tableau_128b_aleatoire[i])
        couleur_gage = hashlib.sha1(bytes(raw_string, encoding='utf-8')).hexdigest()
        out.append(couleur_gage)

    return out


# génère un tableau de x nombres aléatoire de 128 bytes
def genererTableau128ByteAleatoire(x):
    tab128 = []
    for i in range(x):
        tab128.append(secrets.randbits(128))
    return tab128

# cherche une arête aléatoire entre deux noeuds dans le graphe
def getRandomEdge(graphe):
    edge_without_duplication = graphe.getEdgesTuplesWithoutDup()
    if len(edge_without_duplication) == 0:
        return None

    return random.choice(edge_without_duplication)

# vérifie la preuve d'un coloriage (exécuté côté vérificateur)
def preuveColoriage(graphe, couleurs_gagees, i, j , ci, ri, cj, rj):
    # calcul de hi
    raw_string_hi = str(ci.value + ri)
    hi = hashlib.sha1(bytes(raw_string_hi, encoding='utf-8')).hexdigest()

    # calcul de hj
    raw_string_hj = str(cj.value + rj)
    hj = hashlib.sha1(bytes(raw_string_hj, encoding='utf-8')).hexdigest()

    return ci.value != cj.value and hi == couleurs_gagees[i] and hj == couleurs_gagees[j]

def preuveColoriageIterating(nb_iter, graphe, couleurs_gagees, nodes, tableau_128b_aleatoire):
    valid = True
    for _ in range(nb_iter):
        edge = getRandomEdge(graphe)
        if edge != None:
            i = edge[0]
            j = edge[1]

            if preuveColoriage(graphe, couleurs_gagees, i, j, nodes[i].color, tableau_128b_aleatoire[i], nodes[j].color, tableau_128b_aleatoire[j]) == False:
                valid = False
                break

    return valid

def main():
    # === init du graphe ===
    graphe = Graph(20, 0.5)

    # affichage de la matrice d'adjacence dans la console
    graphe.showMatriceAdjacence()



    # === Mise en gage des couleurs ===
    tableau_128b_aleatoire = genererTableau128ByteAleatoire(graphe.nb_nodes)

    nodes = colorPermutation(graphe.nodes)
    couleurs_gagees = miseEnGageColoriage(nodes, tableau_128b_aleatoire)



    # === Validation d'une preuve de coloriage ===
    nb_iter = 400
    preuve = preuveColoriageIterating(nb_iter, graphe, couleurs_gagees, nodes, tableau_128b_aleatoire)
    print("Validation preuve de coloriage en %d itérations : %s" % (nb_iter, str(preuve)))




if __name__ == "__main__":
    # execute only if run as a script
    main()