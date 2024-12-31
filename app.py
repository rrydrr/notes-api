import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import mysql.connector # use correct library

load_dotenv()

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = mysql.connector.connect( # updated to use mysql.connector
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),  # use 'database' instead of 'dbname'
        port=os.getenv('DB_PORT')
    )
    return conn

@app.route('/notes', methods=['POST'])
def create_note():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO notes (title, content) VALUES (%s, %s)', (data['title'], data['content']))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Note created"}), 201

@app.route('/notes', methods=['GET'])
def read_notes():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM notes')
    notes = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(notes), 200

@app.route('/notes/<int:id>', methods=['PUT'])
def update_note(id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE notes SET title = %s, content = %s WHERE id = %s', (data['title'], data['content'], id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Note updated"}), 200

@app.route('/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM notes WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Note deleted"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))