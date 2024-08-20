# Tailorhustle
# SAS for Tailors and Brands to list and provide their clothing facilities online.


Poetry commands

--> ( activate poetry enviornment )
poetry shell

--> ( install pacage into poetry )
poetry add pacagename

--> ( poetry export requirements )
poetry export -f requirements.txt -o requirements.txt

--> ( poetry take the dependencies from requirement.txt )
poetry add $( cat requirements.txt )


Open terminal and run command  ( Wait until all dependancies installation are completed )

sudo docker-compose up --build
sudo docker-compose down
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
python manage.py createsuperuser