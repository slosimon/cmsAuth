Installation
************

After installing Contest Management System you have to install several other features. (For those who haven't yet, install virtualenv and enter it)

For Ubuntu/Debian

    sudo pip install virtualenv
    virtualenv cmsAuthEnv #Or any other name you want to use
    source cmsAuthEnv/bin/activate

Then you will need to install Django and gunicorn

    pip install django gunicorn 

After doing this, you may pull the project from github (make a new folder on the same level as it is your virtualenv folder) e.g.

~/--->cmsAuthEnv
  --->cmsAuth

Enter folder cmsAuth and then into cmsAuth. Open settings.py
Now you have to change some variables into this file. Look at the comments in the file.
go back to first cmsAuth folder. You should see manage.py. From terminal, run 
..sourcecode:: bash
    ./manage.py makemessages -l [your language code]
You should see a file in *locale/[your language code]/LC_MESSAGES/django.po* . Translate it into your language. Save it and run
    ./manage.py compilemessages  
After compiling messages, you should run 
    ./manage.py collectstatic
    ./manage.py makemigrations
    ./manage.py migrate
After that run 
    gunicorn --bind 0.0.0.0:8000 cmsAuth.wsgi:application
You should see your page working on port 8000 localy. Now we have to configure nginx. As you did for CMS, now you have to add another upstream and assign it's location. Now you are ready to use cmsAuth



