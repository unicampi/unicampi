#!/bin/bash

#script para simplesmente rodar o servidor com o sistema atualzizado

echo "#######iniciando script#########"

python3 manage.py makemigrations
python3 manage.py makemigrations dacParser
python3 manage.py makemigrations gda
python3 manage.py migrate
python3 manage.py runserver

echo "#############script terminado#############"
