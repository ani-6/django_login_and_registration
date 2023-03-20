# Django Login and Registration

An example of Django project with basic user functionality.

Credentials:
- Username : test
- Password : test@123

## Functionality

- Log in
    - via username & password
    - with a remember me checkbox (optional)
- Create an account
- Log out (Auto logout after 5 mins of inactivity)
- Reset password
- Resend an activation code
- Change password
- Change email
- Change profile
- Gallery 
- Notebook
- Markdown
- Download imgs form url and upload to google drive (put token in apps>Gdrive folder)


## Installing

### Clone the project

```bash
git clone https://github.com/ani-6/django_login_and_registration.git
cd django_login_and_registration.git
```

### Install dependencies & activate virtualenv

```bash
pip install -r requirements.txt
```

### Configure the settings (connection to the database, connection to an SMTP server, and other options)

- Add environment variables in .env file


### Running

#### A development server

Run this command for http:

```bash
python3 manage.py runserver
```

Run this command for https:

```bash
python3 manage.py runsslserver
```

### Access server on 

```bash
localhost:8000
```
