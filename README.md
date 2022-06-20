# Server Application
Backend Django Project.\
Provides a custom service for managing unity assets.

## Setup (windows)

### RabbitMQ background process:
Download Erlang version compatible with RabbitMQ.\
https://www.erlang.org/patches/otp-24.1

Download RabbitMQ\
https://www.rabbitmq.com/install-windows.html#installer \
Run RabbitMQ setup\
Enable all components in the prompts

RabbitMQ should be running automatically after installation.\
Verify this by running ````RabbitMQ Service - Start```` in the windows search terminal (this should be recognized as a system command).


### Unity project:

Install Unity Editor (using 2020.3.26f1 in this case)\
Include the Android SDK & NDK Tools and OpenJDK modules in the installation.\
Create an empty Unity3D project using the 3D core template.\
Save the project's absolute asset directory path for later (e.g. "C:\Users\olavh\BundleProject\Assets")

### Python environment:
Install python (using version 3.9.12 in this instance)
Install a package manager of choice (we used Anaconda)

Install python packages: 
````django, celery, djangorestframework, django-colorfield, Pillow, django-cleanup, qrcode, gevent````

Generate database:
````shell
python manage.py migrate
````
Change the paths in [tasks.py](https://github.com/Citizen-Participation-Thesis/Server-Application/blob/main/assetserver/bundler/tasks.py) line 15,16 and 17 to fit your local directories.

Run background worker (remember to activate RabbitMQ):
````shell
celery -A assetserver worker -l info -P gevent
````

Run main application (open another terminal):
````shell
python manage.py runserver 0.0.0.0:8000
````

The website should now be available at ````localhost:8000```` and accessible from other devices on the same network.

### Creating assetbundles

Try out the assetbundling by uploading an FBX file to the Model File Form (Add Models page)\
Then create a project and select uploaded model(s).\
Then deploy the project.\
The processing will complete after some time.\
Hooks haven't been added to the webpage, so it doesn't refresh once the bundling process is complete.

After the bundle is created, your deployed project, and link to access the assetbundle is available through the REST api.\
http://localhost:8000/rest/GetProject/

Note that the bundle has been built for the android platform.
