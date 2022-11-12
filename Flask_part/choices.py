category = {
        "healthcare" : 
        {"name": "Etablissement de santé",                                    # list all possible categories
         "category" : ["Clinique", "Pharmacie", "Hopitaux"],
         "title":"oui"
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
            "title":"oui"
            },
        "cinema" : 
        {"name": "Cinéma",
         "category" : ["MK2", "Pathé Gaumont", "UGC"],
         "title":"oui"
         },
        "cycleway" :
            {"name": "Piste cyclable",}, 
        "library" : 
        {"name": "Bibliothèque",
         "category" : ["Bibliothèque", "Médiathèque", "Dépôt à livres"],
         "title":"oui"
         },
        "playground" :
        {"name": "Terrain de jeu",
        "title":"oui"}, 
        "recycling" :
        {"name": "Recyclage",}, 
        "shop_craft_office" : 
        {"name": "Commerce",
         "category" : ["Achat et entretien voitures", "Agence immobilière", "Boucher", "Boulangerie/Pâtisserie", 
         "Café", "Coiffeur", "Opticien", "Supermarché/Epicerie", "Vêtements/Chaussures"],
         "title":"oui"
         },
        "allotments" :
        {"name": "Jardins familiaux",
         "category" : ["Jardin", "Potager", "Géré par une association", "Autre"], 
         "title":"oui"
         },
        "bicycle_parking" :
        {"name": "Parking à vélos",
         "category" : ["Privé", "Libre accès"]
         },
        "education" : 
        {"name": "Education",
         "category" : ["Crèche", "Ecole primaire ou secondaire", "Enseignement supérieur hors université", "Université"],
         "title":"oui"
         },
        "fire_hydrant" :
        {"name": "Equipement de lutte contre incendie",
         "category" : ["Utiliser par tous", "Utiliser que par les pompiers"]
         },
        "historic" :
        {"name": "Historique",
         "category" : ["Bâtiment", "Château", "Fontaine ou aménagement de cours d'eau", "Industriel", "Lieu de culte", "Monument",
         "Mémorial", "Naturel", "Patrimoine militaire", "Patrimoine scientifique", "Ruines", "Site archéologique", "Tombe", "Transport", "Autre"],
         "title":"oui"
         },
        "hosting" :
        {"name": "Hébergement touristique",
         "category" : ["Hôtel", "Maison d'hôte", "Espaces extérieur", "Autre"]
         },
        "internet_access" :
        {"name": "Point d'accès internet",
         "category" : ["Wifi", "Connection par câble", "Fournisseur de service", "Autre"] 
         },
        "parking" :
        {"name": "Parking",
         "category" : ["Ouvrage", "Enclos en surface"] 
         },
        "sports" : 
        {"name": "Sportif",
         "category" : ["Aire de jeux", "Centre d'équitation", "Complexe sportif",
         "Equipement de fitness ou de gymnastique", "Piscine", "Piste d'athlétisme", "Stade",
         "Terrain de golf", "Terrain de sport", "Autre"],
         "title":"oui"
         },
        "drinking_water":
        {"name": "Eau Potable",
         "category" : ["Gratuit", "Payant"]
         },
        "toilets":
        {"name": "Toilettes",
         "category" : ["Gratuit", "Payant"]
         },
        "taxi":
        {"name": "Taxi",
         },
        "fuel":
        {"name": "Station électrique",
         },
        "power_supports":
        {"name": "Support du courant",
         "category" : [ "Pylône électrique", "Poteau électrique"]
         },
        "restaurant":
        {"name": "Restaurants",
         "category" : ["Bar ou Pub", "Café", "Glacier", "Foire alimentaire", "Restaurant", "Restaurant Fast Food", 
         "Restaurant Français", "Restaurant Régional", "Restaurant Italien", "Restaurant Japonais", "Restaurant Indien"],
         "title":"oui"
         },
        "public_service":
        {"name": "Services Publiques",
         "category" : ["Mairie ou Hôtel de ville", "Organisme gouvernemental", "Service de conseil", "Diplomatique", "Autre"],
         "title":"oui"
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
