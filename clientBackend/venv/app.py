from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

mysql = MySQL(app)




@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    if not user:
        cursor.close()
        return jsonify({'message': 'Incorrect username'}), 401
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    if user:
        token = jwt.encode({
            'user_id': user['id'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})
    return jsonify({'message': 'Incorrect password'}), 401


@app.route("/users/<int:user_id>", methods=['GET'])
def fetchUsers(user_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT username FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if user:
            return jsonify(user)
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route("/schedules", methods=['GET'])
def fetchSchedules():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM schedules")
        rows = cursor.fetchall()
        cursor.close()
        return jsonify(rows)
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/addschedules', methods=['POST'])
def addSchedule():
    try:
        data = request.get_json()
        schedule_date = data['schedule_date']
        schedule_description = data['schedule_description']
        schedule_header = data['schedule_header']
        user_id = 1  # Default user_id

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO schedules (schedule_date, schedule_description, schedule_header, user_id) VALUES (%s, %s, %s, %s)",
                       (schedule_date, schedule_description, schedule_header, user_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Schedule added successfully'}), 201
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    

@app.route('/editschedules/<int:schedule_id>', methods=['PUT'])
def editSchedule(schedule_id):
    try:
        data = request.get_json()
        schedule_description = data['schedule_description']
        schedule_header = data['schedule_header']

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE schedules SET schedule_description=%s, schedule_header=%s WHERE id=%s",
                       (schedule_description, schedule_header, schedule_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Schedule updated successfully'}), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    
@app.route('/deleteschedules/<int:schedule_id>', methods=['DELETE'])
def deleteSchedule(schedule_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM schedules WHERE id = %s", (schedule_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Schedule deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500