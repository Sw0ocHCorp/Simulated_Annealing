import numpy as np
import random
from math import *

def logarithmic_cooling(initial_temperature, final_temperature, num_iterations):
    cooling_rate = -log(final_temperature / initial_temperature) / num_iterations
    temperatures = [initial_temperature * exp(cooling_rate * i) for i in range(num_iterations)]
    return temperatures

def calculate_interest_pizza(state, env):
    set_ingred= set(state)
    score= 0
    #Test de popularité de la pizza
    for i in range(len(env["liked_ingredients"])):
        #Pénalisation s'il y a un ingrédient détesté par le client
        if (any(item in env["disliked_ingredients"][i] for item in state)) and (not len(env["disliked_ingredients"][i]) == 0):
            score-= 1
        #Bonus s'il y a un ingrédient aimé par le client
        elif (set(env["liked_ingredients"][i]).issubset(set_ingred)) and (len(env["liked_ingredients"][i]) > 0):
            score+= 1
    return score

def evaluate_value_knapsack(state, env):
    value= 0
    weight= env["max_weight"]
    for ele in state:
        value+= ele[0]
        weight-= ele[1]
        if weight < 0:
            return 0
    return value

def evaluate_ratio_knapsack(state, env):
    value= 0
    weight= 0
    for ele in state:
        value+= ele[0]
        weight+= ele[1]
    if weight > env["max_weight"]:
        return 0
    return value/weight

def run_algorithm(initial_state, temperature_scheme, env, evaluation_function, exploration_rate= 0.99):
    n= initial_state
    for t in temperature_scheme:
        #Récupérer de manière random un autre état | A DECOMMENTER POUR LA VERSION PIZZA ET COMMENTER LA VERSION KNAPSACK
        other_state= np.random.choice(list(env["items"].keys()), random.randint(1, len(env["items"])), replace= False).tolist()
        
        #Récupérer de manière random un autre état | A DECOMMENTER POUR LA VERSION KNAPSACK ET COMMENTER LA VERSION PIZZA
        #other_state= random.sample(list(env["items"].keys()), random.randint(1, len(env["items"])))
        #other_state= [(env["items"][key_selected][0], env["items"][key_selected][1], key_selected) for key_selected in other_state]
        
        diff_energy= evaluation_function(other_state, env) - evaluation_function(n, env)
        if diff_energy > 0:
            n = other_state
        else:
            test= exp(diff_energy/t)
            if test > exploration_rate:
                n = other_state
    return n

def run_opti_algorithm(initial_state, temperature_scheme, env, evaluation_function, exploration_rate= 0.99, k=10):
    n= initial_state
    memory= []
    for t in temperature_scheme:
        #Récupérer de manière random un autre état
        other_state= np.random.choice(list(env["items"].keys()), random.randint(1, len(env["items"])), replace= False).tolist()
        #other_state= random.sample(list(env["items"].keys()), random.randint(1, len(env["items"])))
        #other_state= [(env["items"][key_selected][0], env["items"][key_selected][1], key_selected) for key_selected in other_state]
        while other_state in memory:
            other_state= np.random.choice(list(env["items"].keys()), random.randint(1, len(env["items"])), replace= False).tolist()
            #other_state= random.sample(list(env["items"].keys()), random.randint(1, len(env["items"])))
            #other_state= [(env["items"][key_selected][0], env["items"][key_selected][1], key_selected) for key_selected in other_state]
        #Introduction de la mémoire pour la Recherche Tabou | Limite le retour sur les états déjà visités
        if len(memory) < k:
            memory.append(other_state)
        else:
            memory.pop(0)
            memory.append(other_state)
        diff_energy= evaluation_function(other_state, env) - evaluation_function(n, env)
        if diff_energy > 0:
            n = other_state
        else:
            test= exp(diff_energy/t)
            if test > exploration_rate:
                n = other_state
    return n

