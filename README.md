# Project Goal
# Planning
In the beginning of the project, I focused on planning. I started by creating user stories for the frontend application. These stories were based on the project's goals and helped me understand what users would want from the app.

The user stories served as a guide to create wireframes, which showed how the app would work and how users would use it. They gave me a clear picture of how people would interact with the app and the steps they would take to get things done.

Once I had the user stories and wireframes ready, I figured out the essential features needed to make a Minimum Viable Product (MVP). I broke down each user story into smaller tasks and connected them to the necessary parts of the app's backend (API endpoints) that would support the required features.

This process of creating user stories, making wireframes, and connecting them to the backend ensured that my development path was clear and focused. It helped me create a seamless and user-friendly app by aligning the frontend experience with the backend functionality.
# Data models
I planned the data model schema concurrently with the API endpoints by utilizing an entity relationship diagram.
The custom models implemented for the project include:
## Tutorial
## Subscribers
## Profiles
## Likes

## ERD
![ERD picture](../gameversity-api/reamde/readme-erd.png)
# API Endpoints
# Frameworks, Libraries and Dependencies
# Testing
# Deployment

## Github Repository
* Create repository from the Code institute **[ci-full-template](https://github.com/Code-Institute-Org/ci-full-template)**
* Give it a name
* Open it up with Github from the green **Gitpod** button
    * If there is no button. Download the **Gitpod** extention for your browser.

## Django
* Install **Django** by entering **`pip3 install 'django<4'`** in the terminal 
* Create a project by entering **`django-admin startproject <projectname> .`** in the terminal

## Create Django app
* In the terminal enter **`python manage.py startapp <appname>`**
* And add the app to the installed app inside **settings.py**

## Cloudinary
* Go to **[Cloudinary](https://cloudinary.com/)**
* Fill out the form and sign up for free
* Go to the dashboard and 
* To be able to connect to Cloudinary enter **`pip install django-cloudinary-storage`** in the terminal
* Add **Cloudinary** to Installed apps in **settings.py**
* Install **Pillow** by entering **`pip install Pillow`** in the terminal
* Create **env.py** file and add **`import os`** and **`os.environ ['CLOUDINARY_URL'] = '<URL from Cloudinary Dashboard>'`**
* Inside **settings.py**, under **`from pathlib import Path`** add the following code to set up Cloudinary storage:
```
import os

if os.path.exists('env.py'):
    import env

CLOUDINARY_STORAGE = {
    'CLOUDINARY_URL': os.environ.get('CLOUDINARY_URL')
}
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```
## Heroku
* Login to **[Heroku](https://dashboard.heroku.com/apps)** and go to the **Dashboard**
* Click **New**
* Click **Create new app**
* Give your app a name and select the region closest to you. When you’re done, click **Create app** to confirm
    * *Heroku app names must be unique. If yours isn't, Heroku will give you a warning*
* Open the **Settings** tab
* Add a Config Var **DATABASE_URL**, and for the value, copy in your database URL from ElephantSQL
    * *View the next section to find the ElephantSQL deployment*
* Install **gunicorn**. Enter in the terminal:
```
 pip3 install gunicorn django-cors-headers
```
* Update your **requirements.txt**
```
 pip freeze --local > requirements.txt
```
* Create a **Procfile**, inside the file add:
```
 release: python manage.py makemigrations && python manage.py migrate
 web: gunicorn <projectname>.wsgi
```
* In your **settings.py** file, update the value of the **ALLOWED_HOSTS** variable to include your Heroku app’s URL
    * *Make use not to use **https://** in the URL. To me that caused a problem with Heroku.*
```
ALLOWED_HOSTS = ['localhost', '<your_app_name>.herokuapp.com']
```
* Add corsheaders to INSTALLED_APPS
```
INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
 ]
```

* Add **corsheaders** middleware to the **TOP** of the **MIDDLEWARE**

``` 
SITE_ID = 1
MIDDLEWARE = [
     'corsheaders.middleware.CorsMiddleware',
     ...
 ]
 ```

* **Under the MIDDLEWARE** list, set the **ALLOWED_ORIGINS** for the network requests made to the server with the following code:

``` 
 if 'CLIENT_ORIGIN' in os.environ:
     CORS_ALLOWED_ORIGINS = [
         os.environ.get('CLIENT_ORIGIN')
     ]
 else:
     CORS_ALLOWED_ORIGIN_REGEXES = [
         r"^https://.*\.gitpod\.io$",
     ]
 ```
 * Enable sending cookies in cross-origin requests so that users can get authentication functionality
 ```
 else:
     CORS_ALLOWED_ORIGIN_REGEXES = [
         r"^https://.*\.gitpod\.io$",
     ]

 CORS_ALLOW_CREDENTIALS = True
 ```
* To be able to have the front end app and the API deployed to different platforms, set the **JWT_AUTH_SAMESITE** attribute to **'None'**. Without this the cookies would be blocked
```
JWT_AUTH_COOKIE = 'my-app-auth'
JWT_AUTH_REFRESH_COOKE = 'my-refresh-token'
JWT_AUTH_SAMESITE = 'None'
```
* Remove the value for SECRET_KEY and replace with the following code to use an environment variable instead
```
SECRET_KEY = os.getenv('SECRET_KEY')
```
* Set the DEBUG value to be **True only if the DEV environment variable exists**. This will mean it is True in development, and False in production
```
DEBUG = 'DEV' in os.environ
```
* Comment **DEV** back in **env.py**
```
import os

 os.environ['CLOUDINARY_URL'] = "cloudinary://..."
 os.environ['SECRET_KEY'] = "Z7o..."
 os.environ['DEV'] = '1'
 os.environ['DATABASE_URL'] = "postgres://..."
```
Ensure the project **requirements.txt** file is up to date. In the **IDE terminal** of your project enter the following:
```
pip freeze --local > requirements.txt
```
* **Add, commit and push** your code to **GitHub**

## Elephant SQL
* Login to **[ElephantSQL](https://www.elephantsql.com/)**
* Click **Create New Instance**
* Set up your plan:
    * Give you plan a name
    * Select the **Tiny Turtle** plan **(Free)**
    * **Tags** can be left blank
* Click **Select Region**
* Select a data center near you
* Click **Review**
* Check your details and then click **Create Instance**
* Install **dj_database_url** and **psycopg2**, both of these are needed to connect to your external database
* In the terminal, enter:
```
 pip3 install dj_database_url==0.5.0 psycopg2
```
* In your **settings.py** file, import **dj_database_url** underneath the import for os
```
 import os
 import dj_database_url
```
* Update the DATABASES section to the following:
```
if 'DEV' in os.environ:
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.sqlite3',
             'NAME': BASE_DIR / 'db.sqlite3',
         }
     }
 else:
     DATABASES = {
         'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
     }
```
* Return to the ElephantSQL dashboard and click on the **database instance name** for your project
* In the URL section, click the copy icon to **copy the database URL**
* In your **env.py** file, add a new environment variable with the key set to **DATABASE_URL**, and the value to your **ElephantSQL database URL**
```
 os.environ['DATABASE_URL'] = "<your PostgreSQL URL here>"
```
* Migrate your database models to your new database
```
  python3 manage.py migrate
```
* Create a superuser for your new database
```
 python3 manage.py createsuperuser
```
* Follow the steps to create your superuser username and password
* Confirm that the data in your database on ElephantSQL has been created
* On the **ElephantSQL** page for your database, in the left side navigation, select **BROWSER**
* Click the **Table queries** button, select **auth_user**
* When you click **Execute**, you should see your newly created superuser details displayed. This confirms your tables have been created and you can add data to your database