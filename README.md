# koda

## Setting up for local development

#### Requirememnts
- python 3
- Make sure you have a version of redis running on port 6379

#### Setup

Make a python3 virtual environment in the root of the project
```bash
$ virtualenv -p /usr/bin/python3.6 venv
```

Install required packages
```bash
$ pip install -r requirements.txt
```

Tell django what settings you want to use
```bash
$ export DJANGO_SETTINGS_MODULE=koda.settings.local
```

Migrate database
```bash
$ python manage.py migrate
```

Create a super user for yourself
```bash
$ python manage.py createsuperuser
```

#### Running the development server

```bash
$ python manage.py runserver
```
