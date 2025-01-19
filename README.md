### Table of Contents

1. [Introduction](#introduction)
2. [Project Functionality](#functionality)
3. [Project Features](#features)
4. [Deployment](#live)
5. [Running the Project Locally](#clone)
6. [Running the Tests](#test)

#### 1. <a name="introduction"></a> Introduction

The project is a **Django**-powered web listing platform focused on being a marketplace for buyers and sellers of books. It's a platform that allows authors to post book listings for sale, create events, and communicate with other users.

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
```
git clone https://github.com/M0673N/bookstore.git
```
##### Make sure to add your `.env` file to the bookstore folder. You will need a Cloudinary account, a Gmail account (set up properly), and a PostgreSQL provider account.
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
