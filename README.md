# Flask API with Swagger UI

This project demonstrates how to build a simple Flask API integrated with Swagger UI and PostgreSQL. The API provides CRUD operations for a `users` table, and Swagger UI allows you to interact with the API in an easy-to-use interface.

## Features
- **Swagger UI** for easy API interaction.
- **CRUD Operations** for user management (`GET`, `POST`, `PUT`, `DELETE`).
- **PostgreSQL Database** for storing user data.

## Project Setup

### 1. Prerequisites
Before starting, ensure you have the following installed:
- Python 3.x
- PostgreSQL Database
- pip (Python's package installer)

### 2. Install Dependencies
Clone the repository or create a new project directory, then create a virtual environment and install the required dependencies.

```bash
# Install Python
- Ensure Python 3.x is installed on your
python --version
```
- If not installed, download and install Python from [python.org](https://www.python.org/).

```bash
# Create a new directory (if not already done)
mkdir flask-swagger-api
cd flask-swagger-api

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# For Windows
venv\Scripts\activate
# For MacOS/Linux
source venv/bin/activate

# Install required Python packages
pip install -r requirements.txt

# Install Dependencies
Install `Flask`, `Flask-CORS`, `flask-swagger-ui`, and `psycopg2`:
pip install flask flask-cors flask-swagger-ui psycopg2
```

Your `requirements.txt` should include:
```
Flask==2.2.5
Flask-Cors==3.0.10
psycopg2==2.9.7
flask-swagger-ui==4.11.1
```

### 3. PostgreSQL Setup
Ensure PostgreSQL is installed and running. Create a new database for this project.

1. Start PostgreSQL (if not already running).
2. Create a new database:
   ```bash
   psql -U postgres
   CREATE DATABASE flaskapi;
   ```

3. Update the database connection string in the Flask app to use the correct credentials:
   ```python
   app.config['DATABASE_URL'] = 'postgresql://postgres:1234@localhost:5433/flaskapi'
   ```
- `postgres`: Default username
- `1234`: Replace with your password
- `5433`: Replace with your PostgreSQL port (default is usually `5432`)
### 4. Running the Application

Once everything is set up, run the application:

```bash
# Start the Flask application
python app.py
```

By default, the application will run at `http://localhost:5000`.

### 5. Access Swagger UI

Once the application is running, you can access Swagger UI at the following URL:
```
http://localhost:5000/swagger
```

Swagger UI will allow you to interact with your API using the following routes:
- `GET /users` - Retrieve all users.
- `GET /users/{user_id}` - Retrieve a single user by ID.
- `POST /users` - Add a new user.
- `PUT /users/{user_id}` - Update user details.
- `DELETE /users/{user_id}` - Delete a user by ID.
- `DELETE /users` - Delete all users.

### 6. Example Requests

- **GET /users**: Retrieve all users.
  - Response: A list of all users in the database.

- **GET /users/{user_id}**: Retrieve a user by ID.
  - Response: The user’s details in JSON format.

- **POST /users**: Add a new user.
  - Request Body:
    ```json
    {
      "name": "John Doe",
      "email": "john.doe@example.com",
      "placeOfBirth": "New York"
    }
    ```
  - Response: A success message confirming user creation.

- **PUT /users/{user_id}**: Update an existing user.
  - Request Body (only send fields you want to update):
    ```json
    {
      "name": "John Updated"
    }
    ```

- **DELETE /users/{user_id}**: Delete a user by ID.
  - Response: A success message confirming user deletion.

- **DELETE /users**: Delete all users.
  - Response: A success message confirming all users have been deleted.

## Directory Structure
```
flask-swagger-api/
│
├── app.py                  # Main Flask app and routes
├── static/
│   └── swagger.json        # Swagger specification file
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## Step-by-Step to Implement Swagger UI in Flask

### 1. Install Required Packages
To use Swagger UI in Flask, you need the `flask-swagger-ui` package. Install it using:
```bash
pip install flask-swagger-ui
```

### 2. Create a Flask Application
Set up your basic Flask app. Import necessary packages and initialize your app:
```python
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
```

### 3. Configure Swagger UI
Set the URL paths for Swagger UI and the Swagger JSON file:
```python
SWAGGER_URL = '/swagger'  # URL for Swagger UI
API_URL = '/swagger.json'  # URL for the Swagger JSON file

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI endpoint
    API_URL,      # Swagger JSON endpoint
    config={       # Swagger UI configuration
        'app_name': "User Management API"
    }
)

# Register the blueprint with Flask
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
```

### 4. Serve the Swagger JSON File
Swagger UI requires a `swagger.json` file to define the API endpoints. Create the file manually or generate it dynamically.

Example:
```json
{
  "swagger": "2.0",
  "info": {
    "title": "User Management API",
    "version": "1.0.0"
  },
  "paths": {
    "/users": {
      "get": {
        "summary": "Get all users",
        "responses": {
          "200": {
            "description": "A list of users"
          }
        }
      },
      "post": {
        "summary": "Create a new user",
        "responses": {
          "201": {
            "description": "User created successfully"
          }
        }
      }
    },
    "/users/{id}": {
      "get": {
        "summary": "Get a user by ID",
        "responses": {
          "200": {
            "description": "User found"
          },
          "404": {
            "description": "User not found"
          }
        }
      },
      "put": {
        "summary": "Update a user",
        "responses": {
          "200": {
            "description": "User updated"
          }
        }
      },
      "delete": {
        "summary": "Delete a user",
        "responses": {
          "200": {
            "description": "User deleted"
          }
        }
      }
    }
  }
}
```
Place this file as `static/swagger.json` in your project.

### 5. Launch the App
Start your Flask app:
```bash
python app.py
```
Navigate to `http://localhost:5000/swagger` to interact with the API through Swagger UI.

---
![image](https://github.com/user-attachments/assets/24071c92-33ce-4280-b3fd-f25c5ac3746b)

## Troubleshooting

- **Database Connection Error**: Ensure your PostgreSQL database is running and the connection string is correct.
- **Swagger UI Not Showing**: Ensure that the `swagger.json` file exists in the `static` directory and is accessible.
- **API Not Working**: Check Flask logs for error messages and ensure you are using the correct routes.

---

## Conclusion

This project provides a full example of how to set up Swagger UI with a Flask REST API, providing a user management system with full CRUD operations connected to a PostgreSQL database. Swagger UI makes it easy to visualize and interact with the API.

Feel free to extend this project by adding more endpoints or integrating additional features such as authentication or logging.
