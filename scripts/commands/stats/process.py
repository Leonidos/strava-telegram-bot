#  -*- encoding: utf-8 -*-

import json
from os import sys, path

import psycopg2
from telegram import InlineKeyboardMarkup

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from scripts.commands.stats.calculate import CalculateStats
from scripts.common.constants_and_variables import BotConstants, BotVariables
from scripts.common.operations import Operations
from scripts.commands.stats.format import FormatStats


class ProcessStats(object):

    def __init__(self, bot, update, user_data, athlete_token):
        self.bot = bot
        self.update = update
        self.telegram_username = self.update.message.from_user.username
        self.user_data = user_data
        self.athlete_token = athlete_token
        self.bot_constants = BotConstants()
        self.bot_variables = BotVariables()
        self.operations = Operations()

    def insert_strava_data(self, strava_data):
        database_connection = psycopg2.connect(self.bot_variables.database_url, sslmode='require')
        cursor = database_connection.cursor()
        cursor.execute(self.bot_constants.QUERY_UPDATE_STRAVA_DATA.format(strava_data=strava_data,
                                                                          telegram_username=self.telegram_username))
        cursor.close()
        database_connection.commit()
        database_connection.close()

    def get_strava_data(self):
        database_connection = psycopg2.connect(self.bot_variables.database_url, sslmode='require')
        cursor = database_connection.cursor()
        cursor.execute(self.bot_constants.QUERY_GET_STRAVA_DATA.format(telegram_username=self.telegram_username))
        strava_data = cursor.fetchone()[0]
        cursor.close()
        database_connection.close()

        return strava_data

    def process(self):
        calculate_stats = CalculateStats(self.bot, self.update, self.user_data, self.athlete_token)

        calculated_stats = calculate_stats.calculate()
        calculated_stats = json.dumps(calculated_stats)
        self.insert_strava_data(calculated_stats)

        strava_data = self.get_strava_data()

        format_stats = FormatStats(strava_data)

        stats = dict()
        stats['all_time_ride_stats'] = format_stats.all_time_ride_stats()
        stats['ytd_ride_stats'] = format_stats.ytd_ride_stats()
        stats['py_ride_stats'] = format_stats.py_ride_stats()
        stats['cm_ride_stats'] = format_stats.cm_ride_stats()
        stats['pm_ride_stats'] = format_stats.pm_ride_stats()
        stats['all_time_run_stats'] = format_stats.all_time_run_stats()
        stats['ytd_run_stats'] = format_stats.ytd_run_stats()
        stats['py_run_stats'] = format_stats.py_run_stats()
        stats['cm_run_stats'] = format_stats.cm_run_stats()
        stats['pm_run_stats'] = format_stats.pm_run_stats()
        self.user_data['stats'] = stats
        self.update.message.reply_text(self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU,
                                       reply_markup=InlineKeyboardMarkup(self.bot_constants.STATS_MAIN_KEYBOARD_MENU))