pip install virtualenv==20.7.2
env\Script\activate
pip install -r ChallengerLibraryBookCatalog\requirements.txt
python manage.py migrate
python manage.py loaddata apps\books\fixtures\fixture_genre.json
python manage.py loaddata apps\books\fixtures\fixture_books.json
python manage.py loaddata apps\books\fixtures\fixture_info.json
python manage.py compilemessages
python manage.py rebuild_index
python manage.py test