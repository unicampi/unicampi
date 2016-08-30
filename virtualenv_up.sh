#!/bin/bash

#gera uma virtualenv com o nome de env e ativa
virtualenv env
source env/bin/activate

#instala dependencias
pip3 install -r dependencies.txt

echo "########## Script terminado ########"
