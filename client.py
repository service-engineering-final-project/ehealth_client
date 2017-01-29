#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# Author:       Alan Ramponi                                                   #
# Course:       Service design and engineering                                 #
# Description:  A telegram bot client to demonstrate the healthy-me service    #
#               (main class that handles transition states)                    #
################################################################################

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)
from StringIO import StringIO
import logging
import rest_requests
import requests
import json
import untangle
from PIL import Image
import multipart

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables used for transition states
STATE1, STATE2, STATE3, STATE4, STATE5, STATE6, STATE7, STATE8, STATE9, STATE10, STATE11, STATE12, STATE13, STATE14, STATE15 = range(15)


class Patient:
    id = 0
    name = "alan"
    goal = "weight"

    def __init__(self, id, name, goal):
        Patient.id = id
        Patient.name = name
        Patient.goal = goal

    def getId(self):
        return self.id


def start(bot, update):
    update.message.reply_text("Hi doctor! Welcome to the <b>HealthyMe</b> application :-)\n\n"
        "As you know, this service aims to support hypertensive patients helping "
        "them to achieve healthy goals. Please, insert the patient's data in order to "
        "allow him to start using this application.\n\n"
        "[<b>firstname lastname birthdate</b>]\n"
        "Note: <i>birthdate must be in the format MM-DD-YYYY</i>.", 
        parse_mode="HTML")

    return STATE1


