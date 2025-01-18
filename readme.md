# Django Gallery With Login and Registration

This is an example of a Django project providing basic user authentication and related functionality. The template includes login, registration, password management, and more, as well as additional features like a gallery and a basic chat application with rest apis usign Django rest framework.

## Features

- **Login & Authentication:**
    - Log in with username and password
    - "Remember me" checkbox (optional)
- **Account Management:**
    - Create an account
    - Reset password
    - Resend an activation code
    - Change password
    - Change email
    - Change profile information
- **Additional Features:**
    - Gallery for images
    - Download files from a URL and upload to Google Drive (requires a token in the `base/Gdrive` folder)
    - Basic chat application
    - Feedback form
- **APIs:**
    - REST APIs for all views (for integration with external systems)
  
## Credentials (default for testing)

- **Username**: admin  
  **Password**: serveradmin987
  
- **Username**: test_user  
  **Password**: test@123

## Installation

### 1. Install Dependencies & Set Up Virtual Environment

To get started, install the required dependencies and activate a virtual environment:

```bash
pip install -r requirements.txt
```


### 2. Configure Settings

Ensure the following configurations are done:
- Database Connection: Edit the settings to connect to your desired database.
- SMTP Server: Configure the SMTP server settings for email-related functionality.
- Google Drive Token: Place the Google Drive token in base/Gdrive to enable file downloading and uploading to Google Drive.
- Define Trusted origins for CORS and CSRF in env files.

You can add environment variables in a .env file to configure settings like database credentials, SMTP server settings, and Google Drive token.

### 3. Create Required Groups, Superuser, and Test Users

If you are using a new database, create the necessary groups, superuser, and test users:

``` bash
python3 manage.py creategroups
python3 manage.py loadadmin 1 --admin
python3 manage.py loadadmin 2 -p test
```

- The first command creates necessary user groups.
- The second command creates an admin user with username admin and password serveradmin987.
- The third command creates a test user with username test_user and password test@123.


## Running the Project
### Development Server

To run the development server, execute the following command:

```bash
python3 manage.py runserver
```

This will start the server at http://localhost:8000.
### Docker & HTTPS

If you prefer to use Docker with Nginx and HTTPS, you can run the project using Docker Compose:

```bash
docker compose up -d
```

This will start the application with HTTPS on your local environment.


## Screenshots

<img src="Screenshots/Screenshot 2024-04-06 165256.png" height="auto" width="800">
<img src="Screenshots/Screenshot 2024-04-06 170051.png" height="auto" width="800">
<img src="Screenshots/Screenshot 2024-04-06 165937.png" height="auto" width="800">
<img src="Screenshots/Screenshot 2024-04-06 165956.png" height="auto" width="800">
<img src="Screenshots/Screenshot 2024-04-06 170016.png" height="auto" width="800">