# KODA
Knockoff Discord Application by Brian Seidl and Grant Clark

## Production
If you just want to check out the final product, it is currently deployed at https://koda-app.herokuapp.com/.

#### Disclaimer

You will not be able to view or send messages if you do not have a production koda account.  For more information on creating an account, please contact one of the developers.

## Local development

### Requirememnts
- python 3 and pip
- virtualenv (highly recommended)
- Make sure you have redis running on port 6379
    - For more information on redis, visit https://redis.io/topics/quickstart.

### Setup

Make a python 3 virtual environment and activate it. (Not mandatory but highly recommended)
```bash
$ virtualenv -p /usr/bin/python3.6 venv
$ source venv/bin/activate
```

Before you bring up your development server, you need to install required python modules and packages, enable local settings, and migrate you local database.
```bash
$ pip install -r requirements.txt
$ export DJANGO_SETTINGS_MODULE=koda.settings.local  #put this in your shell's startup script
$ python manage.py migrate
```

Next you will need to create a super user for yourself to have to ability to access the admin pages.
```bash
$ python manage.py createsuperuser
```

### Running the Development Server

```bash
$ python manage.py runserver
```

Your version of koda will be running on http://localhost:8000/, but you are not done yet.  You will need to add users and create rooms/chats.  You can do so by accessing the admin page at http://localhost:8000/admin/.

### Running the Tests

- Test cases can be found in the module `rooms.tests`.
- To run the tests, do the following:

    ```bash
    $ python manage.py test
    ```

### Important

Just some extra information for local development and what not.

- When you add users, make sure you also add the user's first name.  The first and last name is an optional field in the django User model, but we use the first name field in this application.

- A direct message is just a room with two people.  This was done to save time. To make a direct message, create a room and change the `rtype` value from `room` to `chat`.  So technically you can have a direct message with more than two people, just don't do it.  This is why I am the admin in production.
