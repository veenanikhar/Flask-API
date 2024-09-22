from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

# ***EXECUTE ON PYTHON SHELL***
# import secrets
# print(secrets.token_hex(16))

app.config['SECRET_KEY'] = '37222d30b678bcfba17a43195a9447bf'
app.config['DATABASE_URL'] = 'postgresql://postgres:1234@localhost:5432/flaskapi'

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(app.config['DATABASE_URL'])
    return conn

# Initialize the database schema
def initialize_db():
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(''' 
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(80) NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL
            );
        ''')
        conn.commit()
        conn.close()

initialize_db()

# # Route to get all users
# @app.route('/users', methods=['GET'])
# def get_users():
#     conn = get_db_connection()
#     with conn.cursor() as cur:
#         cur.execute('SELECT * FROM users;')    
#         users = cur.fetchall()
#         conn.close()
#     return jsonify([{'id': user[0], 'name': user[1], 'email': user[2]} for user in users])

# Route to get all users or search by query parameters (name, email)
@app.route('/users', methods=['GET'])
def get_users():
    # GET query parameters from the URL
    name = request.args.get('name') # None if not provided
    email = request.args.get('email') # None if not provided
    
    conn = get_db_connection()
    with conn.cursor() as cur:
        query = 'SELECT * FROM users'
        filters = []
        values = []
    
        # Apply filters if query parameters are provided
        if name:
            filters.append('name = %s')
            values.append(name)
        
        if email:
            filters.append('email = %s')
            values.append(email)
        
        if filters:
            query += ' WHERE ' + ' AND '.join(filters)    
        cur.execute(query, tuple(values))
        users = cur.fetchall()
    conn.close()
    
    return jsonify([{'id': user[0], 'name': user[1], 'email': user[2]} for user in users])
    

# Route to get a user by ID
@app.route('/users/<int:user_id>',methods=['GET'])
def get_user_by_id(user_id):
    conn = get_db_connection()
    with conn.cursor() as cur:
        # (user_id,) bcoz %s accepts tuple
        cur.execute('SELECT * FROM users WHERE id = %s;',(user_id,))
        user = cur.fetchone()
        conn.close()
        return jsonify({'id': user[0], 'name': user[1], 'email': user[2]})

# Route to add a new user
@app.route('/users', methods = ['POST'])
def add_user():
    data = request.get_json() # Get the JSON data from the request
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute('INSERT INTO users (name, email) values (%s, %s);',
                    (data['name'], data['email']))
        conn.commit()
        conn.close()
    return jsonify({'message': 'User added successfully!'})

# Route to update specific details
@app.route('/users/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    # data represents the incoming JSON payload, let's assume it's:
    # data = {"name": "Updated Name", "email": "updated.email@example.com"}
    data = request.get_json()
    
    # Establishes a database connection using a helper function
    conn = get_db_connection()
    
    # Creating a cursor object to interact with the PostgreSQL database
    with conn.cursor() as cur:
        
        # Initialize an empty list to store SQL fragments for the SET clause
        # and another list for corresponding values.
        set_clause = []
        values = []
        
        # Checking if the 'name' field exists in the incoming JSON data
        if 'name' in data:
            # Add the SQL fragment for the 'name' field to the set_clause list
            # and append the value to the values list.
            set_clause.append('name = %s')
            values.append(data['name'])  # values = ['Updated Name']

        # Checking if the 'email' field exists in the incoming JSON data
        if 'email' in data:
            # Add the SQL fragment for the 'email' field to the set_clause list
            # and append the value to the values list.
            set_clause.append('email = %s')
            values.append(data['email'])  # values = ['Updated Name', 'updated.email@example.com']
        
        # After Processing:
        # set_clause = ['name = %s', 'email = %s']
        # values = ['Updated Name', 'updated.email@example.com']
        
        # If no data is provided in the request body, return an error.
        if not set_clause:
            conn.close()  # Close the database connection.
            return jsonify({'error': 'No data to update'}), 400
        
        # Join the set_clause list into a single string with commas separating each field.
        set_clause_str = ', '.join(set_clause)  
        # set_clause_str = 'name = %s, email = %s'
        
        # Append the user_id to the values list since it's needed in the WHERE clause.
        values.append(user_id)  
        # values = ['Updated Name', 'updated.email@example.com', 1]
        
        # Construct the SQL UPDATE statement dynamically and execute it with the provided values.
        cur.execute(f'UPDATE users SET {set_clause_str} WHERE id = %s;', tuple(values))
        # SQL query becomes: 
        # 'UPDATE users SET name = %s, email = %s WHERE id = %s;'
        # The actual values passed are: ['Updated Name', 'updated.email@example.com', 1]

        # Commit the transaction to make sure the changes are saved in the database.
        conn.commit()
        
        # Close the database connection after committing the changes.
        conn.close()
    
    # Return a success message as a JSON response.
    return jsonify({'message' : 'User Updated Successfully'})


if __name__ == "__main__":
    app.run(debug=True)