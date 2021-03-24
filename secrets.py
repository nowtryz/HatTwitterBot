from os import environ
from dotenv import load_dotenv

load_dotenv()

api_key = environ['API_KEY']
api_secret_key = environ['API_SECRET_KEY']
bearer_token = environ['BEARER_TOKEN']
access_token = environ['ACCESS_TOKEN']
access_token_secret = environ['ACCESS_TOKEN_SECRET']
