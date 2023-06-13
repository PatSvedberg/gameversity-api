# Deployment

# Repository
* Create repository from the Code institute [ci-full-template](https://github.com/Code-Institute-Org/ci-full-template)
* Give it a name
* Open it up with Github from the green Github button
    * If there is no button. Download the Github extention for your browser.
## Django
* Install Django by entering `pip3 install 'django<4'` in the terminal 
* Create a project by entering `django-admin startproject <projectname> .` in the terminal 
## Cloudinary
* Go to [Cloudinary](https://cloudinary.com/)
* Fill out the form and sign up for free
* Go to the dashboard and 
* To be able to connect to Cloudinary enter `pip install django-cloudinary-storage` in the terminal
* Add Cloudinary to Installed apps in Settings.py
* Install Pillow by entering `pip install Pillow` in the terminal
* Create env.py file and add `import os` and `os.environ ['CLOUDINARY_URL'] = '<URL from Cloudinary Dashboard>'`
* Inside Settings.py, under `from pathlib import Path` add the following code to set up Cloudinary storage:
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
