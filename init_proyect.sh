#!/bin/bash

# Install Packages
sudo apt-get update -y
sudo apt-get install python3.8
sudo apt-get install python3-pip
sudo apt-get install mysql-server-8.0

# Install Dependencies
pip install -r requirements.txt
pip install wheel 
# Config Database
export MYSQL_DATABASE_HOST=localhost
export MYSQL_DATABASE_USER=root
export MYSQL_DATABASE_PASSWORD=root
export MYSQL_DATABASE_DB=ensolvers
export FLASK_APP=app.py

mysql -u root -p ensolvers < schema.sql

# Run App
flask run
