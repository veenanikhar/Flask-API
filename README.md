# Flask API with PostgreSQL Integration

This is a basic RESTful API built with Flask and PostgreSQL. The API allows you to manage users by providing endpoints for creating, reading, updating, and retrieving users from a PostgreSQL database.

## Prerequisites

- **Python 3.x**
- **Flask** and **psycopg2** libraries
- **PostgreSQL**

## Setup and Configuration

1. **Clone the repository:**

   ```bash
   git clone https://github.com/veenanikhar/React-Learning.git
   cd React-Learning
   ```

2. **Install required packages:**

   Install Flask and psycopg2 using pip.

   ```bash
   pip install Flask psycopg2
   ```

3. **Database Setup:**

   - Ensure PostgreSQL is installed and running.
   - Create a PostgreSQL database and user for the API.

   ```sql
   CREATE DATABASE flaskapi;
   CREATE USER postgres WITH PASSWORD '1234';
   ALTER ROLE postgres SET client_encoding TO 'utf8';
   ALTER ROLE postgres SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE flaskapi TO postgres;
   ```

4. **Configure Environment Variables:**

   In the `app.config` section of your Python file, replace `'DATABASE_URL'` with your PostgreSQL URL:
   
   ```python
   app.config['DATABASE_URL'] = 'postgresql://username:password@localhost:port/database'
   ```

5. **Generate a Secret Key:**

   To secure your Flask app, generate a secret key.

   ```python
   import secrets
   print(secrets.token_hex(16))
   ```

   Replace the `SECRET_KEY` in the code:

   ```python
   app.config['SECRET_KEY'] = 'your_generated_secret_key'
   ```

6. **Initialize Database Schema:**

   When the app is first run, it will automatically initialize the `users` table in PostgreSQL.

## API Endpoints

### 1. Get All Users

   - **URL:** `/users`
   - **Method:** `GET`
   - **Query Parameters:** Optional - `name`, `email`
   - **Description:** Retrieves all users or filters users by `name` or `email`.

### 2. Get User by ID

   - **URL:** `/users/<user_id>`
   - **Method:** `GET`
   - **Description:** Retrieves user details by `user_id`.

### 3. Add a New User

   - **URL:** `/users`
   - **Method:** `POST`
   - **Data Format:** JSON - `{"name": "User Name", "email": "user@example.com"}`
   - **Description:** Adds a new user to the database.

### 4. Update User Details

   - **URL:** `/users/<user_id>`
   - **Method:** `PATCH`
   - **Data Format:** JSON - `{"name": "Updated Name", "email": "updated.email@example.com"}`
   - **Description:** Updates user details, supporting partial updates.

## Running the Application

Start the Flask application by running:

```bash
python app.py
```

The API will be accessible at `http://127.0.0.1:5000`.

## Example Requests

### Get All Users

```bash
curl http://127.0.0.1:5000/users
```

### Add a User

```bash
curl -X POST -H "Content-Type: application/json" -d '{"name": "John Doe", "email": "john@example.com"}' http://127.0.0.1:5000/users
```

### Update a User

```bash
curl -X PATCH -H "Content-Type: application/json" -d '{"name": "Jane Doe"}' http://127.0.0.1:5000/users/1
```
