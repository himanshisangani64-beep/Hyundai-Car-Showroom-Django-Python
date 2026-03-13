# online website Hyundai Car Showroom Management System (Django Project)

## Project Description
The Hyundai Car Showroom Management System is a web application developed using Python and Django.  
This system allows users to browse Hyundai car models, view categories, add products to cart, and generate bills.  
The system also includes an admin dashboard to manage products, categories, users, and orders.

---

# Technologies Used

Backend
- Python
- Django Framework

Frontend
- HTML
- CSS
- JavaScript
- Bootstrap

Database
- MySQL

Other Tools
- Git
- GitHub

---

# Software Requirements

The following software must be installed:

Python 3.10 or higher  
Django 4.x  
MySQL Server  
Git  
Code Editor (VS Code / PyCharm)

---

# Python Libraries / Dependencies

Libraries used in the project:

Django  
Matplotlib  
ReportLab  
WeasyPrint  
Num2Words  
Pillow  
MySQL Client

Install dependencies using:
pip install django
pip install matplotlib
pip install reportlab
pip install weasyprint
pip install num2words
pip install pillow
pip install mysqlclient


Or install all using:


pip install -r requirements.txt


---

# Project Modules

RegistrationApp – User registration and login  
ProductApp – Manage car products  
CategoryApp – Manage categories and subcategories  
CartApp – Cart functionality  
BillApp – Billing and invoice generation  
DashboardApp – Admin dashboard  
DemoApp – Order management  

---

# Installation Guide

## Step 1 Clone the Repository


git clone https://github.com/himanshisangani64-beep/Hyundai-Car-Showroom-Django-Python.git


## Step 2 Go to Project Folder


cd Hyundai-Car-Showroom-Django-Python


## Step 3 Create Virtual Environment


python -m venv venv


Activate environment:

Windows


venv\Scripts\activate


Linux / Mac


source venv/bin/activate


---

## Step 4 Install Dependencies


pip install -r requirements.txt


---

## Step 5 Configure MySQL Database

Update database settings in:


Hyundai_CarShowroom/settings.py


Example configuration:


DATABASES = {
'default': {
'ENGINE': 'django.db.backends.mysql',
'NAME': 'hyundai_db',
'USER': 'root',
'PASSWORD': '',
'HOST': 'localhost',
'PORT': '3306',
}
}


---

## Step 6 Run Database Migration


python manage.py migrate


---

## Step 7 Create Admin User


python manage.py createsuperuser


---

## Step 8 Run Development Server


python manage.py runserver


Open browser:


http://127.0.0.1:8000/


Admin panel:


http://127.0.0.1:8000/admin


---

# Features

User Registration and Login  
Browse Hyundai Cars  
Category and Subcategory Management  
Add to Cart System  
Bill Generation with PDF  
Admin Dashboard  
Product Management  

---

# Author

Himanshi Sangani

---

# License

This project is created for educational purposes.