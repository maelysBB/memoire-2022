from subprocess import call
import sys

distance=5000

directory_list = "./documents_update/"

import create_template

import create_docs

sys.path.append("./documents_update/")
import update_docs_aed
import update_docs_bank
import update_docs_carpool
import update_docs_cinema
import update_docs_healthcare
import update_docs_charging_stations
import update_docs_library
import update_docs_playground
import update_docs_shop_craft_office
import update_docs_allotments
import update_docs_bicycle_parking
import update_docs_education
import update_docs_fire_hydrant
import update_docs_historic
import update_docs_hosting
import update_docs_parking
import update_docs_sports
import update_docs_drinking_water
import update_docs_fuel
import update_docs_public_service
import update_docs_restaurants
import update_docs_taxi
import update_docs_toilets