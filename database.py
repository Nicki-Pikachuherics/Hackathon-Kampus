import json
import psycopg2

import requests

from keys import DB_HOST,DB_NAME,DB_USER,DB_PASSWORD

class Database:
    connectionstring = f'host={DB_HOST} user={DB_USER} password={DB_PASSWORD!r} dbname={DB_NAME}'
    
    @staticmethod
    def getAllUsers():
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * from users')
            return cursor.fetchall()
    
    @staticmethod
    def getUserById(id):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * from users WHERE id = %s', (id,))
            return cursor.fetchone()