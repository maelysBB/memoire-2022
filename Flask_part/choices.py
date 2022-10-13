category = {
        "healthcare" : 
        {"name": "Etablissement de santé",                                    # list all possible categories
         "category" : ["Clinique", "Pharmacie", "Hopitaux"]
         },
        "charging_station" :
            {"name": "Bornes de chargement", 
            },
        "aed" : 
        {"name": "Défibrillateur",
         "category" : ["Intérieur", "Extérieur"]
         },
        "bank" :
            {"name": "Banque",
            "category" : ["Banque Postale", "BNP Paribas", "BRED/Banque populaire", "Caisse d'Epargne", "CIC", "Crédit Agricole", "Crédit Mutuel", "HSBC", "LCL", "Société Générale"] 
            },
        "carpool" : 
        {"name": "Espace de covoiturage",
         "category" : ["Aire de covoiturage", "Parking"]
         },
        "cemetery" :
            {"name": "Cimetière", 
            },
        "cinema" : 
        {"name": "Cinéma",
         "category" : ["MK2", "Pathé Gaumont", "UGC"]
         },
        "cycleway" :
            {"name": "Piste cyclable",}, 
        "library" : 
        {"name": "Bibliothèque",
         "category" : ["Bibliothèque", "Médiathèque", "Dépôt à livres"]
         },
        "playground" :
        {"name": "Terrain de jeu",}, 
        "recycling" :
        {"name": "Recyclage",}, 
        "shop_craft_office" : 
        {"name": "Commerce",
         "category" : ["Achat et entretien voitures", "Agence immobilière", "Boucher", "Boulangerie/Pâtisserie", 
         "Café", "Coiffeur", "Opticien", "Supermarché/Epicerie", "Vêtements/Chaussures"]
         }         
            }

total_number = {} #list the number of subcategory for each type (charging_station, healthcare etc.)
name_cat = []
for key, value in category.items() :
    name_cat.append("name_"+key)
    if "category" in value :
        total_number[key] = len(value["category"])
    else :
        total_number[key] = 1

print(total_number)
print(name_cat)
