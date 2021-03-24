from tweepy import StreamListener, Status, API, User, TweepError
from pprint import PrettyPrinter
import logging
import re

logger = logging.getLogger(__name__)
pp = PrettyPrinter(indent=4)
picture_pattern = re.compile(r'(.*)_normal(.*)', re.IGNORECASE)

class MentionStreamer(StreamListener):
    def __init__(self, api: API, me: User):
        StreamListener.__init__(self, api)
        self.me = me

    def on_connect(self):
        """Called once connected to streaming server.

        This will be invoked once a successful response
        is received from the server. Allows the listener
        to perform some work prior to entering the read loop.
        """
        logger.info("Streamer connected!")

    def keep_alive(self):
        """Called when a keep-alive arrived"""
        return

    def on_status(self, status: Status):
        """Called when a new status arrives. AKA where the magic happen"""
        mentions = [user['screen_name'] for user in status.entities['user_mentions']]
        if self.me.screen_name in mentions:
            try:
                logger.info("Received a tweet, processing")
                # pic = picture_pattern.sub(r'\1\2', status.author.profile_image_url_https)
                self.api.update_with_media(
                    filename='humain1.jpg',
                    status='Hey @%s! Here is a beautiful picture 4U 🥰' % status.user.screen_name,
                    in_reply_to_status_id=status.id)
            except TweepError:
                logger.exception("An exception occurred during tweet processing")
        else:
            logger.info("Got a tweet but we weren't mentioned")
        return

    def on_exception(self, exception):
        """Called when an unhandled exception occurs."""
        logger.error("Unexpected exception:")
        logger.error(exception)
        return

    def on_delete(self, status_id, user_id):
        """Called when a delete notice arrives for a status"""
        return

    def on_event(self, status):
        """Called when a new event arrives"""
        return

    def on_direct_message(self, status):
        """Called when a new direct message arrives"""
        return

    def on_friends(self, friends):
        """Called when a friends list arrives.

        friends is a list that contains user_id
        """
        return

    def on_limit(self, track):
        """Called when a limitation notice arrives"""
        logger.warning("Got limited")
        logger.warning(track)
        return

    def on_error(self, status_code):
        """Called when a non-200 status code is returned"""
        logger.error("Twitter answered with an %d code", status_code)
        if status_code == 420:
            # returning False in on_error disconnects the stream
            return False
        return True

    def on_timeout(self):
        """Called when stream connection times out"""
        logger.warning("Timed out")
        return

    def on_disconnect(self, notice):
        """Called when twitter sends a disconnect notice

        Disconnect codes are listed here:
        https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/streaming-message-types
        """
        logger.info("Disconnected")
        return

    def on_warning(self, notice):
        """Called when a disconnection warning message arrives"""
        logger.warning("Got a warning notice: %s", notice)
        return
