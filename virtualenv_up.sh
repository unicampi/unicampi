#!/bin/bash

#testa se a virtual env esta instalada e decide condicionalmente se é necessário instalá-la ou não
virtualenv --version

#caso não exista, instala
if (( $? )); then
    pip3 install virtualenv
else
    echo "##### Virtualenv já esta instalada #####"
fi

#gera uma virtualenv com o nome de env e ativa
virtualenv env
source env/bin/activate

#instala dependencias
pip3 install -r dependencies.txt

echo "########## Script terminado ########"
