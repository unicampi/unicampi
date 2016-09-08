#!/bin/bash
echo -e "#####################################"
echo -e "# Running only run_script will only #"
echo -e "# install dependencie and runserver #"
echo -e "# --------------------------------- #"
echo -e "# To run with a clean migration:    #"
echo -e "#     ./run_script.sh totalclean    #"
echo -e "# To run with a clean db :          #"
echo -e "#     ./run_script.sh totalclean    #"
echo -e "#####################################\n\n\n"

# we check requirements
if type pip3 &> /dev/null; then
  # download virtual env if its not installed
  if ! pip3 list | grep virtualenv
  then
    echo -e "\nInstalling virtual env"
    sudo pip3 install virtualenv
  fi
else
  echo -e "\n\n#################################"
  echo -e "Please, download and install pip3"
  echo -e "#################################\n\n"
fi

# generates the virtual envirement in env and activate it
if [ -d "env" ]; then
  # Control will enter here if $DIRECTORY exists.
  source env/bin/activate
else
  virtualenv env
  source env/bin/activate
fi

if [[ ! -z "$VIRTUAL_ENV" ]]; then
  echo "Activated virtualenv"
fi

# install dependencies
pip3 install -r dependencies.txt


if [[ "$@" == "clean" ]]; then
  echo 'clean'
  rm -rf gda/migrations/*
  rm -rf dacParser/migrations/*
  python3 manage.py makemigrations dacParser
  python3 manage.py makemigrations gda
  python3 manage.py makemigrations
  python3 manage.py migrate
elif [[ "$@" == "totalclean" ]]; then
  echo 'totalclean'
  rm -rf gda/migrations/*
  rm -rf dacParser/migrations/*
  rm -rf db.sqlite3s
  python3 manage.py makemigrations dacParser
  python3 manage.py makemigrations gda
  python3 manage.py makemigrations
  python3 manage.py migrate
  python3 manage.py createsuperuser
fi

python3 manage.py runserver

.
echo "########## Script terminado ########"
