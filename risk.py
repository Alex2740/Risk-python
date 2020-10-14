## Normes pour le nommage des fonctions et variables.
# Les fonctions doivent être en anglais et en minuscule.
# Les variables doivent être en français et en minuscule.

## Les Modules
print("[Initialisation]: Importation des modules. 1/4")
import numpy as np
import os
from time import time,localtime
import random as rd
import matplotlib.pyplot as plt
os.chdir ('G:\TIPE')

## Les Classes
print("[Initialisation]: Création des classes. 2/4")
class Carte:
    def __init__(self, nom):
        """Fonction permet de créer toutes les variables liées à la carte pour une partie."""
        # On recupère le fichier qui contient la configuration de la carte
        with open('maps/txt/' + nom + '.txt', 'r') as fichier_source:
            # On récupère le nombre de continents et de pays.
            nombre_continents, nombre_pays = fichier_source.readline().strip().split(',')
            self.nombres = {
                'continents': int(nombre_continents),
                'pays': int(nombre_pays)
            }
            
            # On récupère les données des continents.
            self.continents = [] # Variables qui contient les informations sur les continents.
            for i in range(0, self.nombres['continents']):
                nom, bonus = fichier_source.readline().strip().split(',') # exemple : Europe,5
                bonus = int(bonus)
                self.continents.append({
                    'nom': nom,
                    'bonus': bonus,
                    'id_pays': [],
                    'evaluation': 0
                })
                
            # On récupère les données des pays.
            self.pays = [] # Variables qui contient les informations sur les pays (sauf les liens).
            self.liens = np.zeros((self.nombres['pays'], self.nombres['pays']), dtype='int') # Matrice qui code les liens entre les territoires. (1 = connecté)
            for i in range(0, self.nombres['pays']):
                nom, id_continent,liens = fichier_source.readline().strip().split('|') # exemple : France|1|12,14,15
                id_continent = int(id_continent)
                # On ajoute le pays à la carte
                self.pays.append({
                    'nom': nom,
                    'id_continent': id_continent
                })
                # On ajoute les liens.
                liens = liens.split(',')
                for each in liens:
                    self.liens[i,int(each)] = 1
                
                # On ajoute l'id du pays dans la liste des pays du continent
                self.continents[id_continent]['id_pays'].append(i)
                
            # On vérifie si toutes les lignes du fichier ont bien été lues.
            if fichier_source.readline() != "":
                print("[Warning]:Certaines lignes du fichier n'ont pas été lues. Vérifiez le nombre de pays.")
                
        for c in self.continents:            
            premier = c["id_pays"][0]
            dernier = c["id_pays"][-1]
            pays_frontaliers = 0
            for i in c["id_pays"]:
                deb, fin = self.liens[i, 0 : premier], self.liens[i, dernier + 1 :]
                if sum(deb) + sum(fin) > 0:
                    pays_frontaliers += 1
            c["evaluation"] = (15 + c["bonus"] - (4 * pays_frontaliers)) / len(c["id_pays"]) # (15 + Bonus − 4 × Nombre Pays avec Frontières) / Nombre de territoires
        
