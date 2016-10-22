#!/bin/bash
echo -e "#####################################"
echo -e "# Running only run_script will only #"
echo -e "# install dependencies and runserver#"
echo -e "# --------------------------------- #"
echo -e "# If this is the first time running #"
echo -e "#     ./run_script.sh first         #"
echo -e "# If you want to import a database: #"
echo -e "#     ./run_script.sh unicamp       #"
echo -e "# To run with a clean migration:    #"
echo -e "#     ./run_script.sh clean         #"
echo -e "# To run with a clean db :          #"
echo -e "#     ./run_script.sh reset         #"
echo -e "# To create a new config.json       #"
echo -e "#     ./run_script.sh config        #"
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

if [[ "$@" == "first" ]]; then

  echo -e '\nNow, will configure mail and security\n'
  echo '                                      Until here |'
  echo '"Randonly" type on the keyboard about 35 digits  V'
  read secret_key
  echo 'EMAIL_HOST (for gmail use smtp.gmail.com): '
  read email_host
  echo 'EMAIL_PORT (for gmail use 587): '
  read email_port
  echo 'Use TLS? [Y/n]: '
  read email_tls
  echo 'EMAIL_USERNAME (for gmail is the email): '
  read email_username
  echo 'PASSWORD: '
  read password
  echo 'Saving configuration on config.json'

  if [[ $email_tls == 'n' ]];then
    email_tls='False'
  else
    email_tls='True'
  fi

  echo "{
    \"SECRET_KEY\": "\"$secret_key\"",
    \"EMAIL_HOST\": "\"$email_host\"",
    \"EMAIL_PORT\": "\"$email_port\"",
    \"EMAIL_USE_TLS\": "\"$email_tls\"",
    \"EMAIL_HOST_USER\": "\"$email_username\"",
    \"EMAIL_HOST_PASSWORD\": "\"$password\""
  }" > config.json

  echo -e 'This is the first time\n will make migrations and create user'

  python3 manage.py makemigrations
  python3 manage.py migrate

  echo -e "Would you like to import the dev database?  [N/y]:"
  read import_db
  if [[ $import_db == 'y' ]];then
    python3 manage.py loaddata docs/dev.json
  fi

  echo -e 'Now, you ll create a username and password for django'
  python3 manage.py createsuperuser

elif [[ "$@" == "unicamp" ]]; then
  echo 'load data'
  read -n1 -r -p " You're gonna reset all the db - CTRL+C to quit " key
  rm -rf gda/migrations/*
  rm -rf dacParser/migrations/*
  rm -rf stalkeador/migrations/*
  rm -rf db.sqlite3
  python3 manage.py makemigrations dacParser
  python3 manage.py makemigrations gda
  python3 manage.py makemigrations stalkeador
  python3 manage.py makemigrations
  python3 manage.py migrate
  python3 manage.py loaddata docs/dev.json
  python3 manage.py createsuperuser

elif [[ "$@" == "clean" ]]; then
  echo 'clean'
  read -n1 -r -p " You're gonna clean the migrations - CTRL+C to quit " key
  rm -rf gda/migrations/*
  rm -rf dacParser/migrations/*
  rm -rf stalkeador/migrations/*
  python3 manage.py makemigrations dacParser
  python3 manage.py makemigrations gda
  python3 manage.py makemigrations stalkeador
  python3 manage.py makemigrations
  python3 manage.py migrate

elif [[ "$@" == "reset" ]]; then
  echo 'reset'
  read -n1 -r -p " You're gonna reset all the db - CTRL+C to quit " key
  rm -rf gda/migrations/*
  rm -rf dacParser/migrations/*
  rm -rf stalkeador/migrations/*
  rm -rf db.sqlite3
  python3 manage.py makemigrations dacParser
  python3 manage.py makemigrations gda
  python3 manage.py makemigrations stalkeador
  python3 manage.py makemigrations
  python3 manage.py migrate
  python3 manage.py createsuperuser

elif [[ "$@" == "config" ]]; then
  echo -e '\nNow, will configure mail and security\n'
  echo '                                      Until here |'
  echo '"Randonly" type on the keyboard about 35 digits  V'
  read secret_key
  echo 'EMAIL_HOST (for gmail use smtp.gmail.com): '
  read email_host
  echo 'EMAIL_PORT (for gmail use 587): '
  read email_port
  echo 'Use TLS? [Y/n]: '
  read email_tls
  echo 'EMAIL_USERNAME (for gmail is the email): '
  read email_username
  echo 'PASSWORD: '
  read password
  echo 'Saving configuration on config.json'

  if [[ $email_tls == 'n' ]];then
    email_tls='False'
  else
    email_tls='True'
  fi

  echo "{
    \"SECRET_KEY\": "\"$secret_key\"",
    \"EMAIL_HOST\": "\"$email_host\"",
    \"EMAIL_PORT\": "\"$email_port\"",
    \"EMAIL_USE_TLS\": "\"$email_tls\"",
    \"EMAIL_HOST_USER\": "\"$email_username\"",
    \"EMAIL_HOST_PASSWORD\": "\"$password\""
  }" > config.json
elif [[ "$@" == "travis" ]]; then
  echo "{
    \"SECRET_KEY\": \"abracadabratravis\",
    \"EMAIL_HOST\": \"smtp.gmail.com\",
    \"EMAIL_PORT\": \"587\",
    \"EMAIL_USE_TLS\": \"True\",
    \"EMAIL_HOST_USER\": \"oaoa@gmail.com\",
    \"EMAIL_HOST_PASSWORD\": \"ahshasdad\"
  }" > config.json

  python3 manage.py makemigrations dacParser
  python3 manage.py makemigrations gda
  python3 manage.py makemigrations stalkeador
  python3 manage.py makemigrations
  python3 manage.py migrate
  python3 manage.py loaddata docs/dev.json

fi

python3 manage.py runserver

.
echo "########## Script terminado ########"
