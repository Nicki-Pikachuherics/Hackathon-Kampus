import json
import psycopg2
from datetime import datetime, timedelta
import hashlib
from keys import DB_HOST,DB_NAME,DB_USER,DB_PASSWORD

def generateRandomString(length):
    import random
    symbols = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890+/=*@'
    output = ''
    for i in range(length):
        output += symbols[random.randrange(len(symbols))]
    return output

def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()

class Database:
    connectionstring = f'host={DB_HOST} user={DB_USER} password={DB_PASSWORD!r} dbname={DB_NAME}'

    @staticmethod
    def getAllUsers():
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT users.id, roles.role, users.login, users.phone_number, users.email, users.university_id, users.options, users.name, users.surname, users.lastname, users.birthsday, users.gender, professions.name from users join genders on users.gender = genders.id join roles on users.role = roles.id join profession on users.profession = profession.id order by id')
            rows = cursor.fetchall()
            output = []
            for row in rows:
                output.append({
                    'id': row[0],
                    'role': row[1],
                    'login': row[2],
                    'phone_number': row[3],
                    'email': row[4],
                    'university': Database.getUniversityById(row[5]),
                    'options': json.loads(row[6]),
                    'name': row[7],
                    'surname': row[8],
                    'lastname': row[9],
                    'birthsday': row[10], #TODO: Потестить
                    'gender': row[11],
                    'profession': row[12]
                })
            return output
    
    @staticmethod
    def getUserById(id):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT users.id, roles.role, users.login, users.phone_number, users.email, users.university_id, users.options, users.name, users.surname, users.lastname, users.birthsday, users.gender, professions.name from users join genders on users.gender = genders.id join roles on users.role = roles.id join profession on users.profession = profession.id WHERE users.id = %s', (id,))
            row = cursor.fetchone()
            if not row:
                return None
            return {
                    'id': row[0],
                    'role': row[1],
                    'login': row[2],
                    'phone_number': row[3],
                    'email': row[4],
                    'university': Database.getUniversityById(row[5]),
                    'options': json.loads(row[6]),
                    'name': row[7],
                    'surname': row[8],
                    'lastname': row[9],
                    'birthsday': row[10],
                    'gender': row[11],
                    'profession': row[12]
                }
    @staticmethod
    def getUserByLogin(login):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT users.id, roles.role, users.login, users.phone_number, users.email, users.university_id, users.options, users.name, users.surname, users.lastname, users.birthsday, users.gender, professions.name from users join genders on users.gender = genders.id join roles on users.role = roles.id join profession on users.profession = profession.id WHERE users.login = %s', (login,))
            row = cursor.fetchone()
            if not row:
                return None
            return {
                    'id': row[0],
                    'role': row[1],
                    'login': row[2],
                    'phone_number': row[3],
                    'email': row[4],
                    'university': Database.getUniversityById(row[5]),
                    'options': json.loads(row[6]),
                    'name': row[7],
                    'surname': row[8],
                    'lastname': row[9],
                    'birthsday': row[10],
                    'gender': row[11],
                    'profession': row[12]
                }
    
    def getUserByPhone(phone):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT users.id, roles.role, users.login, users.phone_number, users.email, users.university_id, users.options, users.name, users.surname, users.lastname, users.birthsday, users.gender, professions.name from users join genders on users.gender = genders.id join roles on users.role = roles.id join profession on users.profession = profession.id WHERE users.phone_number = %s', (phone,))
            row = cursor.fetchone()
            if not row:
                return None
            return {
                    'id': row[0],
                    'role': row[1],
                    'login': row[2],
                    'phone_number': row[3],
                    'email': row[4],
                    'university': Database.getUniversityById(row[5]),
                    'options': json.loads(row[6]),
                    'name': row[7],
                    'surname': row[8],
                    'lastname': row[9],
                    'birthsday': row[10],
                    'gender': row[11],
                    'profession': row[12]
                }
    
    def getUserByEmail(email):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT users.id, roles.role, users.login, users.phone_number, users.email, users.university_id, users.options, users.name, users.surname, users.lastname, users.birthsday, users.gender, professions.name from users join genders on users.gender = genders.id join roles on users.role = roles.id join profession on users.profession = profession.id WHERE users.email = %s', (email,))
            row = cursor.fetchone()
            if not row:
                return None
            return {
                    'id': row[0],
                    'role': row[1],
                    'login': row[2],
                    'phone_number': row[3],
                    'email': row[4],
                    'university': Database.getUniversityById(row[5]),
                    'options': json.loads(row[6]),
                    'name': row[7],
                    'surname': row[8],
                    'lastname': row[9],
                    'birthsday': row[10],
                    'gender': row[11],
                    'profession': row[12]
                }
    
    def regUserByAdmin(phone_number, email, profession='Студент') -> str: 
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            password = generateRandomString(8)
            cursor.execute('INSERT INTO users (phone_number, email, profession, password_hash) VALUES (%s, %s, %s, %s)', (phone_number, email, profession, hashPassword(password),))
        return password

    @staticmethod
    def loginUser(login,password):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT EXISTS(SELECT 1 FROM users WHERE (login = %s OR phone_number = %s OR email = %s) AND password_hash = %s LIMIT 1', (login, login, login, hashPassword(password),))
            return cursor.fetchone()[0]
    
    @staticmethod
    def likePost(userid: int, postid: int):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT EXISTS(SELECT 1 FROM likes WHERE user_id = %s AND post_id = %s)', (userid, postid,))
            already_liked = cursor.fetchone()[0]
            if already_liked:
                cursor.execute('DELETE FROM likes WHERE user_id = %s AND post_id = %s', (userid, postid,))
            else:
                cursor.execute('INSERT INTO likes (user_id, post_id) VALUES (%s, %s)', (userid, postid,))
            conn.commit()
            return not already_liked
    
    @staticmethod
    def getUserUniversity(userid: int):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT university_id from users WHERE id = %s', (userid,))
            return Database.getUniversityById(cursor.fetchone()[0])
    
    @staticmethod
    def getUniversityById(id: int):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * from universities WHERE id = %s', (id,))
            row = cursor.fetchone()
            return {
                'id': row[0],
                'name': row[1],
                'options': json.loads(row[2])
            }