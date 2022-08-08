Property inspection web app

Built with django

To run local server:
python manage.py migrate

python manage.py runserver


DEV
These details refer only to the development server
    Using virtualenvwrapper-windows
    mkvirtualenv inspection
    
    enter virtualenv

    workon inspection

    Install requirements if needed
    pip install -r requirements.txt

    To generate property_type fixtures:
    python manage.py dumpdata property.PropertyType --output fixtures/property_type.json

   To load property_type fixtures
   python manage.py loaddata property_type

    