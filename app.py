from flask import Flask
from flask import jsonify,request
import psycopg2 #pip install psycopg2 
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash
app=Flask(__name__)

app.secret_key = 'cairocoders-ednalan'
 
DB_HOST = "localhost"
DB_NAME = "sample"
DB_USER = "postgres"
DB_PASS = "c98xa5"
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@app.route('/')
def home_page():
    return "Hello World"
class User:
    def __init__(self,id,username=None,fullname=None,email=None,password=None)->None:
        self.id=id
        self.username=username
        self.fullname=fullname
        self.email=email
        self.password=password
    def to_Json(self):
        return{
            'id':self.id,
            'username':self.username,
            'fullname':self.fullname,
            'email':self.email,
            'password':self.password
        }

@app.route('/users/')
def users():
	conn = None
	cursor = None
	try:
		conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
		cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cursor.execute("SELECT * from users")
		rows = cursor.fetchall()
		return jsonify(rows)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/add', methods=['POST'])
def add_user():
    _json=request.json
    _fullname=_json['fullname']
    _username = _json['username']
    _password = _json['password']
    _email = _json['email']
    if _fullname and _username and _email and _password and request.method == 'POST':
        _hashed_password = generate_password_hash(_password)
        sql = "INSERT INTO users(fullname,username,password,email) VALUES(%s, %s, %s, %s)"
        data = (_fullname,_username,_hashed_password,_email)
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
        cursor.execute(sql, data)
        conn.commit()
        resp = jsonify('User added successfully!')
        resp.status_code = 200
        return resp

@app.route('/user')
def index():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
    cursor.execute("SELECT * from users") 
    rows = cursor.fetchall()
    users_data=[]
    for i in rows:
        dicta={}
        dicta['id']=i[0]
        dicta['fullname']=i[1]
        dicta['username']=i[2]
        dicta['password']=i[3]
        dicta['email']=i[4]
        users_data.append(dicta)
    print(users_data)
    return jsonify(users_data)

    """
    user={}
    data=[]
    users_data=['id','fullname','username','password','email']
    count=len(rows)-1
    for i in range(len(rows)):
        users_list=[]
        for j in range(len(rows[0])):
            user[users_data[j]]=(rows[i][j])
        users_list.append(user)
    return users_list
    """
@app.route('/user/<string:id>')
def user_get(id):
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
        cursor.execute("SELECT * FROM users WHERE id=%s", id)
        rows = cursor.fetchall()
        users_data=[]
        for i in rows:
            dicta={}
            dicta['id']=i[0]
            dicta['fullname']=i[1]
            dicta['username']=i[2]
            dicta['password']=i[3]
            dicta['email']=i[4]
            users_data.append(dicta)
        print(users_data)
        return jsonify(users_data)
@app.route('/user/<string:id>', methods=['PUT'])
def update_user(id):
    _json=request.json
    _fullname=_json['fullname']
    _username = _json['username']
    _password = _json['password']
    _email = _json['email']
    if _fullname and _username and _email and _password and request.method == 'PUT':
        _hashed_password = generate_password_hash(_password)
        sql = "UPDATE users SET fullname=%s,username=%s, password=%s, email=%s WHERE id=%s"
        data = data = (_fullname,_username, _hashed_password, _email, id)
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
        cursor.execute(sql, data)
        conn.commit()
        resp = jsonify('User updated successfully!')
        resp.status_code = 200
        return resp
@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
    cursor.execute("DELETE FROM users WHERE id=%s", (id,))
    conn.commit()
    resp = jsonify('User deleted successfully!')
    resp.status_code = 200
    return resp

if __name__=="__main__":
    app.run(debug=True)
