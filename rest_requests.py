#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# Author:       Alan Ramponi                                                   #
# Course:       Service design and engineering                                 #
# Description:  A telegram bot client to demonstrate the healthy-me service    #
#               (class that handles REST requests)			                   #
################################################################################

from time import gmtime, strftime
import requests
import json
import client


# Global variables useful for REST requests
base_url = "https://storage-data-service-ar.herokuapp.com/rest/"
headers = {'Content-type': 'application/json'}
headers2 = {'Content-type': 'application/xml'}


def post_person(firstname, lastname, birthdate):
	data = {"firstname": firstname, "lastname": lastname, "birthdate": birthdate}


	r = requests.post(base_url + "person/", headers=headers, data=json.dumps(data))

	return r.text


def post_goal(id, title, init_value, final_value, deadline):
	time = strftime("%a %b %d %H:%M:%S CET %Y", gmtime())
	print id, init_value, final_value, deadline, time
	data = {"title": title, "init_value": init_value, "final_value": final_value, "deadline": deadline, "created": time, "achieved": "NO"}

	r = requests.post(base_url + "person/" + str(id) + "/goal", headers=headers, data=json.dumps(data))

	return r.text


def post_measurement(id, measure, value):
	time = strftime("%a %b %d %H:%M:%S CET %Y", gmtime())
	print id, measure, value
	data = {"value": value}

	r = requests.post(base_url + "person/" + str(id) + "/" + measure, headers=headers, data=json.dumps(data))

	return r.text


def get_recipe():
	r = requests.get(base_url + "recipe/random", headers=headers2)

	return r.text


def get_recipe_nutrition_facts(id):
	r = requests.get(base_url + "recipe/" + id, headers=headers2)
	
	return r.text


def get_quote():
	r = requests.get(base_url + "recipe/quote/random", headers=headers2)

	return r.text


def get_person(id):
	r = requests.get(base_url + "person/" + str(id))

	return r.text