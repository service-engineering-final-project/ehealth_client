#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# Author:       Alan Ramponi                                                   #
# Course:       Service design and engineering                                 #
# Description:  A telegram bot client to demonstrate the healthy-me service    #
#               (main class that handles transition states)                    #
################################################################################

import requests
import json


# Global variables useful for REST requests
base_url = "https://storage-data-service-ar.herokuapp.com/rest/"
#base_url = "https://process-centric-service-ar.herokuapp.com/rest/"
headers = {'Content-type': 'application/json'}
headers2 = {'Content-type': 'application/xml'}


def get_person(id):
	r = requests.get(base_url + "person/" + str(id))

	return r.text

def post_person(firstname, lastname, birthdate):
	data = {"firstname": firstname, "lastname": lastname, "birthdate": birthdate}

	r = requests.post(base_url + "person/", headers=headers, data=json.dumps(data))

	return r.text

def get_recipe():
	r = requests.get(base_url + "recipe/random", headers=headers2)

	return r.text

def get_recipe_nutrition_facts(id):
	r = requests.get(base_url + "recipe/" + id, headers=headers2)
	
	return r.text