import json
import psycopg2
from datetime import date,datetime, timedelta
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
            cursor.execute('SELECT users.id, roles.name, users.login, users.phone_number, users.email, users.university_id, users.options, users.name, users.surname, users.lastname, users.birthday, users.gender_id, professions.name from users join genders on users.gender_id = genders.id join roles on users.role_id = roles.id join professions on users.profession_id_id = professions.id order by id')
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
                    'options': row[6],
                    'name': row[7],
                    'surname': row[8],
                    'lastname': row[9],
                    'birthday': row[10], #TODO: Потестить
                    'gender': row[11],
                    'profession': row[12]
                })
            return output
    
    @staticmethod
    def getUserById(id):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT users.id, roles.name, users.login, users.phone_number, users.email, users.university_id, users.options, users.name, users.surname, users.lastname, users.birthday, users.gender_id, professions.name from users join genders on users.gender_id = genders.id join roles on users.role_id = roles.id join professions on users.profession_id = professions.id WHERE users.id = %s', (id,))
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
                    'options': row[6],
                    'name': row[7],
                    'surname': row[8],
                    'lastname': row[9],
                    'birthday': row[10],
                    'gender': row[11],
                    'profession': row[12]
                }
    @staticmethod
    def getUserByLogin(login):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT users.id, roles.name, users.login, users.phone_number, users.email, users.university_id, users.options, users.name, users.surname, users.lastname, users.birthday, users.gender_id, professions.name from users join genders on users.gender_id = genders.id join roles on users.role_id = roles.id join professions on users.profession_id = professions.id WHERE users.login = %s', (login,))
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
                    'options': row[6],
                    'name': row[7],
                    'surname': row[8],
                    'lastname': row[9],
                    'birthday': row[10],
                    'gender': row[11],
                    'profession': row[12]
                }
        
    def getPostComments(postid):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT comments.id, users.login, users.name, users.surname, users.lastname, users.id, comments.text from comments join users on comments.user_id = users.id WHERE comments.post_id = %s', (postid,))
            rows = cursor.fetchall()
            output = []
            for row in rows:
                output.append({
                    'id': row[0],
                    'login': row[1],
                    'name': row[2],
                    'surname': row[3],
                    'lastname': row[4],
                    'user_id': row[5],
                    'text': row[6],
                    'author': Database.getUserById(row[5])
                })
            return output
    
    def createPost(userid, data):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            user = Database.getUserById(userid)
            if not user: raise ValueError('User not found')
            if user['role'] == 'Организатор' or user['role'] == 'Асессор' or user['role'] == 'Администратор':
                cursor.execute('INSERT INTO posts(data, university_id, creation_time) VALUES (%s, %s, CURRENT_TIMESTAMP)', (data, user['university_id']))
            else: raise ValueError('User not allowed to create post')
            conn.commit()
    
    def getUniversityByName(name):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, options from universities WHERE name = %s', (name,))
            row = cursor.fetchone()
            if not row:
                return None
            return {
                    'id': row[0],
                    'name': row[1],
                    'options': row[2]
                }
    
    def CommentPost(postid, userid, text):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO comments(post_id, user_id, text) VALUES (%s, %s, %s)', (postid, userid, text))
            conn.commit()
        
    def getUserByPhone(phone):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT users.id, roles.name, users.login, users.phone_number, users.email, users.university_id, users.options, users.name, users.surname, users.lastname, users.birthday, users.gender_id, professions.name from users join genders on users.gender_id = genders.id join roles on users.role_id = roles.id join professions on users.profession_id = professions.id WHERE users.phone_number = %s', (phone,))
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
                    'options': row[6],
                    'name': row[7],
                    'surname': row[8],
                    'lastname': row[9],
                    'birthday': row[10],
                    'gender': row[11],
                    'profession': row[12]
                }
    
    def getUserByEmail(email):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT users.id, roles.name, users.login, users.phone_number, users.email, users.university_id, users.options, users.name, users.surname, users.lastname, users.birthday, users.gender_id, professions.name from users join genders on users.gender_id = genders.id join roles on users.role_id = roles.id join professions on users.profession_id = professions.id WHERE users.email = %s', (email,))
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
                    'options': row[6],
                    'name': row[7],
                    'surname': row[8],
                    'lastname': row[9],
                    'birthday': row[10],
                    'gender': row[11],
                    'profession': row[12]
                }
    
    def regUserByAdmin(name, surname, lastname, phone_number, email, university_id, gender_id, profession_id=1, role_id=1) -> str: 
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            password = generateRandomString(8)
            cursor.execute('INSERT INTO users (phone_number, email, profession_id, password_hash, university_id, role_id, gender_id, name, surname, lastname) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (phone_number, email, profession_id, hashPassword(password), university_id, role_id, gender_id, name, surname, lastname))
        return password

    @staticmethod
    def loginUser(login,password):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM users WHERE (login = %s OR phone_number = %s OR email = %s) AND password_hash = %s LIMIT 1', (login, login, login, hashPassword(password),))
            info = cursor.fetchone()
            if info:
                return {
                        'id': info[0]
                    }
            else:
                return None
            
    
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
    def getPostLikes(postid: int):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM likes WHERE post_id = %s', (postid,))
            return cursor.fetchone()[0]
    
    @staticmethod
    def getUserPosts(userid: int):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM posts WHERE data.user_id = %s', (userid,))
            rows = cursor.fetchall()
            return [{
                'id': row[0],
                'data': row[1],
                'university_id': row[2],
                'creation_time': row[3]
            } for row in rows]
    
    @staticmethod
    def getAllPosts():
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM posts')
            rows = cursor.fetchall()
            posts = [{
                'id': row[0],
                'data': row[1],
                'university_id': row[2],
                'creation_time': row[3]
            } for row in rows]
            for post in posts: post['likes'] = Database.getPostLikes(post['id'])
            return posts

    @staticmethod
    def getPostsForUser(userid: int):
        posts = Database.getAllPosts()
        #TODO: Вот эту логику надо будет жестко проработать, это буквально система рекомендаций
        return posts
    
    @staticmethod
    def getPostsForUniversity(universityid: int):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM posts WHERE university_id = %s', (universityid,))
            rows = cursor.fetchall()
            posts = [{
                'id': row[0],
                'data': row[1] if row[1] else {},
                'university_id': row[2],
                'creation_time': row[3]
            } for row in rows]
            
            for post in posts: 
                post['likes'] = Database.getPostLikes(post['id'])
                post['data']['comments'] = Database.getPostComments(post['id'])
            return posts
    
    @staticmethod
    def getPostsForUserInUniversity(user_id: int):
        return Database.getPostsForUniversity(Database.getUserUniversity(user_id)['id'])
    
    @staticmethod
    def getPostById(id: int):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM posts WHERE id = %s', (id,))
            row = cursor.fetchone()
            return {
                'id': row[0],
                'data': row[1],
                'university_id': row[2],
                'creation_time': row[3],
                'likes': Database.getPostLikes(id)
            }
    
    @staticmethod
    def getUserUniversity(userid: int):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT university_id from users WHERE id = %s', (userid,))
            return Database.getUniversityById(cursor.fetchone()[0])
    
    @staticmethod
    def getUserOptions(userid: int):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT options from users WHERE id = %s', (userid,))
            return cursor.fetchone()[0]
    
    @staticmethod
    def updateUserOptions(userid: int, options: dict):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET options = %s WHERE id = %s', (json.dumps(options), userid,)) #FIXME: Возможно не надо dumps для json
            conn.commit()
    @staticmethod
    def updateUserInfo(userid: int, login: str, password: str):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET login = %s, password_hash = %s WHERE id = %s', (login, hashPassword(password), userid,))
            conn.commit()
    
    @staticmethod
    def getAllEvents():
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM events')
            rows = cursor.fetchall()
            return [{
                'id': row[0],
                'data': row[1],
                'creation_time': row[2]
            } for row in rows]
    
    @staticmethod
    def getEventById(id: int):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM events WHERE id = %s', (id,))
            row = cursor.fetchone()
            return {
                'id': row[0],
                'data': row[1],
                'creation_time': row[2]
            }
    
    @staticmethod
    def getEventsForUniversity(universityid: int):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM events WHERE data.university_id = %s', (universityid,))
            rows = cursor.fetchall()
            return [{
                'id': row[0],
                'data': row[1],
                'creation_time': row[2]
            } for row in rows]
    
    @staticmethod
    def getAllEventsForUser(userid: int):
        events = Database.getAllEvents()
        #TODO: Вот эту логику надо будет жестко проработать, это буквально система рекомендаций
        return events
    
    @staticmethod
    def getEventsForUserInUniversity(userid: int):
        university = Database.getUserUniversity(userid)
        events = Database.getEventsForUniversity(university['id'])
        #TODO: Вот эту логику надо будет жестко проработать, это буквально система рекомендаций
        return events
    @staticmethod
    def GetAllUnivercities():
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM universities')
            rows = cursor.fetchall()
            output = []
            for row in rows:
                output.append({
                    'id': row[0],
                    'name': row[1],
                    'options': row[2]
                }) 
            return output
    @staticmethod
    def getUniversityById(id: int):
        with psycopg2.connect(Database.connectionstring) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * from universities WHERE id = %s', (id,))
            row = cursor.fetchone()
            return {
                'id': row[0],
                'name': row[1],
                'options': row[2]
            }

#print(Database.regUserByAdmin(name='John', surname='Doe', lastname='Smith',phone_number='+71111111111', email = 'example@admin.com', university_id=1, gender_id=1, profession_id=5, role_id=4))