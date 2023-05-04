# social media API

Simple RESTful social media API for any social media web-service

#Installation

```
    git clone git@github.com:NEkropo1/py-social-media.git
    cd cinema-api
    python -m venv venv
```
Create a new .env file by copying .env.sample with cp .env.sample .env on Linux or simply copypaste on Windows.

Open the .env file in a text editor and update the values of the environment variables according to sample.

Linux/macOS:

  source venv/bin/activate
  pip install -r requirements.txt
  source .env

Windows:

  venv\Scripts\activate
  pip install -r requirements.txt
  npm install -g dotenv

Change directory to your project, like in this sample: cd C:\myproject You should be able to run .env with simple dotenv command.

After these commands, on any system, run and apply migrations:

  python manage.py migrate
  python manage.py runserver

You will be able to use application on localhost.


Features:

Admin panel localhost/admin/
Documentation is located at localhost/api/doc/swagger/
Creating user with profile and picture
Manage your user profile
Create and manage posts with pictures
Follow/unfollow other user to see their posts
