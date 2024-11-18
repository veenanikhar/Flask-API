from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

import psycopg2

app = Flask(__name__)
CORS(app)

app.config['DATABASE_URL'] = 'postgresql://postgres:1234@localhost:5433/flaskapi'  # Update with your database credentials

SWAGGER_URL = '/swagger'  # URL to access Swagger UI
API_URL = '/swagger.json'  # URL where Swagger JSON is served

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI endpoint
    API_URL,      # Swagger JSON endpoint
    config={       # Swagger UI configuration
        'app_name': "User Management API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/swagger.json')
def swagger_json():
    return app.send_static_file('swagger.json')


# Database connection function
def get_db_connection():
    try:
        conn = psycopg2.connect(app.config['DATABASE_URL'])
        return conn
    except psycopg2.Error as e:
        print("Unable to connect to the database:", e)
        return None

# Initialize the database schema
def initialize_db():
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute('''
                 CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(80) NOT NULL,
                    email VARCHAR(120) UNIQUE NOT NULL,
                    placeOfBirth VARCHAR(120)
                );
            ''')
            conn.commit()
            conn.close()

initialize_db()

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM users;')
            users = cur.fetchall()
            users_list = []
            for user in users:
                user_dict = {
                    'id': user[0],
                    'name': user[1],
                    'email': user[2],
                    'placeOfBirth': user[3]
                }
                users_list.append(user_dict)
        conn.close()
        return jsonify(users_list)
    else:
        return jsonify({'error': 'Failed to connect to database'}), 500

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM users WHERE id = %s;', (user_id,))
            user = cur.fetchone()
            if user:
                user_dict = {
                    'id': user[0],
                    'name': user[1],
                    'email': user[2],
                    'placeOfBirth': user[3]
                }
                conn.close()
                return jsonify(user_dict)
            else:
                conn.close()
                return jsonify({'message': 'User not found'}), 404
    else:
        return jsonify({'error': 'Failed to connect to database'}), 500
    
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    if not all(key in data for key in ['name', 'email', 'placeOfBirth']):
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO users (name, email, placeOfBirth) VALUES (%s, %s, %s);',
                        (data['name'], data['email'], data['placeOfBirth']))
            conn.commit()
        conn.close()
        return jsonify({'message': 'User added successfully!'}), 201
    else:
        return jsonify({'error': 'Failed to connect to database'}), 500

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not any(key in data for key in ['name', 'email', 'placeOfBirth']):
        return jsonify({'error': 'No valid fields to update'}), 400

    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            query = 'UPDATE users SET '
            params = []
            
            if 'name' in data:
                query += 'name = %s, '
                params.append(data['name'])
            if 'email' in data:
                query += 'email = %s, '
                params.append(data['email'])
            if 'placeOfBirth' in data:
                query += 'placeOfBirth = %s, '
                params.append(data['placeOfBirth'])
            
            # Remove trailing comma and space
            query = query.rstrip(', ') + ' WHERE id = %s;'
            params.append(user_id)
            
            cur.execute(query, tuple(params))
            conn.commit()
            conn.close()
            return jsonify({'message': 'User updated successfully!'}), 200
    else:
        return jsonify({'error': 'Failed to connect to database'}), 500

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM users WHERE id = %s;', (user_id,))
            conn.commit()
            conn.close()
            return jsonify({'message': 'User deleted successfully!'}), 200
    else:
        return jsonify({'error': 'Failed to connect to database'}), 500

@app.route('/users', methods=['DELETE'])
def delete_all_users():
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM users;')
            conn.commit()
        conn.close()
        return jsonify({'message': 'All users deleted successfully!'}), 200
    else:
        return jsonify({'error': 'Failed to connect to database'}), 500

if __name__ == "__main__":
    app.run(debug=True)
