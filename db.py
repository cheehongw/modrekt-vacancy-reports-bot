import psycopg2, pandas

#import config function that returns a config dictionary
from config import config

def connect():
    params = config()
    connection = psycopg2.connect(**params)
    return connection