class Joueur:
    def __init__(self, identifiant, degre, nombre_pays_total):
        """Fonction qui créer le joueur."""
        self.identifiant = identifiant # int
        self.degre_agressivite = degre # flottant entre 0 et 1 ou -1 pour aléatoire
        self.possessions = np.zeros(nombre_pays_total, dtype='int')
        
    def update(self, modifications):
        """Fonction qui met à jour les possessions du joueur."""
        self.possessions += modifications.astype('int32')
        
    def continents_conquis(self, carte):
        """Fonction qui envoie la liste des continents conquis."""
        nombre_pays_continent = [len(each['id_pays']) for each in carte.continents]
        continents_conquis = []
        for i in range(len(nombre_pays_continent)):
            taille_precedente = sum(nombre_pays_continent[0:i])
            if sum([(each > 0) for each in self.possessions[taille_precedente:taille_precedente + nombre_pays_continent[i]]]) == nombre_pays_continent[i]:
                continents_conquis.append(i)
        return continents_conquis
        
    def continents_pourcentage(self, carte):
        """Fonction qui envoie la liste des continents conquis."""
        nombre_pays_continent = [len(each['id_pays']) for each in carte.continents]
        continents_pourcentage = []
        for i in range(len(nombre_pays_continent)):
            taille_precedente = sum(nombre_pays_continent[0:i])
            pourcentage = sum([(each > 0) for each in self.possessions[taille_precedente:taille_precedente + nombre_pays_continent[i]]])/nombre_pays_continent[i]
            continents_pourcentage.append(pourcentage)
        return continents_pourcentage
        
    def supply_troupes(self, carte):
        """Fonction qui renvoie le nombre de troupes que le joueur reçoit pour la phase de supply."""
        nombre_troupe = max(3,sum([(each > 0) for each in self.possessions])//3)
        for each in self.continents_conquis(carte):
            nombre_troupe += carte.continents[each]['bonus']
        
        return nombre_troupe
        
        
## Les Constantes
# Probabilités
g11 = 5/12
g21 = 125/216
ga1 = 95/144
g32 = 1445/3888
g12 = 55/216
g22 = 295/1296

p22 = 581/1296
p32 = 2275/7776

# Limite de tours pour les partie
limite_nombre_tours = {
    "Lord of the Rings": 1000,
    "Classique": 1000,
    "Frozen Classique": 1000,
    "The Walking Dead": 1000,
    "map_test": 100
}

## Calcul des Probabilités
def get_probabilites():
    n = 500 # limite: 500
    fichier = open('probabilité de gagner une attaque.txt','r')
    probs = np.zeros((n+1,n+1))
    for i in range(n+1):
        ligne = fichier.readline().strip().split('|')
        lg = np.array([float(each) for each in ligne][0:n+1])
        probs[i] = lg
    fichier.close()
    
    return probs

probabilites_calculees = []

def probabilite(a, d):
    """
    Fonction qui renvoie la probabilité de gagner une attaque de a troupes contre b troupes.
    probabilites est le tableau qui contient toutes les probabilités.
    Int -> Int -> Float
    """
    global probabilites, probabilites_calculees
    try:
        probabilites_calculees.append([a,d])
        return probabilites[a,d]
    except: # Si la probabilités demandés n'est pas dans le tableau, on envoie une erreur.
        print("La probabilité demandée n'est pas dans le tableau. Il y a trop de troupes sur un territoire.")
        
        
try:
    taille = len(probabilites)
    print("[Initialisation]: La matrice de probabilités des attaques existe déjà. 3/4")
except:
    print("[Initialisation]: Récupération de la matrice de probabilités des attaques. 3/5")
    probabilites = get_probabilites() # On récupère les probabilités jusqu'à 10000. (temps: < 2 min)
    print("[Initialisation]: La matrice de probabilités des attaques a été récupérée. (max: 5000)")
    
## Fonctions Génériques
print("[Initialisation]: Création des fonctions. 4/4")
def is_connected(pays_1, pays_2, possessions, carte):
    """Fonction qui renvoie si les teritoires sont connectés à l'aide d'un parcours en profondeur."""
    def dfs(pays, possessions, carte, visited=None, ter_ennemi=None):
        """Fonction de parcourt en profondeur."""
        if visited is None:
            visited = []
            
        if ter_ennemi is None:
            ter_ennemi = []
        
        unvisited = []
        if possessions[pays] > 0:
            if pays not in visited:
                visited.append(pays)
                
            liens = carte.liens[pays]
            for i in range(len(liens)):
                if i not in visited and liens[i] > 0:
                    unvisited.append(i)
        else:
            if pays not in ter_ennemi:
                ter_ennemi.append(pays)
                
        for ps in unvisited:
            dfs(ps, possessions, carte, visited, ter_ennemi)
            
        return visited
        
    return pays_2 in dfs(pays_1, possessions, carte)

def get_border_countries(id_pays, joueurs, num_joueur, carte):
    """Fonction qui renvoie les pays frontaliers ennemis."""
    
    # On récupère tous les pays frontaliers.
    border_countries = []
    for i in range(carte.nombres['pays']):
        if carte.liens[id_pays, i]:
            border_countries.append(i)
    
    # On ne garde que les pays ennemis.
    border_enemies_countries = []
    for each in border_countries:
        if joueurs[num_joueur].possessions[each] == 0:
            border_enemies_countries.append(each)
            
    return border_enemies_countries
    
def full_tab(tab, joueur, carte):
    """Fonction qui renvoie le tableau de taille maximale."""
    full_tab = np.zeros(carte.nombres['pays'])
    id_tab = 0
    for each in range(carte.nombres['pays']):
        if (joueur.possessions[each] > 0):
            full_tab[each] = tab[id_tab]
            id_tab += 1

    return full_tab
    
def full_order(ordre, joueur, carte):
    """Fonction qui renvoie les id des possessions dans l'ordre décroissante."""
    id_possessions = np.zeros(len(ordre))
    nombre_territoires_parcouru = 0
    
    for i in range(carte.nombres['pays']):
        if joueur.possessions[i] > 0:
            id_possessions[nombre_territoires_parcouru] = i
            nombre_territoires_parcouru += 1
    full_ordre = np.zeros(len(ordre))
            
    for i in range(len(ordre)):
        full_ordre[i] = id_possessions[ordre[i]]

    return full_ordre

def troops_territory(id, joueurs):
    """Fonction qui renvoie le nombre de troupes sur un territoire."""
    return sum([j.possessions[id] for j in joueurs])
    
def continent(id, carte):
    """Fonction qui renvoie l'id du continent du territoire."""
    for i in range(carte.nombres["continents"]):
        if id in carte.continents[i]["id_pays"]:
            return i
            
def joueur(id, joueurs, carte):
    """Fonction qui renvoie le  possédant le territoire."""
    for i in range(len(joueurs)):
        if joueurs[i].possessions[id] > 0:
            return i

## Fonctions de debug
def save_map_state(joueurs, id_partie):
    """Fonction qui sauvegarde l'état de la carte."""
    chemin = 'debug/results/'
    if not os.path.exists(chemin):
        os.makedirs(chemin)
    nom = chemin + str(id_partie)
    
    with open(nom + '.txt', 'a') as fichier:
        for each in joueurs:
            ligne = str(each.degre_agressivite) + "\t" + str(each.possessions)
            fichier.write(ligne + "\n")

def write_log(id_partie, numero_tour, joueur, phase, destination, troupes_deplacees, origine = -1, troupes_rencontrees = -1, troupes_perdues = -1, troupes_ennemies_perdues = -1):
    """Fonction qui écrit les logs de la partie."""
    
    chemin = 'debug/log'
    if not os.path.exists(chemin):
        os.makedirs(chemin)
        
    with open(chemin + "/" + str(id_partie) + ".txt", "a") as log:
        nouvelle_ligne = str(numero_tour)
        nouvelle_ligne += "\t" + str()
        nouvelle_ligne += "\t" + str(phase)
        nouvelle_ligne += "\t" + str(origine)
        nouvelle_ligne += "\t" + str(destination)
        nouvelle_ligne += "\t" + str(troupes_deplacees)
        nouvelle_ligne += "\t" + str(troupes_rencontrees)
        nouvelle_ligne += "\t" + str(troupes_perdues)
        nouvelle_ligne += "\t" + str(troupes_ennemies_perdues)
        log.write(nouvelle_ligne + "\n")

def modifications_to_log(id_partie, numero_tour, numero_joueur, phase, modifications):
    if phase == 0: # Phase de supply
        for i in range(len(modifications)):
            if modifications[i] != 0:
                write_log(id_partie, numero_tour, numero_joueur, 0, i, int(modifications[i]))
    elif phase == 2: # Phase de reinforcement
        origine = -1
        arrivee = -1
        troupes = -1
        depart = -1
        for i in range(len(modifications)):
            if modifications[i] > 0:
                arrivee = i
                troupes = int(modifications[i])
            if modifications[i] < 0:
                depart = i
        write_log(id_partie, numero_tour, numero_joueur, 2, arrivee, troupes, depart)

## Fonctions Heristiques (pour les évaluations)
def border_security_threat(id_pays,joueurs,num_joueur, carte):
    """Fonction qui renvoie le nombre total de troupes aux frontières d'un pays."""
    total_troupes = 0
    border_enemies_countries = get_border_countries(id_pays,joueurs,num_joueur, carte)
    for i in range(len(joueurs)):
        if (i != num_joueur) :
            for each in border_enemies_countries:
                total_troupes += joueurs[i].possessions[each]
                
    return total_troupes

def border_security_ration(id_pays,joueurs,num_joueur, carte):
    return border_security_threat(id_pays,joueurs,num_joueur, carte)/joueurs[num_joueur].possessions[id_pays]
    
def normalized_border_security_ratio_s(joueurs,num_joueur, carte):
    """Fonction qui renvoie l'ensemble des NBSR d'un ."""
    border_security_ratio_s = []
    for i in range(carte.nombres['pays']):
        if (joueurs[num_joueur].possessions[i] > 0):
            border_security_ratio_s.append(border_security_ration(i,joueurs,num_joueur, carte))
    return np.array(border_security_ratio_s)/sum(border_security_ratio_s)

def border_attack_win_against(id_pays,id_def,joueurs,num_joueur, carte):
    enemies_units = sum([joueurs[i].possessions[id_def] for i in range(len(joueurs))])
    return joueurs[num_joueur].possessions[id_pays]/enemies_units
    
def border_attack_win(id_pays,joueurs,num_joueur, carte):
    """Fonction qui renvoie le BAW d'un pays."""
    border_enemies_countries = get_border_countries(id_pays,joueurs,num_joueur, carte)
    baw = 0
    for each in border_enemies_countries:
        baw += border_attack_win_against(id_pays,each,joueurs,num_joueur, carte)
        
    return baw
    
def normalized_border_attack_win_s(joueurs,num_joueur, carte):
    """Fonction qui renvoie l'ensemble des NBAW d'un ."""
    border_attack_win_s = []
    for i in range(carte.nombres['pays']):
        if (joueurs[num_joueur].possessions[i] > 0):
            border_attack_win_s.append(border_attack_win(i,joueurs,num_joueur, carte))
    return np.array(border_attack_win_s)/sum(border_attack_win_s)
    
def evaluation_possession(joueurs,num_joueur, carte):
    """Fonction qui renvoie l'évaluation de chaque territoiredu ."""
    degre = joueurs[num_joueur].degre_agressivite

    evalDef = normalized_border_security_ratio_s(joueurs,num_joueur, carte)
    evalAtt = normalized_border_attack_win_s(joueurs,num_joueur, carte)
        
    return degre * evalAtt + (1 - degre) * evalDef

## Fonctions utilisées pour l'attaque
def eval_continents(joueurs, num_joueur, carte):
    """Fonction qui renvoie l'évaluation des continents pour un ."""
    eval = np.zeros(carte.nombres["continents"])
    
    for id_continent in range(carte.nombres["continents"]):
        continent = carte.continents[id_continent]
        permier = continent["id_pays"][0]
        dernier = continent["id_pays"][-1]
        
        # Calcul des consantes nécessaires à l'évaluation.
        troupes = sum(joueurs[num_joueur].possessions[permier : dernier + 1])
        total_troupes = sum([sum(joueurs[i].possessions[permier : dernier + 1]) for i in range(len(joueurs))])
        territoires = sum([(each > 0) for each in joueurs[num_joueur].possessions[permier : dernier + 1]])
        
        # ACR(C) = (((Armies of actual player on C / Total Armies on C) + (Territories of actual player on C / Territories on C)) / 2) * continent rating(C)
        evaluation = continent["evaluation"] * ((troupes / total_troupes) + (territoires / len(continent["id_pays"]))) / 2
        
        # On augmente les évaluations inférieures à 0.1. (laisser la posibilité au  de changer de continent.)
        if evaluation < 0.1:
            evaluation = 0.1
        
        eval[id_continent] = evaluation
        
    return eval

def get_possible_attack(joueurs, num_joueur ,carte):
    """Fonction qui récupère toutes les attaques possibles par un ."""
    evaluation_continents = eval_continents(joueurs, num_joueur ,carte)
    attaques_possibles = []
    possessions = joueurs[num_joueur].possessions
    
    for id_terr in range(len(possessions)): # On parcourt chaque pays.
        if possessions[id_terr] > 1:
            pays_frontaliers = get_border_countries(id_terr, joueurs, num_joueur ,carte)
            
            for id_ennemi in pays_frontaliers: # On parcourt chaque pays frontaliers.
                id_continent = continent(id_ennemi ,carte)
                prob = probabilite(joueurs[num_joueur].possessions[id_terr], troops_territory(id_ennemi, joueurs))
                eval = prob * evaluation_continents[id_continent]
                attaques_possibles.append([id_terr, id_ennemi, eval, prob])
                
    return np.array(attaques_possibles)

def assault(troupes_attaquantes, troupes_defendantes):
    """Fonction qui renvoie les troupes restantes à la fin d'un assaut."""
    
    # Lancé des dés de l'attaquant
    if (troupes_attaquantes >= 3):
        lance_attaquant = np.random.randint(1, 6, 3) # Nombre maximal de dés pour l'attaquant.
    else:
        lance_attaquant = np.random.randint(1, 6, troupes_attaquantes)
        
    # Lancé des dés du défenseur
    if (troupes_defendantes >= 2):
        lance_defenseur = np.random.randint(1, 6, 2) # Nombre maximal de dés pour le défenseur.
    else:
        lance_defenseur = np.random.randint(1, 6, troupes_defendantes)
        
    # On trie les résultats des lancés de dés pour ordre croissant.
    lance_attaquant = sorted(lance_attaquant, reverse = True)
    lance_defenseur = sorted(lance_defenseur, reverse = True)
    
    for i in range(min(len(lance_attaquant), len(lance_defenseur))): # On compare les dés un par un en commençant par les plus élevés.
        if lance_attaquant[i] > lance_defenseur[i]: # L'attaquant gagne si son dé est strictement supérieur à celui du défenseur.
            troupes_defendantes -= 1
        else:
            troupes_attaquantes -= 1
            
    return troupes_attaquantes, troupes_defendantes

attaques_realisees = []  

def battle(troupes_attaquantes, troupes_defendantes):
    """Fonction qui renvoie les troupes restantes à la fin d'une bataille."""
    global attaques_realisees
    
    attaques_realisees.append([troupes_attaquantes, troupes_defendantes])
    
    while (troupes_attaquantes > 0) and (troupes_defendantes > 0): # On continue les assauts tant qu'il reste des troupes engagées de chaque coté.
        troupes_attaquantes, troupes_defendantes = assault(troupes_attaquantes, troupes_defendantes)
    return troupes_attaquantes, troupes_defendantes
    
## Fonctions pour le  aléatoire
def random_supply(id_partie, numero_tour, joueur, carte, debug):
    """Fonction qui réalise la phase de Supply d'un  aléatoire."""
    supply = joueur.supply_troupes(carte)
    modifications = np.zeros((sum([(each > 0) for each in joueur.possessions])))
    for _ in range(supply):
        modifications[rd.randrange(len(modifications))] += 1
    
    if debug:
        modifications_to_log(id_partie, numero_tour, joueur.identifiant, 0, modifications)
    
    joueur.update(full_tab(modifications, joueur ,carte))
 
def random_attack(id_partie, numero_tour, joueurs, num_joueur, carte, debug):
    """Fonction qui réalise la phase d'Attaque d'un joueur aléatoire."""
    attaquant = joueurs[num_joueur]
    can_attaque = True
    
    while can_attaque:
        if np.random.randint(0,2) == 1: # Le joueur tire au pile ou face s'il attaque.
            attaques_possibles = get_possible_attack(joueurs, num_joueur ,carte) # On récupère l'ensemble des attaques possibles.
            if len(attaques_possibles) == 0:
                can_attaque = False
                
            else:
                attaque = attaques_possibles[np.random.randint(0,len(attaques_possibles))] # On prend une attaque au hazard.
                
                # On prend les ids des territoires.
                ter_attaquant = int(attaque[0])
                ter_defenseur = int(attaque[1])

                defenseur = joueurs[joueur(ter_defenseur, joueurs, carte)]
                troupes_depart = (attaquant.possessions[ter_attaquant] - 1, defenseur.possessions[ter_defenseur]) # On récupère les troupes sur les territoires.

                troupes_fin = battle(troupes_depart[0], troupes_depart[1]) # On fait l'attaque.
                pertes_attaquant = troupes_fin[0] - troupes_depart[0] # On calcule les pertes de troupes.
                pertes_defenseur = troupes_fin[1] - troupes_depart[1]
                
                modification_attaquant = np.zeros(len(attaquant.possessions))
                modification_defenseur = np.zeros(len(attaquant.possessions))
                
                if troupes_fin[0] == 0:
                        modification_attaquant[ter_attaquant] = pertes_attaquant
                        modification_defenseur[ter_defenseur] = pertes_defenseur
                else:
                        delta = min(3, troupes_fin[0]) # Nombre de troupes placées sur le nouveaux territoires.
                        modification_attaquant[ter_attaquant] = pertes_attaquant - delta
                        modification_attaquant[ter_defenseur] = delta
                        modification_defenseur[ter_defenseur] = pertes_defenseur
    
                # On met à jour les possessions des joueurs.
                attaquant.update(modification_attaquant)
                defenseur.update(modification_defenseur)
                
                if debug:
                    write_log(id_partie, numero_tour, attaquant.identifiant, 1, ter_defenseur, troupes_depart[0], ter_attaquant, troupes_depart[1], pertes_attaquant, pertes_defenseur)
            
        else:
            can_attaque = False
 
def random_reinforcement(id_partie, numero_tour, joueur, carte, debug):
    """Fonction qui réalise la phase de Reinforcement d'un joueur aléatoire."""
    modifications = np.zeros((sum([(each > 0) for each in joueur.possessions])))
    
    if len(modifications) > 1:
        resultat = rd.sample(range(len(modifications)), 2)
        modifications[resultat[0]] = -1
        modifications[resultat[1]] = 1
        modifications_complet = full_tab(modifications, joueur ,carte)
        resultat_id = [0, 0]
        for id in range(carte.nombres['pays']):
            if modifications_complet[id] < 0:
                resultat_id[0] = id
            if modifications_complet[id] > 0:
                resultat_id[1] = id
    
        if is_connected(resultat_id[0], resultat_id[1], joueur.possessions, carte):
            # Les deux territoires sont connectés.
            nombre_troupes = rd.randint(0, joueur.possessions[resultat_id[0]] - 1)
            modifications_complet_2 = np.array(modifications_complet*nombre_troupes)
            
            if debug:
                modifications_to_log(id_partie, numero_tour, joueur.identifiant, 2, modifications_complet_2)
            
            joueur.update(modifications_complet_2)

## Fonctions pour les autres joueurs
def supply(id_partie, numero_tour, joueurs, num_joueur, carte, debug):
    """Fonction qui réalise la phase de Supply d'un joueur."""
    ordre = (-evaluation_possession(joueurs, num_joueur, carte)).argsort()
    nombre_troupes = joueurs[num_joueur].supply_troupes(carte)
    nombre_territoires = len(ordre)
    
    if nombre_territoires > 2: # Nombre de territoires >= 3
        # -- Demi-Quart-One
        modifications = np.zeros(nombre_territoires)
        
        # On calcul les demi et quart pour la répartition.
        demi = nombre_troupes//2
        quart = nombre_troupes//4
        if quart == 0: # Correction si le quart est nul.
            quart = 1
        
        # On repartit les premières troupes.
        modifications[ordre[0]] = demi
        modifications[ordre[1]] = quart
        nombre_troupes -= demi + quart
        
        # On répartit les dernières troupes une par une.
        i = 2
        while nombre_troupes != 0:
            modifications[ordre[i]] += 1
            nombre_troupes -= 1
            i = (i+1)%nombre_territoires
        
    elif nombre_territoires == 2: # Nombre de territoires = 2
        # -- Quart-One
        modifications = np.zeros(nombre_territoires)
        
        # On calcul le quart pour la répartition.
        quart = nombre_troupes//4
        if quart == 0: # Correction si le quart est nul.
            quart = 1
        
        # On repartit les premières troupes.
        modifications[ordre[0]] = quart
        nombre_troupes -= quart
        
        # On répartit les dernières troupes une par une.
        i = 1
        while nombre_troupes != 0:
            modifications[ordre[i]] += 1
            nombre_troupes -= 1
            i = (i+1)%nombre_territoires
            
    else: # Nombre de territoires = 1
        # -- One
        # On met toutes les troupes sur le territoire.
        modifications = np.array([nombre_troupes])
    
    modifications = full_tab(modifications, joueurs[num_joueur], carte)
    if debug:
        modifications_to_log(id_partie, numero_tour, joueurs[num_joueur].identifiant, 0, modifications)
    
    joueurs[num_joueur].update(modifications)

def attack(id_partie, numero_tour, joueurs, num_joueur, carte, debug):
    """Fonction qui réalise la phase d'Attaque d'un joueur."""
    can_attaque = True
    
    while can_attaque:
        attaques_possibles = get_possible_attack(joueurs, num_joueur ,carte)
        if len(attaques_possibles) == 0:
            can_attaque = False
        else:
            index = np.argsort(-np.transpose(attaques_possibles)[2]) # Ordre des lignes de la matrice dans l'ordre croissant.
            attaques_possibles_triees = np.transpose(np.transpose(attaques_possibles)[:,index])
            meilleure_attaque = attaques_possibles_triees[0] # On récupère la meilleure attaque
            if meilleure_attaque[3] >= (1 - joueurs[num_joueur].degre_agressivite): # L'attaque est faite si l'évaluation est supérieure à la limite.

                ter_attaquant, ter_defenseur = int(meilleure_attaque[0]), int(meilleure_attaque[1])

                attaquant = joueurs[num_joueur]
                defenseur = joueurs[joueur(ter_defenseur, joueurs ,carte)]

                troupes_depart = [attaquant.possessions[ter_attaquant] - 1, defenseur.possessions[ter_defenseur]]

                troupes_fin = battle(troupes_depart[0], troupes_depart[1]) # On réalise l'attaque.

                modification_attaquant = np.zeros(len(joueurs[num_joueur].possessions))
                modification_defenseur = np.zeros(len(joueurs[num_joueur].possessions))
                
                # Calcul des pertes pour chaque joueur.
                pertes_attaquant = troupes_fin[0] - troupes_depart[0]
                pertes_defenseur = troupes_fin[1] - troupes_depart[1]

                if troupes_fin[0] == 0:
                     modification_attaquant[ter_attaquant] = pertes_attaquant
                     modification_defenseur[ter_defenseur] = pertes_defenseur
                else:
                     delta = min(3, troupes_fin[0]) # Nombre de troupes placées sur le nouveaux territoires.
                     modification_attaquant[ter_attaquant] = pertes_attaquant - delta
                     modification_attaquant[ter_defenseur] = delta
                     modification_defenseur[ter_defenseur] = pertes_defenseur

                # On met à jour les possessions des joueurs.
                attaquant.update(modification_attaquant)
                defenseur.update(modification_defenseur)
                
                if debug:
                    write_log(id_partie, numero_tour, attaquant.identifiant, 1, ter_defenseur, troupes_depart[0], ter_attaquant, troupes_depart[1], pertes_attaquant, pertes_defenseur)
            else:
                can_attaque = False
    
def reinforcement(id_partie, numero_tour, joueurs, num_joueur, carte, debug):
    """Fonction qui réalise la phase de Reinforcement d'un joueur."""
    joueur = joueurs[num_joueur]
    modifications = np.zeros(carte.nombres['pays'], dtype="int")
    
    evaluations = evaluation_possession(joueurs, num_joueur ,carte) # On récupère l'évluation des territoires.
    
    ordre = evaluations.argsort() # On récupère l'odre croissant des évaluations.
    complet_ordre = full_order(evaluations.argsort(), joueur ,carte).astype('int32')
    
    # On prend le déplacement avec la plus grande différence d'évaluation.
    indice_arrivee = 0
    indice_depart = 0
    difference = 0
    
    for i in range(len(ordre)):
        for j in range(i + 1, len(ordre)):
            diff = evaluations[ordre[j]] - evaluations[ordre[i]]
            if (diff > difference) and (is_connected(complet_ordre[i], complet_ordre[j], joueur.possessions ,carte)) and (joueur.possessions[complet_ordre[j]] > 1):
                indice_arrivee = i
                indice_depart = j
                difference = diff
    
    if indice_depart != indice_arrivee: # On effectue le déplacement si ce dernier est possible.
        modifications[complet_ordre[indice_depart]] = - int((joueur.possessions[complet_ordre[indice_depart]] - 1) * (1 - evaluations[ordre[indice_depart]]))
        modifications[complet_ordre[indice_arrivee]] = int((joueur.possessions[complet_ordre[indice_depart]] - 1) * (1 - evaluations[ordre[indice_depart]]))
        
        if debug:
            modifications_to_log(id_partie, numero_tour, joueur.identifiant, 2, modifications)
        joueur.update(modifications)

## Fonctions pour le début de la partie
def distribution(joueurs, carte):
    """Fonction qui réalise la distributon des territoires au début de partie."""
    ordre_distribution = [i for i in range(len(joueurs[0].possessions))]
    np.random.shuffle(ordre_distribution) # On génère l'ordre de distribution des territoires.
    ordre_joueurs = [[] for _ in range(len(joueurs))]
    
    # On distribut les territoires à chaque joueurs.
    for i in range(len(ordre_distribution)):
        ordre_joueurs[i%len(joueurs)].append(ordre_distribution[i])
    
    # On place les troupes sur les territoires.
    for i in range(len(joueurs)):
        modifications = np.zeros(carte.nombres['pays'], dtype='int')
        nombre_troupes = 30 - len(ordre_joueurs[i])
        for id_territoire in ordre_joueurs[i]: # On place d'abord une troupe sur chaque territoire.
            modifications[id_territoire] += 1
        
        for id_troupe in range(0, nombre_troupes): # On repartie les troupes de manière aléatoire.
            modifications[np.random.choice(ordre_joueurs[i])] += 1
        
        joueurs[i].update(modifications)
        
def create_players(liste_degres, carte):
    """Fonction qui ranvoie une liste des joueurs (avec leur degré d'agressivité) pour la partie ."""
    joueurs = []
    for id in range(len(liste_degres)):
        joueurs.append(Joueur(id, liste_degres[id], carte.nombres['pays'])) # On créé la classe de chaque joueur.
    return joueurs
    
## Fonctions pour la simulation
def game_simulation(liste_degres, nom_carte, debug=False):
    """Fonction qui réalise une partie de Risk."""
    top = time()
    # --- Initialisation de la partie ---
    # Indenftifiant de la partie donné en fonction de la date et de l'heure.
    id_partie = str(localtime(time()).tm_year)
    id_partie += str(localtime(time()).tm_mon)
    id_partie += str(localtime(time()).tm_mday)
    id_partie += str(localtime(time()).tm_hour)
    id_partie += str(localtime(time()).tm_min)
    id_partie += str(localtime(time()).tm_sec)
    
    carte = Carte(nom_carte) # Création de la carte
    joueurs = create_players(liste_degres, carte) # Création des joueurs
    np.random.shuffle(joueurs) # Détermination de l'ordre des joueurs
    distribution(joueurs, carte) # Distribution des teritoires entre les joueurs.
    # --- Début de la partie ---
    numero_joueur = 0
    numero_tour = 0
    while (len(joueurs) > 1) and (numero_tour < limite_nombre_tours[nom_carte]):
        if sum(joueurs[numero_joueur].possessions) > 0:
            numero_tour += 1
            if joueurs[numero_joueur].degre_agressivite < 0: # Si le joueur est aléatoire.
                random_supply(id_partie, numero_tour, joueurs[numero_joueur], carte, debug)
                random_attack(id_partie, numero_tour, joueurs, numero_joueur, carte, debug)
                random_reinforcement(id_partie, numero_tour, joueurs[numero_joueur], carte, debug)
            else:
                supply(id_partie, numero_tour, joueurs, numero_joueur, carte, debug)
                attack(id_partie, numero_tour, joueurs, numero_joueur, carte, debug)
                reinforcement(id_partie, numero_tour, joueurs, numero_joueur, carte, debug)
        else:
            del joueurs[numero_joueur]
        numero_joueur = (numero_joueur + 1) % len(joueurs)
        
    if debug:
        save_map_state(joueurs, id_partie)
    return joueurs[0].identifiant, numero_tour, time() - top
    
def multiple_simulation(liste_degres, nom_carte, nombre_partie, stats=False):
    """Fonction qui effectue plusieurs simulations de partie avec les mêmes paramètres."""
    # On récupère les informations liées à la date et l'heure utilisées après pour la sauvegarde de résultats.
    if (localtime(time()).tm_hour < 10):
        heures = '0' + str(localtime(time()).tm_hour)
    else :
        heures = str(localtime(time()).tm_hour)
        
    if (localtime(time()).tm_min < 10):
        mins = '0' + str(localtime(time()).tm_min)
    else :
        mins = str(localtime(time()).tm_min)
        
    annee = str(localtime(time()).tm_year)
    
    if (localtime(time()).tm_mon < 10):
        mois = '0' + str(localtime(time()).tm_mon)
    else :
        mois = str(localtime(time()).tm_mon)
        
    if (localtime(time()).tm_mday < 10):
        jour = '0' + str(localtime(time()).tm_mday)
    else :
        jour = str(localtime(time()).tm_mday)
        
    # On initialise les variables pour les résultats.
    resultats = np.zeros(len(liste_degres), dtype="int")
    nombre_egalite = 0
    tours = []
    temps = []
    
    for num_partie in range(nombre_partie): # On réalise les parties.
        if num_partie % 10 == 0: # Affichage pour l'avancement
            print("[Simulation]: Partie " + str(num_partie) + "/" + str(nombre_partie))
            
        res = game_simulation(liste_degres, nom_carte) # La partie
        
        # On ajoute les résultats.
        if res[1] == limite_nombre_tours[nom_carte]:
            nombre_egalite += 1
        else:
            resultats[res[0]] += 1
        tours.append(res[1])
        temps.append(res[2])
    
    if stats: # Affichage des résultats.
        plt.close()
        figure = plt.figure(figsize = (5, 5))
        plt.gcf().subplots_adjust(left = 0.1, bottom = 0.1, right = 0.9, top = 0.9, wspace = 0.2, hspace = 0.2)
        
        gr = figure.add_subplot(1, 2, 1)
        gr.set_title("Nombre de parties gagnées")
        gr.set_ylabel("Nombre de partie gagnées")
        gr.bar(liste_degres, resultats, width=0.1) 
    
        gr = figure.add_subplot(2, 2, 2)
        gr.set_title("Nombre de tours par partie")
        gr.set_ylabel("Nombre de tours")
        gr.plot(range(nombre_partie), tours, color = 'green')
        
        gr = figure.add_subplot(2, 2, 4)
        gr.set_title("Temps de calcul par partie")
        gr.set_ylabel("Temps en secondes")
        gr.plot(range(nombre_partie), temps, color = 'red')
        plt.show()
      
    # Sauvegarde des résultats.
    chemin = "result/"
    if not os.path.exists(chemin):
        os.makedirs(chemin)
        
    nom = chemin + annee + mois + jour + ".txt"
    with open(nom, 'a') as fichier:
        texte = "[" + heures + ":" + mins + "]\t"
        texte += nom_carte + "\t"
        texte += str(nombre_partie) + "\t"
        texte += str(liste_degres) + "\t"
        texte += str(resultats) + "\t"
        texte += str(temps) + "\n"
        fichier.write(texte)
    
    return resultats, nombre_egalite, sum(temps)
    
print("[Initialisation]: Initialisation terminée !")

def batch(type):
    if type == "normal": # 35 mins
        print("[Simulation]: Début simulation Classique")
        multiple_simulation([-1, 0.8, 0.5, 0.2], "Classique", 100) # 5 mins
        print("[Simulation]: Début simulation Frozen Classique")
        multiple_simulation([-1, 0.8, 0.5, 0.2], "Frozen Classique", 100) # 5 mins
        print("[Simulation]: Début simulation Lord of the Rings")
        multiple_simulation([-1, 0.8, 0.5, 0.2], "Lord of the Rings", 100) # 20 mins
        print("[Simulation]: Début simulation The Walking Dead")
        multiple_simulation([-1, 0.8, 0.5, 0.2], "The Walking Dead", 100) # 5 mins
    elif type == "evolution": # 45 mins
        print("[Simulation]: Début simulation de l'évolution sur Classique")
        multiple_simulation([1, 0.8, 0.5, 0.2], "Classique", 10)
        multiple_simulation([0.9, 0.8, 0.5, 0.2], "Classique", 10)
        multiple_simulation([0.8, 0.8, 0.5, 0.2], "Classique", 10)
        multiple_simulation([0.7, 0.8, 0.5, 0.2], "Classique", 10)
        multiple_simulation([0.6, 0.8, 0.5, 0.2], "Classique", 10)
        multiple_simulation([0.5, 0.8, 0.5, 0.2], "Classique", 10)
        multiple_simulation([0.4, 0.8, 0.5, 0.2], "Classique", 10)
        multiple_simulation([0.3, 0.8, 0.5, 0.2], "Classique", 10)
        multiple_simulation([0.2, 0.8, 0.5, 0.2], "Classique", 10)
        multiple_simulation([0.1, 0.8, 0.5, 0.2], "Classique", 10)
        multiple_simulation([0, 0.8, 0.5, 0.2], "Classique", 10)
        
        print("[Simulation]: Début simulation de l'évolution sur Frozen Classique")
        multiple_simulation([1, 0.8, 0.5, 0.2], "Frozen Classique", 10)
        multiple_simulation([0.9, 0.8, 0.5, 0.2], "Frozen Classique", 10)
        multiple_simulation([0.8, 0.8, 0.5, 0.2], "Frozen Classique", 10)
        multiple_simulation([0.7, 0.8, 0.5, 0.2], "Frozen Classique", 10)
        multiple_simulation([0.6, 0.8, 0.5, 0.2], "Frozen Classique", 10)
        multiple_simulation([0.5, 0.8, 0.5, 0.2], "Frozen Classique", 10)
        multiple_simulation([0.4, 0.8, 0.5, 0.2], "Frozen Classique", 10)
        multiple_simulation([0.3, 0.8, 0.5, 0.2], "Frozen Classique", 10)
        multiple_simulation([0.2, 0.8, 0.5, 0.2], "Frozen Classique", 10)
        multiple_simulation([0.1, 0.8, 0.5, 0.2], "Frozen Classique", 10)
        multiple_simulation([0, 0.8, 0.5, 0.2], "Frozen Classique", 10)
        
        print("[Simulation]: Début simulation de l'évolution sur The Walking Dead")
        multiple_simulation([1, 0.8, 0.5, 0.2], "The Walking Dead", 10)
        multiple_simulation([0.9, 0.8, 0.5, 0.2], "The Walking Dead", 10)
        multiple_simulation([0.8, 0.8, 0.5, 0.2], "The Walking Dead", 10)
        multiple_simulation([0.7, 0.8, 0.5, 0.2], "The Walking Dead", 10)
        multiple_simulation([0.6, 0.8, 0.5, 0.2], "The Walking Dead", 10)
        multiple_simulation([0.5, 0.8, 0.5, 0.2], "The Walking Dead", 10)
        multiple_simulation([0.4, 0.8, 0.5, 0.2], "The Walking Dead", 10)
        multiple_simulation([0.3, 0.8, 0.5, 0.2], "The Walking Dead", 10)
        multiple_simulation([0.2, 0.8, 0.5, 0.2], "The Walking Dead", 10)
        multiple_simulation([0.1, 0.8, 0.5, 0.2], "The Walking Dead", 10)
        multiple_simulation([0, 0.8, 0.5, 0.2], "The Walking Dead", 10)
        
        print("[Simulation]: Début simulation de l'évolution sur Lord of the Rings")
        multiple_simulation([1, 0.8, 0.5, 0.2], "Lord of the Rings", 10)
        multiple_simulation([0.9, 0.8, 0.5, 0.2], "Lord of the Rings", 10)
        multiple_simulation([0.8, 0.8, 0.5, 0.2], "Lord of the Rings", 10)
        multiple_simulation([0.7, 0.8, 0.5, 0.2], "Lord of the Rings", 10)
        multiple_simulation([0.6, 0.8, 0.5, 0.2], "Lord of the Rings", 10)
        multiple_simulation([0.5, 0.8, 0.5, 0.2], "Lord of the Rings", 10)
        multiple_simulation([0.4, 0.8, 0.5, 0.2], "Lord of the Rings", 10)
        multiple_simulation([0.3, 0.8, 0.5, 0.2], "Lord of the Rings", 10)
        multiple_simulation([0.2, 0.8, 0.5, 0.2], "Lord of the Rings", 10)
        multiple_simulation([0.1, 0.8, 0.5, 0.2], "Lord of the Rings", 10)
        multiple_simulation([0, 0.8, 0.5, 0.2], "Lord of the Rings", 10)

def double_batch(): # 1 heure 20 mins
    batch("normal")
    batch("evolution")
    
def show_attaques_made(lim = 10000):
    global attaques_realisees
    
    tableau = np.array(attaques_realisees)
    n = max(max(tableau[:,0]),max(tableau[:,1])) + 1
    
    res = np.zeros((n,n), dtype="int")
    
    for (x,y) in attaques_realisees:
        res[x, y] += 1
    
    m = min(lim, n)
    
    plt.close()
    plt.figure(figsize = (7,7))
    plt.imshow(res[1:m,1:m],extent=[1,m,1,m],origin="lower",interpolation='nearest', cmap="Paired")
    plt.colorbar()
    plt.show()
    
    return n

def show_prob_calculed(lim = 10000):
    global probabilites_calculees
    
    tableau = np.array(probabilites_calculees)
    n = max(max(tableau[:,0]),max(tableau[:,1])) + 1
    
    res = np.zeros((n,n), dtype="int")
    
    for (x,y) in probabilites_calculees:
        res[x, y] += 1
    
    m = min(lim, n)
    
    plt.close()
    plt.figure(figsize = (7,7))
    plt.imshow(res[1:m,1:m],extent=[1,m,1,m],origin="lower",interpolation='nearest', cmap="Paired")
    plt.colorbar()
    plt.show()
    
    return n