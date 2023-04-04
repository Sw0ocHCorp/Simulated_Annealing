#Preparation des données d'entrée
ingredients= dict()
liked_ingredients= []
disliked_ingredients= []
with open("input_data/b_basic.in.txt", "r") as f:
#with open("input_data/a_an_example.in.txt", "r") as f:
#with open("input_data\custom_example.in.txt", "r") as f:
#with open("input_data/c_coarse.in.txt", "r") as f:
#with open("input_data/d_difficult.in.txt", "r") as f:
#with open("input_data/e_elaborate.in.txt", "r") as f:
    client_number= int(f.readline())
    for i in range(client_number):
        ingred= []
        like_line= next(f).split()
        dislike_line= next(f).split()
        for token in like_line:
            if not token.isnumeric():
                ingred.append(token)
                if token in ingredients:
                    ingredients[token]+= 1
                else:
                    ingredients[token]= 1
        liked_ingredients.append(ingred)
        ingred= []
        for token in dislike_line:
            if not token.isnumeric():
                ingred.append(token)
                if token in ingredients:
                    ingredients[token]-= 1
                else:
                    ingredients[token]= -1
        disliked_ingredients.append(ingred)
    
#Recherche de la meilleure composition de pizza
pizzas_ingredients= []
satisfied_clients= 0
sorted_ingredients= sorted(ingredients.items(), key= lambda x: x[1], reverse= True)
for ingredient in sorted_ingredients:
    cpt_clients= 0
    list_ingred= pizzas_ingredients.copy()
    list_ingred.append(ingredient[0])
    set_ingred= set(list_ingred)
    
    #Test de popularité de la pizza
    for i in range(len(liked_ingredients)):
        #Pénalisation s'il y a un ingrédient détesté par le client
        if (any(item in disliked_ingredients[i] for item in list_ingred)) and (not len(disliked_ingredients[i]) == 0):
            cpt_clients-= 1
        #Bonus s'il y a un ingrédient aimé par le client
        elif (set(liked_ingredients[i]).issubset(set_ingred)) and (len(liked_ingredients[i]) > 0):
            cpt_clients+= 1
    #Si la pizza est plus populaire, on garde l'ingrédient dans la pizza "Finale"
    if cpt_clients >= satisfied_clients:
        pizzas_ingredients.append(ingredient[0])
        satisfied_clients= cpt_clients
        
print(pizzas_ingredients, len(pizzas_ingredients))
print(satisfied_clients)
str_ingred= ""
for ele in pizzas_ingredients:
    str_ingred= str_ingred + ele + " "
file= open("custom_example.out.txt", "w")
file.write(str(len(pizzas_ingredients)) + " " + str_ingred)