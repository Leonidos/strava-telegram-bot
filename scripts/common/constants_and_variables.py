#  -*- encoding: utf-8 -*-

from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from telegram import InlineKeyboardButton
import os


class BotConstants(object):
    QUERY_FETCH_TOKEN = "select access_token from athletes where telegram_username='{telegram_username}'"

    MESSAGE_START_COMMAND = "Hey {first_name}! I'm your Strava Bot. Type '/' to get the list of command(s) that I understand."
    MESSAGE_STATS_COMMAND = "Hey {first_name}! Give me a minute or two while I fetch your data."
    MESSAGE_STATS_MAIN_KEYBOARD_MENU = "Choose an activity type to view your stats:"
    MESSAGE_STATS_RIDE_KEYBOARD_MENU = "Choose the type of stat you want to see:"
    MESSAGE_UNREGISTERED_ATHLETE = "Hi {first_name}! You are not a registered user yet.\n\nVisit the following link to register: {registration_url}\n\nPing {admin_user_name} in case you face any issue."
    MESSAGE_EXIT_BUTTON = "Thank you!"

    STATS_MAIN_KEYBOARD_MENU = [[InlineKeyboardButton("Ride", callback_data='stats_ride'),
                                 InlineKeyboardButton("Run", callback_data='stats_run')],
                                [InlineKeyboardButton("Exit", callback_data='exit')]]

    STATS_RIDE_KEYBOARD_MENU = [[InlineKeyboardButton("All Time", callback_data='stats_ride_all_time'),
                                 InlineKeyboardButton("Year to Date", callback_data='stats_ride_ytd'),
                                 InlineKeyboardButton("Misc", callback_data='stats_ride_misc')],
                                [InlineKeyboardButton("Back", callback_data='back'),
                                 InlineKeyboardButton("Exit", callback_data='exit')]]

    STATS_RUN_KEYBOARD_MENU = [[InlineKeyboardButton("All Time", callback_data='stats_run_all_time'),
                                InlineKeyboardButton("Year to Date", callback_data='stats_run_ytd')],
                               [InlineKeyboardButton("Back", callback_data='back'),
                                InlineKeyboardButton("Exit", callback_data='exit')]]


class BotVariables(object):
    database_url = os.environ['DATABASE_URL']
    crypt_key_length = os.environ['CRYPT_KEY_LENGTH']
    crypt_key = os.environ['CRYPT_KEY']
    admin_user_name = os.environ['ADMIN_USER_NAME']
    app_name = os.environ.get('APP_NAME')
    port = os.environ.get('PORT')
    registration_url = os.environ['REGISTRATION_URL']
    telegram_bot_token = os.environ['TELEGRAM_BOT_TOKEN']