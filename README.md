Catalyst-Count
==========================

This is a Django project for Assignment Purpose
- Upload large Files using Chunk Upload 
- Save and upload data into database
- Authentication system
- Search Filters

Try it locally
--------------

1. Clone the repo.

::

    git clone git@github.com:krutikaParab/Catalyst_Count.git
    cd Catalyst_Count/

2. Install the requirements (I suggest using a virtualenv).

::

    virtualenv venv

    windows: .\venv\Scripts\activate
    linux: source venv/bin/activate

    pip install -r requirements.txt

3. Create the tables.

::

    ./manage.py migrate

4. Run the server.

::

    ./manage.py runserver

5. Go to `127.0.0.1:8000 <http://127.0.0.1:8000>` and upload a file.


TODO:
-------
1. create a superuser using Custom User Model

Support
-------

If you find any bug or you want to propose a new feature, please use the `issues tracker <https://github.com/krutikaParab/Catalyst_Count/issues>`__. I'll be happy to help you! :-)