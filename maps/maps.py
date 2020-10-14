import os
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as ptch
import scipy
os.chdir ("G:\TIPE")

## Définition des classes

class Continent:
    def __init__(self,id,nom,pnt):
        self.id = id # int
        self.nom = nom # string
        self.pnt = pnt # int
        self.pays = [] # liste vide puis remplie des id des pays
        
class Pays:
    def __init__(self,id,nom,idContinent,liens):
        self.id = id # int
        self.nom = nom # string
        self.continent = idContinent # int
        self.liens = liens # int array
                        
class Carte:
    def __init__(self,nom):
        """Fonction qui va récupérer tous les donnés de la carte à partir des fichiers"""
        self.continents = [] # variable qui vont contenir les contients de la carte
        self.pays = [] # variable qui vont contenir les pays de la carte
        
        # on recupère le fichier qui contient la configuration de la carte
        fichiersource=open('maps/txt/' + nom + ".txt", 'r')
        
        nbContinent = int(fichiersource.readline().strip()[0]) # on récupère le nombre de continents
        
        # on ajoute les contients dans la variables de la carte
        for i in range(0,nbContinent):
            nom,pnt = fichiersource.readline().strip().split(',') # exemple : Europe,5
            pnt = int(pnt)
            self.continents.append(Continent(i,nom,pnt))
            
        # on ajoute les pays dans la variables de la carte
        i = 0 # le compteur sert pour associer un id à chaque pays
        for pays in fichiersource:
            nom,idContinent,liens = pays.strip().split('|') # exemple : France|1|12,14,15
            idContinent = int(idContinent)
            # on transforme la variable liens en un tableau d'entiers
            liens = liens.split(',')
            for j in range(0,len(liens)):
                liens[j]=int(liens[j])
            
            self.pays.append(Pays(i,nom,idContinent,liens)) # on ajoute le pays à la carte
            self.continents[idContinent].pays.append(i) # on ajoute l'id du pays dans la liste des pays du continent
            i+=1
        
        fichiersource.close() # on ferme le fichier source
        

def createGraphMap(name):
    colorsGraph = ['green','blue','yellow','orange','red','pink','purple','magenta','cyan']
    carte = Carte(name)
    continents = carte.continents
    pays = carte.pays
    G = nx.Graph()
    
    # création des couleurs
    colors = []
    for cont in continents:
        colors.append(colorsGraph[0])
        colorsGraph = colorsGraph[1:]
    
    # création des Nodes (Pays)
    colorsNode = []
    for ps in pays:
        G.add_node(ps.nom)
        colorsNode.append(colors[ps.continent])
    
    # création des liens
    links = []
    for ps in pays:
        for id in ps.liens:
            if (ps.id < id) :
                link = (ps.id,id)
            else:
                link = (id,ps.id)
            if not(link in links):
                links.append(link)
                G.add_edge(ps.nom, pays[id].nom)
    
    plt.close()
    plt.figure(figsize = (10,10))
    nx.draw_kamada_kawai(G, with_labels=False, font_weight='bold', node_color=colorsNode, node_size=1000, node_shape="o", width=1)
    
    rectLegend = []
    nameContinents = []
    for i in range(len(continents)):
        nameContinents.append(continents[i].nom)
        rectLegend.append(ptch.Rectangle((0, 0), 0, 0, color = colors[i]))
    plt.legend(rectLegend, nameContinents, markerscale = 100, frameon = False, fontsize = 15, loc='best')
    path = 'maps/png/'
    if not os.path.exists(path):
        os.makedirs(path)
    plt.savefig(path + name + ".png")
    plt.close()
    
def createMap():
    name = input('nom de la carte : ')
    fichier = open('maps/txt/' + name + ".txt", "w")
    nbContinents = input('Combien de continents ? ')
    fichier.write(nbContinents + '\n')
    nbContinents = int(nbContinents)
    continents = []
    for i in range(nbContinents):
        nom = input('nom du continent ' + str(i) + ' : ')
        pnt = input('Valeur du continent : ')
        texte = nom + ',' + pnt + '\n'
        fichier.write(texte)
        continents.append(nom)
    id = 0
    for i in range(nbContinents):
        nbPays = int(input('Combien de pays dans le continent : ' + continents[i] +' ? '))
        for j in range(nbPays):
            nom = input('nom du pays ' + str(id) + ' : ')
            links = input('Liens du pays (ids séparés par une virgule) : ')
            texte = nom + '|' + str(i) + '|' + links + '\n'
            fichier.write(texte)
            id += 1
    fichier.close()