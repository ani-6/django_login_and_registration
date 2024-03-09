# Django Login and Registration Template

An example of Django project with basic user functionality.

Credentials:
- Username : admin
- password : serveradmin987

- Username : test_user
- Password : test@123


## Functionality

- Log in
    - via username & password
    - with a remember me checkbox (optional)
- Create an account
- Reset password
- Resend an activation code
- Change password
- Change email
- Change profile
- Gallery 
- Download files form url and upload to google drive (put token in base>Gdrive folder)
- Basic chat application
- Feedback form


### Install dependencies & activate virtualenv

```bash
pip install -r requirements.txt
```

### Configure the settings (connection to the database, connection to an SMTP server, and other options)

- Add environment variables in .env file
- Put your credentials/token file in base/Gdrive to make downloader work

### Create required groups, superuser and test users (req only if running new DB)
create superuser and test users with prefix test

```bash
python3 manage.py creategroups
python3 manage.py loadadmin 1 --admin 
python3 manage.py loadadmin 2 -p test
```


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
