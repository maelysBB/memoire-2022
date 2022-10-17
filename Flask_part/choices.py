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
         },
        "allotments" :
        {"name": "Jardins familiaux",
         "category" : ["garden", "Autre", "potager", "association"]
         },
        "bicycle_parking" :
        {"name": "Parking à vélos",
         "category" : ["prive", "libre acces", "Missing"]
         },
        "education" : 
        {"name": "Education",
         "category" : ["kindergarten", "school", "university", "college"]
         },
        "fire_hydrant" :
        {"name": "Equipement de lutte contre incendie",
         "category" : ["utiliser_que_par_les_pompiers", "utiliser_par_tous"]
         },
        "historic" :
        {"name": "Historique",
         "category" : ["memorial", "nature", "man-made_waterbody", "place_of_worship",
         "monument", "tomb", "castle", "ruins", "Autre", "archaeological_site", "building", 
         "industrial ", "military", "vehicle", "scientific"]
         },
        "hosting" :
        {"name": "Hébergement touristique",
         "category" : ["hotel", "guest_house", "outdoor", "Autre"]
         },
        "internet_access" :
        {"name": "Point d'accès internet",
         "category" : ["wlan", "terminal", "Autre", "wired", "service_provider"] 
         },
        "parking" :
        {"name": "Parking",
         "category" : ["Missing", "ouvrage", "enclos_en_surface"] 
         },
        "sports" : 
        {"name": "Sportif",
         "category" : ["sports_centre", "pitch", "horse_riding", "swimming_pool",
         "golf_course", "fitness_station", "recreation_ground", "track",
         "stadium", "grass", "Autre"]
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
