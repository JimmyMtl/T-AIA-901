"""Version pour retourner moins de resultat"""

import random
from tqdm import tqdm

def load_phrases():
    phrases = []
    with open("Exemples_phrases.txt", 'r', encoding='UTF-8') as f:
        content = f.readlines()
        for lines in content:
            phrases.append(lines.strip().split("\n")[0])
    return phrases

def generation():
    liste_villes_française = ['Nancy', 'Paris', 'Lyon', 'Marseille', 'Toulouse', 'Bordeaux', 'Lille', 'Rennes', 'Nice',
    'Strasbourg', 'Montpellier', 'Nantes', 'Le Havre', 'Toulon', 'Grenoble', 'Dijon', 'Angers', 'Saint-Étienne', 'Brest',
    'Le Mans', 'Reims', 'Nîmes', 'Clermont-Ferrand', 'Amiens', 'Tours', 'Limoges', 'Caen', 'Perpignan', 'Metz', 'Orléans',
    'Besançon', 'Mulhouse', 'Rouen', 'Boulogne-Billancourt', 'Troyes', 'Montreuil', 'Saint-Denis', 'Nanterre', 'Argenteuil',
    'Roubaix', 'Aulnay-sous-Bois', 'Tourcoing', 'Avignon', 'Vitry-sur-Seine', 'Créteil', 'Dunkerque', 'Poitiers', 'Versailles']
    
    phrases = load_phrases()
    
    for i in tqdm(phrases):
        new_phrase = i

        for x in liste_villes_française:
            nb_villes = 2 #si 10, retourne environ 4k resultats
            for y in random.sample(liste_villes_française, nb_villes):
                if x != y:
                    txt = new_phrase.replace("ARR", x).replace("DEP", y)
                    with open("inputs.txt", 'a', encoding='UTF-8') as f:
                        f.write('("' + txt + '", {"entities": [(' + str(txt.index(x)) + ',' + str(txt.index(x) + len(x)) + ",'ARR'), (" + str(txt.index(y)) + ',' + str(txt.index(y) + len(y)) + ", 'DEP')]})")
                        f.write("\n")

if __name__ == "__main__":
    generation()