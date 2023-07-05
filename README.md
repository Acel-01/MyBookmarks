# My Bookmarks REST API

This is a Django project that utilizes Pipenv and requires Python 3.8.

## Prerequisites

Before running the project, ensure you have the following software installed on your system:

- Python 3.8: You can download and install Python 3.8 from the official Python website (https://www.python.org/downloads/).
- Pipenv: Pipenv is a package manager and virtual environment tool for Python. Install it by running the following command:

### On Windows:


      pip install --user pipenv

### On macOS and Linux:


      pip3 install --user pipenv

## Setup

Follow these steps to set up and run the Django project:


**1. Clone the project repository:**
   

    git clone https://github.com/Acel-01/MyBookmarks.git


**2. Change into the project directory:**
   
   
    cd MyBookmarks/


**3. Install project dependencies using Pipenv:**
   
    
    pipenv install


**4. Activate the virtual environment:**


    pipenv shell


**5. Apply database migrations:**
   

    python manage.py migrate


**6. Start the development server:**
   

     python manage.py runserver