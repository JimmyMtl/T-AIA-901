import random
import time
from tqdm import tqdm

def reformulation():
    depart = ["Metz", "Nancy", "Paris", "Lyon", "Marseille", "Bordeaux", "Lille", "Toulouse", "Nice", "Strasbourg"]
    arrivee = ["Metz", "Nancy", "Paris", "Lyon", "Marseille", "Bordeaux", "Lille", "Toulouse", "Nice", "Strasbourg"]

    for i in tqdm(range(50)):
        rand1 = random.choice(depart)
        rand2 = random.choice(arrivee)

        if rand1 == rand2:
            continue
        
        sentence = "('Je pars de " + rand1 + " pour aller à " + rand2 + "', {'entities': [(11, "+ str(11+len(rand1))+", 'DEP'), ("+str(25+len(rand1))+", "+str(25+len(rand1)+len(rand2))+", 'ARR')]}),"
        sentence1 = "('Je vais à " + rand1 + " depuis " + rand2 + "', {'entities': [(10, "+ str(10+len(rand1))+", 'ARR'), ("+str(18+len(rand1))+", "+str(18+len(rand1)+len(rand2))+", 'DÉPART')]}),"
        sentence2 = "('On voudrait aller à " + rand1 + " en partant de " + rand2 + "', {'entities': [(20, "+ str(20+len(rand1))+", 'ARR'), ("+str(35+len(rand1))+", "+str(35+len(rand1)+len(rand2))+", 'DÉPART')]}),"

        with open("inputs.txt", 'a', encoding='UTF-8') as f:
            f.write(sentence)
            f.write("\n")
            f.write(sentence1)
            f.write("\n")
            f.write(sentence2)
            f.write("\n")
            f.close()
        time.sleep(0.5)

reformulation()