def add_person(bot, update):
    reply_keyboard = [["Yes", "No"]]

    # Store the input data into some variables
    firstname, lastname, birthdate = str(update.message.text).split(" ", 2)

    # Call the service to add the person to the database and get the response
    response = rest_requests.post_person(firstname, lastname, birthdate)
    json_response = json.loads(response)
    logger.info("\nadd_person() response:\n%s\n" % (str(response)))

    # Store the person's data
    p = Patient(json_response["id"], json_response["firstname"], "")

    update.message.reply_text("The person was successfully inserted into the database:\n\n"
        "Firstname: <b>%s</b>\nLastname: <b>%s</b>\nBirthdate: <b>%s</b>\n\n"
        % (json_response["firstname"], json_response["lastname"], json_response["birthdate"]), 
        parse_mode="HTML")
    update.message.reply_text("It is correct?", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return STATE2


def manage_person(bot, update):
    reply_keyboard = [["Update", "Delete"]]

    update.message.reply_text("Don't worry. Which action do you want to perform?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return STATE3


def modify_person(bot, update):
    update.message.reply_text("Insert the new data for the patient.\n\n",
        "[<b>firstname lastname birthdate</b>]\n"
        "Note: <i>birthdate must be in the format MM-DD-YYYY</i>.")
    
    return STATE4


def modify_person_2(bot, update):
    reply_keyboard = [["Yes", "No"]]

    update.message.reply_text("Are you sure you want to delete the patient from the database?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return STATE5


def update_person(bot, update):
    update.message.reply_text("The person was successfully updated!")

    return STATE6


def delete_person(bot, update):
    update.message.reply_text("The person was successfully deleted!\n\nType /start to add a new person :-)")

    return STATE1


def choose_goal(bot, update):
    reply_keyboard = [['weight', 'steps', 'sleep_hours'], ['proteins', 'carbohydrates', 'lipids'], ['calories', 'sodium']]

    update.message.reply_text("Which goal do you want to add for him?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return STATE6


def add_goal(bot, update):
    # Store the patient's goal
    p = Patient(Patient.id, Patient.name, update.message.text)

    update.message.reply_text("Please, insert the following data for the patient's goal.\n\n"
        "[<b>init_value final_value deadline</b>]\n"
        "Note: <i>deadline must be in a format e.g., Wed Feb 15 10:00:00 CET 2017</i>.",
        parse_mode="HTML")

    return STATE7


def check_goal(bot, update):
    reply_keyboard = [["Yes", "No"]]

    # Store the input data into some variables
    init_value, final_value, deadline = str(update.message.text).split(" ", 2)

    # Call the service to add the person to the database and get the response
    response = rest_requests.post_goal(Patient.id, Patient.goal, init_value, final_value, deadline)
    json_response = json.loads(response)
    logger.info("\nadd_goal() response:\n%s\n" % (str(response)))

    update.message.reply_text("The goal was successfully inserted into the database:\n\n"
        "Init value: <b>%s</b>\nFinal value: <b>%s</b>\nDeadline: <b>%s</b>\n\n"
        % (json_response["init_value"], json_response["final_value"], json_response["deadline"]), 
        parse_mode="HTML")
    update.message.reply_text("It is correct?", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return STATE8


def another_goal(bot, update):
    reply_keyboard = [["Yes", "No"]]

    update.message.reply_text("Do you want to add another goal?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return STATE9


def manage_goal(bot, update):
    reply_keyboard = [["Update", "Delete"]]

    update.message.reply_text("Don't worry. Which action do you want to perform?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return MODIFY_GOAL


def modify_goal(bot, update):
    update.message.reply_text("Insert the new data for the goal.\n\n",
        "[<b>init_value final_value deadline</b>]\n"
        "Note: <i>deadline must be in the format MM-DD-YYYY</i>.")
    
    return ConversationHandler.END


def modify_goal_2(bot, update):
    reply_keyboard = [["Yes", "No"]]

    update.message.reply_text("Are you sure you want to delete the goal from the database?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return ConversationHandler.END


def doctor_end(bot, update):
    update.message.reply_text("The service is setted for your patient!\n\n",
        "Now tell the patient to type /patient in order to start to use the healthyme service :-)")

    return STATE1


def patient(bot, update):
    update.message.reply_text("Hi patient! Welcome to the <b>HealthyMe</b> application :-)\n\n"
        "As you know, this service aims to help you to achieve healthy goals.\n\n",
        "What do you want to do?")

    return STATE13





def add_measurement(bot, update):
    update.message.reply_text("Please, insert the following data for your health measurements.\n\n"
        "[<b>name value</b>]\n"
        #"[<b>name value</b>]\n",
        #"...\n",
        #parse_mode="HTML")
        )

    return STATE10


def check_measurement(bot, update):
    reply_keyboard = [["Yes", "No"]]

    # Store the input data into some variables
    measure, value = str(update.message.text).split(" ", 1)

    # Call the service to add the measurement to the database and get the response
    response = rest_requests.post_measurement(Patient.id, measure, value)
    json_response = json.loads(response)
    logger.info("\nadd_measurement() response:\n%s\n" % (str(response)))

    update.message.reply_text("The measurement was successfully inserted into the database:\n\n"
        "Measure: <b>%s</b>\nValue: <b>%s</b>\n\n"
        % (json_response["measure"], json_response["value"]), 
        parse_mode="HTML")
    update.message.reply_text("It is correct?", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return STATE11


def get_recipe(bot, update):

    # Call the service to add the person to the database and get the response
    response = rest_requests.get_recipe()
    obj = untangle.parse(str(response))
    #logger.info("\nadd_person() response:\n%s\n" % (str(response)))

    update.message.reply_text("Well done! This is an healthy recipe suggested for you!\n\n"
        "%s" % (obj.recipe.name.cdata), 
        parse_mode="HTML")

    response2 = rest_requests.get_recipe_nutrition_facts(obj.recipe.id.cdata)
    obj2 = untangle.parse(str(response2))

    #response3 = rest_requests.get_quote()
    #obj3 = untangle.parse(str(response3))

    update.message.reply_text("Nutrition facts:\n\n"
        "Proteins: %s\nCarbohydrates: %s\nLipids: %s\n\nCheck the following URL to know how to prepare it! :-)\n%s\n\nAnd remember: %s" 
        "Proteins: %s\nCarbohydrates: %s\nLipids: %s\n\nCheck the following URL to know how to prepare it! :-)\n%s"
        #% (obj2.recipeNutritionFacts.proteins.cdata, obj2.recipeNutritionFacts.carbohydrates.cdata, obj2.recipeNutritionFacts.lipids.cdata, obj2.recipeNutritionFacts.websiteUrl.cdata, obj2.quote.text.cdata), 
        % (obj2.recipeNutritionFacts.proteins.cdata, obj2.recipeNutritionFacts.carbohydrates.cdata, obj2.recipeNutritionFacts.lipids.cdata, obj2.recipeNutritionFacts.websiteUrl.cdata),
        parse_mode="HTML")

    #sendImageFromUrl(obj.recipe.image.cdata)

    return ConversationHandler.END



def sendImageFromUrl(url):
    #this tweak added if request image failed
    headers = {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'}
    response = requests.get(url, headers=headers)
    #response = requests.get(url)
    output = StringIO(response.content)
    img = Image.open(output)
    img.show()
    img.save(output, 'JPEG')
    resp = multipart.post_multipart(BASE_URL + 'sendPhoto', [
        ('chat_id', str(21779648)),
        ('caption', 'Your Caption'),
    ], [
        ('photo', 'image.jpg', output.getvalue()),
    ])


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("325942660:AAG7XiAvigXnWFmbKXNoylmdNB82taRwN9k")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('patient', patient))

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            STATE1: [MessageHandler(Filters.text, add_person)],
            STATE2: [RegexHandler('^(Yes)$', choose_goal), RegexHandler('(No)$', manage_person)],
            STATE3: [RegexHandler('^(Update)$', modify_person), RegexHandler('(Delete)$', modify_person_2)],
            STATE4: [MessageHandler(Filters.text, update_person)],
            STATE5: [MessageHandler(Filters.text, delete_person)],
            STATE6: [MessageHandler(Filters.text, add_goal)],
            STATE7: [MessageHandler(Filters.text, check_goal)],
            STATE8: [RegexHandler('^(Yes)$', another_goal), RegexHandler('(No)$', manage_goal)],
            STATE9: [RegexHandler('^(Yes)$', add_goal), RegexHandler('(No)$', add_measurement)],    #doctor_end - welcome_patient
            STATE10: [MessageHandler(Filters.text, get_recipe)],
            STATE11: [RegexHandler('^(Yes)$', another_goal), RegexHandler('(No)$', manage_goal)],
            STATE12: [RegexHandler('^(Update)$', modify_goal), RegexHandler('(Delete)$', modify_goal_2)],
            STATE13: [MessageHandler('^(Yes)$', choose_goal), RegexHandler('(No)$', get_recipe),

            ]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()