#! /bin/bash

# 50 character string to use as temporary secret key
NEW_UUID=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 50 | head -n 1)

cd "$( dirname "${BASH_SOURCE[0]}" )";
echo "\e[36;1m Creating virtual environment...\e[0m";
virtualenv -p python3 venv;
source venv/bin/activate;

echo "\e[36;1m Installing dependencies...\e[0m"
pip install -r requirements.txt;
cd bingo;
mkdir bingo/secrets;

if [ ! -f bingo/secrets/django-secret.key ];
then
    echo "$NEW_UUID" > bingo/secrets/django-secret.key;
fi;

if [ ! -f bingo/secrets/database.password ];
then
    echo "1234" > bingo/secrets/database.password;
fi;

if [ ! -f bingo/secrets/email.password ];
then
    echo "1234" > bingo/secrets/email.password;
fi;
if [ ! -f bingo/secrets/email/from ];
then
    echo "1234" > bingo/secrets/email.from;
fi;

echo "\e[36;1m Performing Migrations...\e[0m"
python manage.py makemigrations;
python manage.py migrate;

echo "\e[36;1m Running tests...\e[0m"
python manage.py test;

echo "\e[36;1m Install Complete.\e[0m"
echo "Configure email settings before running server."