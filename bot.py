import tweepy
import logging
from secrets import access_token, access_token_secret, api_key, api_secret_key
from stream import MentionStreamer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Authentication
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
me = api.me()
logger.info("Logged as %s (@%s)" % (me.name, me.screen_name))

# Booting listener
mention = '@' + me.screen_name
listener = MentionStreamer(api, me)
stream = tweepy.Stream(auth=api.auth, listener=listener)
logger.info("Streaming API, filtering track for %s..." % mention)
stream.filter(track=[mention])


