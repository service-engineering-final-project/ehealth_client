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
ADD_PERSON, CHECK_PERSON, MODIFY_PERSON, UPDATE_PERSON, DELETE_PERSON, CHOOSE_GOAL, ADD_GOAL, CHECK_GOAL, MODIFY_GOAL, SUCC_GOAL, GENDER, PHOTO, LOCATION, BIO = range(14)

# Useful global variables to keep track of the user
PATIENT_NAME = "no_name_yet"


def start(bot, update):
    update.message.reply_text("Hi doctor! Welcome to the <b>HealthyMe</b> application :-)\n\n"
        "As you know, this service aims to support hypertensive patients helping "
        "them to achieve healthy goals. Please, insert the patient's data in order to "
        "allow him to start using this application.\n\n"
        "[<b>firstname lastname birthdate</b>]\n"
        "Note: <i>birthdate must be in the format MM-DD-YYYY</i>.", 
        parse_mode="HTML")

    return ADD_PERSON


def add_person(bot, update):
    reply_keyboard = [["Yes", "No"]]

    # Store the input data into some variables
    firstname, lastname, birthdate = str(update.message.text).split(" ", 2)

    # Call the service to add the person to the database and get the response
    #response = calls.post_person(firstname, lastname, birthdate)
    #json_response = json.loads(response)
    #logger.info("\nadd_person() response:\n%s\n" % (str(response)))

    # Store the person's name
    #PATIENT_NAME = json_response["firstname"]
    PATIENT_NAME = firstname

    update.message.reply_text("The person was successfully inserted into the database:\n\n"
        "Firstname: <b>%s</b>\nLastname: <b>%s</b>\nBirthdate: <b>%s</b>\n\n"
        #% (json_response["firstname"], json_response["lastname"], json_response["birthdate"]), 
        % (firstname, lastname, birthdate), 
        parse_mode="HTML")
    update.message.reply_text("It is correct?", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return CHECK_PERSON


def manage_person(bot, update):
    reply_keyboard = [["Update", "Delete"]]

    update.message.reply_text("Don't worry. Which action do you want to perform?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return MODIFY_PERSON


def modify_person(bot, update):
    update.message.reply_text("Insert the new data for the patient.\n\n",
        "[<b>firstname lastname birthdate</b>]\n"
        "Note: <i>birthdate must be in the format MM-DD-YYYY</i>.")
    
    return UPDATE_PERSON


def modify_person_2(bot, update):
    reply_keyboard = [["Yes", "No"]]

    update.message.reply_text("Are you sure you want to delete the patient from the database?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return DELETE_PERSON


def update_person(bot, update):
    update.message.reply_text("The person was successfully updated!")

    return CHOOSE_GOAL


def delete_person(bot, update):
    update.message.reply_text("The person was successfully deleted!\n\nType /start to add a new person :-)")

    return ConversationHandler.END


def choose_goal(bot, update):
    reply_keyboard = [['Weight', 'Steps', 'Bloodpressure'], ['Sleep hours', 'Calories', 'Sodium']]

    update.message.reply_text("Which goal do you want to add for him?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return ADD_GOAL


def add_goal(bot, update):
    reply_keyboard = [["Yes", "No"]]

    print update.message.text

    update.message.reply_text("Please, insert the patient's goal.\n\n"
        "[<b>init_value final_value deadline</b>]\n"
        "Note: <i>deadline must be in the format MM-DD-YYYY</i>.",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), 
        parse_mode="HTML")

    return CHECK_GOAL


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


def another_goal(bot, update):
    reply_keyboard = [["Yes", "No"]]

    update.message.reply_text("Do you want to add another goal?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return SUCC_GOAL


def add_measurement(bot, update):
    reply_keyboard = [['Weight', 'Steps', 'Bloodpressure', 'Sleep hours', 'Proteins', 'Carbohydrates', 'Lipids', 'Sodium']]

    update.message.reply_text('Sei un paziente', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return GENDER




def get_recipe(bot, update):

    # Call the service to add the person to the database and get the response
    response = rest_requests.get_recipe()
    obj = untangle.parse(str(response))
    #logger.info("\nadd_person() response:\n%s\n" % (str(response)))

    update.message.reply_text("Recipe:\n\n"
        "%s" % (obj.recipe.name.cdata), 
        parse_mode="HTML")

    response2 = rest_requests.get_recipe_nutrition_facts(obj.recipe.id.cdata)
    obj2 = untangle.parse(str(response2))

    update.message.reply_text("Nutrition:\n\n"
        "%s %s %s %s" % (obj2.recipeNutritionFacts.proteins.cdata, obj2.recipeNutritionFacts.carbohydrates.cdata, obj2.recipeNutritionFacts.lipids.cdata, obj2.recipeNutritionFacts.websiteUrl.cdata), 
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



def gender(bot, update):
    user = update.message.from_user
    logger.info("Gender of %s: %s" % (user.first_name, update.message.text))
    update.message.reply_text('I see! Please send me a photo of yourself, '
                              'so I know what you look like, or send /skip if you don\'t want to.',
                              reply_markup=ReplyKeyboardRemove())

    return PHOTO


def photo(bot, update):
    user = update.message.from_user
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s" % (user.first_name, 'user_photo.jpg'))
    update.message.reply_text('Gorgeous! Now, send me your location please, '
                              'or send /skip if you don\'t want to.')

    return LOCATION


def skip_photo(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a photo." % user.first_name)
    update.message.reply_text('I bet you look great! Now, send me your location please, '
                              'or send /skip.')

    return LOCATION


def location(bot, update):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f"
                % (user.first_name, user_location.latitude, user_location.longitude))
    update.message.reply_text('Maybe I can visit you sometime! '
                              'At last, tell me something about yourself.')

    return BIO


def skip_location(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a location." % user.first_name)
    update.message.reply_text('You seem a bit paranoid! '
                              'At last, tell me something about yourself.')

    return BIO


def bio(bot, update):
    user = update.message.from_user
    logger.info("Bio of %s: %s" % (user.first_name, update.message.text))
    update.message.reply_text('Thank you! I hope we can talk again some day.')

    return ConversationHandler.END


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
    updater = Updater("325642990:AAG7XiAvigXnWFmbKXNoylmdNB82taRwN6k")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            ADD_PERSON: [MessageHandler(Filters.text, get_recipe)],
            #ADD_PERSON: [MessageHandler(Filters.text, add_person)],
            CHECK_PERSON: [RegexHandler('^(Yes)$', choose_goal), RegexHandler('(No)$', manage_person)],
            MODIFY_PERSON: [RegexHandler('^(Update)$', modify_person), RegexHandler('(Delete)$', modify_person_2)],
            UPDATE_PERSON: [MessageHandler(Filters.text, update_person)],
            DELETE_PERSON: [MessageHandler(Filters.text, delete_person)],
            CHOOSE_GOAL: [MessageHandler(Filters.text, choose_goal)],
            ADD_GOAL: [MessageHandler(Filters.text, add_goal)],
            CHECK_GOAL: [RegexHandler('^(Yes)$', another_goal), RegexHandler('(No)$', manage_goal)],
            MODIFY_GOAL: [RegexHandler('^(Update)$', modify_goal), RegexHandler('(Delete)$', modify_goal_2)],
            SUCC_GOAL: [MessageHandler('^(Yes)$', choose_goal), RegexHandler('(No)$', get_recipe)],
            GENDER: [RegexHandler('^(Doctor)$',
                                    add_goal),
                       RegexHandler('(Patient)$',
                                    add_measurement),
                       ],
            #GENDER: [RegexHandler('^(Doctor|Patient)$', gender)],

            PHOTO: [MessageHandler(Filters.photo, photo),
                    CommandHandler('skip', skip_photo)],

            LOCATION: [MessageHandler(Filters.location, location),
                       CommandHandler('skip', skip_location)],

            BIO: [MessageHandler(Filters.text, bio)]
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