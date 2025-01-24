### Table of Contents

1. [Introduction](#introduction)
2. [Project Functionality](#functionality)
3. [Project Features](#features)
4. [Deployment](#live)
5. [Running the Project Locally](#clone)
6. [Running the Tests](#test)
7. [Running with Docker](#docker)
8. [Running with docker-compose](#docker-compose)

#### 1. <a name="introduction"></a> Introduction

The project is a **Django**-powered web listing platform focused on being a marketplace for buyers and sellers of books. It's a platform that allows authors to post book listings for sale, create events, and communicate with other users for FREE.

#### 2. <a name="functionality"></a> Project Functionality

- Manage listings: Authenticated users can create, edit, and delete listings of their created content.
- Unauthenticated users have access only to view the featured listings and order books.
- Like, Dislike, and Comment/Review functionality for books, profiles, and events.
- Search and filter books by name, genre, and ownership.
- Authenticated users with complete profiles can send messages to other users.
- Authenticated users with complete profiles can request books to be signed by the author upon purchase.
- Admin panel (accessible by admins only).
- Admins have full access to all content: manage website users, listings, and team members.

#### 3. <a name="features"></a> Project Features

- Extended custom user model
- Email verification
- Cloud storage
- Django REST Framework
- Exception handling and logging
- Translation support
- Pagination

#### 4. <a name="live"></a> Deployment - <a href="https://m0673n-bookstore.onrender.com">m0673n-bookstore.onrender.com</a>

#### 5. <a name="clone"></a> Running the Project Locally

##### Requirements
- **Python 3**: [Download Python 3.10](https://www.python.org/downloads/release/python-3100/)
- **<a name="env">`.env` file</a>**: Before running the application, ensure you have an `.env` file in your project directory with the following variables:
```
# Required for the bookstore application
SECRET_KEY=your_secret_key

EMAIL_HOST_USER=your_email # Use "" if you are using docker-compose
EMAIL_HOST_PASSWORD=your_email_pass # Use "" if you are using docker-compose
EMAIL_HOST=your_email_host # Use mailhog if you are using docker-compose
EMAIL_PORT=your_email_port # Use 1025 if you are using docker-compose
EMAIL_USE_TLS=true_or_false # Use False if you are using docker-compose

CLOUDINARY_NAME=your_cloudinary_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret

POSTGRES_DATABASE=your_postgre_db
POSTGRES_USERNAME=your_postgre_username
POSTGRES_PASSWORD=your_postgre_password
POSTGRES_HOST=your_postgre_host # Use bookstore_database if you are using docker-compose

SITE_OWNER_EMAIL=your_email

# Required for the database if run the docker-compose configuration
POSTGRES_USER=your_postgre_username
POSTGRES_PASSWORD=your_postgre_password
POSTGRES_DB=your_postgre_db
```

##### Clone the project
```
git clone https://github.com/M0673N/bookstore.git
```
##### Make sure to add your `.env` file to the bookstore folder
```
cd ./bookstore/ &&
python3 -m venv .venv &&
source .venv/bin/activate &&
python3 -m pip install --upgrade pip &&
pip3 install -r requirements.txt &&
python3 manage.py migrate &&
waitress-serve --port=8000 --threads=6 bookstore.wsgi:application
```

#### 6. <a name="test"></a> Running the Tests
```
python3 manage.py test
```

#### 7. <a name="docker"></a> Running with Docker
- Don't forget the [.env](#env) file.
```
docker run -p 8000:8000 -d --name bookstore --env-file .env m0673n/bookstore
```

#### 8. <a name="docker-compose"></a> Running with docker-compose
- You need the [.env](#env) file and the `nginx.conf` file in the same folder with the docker-compose.yml file
```
docker compose up -d
```