if __name__ == "__main__":
    """
    #-> ONE PIZZA
    env= {"items": {}, "liked_ingredients":[], "disliked_ingredients":[]}
    #Preparation des données d'entrée
    #with open("C:/Users/nclsr/OneDrive/Bureau/Cours_L3IA/Recherche_Heuristique/Projet_One_Pizza/input_data/a_an_example.in.txt", "r") as f:
    #with open("C:/Users/nclsr/OneDrive/Bureau/Cours_L3IA/Recherche_Heuristique/Projet_One_Pizza/input_data/c_coarse.in.txt", "r") as f:
    #with open("C:/Users/nclsr/OneDrive/Bureau/Cours_L3IA/Recherche_Heuristique/Projet_One_Pizza/input_data/d_difficult.in.txt", "r") as f:
    #with open("input_data/e_elaborate.in.txt", "r") as f:
    with open("C:/Users/nclsr/OneDrive/Bureau/Cours_L3IA/Recherche_Heuristique/Projet_One_Pizza/input_data/b_basic.in.txt", "r") as f:
        client_number= int(f.readline())
        for i in range(client_number):
            ingred= []
            like_line= next(f).split()
            dislike_line= next(f).split()
            for token in like_line:
                if not token.isnumeric():
                    ingred.append(token)
                    if token in env["items"]:
                        env["items"][token]+= 1
                    else:
                        env["items"][token]= 1
            env["liked_ingredients"].append(ingred)
            ingred= []
            for token in dislike_line:
                if not token.isnumeric():
                    ingred.append(token)
                    if token in env["items"]:
                        env["items"][token]-= 1
                    else:
                        env["items"][token]= -1
            env["disliked_ingredients"].append(ingred)
    
    #--> Version sans optimisation | Commenter ligne 50-51 du programme et Decommenter ligne 52-53
    #----------------------------------
    print(run_algorithm(["cheese", "basil"], [2000/float(i + 1) for i in range(3000)], env, calculate_interest_pizza))
    #--> Version avec optimisation | Commenter ligne 68-69-72-73 du programme et Decommenter ligne 67-71
    #----------------------------------
    print(run_opti_algorithm(["cheese", "basil"], [2000/float(i + 1) for i in range(3000)], env, calculate_interest_pizza))
    """


    #-> KNAPSACK PROBLEM
    """
    save_list= [(38, 2, 'Machette'), (28, 4, 'Peignoir'), (53, 19, 'Bouteille thermos'), (54, 5, 'Jeu de belote'), (63, 19, 'Chaussures de marche'), 
                (72, 17, 'Boules Qui�s'), (28, 15, 'B�tons de marche'), (38, 7, 'Serviettes de toilette'), (29, 20, 'Cartes IGN'), (80, 5, 'Gourde'), 
                (89, 10, 'Oreiller'), (10, 12, 'Produits d�hygi�ne'), (97, 17, 'Couvers en plastique'), (74, 10, 'R�chaud � gaz'), (42, 13, 'imperm�able'), 
                (11, 5, 'Trousse secours'), (40, 9, 'Sacs poubelle'), (50, 1, 'Pompe � air'), (67, 13, 'Glaci�re'), (84, 14, 'Bottes de pluie'), (97, 11, 'V�tements l�gers'), 
                (28, 6, 'Allumettes'), (5, 4, 'Appareil photo'), (3, 5, 'Sacs poubelle'), (85, 11, 'Tire-bouchon'), (44, 13, 'Papier toilette')]
    env= {"items": {}, "max_weight": 250}
    for item in save_list:
        env["items"][item[2]]= (item[0], item[1])
    initial_state= random.sample(save_list, 4)
    #--> Version sans optimisation | Decommenter ligne 50-51 du programme et Commenter ligne 47
    #----------------------------------
    #knapsack_items= run_algorithm(initial_state, logarithmic_cooling(1000, 10, 3000), env, evaluate_value_knapsack)
    #--> Version avec optimisation | Decomenter ligne 68-69-72-73 du programme et Commenter ligne 67-71
    #----------------------------------
    knapsack_items= run_opti_algorithm(initial_state, logarithmic_cooling(1000, 10, 3000), env, evaluate_value_knapsack, k= 75)
    total_income= 0
    weight= 0
    for item in knapsack_items:
        total_income+= item[0]
        weight+= item[1]
    print(knapsack_items, total_income, weight, total_income/weight)"""