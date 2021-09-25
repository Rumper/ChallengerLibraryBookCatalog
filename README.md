# ChallengerLibraryBookCatalog
Challenge to create a project on a library catalog of books.


# The Requiments...

The proyect is developed in:
- Django==3.2.7
- Python==3.9.27
- Virtualenv==20.7.2

# Before the starting...
You need install Docker, by you use elasticsearch
		
	docker pull docker.elastic.co/elasticsearch/elasticsearch:5.5.3

Run Docker:

	docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:5.5.3

Gettext by translations (64bits) https://github.com/mlocati/gettext-iconv-windows/releases/download/v0.21-v1.16/gettext0.21-iconv1.16-shared-64.exe

Execute:

Run the file to install all dependecies. This file is in root folder of the project:

	excecute_install.bat

You must have run the Docker instance before running the file.
This file will perfom:
- Create virtual environment
- Install the pip requirements package.
- The migrations
- Install the fixed data of the books
- Compile the translations
- Create the index in elastisearch <- Is need to has run the docker instance 
- Execute the test
Inspect file but more details

# Run Proyect...
To start the project use the command: 
	*python manage.py runserver*
You can view the project website at 
	*http://127.0.0.1:8000* 
and it's time to tamper with the web.  

# Create SuperUser...
Use command:

	python manage.py createsuperuser
