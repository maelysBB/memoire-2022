category = {                                # list all possible category
    "healthcare" : 
        {"name": "Etablissement de santé",
         "category" : ["Clinique", "Pharmacie", "Hopitaux"]
         },
        "charging_station" :
            {"name": "Bornes de chargement", 
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
