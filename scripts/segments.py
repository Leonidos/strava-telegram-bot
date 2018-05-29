import logging

import telegram

from common import Common
from strava_api import StravaApi


class Segments(StravaApi, Common):
    stats_format = "<strong>%s. %s</strong>\n\n<b>Personal Record:</b>\n- <i>Time</i>: %s\n- <i>Date</i>: %s\n- <i>Total Attempts</i>: %s\n\n<b>Segment Details:</b>\n- <i>Distance</i>: %s kms\n- <i>Created</i>: %s\n- <i>Avg Gradient</i>: %s percent\n- <i>Max Gradient</i>: %s percent\n- <i>Highest Elevation</i>: %s meters\n- <i>Lowest Elevation</i>: %s meters\n- <i>Total Elevation Gain</i>: %s meters\n- <i>Total Athletes Attempted</i>: %s\n- <i>Total Attempts</i>: %s\n\n<b>Leaderboard:</b>\n%s" + "\n\n"

    leaderboard_format = "%s. %s | %s | %s\n"

    def __init__(self, bot, update, athlete_token, shadow_mode, shadow_chat_id):
        logging.info("Initializing %s" % self.__class__.__name__)
        self.bot = bot
        self.update = update
        self.shadow_mode = shadow_mode
        self.shadow_chat_id = shadow_chat_id
        StravaApi.__init__(self, athlete_token)

    def send_message(self, bot, update, message):
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        update.message.reply_text(message, parse_mode="HTML", disable_web_page_preview=True)
        if self.shadow_mode and (
                int(self.shadow_chat_id) != int(update.message.chat_id)):
            bot.send_message(chat_id=self.shadow_chat_id, text=message,
                             parse_mode="HTML", disable_notification=True,
                             disable_web_page_preview=True)
        else:
            logging.info("Chat ID & Shadow Chat ID are the same")

    def prepare_leaderboard(self, leaderboard):
        message = ""
        for leader in leaderboard['entries']:
            message += (self.leaderboard_format
                        % (leader['rank'],
                           self.seconds_to_human_readable(leader['elapsed_time']),
                           self.date_to_human_readable_with_short_year(leader['start_date_local']),
                           leader['athlete_name']))
        return message

    def collect_stats(self, starred_segments):
        segment_count = 1
        for segment in starred_segments:
            segment_details = self.get_segment_details(segment['id'])
            segment_leaderboard = self.get_segment_leaderboard(segment['id'], "1", "10")
            segment_stats = (self.stats_format %
                             (
                                  segment_count,
                                  segment['name'],
                                  self.seconds_to_human_readable(segment['athlete_pr_effort']['elapsed_time']),
                                  self.date_to_human_readable_with_time(
                                      segment['athlete_pr_effort']['start_date_local']),
                                  segment_details['athlete_segment_stats']['effort_count'],
                                  self.meters_to_kilometers(segment['distance']),
                                  self.date_to_human_readable(segment_details['created_at']),
                                  segment['average_grade'],
                                  segment['maximum_grade'],
                                  segment['elevation_high'],
                                  segment['elevation_low'],
                                  segment_details['total_elevation_gain'],
                                  segment_details['athlete_count'],
                                  segment_details['effort_count'],
                                  self.prepare_leaderboard(segment_leaderboard)
                              ))
            segment_count += 1
            self.send_message(self.bot, self.update, segment_stats)


    def main(self):
        message = "You don't have any starred segments."
        starred_segments = self.get_starred_segments("200", "1")
        if len(starred_segments) > 0:
            self.collect_stats(starred_segments)
            return "Finished fetching stats for %s starred segment(s)." % len(starred_segments)
        else:
            return message
