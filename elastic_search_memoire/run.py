from subprocess import call
import sys

directory_list = "./documents_update/"

import create_template

import create_docs

sys.path.append("./documents_update/")
import update_docs_aed
import update_docs_bank
import update_docs_carpool
import update_docs_cemetery
import update_docs_cinema
import update_docs_cycleway
import update_docs_healthcare
import update_docs_charging_stations
import update_docs_library
import update_docs_playground
import update_docs_recycling
import update_docs_shop_craft_office