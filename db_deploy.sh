#!/bin/bash

# Variables
ORANGE_PI_IP="orange_pi_ip"
USERNAME="your_username"
DB_NAME="your_db_name"
DB_USER="your_db_user"
DB_PASSWORD="your_db_password"

# SSH into Orange Pi and run commands
ssh $USERNAME@$ORANGE_PI_IP << 'ENDSSH'

# Pull the latest PostgreSQL image
docker pull postgres

# Run PostgreSQL container
docker run --name postgres_container -e POSTGRES_DB=$DB_NAME -e POSTGRES_USER=$DB_USER -e POSTGRES_PASSWORD=$DB_PASSWORD -p 5432:5432 -v postgres_data:/var/lib/postgresql/data -d postgres

ENDSSH
